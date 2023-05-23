import logging
import yfinance as yf
from typing import List
import datetime
import pytz


class SpotService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.cache = {}

    def get_live_price(self, tickers: List[str] = None):
        """
        Retrieves live prices for the given tickers.
        Args:
            tickers (List[str]): List of ticker symbols. Default is None.
        Returns:
            dict: A dictionary mapping tickers to their corresponding live prices.
                  If live prices are not available, the function falls back to fetching close prices.
        """

        current_date = datetime.date.today()
        data = yf.download(tickers=tickers, interval="1m", start=current_date,
                           end=current_date + datetime.timedelta(days=1))

        spot_map = {}
        tickers_to_fetch_cp = []

        if not data.empty:
            current_time = datetime.datetime.now().astimezone(pytz.timezone('UTC'))
            for ticker in tickers:
                # Fetch the latest timestamp time for the ticker
                latest_timestamp_time = data[data['High'][ticker].notna()].index.max().to_pydatetime()

                if latest_timestamp_time <= current_time:
                    # If the latest timestamp is older or equal to the current time, add the ticker to fetch close price
                    tickers_to_fetch_cp.append(ticker)
                else:
                    # Calculate the spot price for the ticker using the high and low values of the latest timestamp
                    spot_map[ticker] = (data['High'][ticker][data[data['High'][ticker].notna()].index.max()] +
                                        data['Low'][ticker][data[data['Low'][ticker].notna()].index.max()]) / 2

        # Update the spot_map with close prices for tickers that need to be fetched
        spot_map.update(self.get_close_price(tickers_to_fetch_cp, current_date))

        # Return spot_map if it is not empty, otherwise, return the result of get_close_price for all tickers
        return spot_map or self.get_close_price(tickers, current_date)

    def get_close_price(self, tickers: List[str] = None,
                        date: datetime.date = datetime.date.today() - datetime.timedelta(days=1)):
        """
        Get the close prices for the given tickers on the specified date.
        Args:
            tickers (List[str]): List of tickers.
            date (datetime.date): Date to fetch the close prices. Defaults to today's date.
        Returns:
            dict: A dictionary containing the close prices for each ticker on the specified date.
        """
        if not tickers:
            return {}

        return self._get_data_from_cache(tickers, date)

    def _get_data_from_cache(self, tickers, date):
        """
        Get data from cache or update cache if required.
        Args:
            tickers (List[str]): List of tickers.
            date (datetime.date): Date to fetch the data.
        Returns:
            dict: A dictionary containing the data for each ticker on the specified date.
        """
        tickers_to_fetch = [ticker for ticker in tickers if (ticker, date) not in self.cache]

        if len(tickers_to_fetch) > 1:
            self._update_cache(tickers_to_fetch, date)

        return {ticker: self.cache.get((ticker, date)) for ticker in tickers}

    def _update_cache(self, tickers, date):
        """
        Update the cache with data for the given tickers and date.
        Args:
            tickers (List[str]): List of tickers to fetch data for.
            date (datetime.date): Date to fetch the data.
        """
        try:
            original_date = date
            while True:
                end_date = date + datetime.timedelta(days=1)
                downloaded_data = yf.download(tickers=tickers, start=date, end=end_date)
                if (not downloaded_data.empty) and str(date) in downloaded_data.index:
                    break
                date -= datetime.timedelta(days=1)

            downloaded_data = downloaded_data.loc[str(date), 'Adj Close']

            while True:
                for ticker in tickers:
                    self.cache[(ticker, date)] = downloaded_data.loc[ticker] if len(tickers) > 1 else downloaded_data
                if date == original_date:
                    break
                date += datetime.timedelta(days=1)

        except Exception as e:
            self.logger.error(f"Failed to update cache for tickers '{tickers}': {e}")

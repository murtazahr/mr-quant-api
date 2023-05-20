import logging
import yfinance as yf
from typing import List
import datetime


class SpotService:
    def __init__(self):
        self.data = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.cache = {}

    def get_close_price(self, tickers: List[str] = None, date: datetime.date = datetime.date.today()):
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
                    self.cache[(ticker, date)] = downloaded_data.loc[ticker]
                if date == original_date:
                    break
                date += datetime.timedelta(days=1)

        except Exception as e:
            self.logger.error(f"Failed to update cache for tickers '{tickers}': {e}")


# Configure logging
logging.basicConfig(level=logging.INFO)

# Example usage
spot_service = SpotService()
result = spot_service.get_close_price(['GOOGL', 'AAPL', 'SPX'])
logging.info(f"Close prices: {result}")

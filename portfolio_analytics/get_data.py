import os
from datetime import datetime
import yfinance as yf


CURRENT_DATE = str(datetime.now())[0:10]


class GetData:
    def __init__(
        self, tickers, start="1970-01-02", end=CURRENT_DATE, interval="1d", **kwargs
    ):
        """
        Initialtes GetData object by downloading data from `yfinance` which the user can use within `Python` or save as `.csv`

        :param tickers: Tickers of assets for which data is to be downloaded
        :type tickers: list
        :param start: Download start date for the data, defaults to "1970-01-02"
        :type start: str, optional
        :param end: Download end date for the data, defaults to CURRENT_DATE
        :type end: str, optional
        :param interval: Data interval. Valid intervals are: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo, defaults to "1d"
        :type interval: str, optional
        """

        if len(tickers) == 1:
            self.ticker = yf.Ticker(tickers[0])
            self._data = self.ticker.history(
                start=start, end=end, interval=interval, **kwargs
            )
        elif len(tickers) > 1:
            self.tickers = yf.Tickers(tickers)
            self._data = self.tickers.history(
                start=start, end=end, interval=interval, **kwargs
            )

    @property
    def data(self):
        """
        Gives access to the full DataFrame of the downloaded data

        :return: Data downloaded
        :rtype: pd.DataFrame
        """

        return self._data

    @property
    def close(self):
        """
        Gives access to the asset prices at trading close

        :return: Data downloaded
        :rtype: pd.DataFrame
        """

        return self._data["Close"]

    def save_all_long(self):
        """
        Saves downloaded data as `.csv` in long format
        """

        data_long = (
            self.data.stack(level=1)
            .reset_index(1)
            .rename(columns={"Symbols": "Ticker"})
            .sort_values("Ticker")
        )
        data_long.to_csv("all_tickers_data_long.csv")

    def save_all_wide(self):
        """
        Saves downloaded data as `.csv` in wide format
        """

        self.data.to_csv("all_tickers_data_wide.csv")

    def save_close_only(self):
        """
        Saves trading close prices as `.csv`
        """

        self.close.to_csv("close_only.csv")

    def save_separately(self):
        """
        Saves trading data as `.csv` for each asset separately
        """

        os.mkdir("tickers_data")
        os.chdir("tickers_data")
        current_data = self.data
        current_data.columns = self.data.columns.swaplevel("Symbols", "Attributes")
        for ticker in current_data.columns:
            time_series = current_data[ticker]
            time_series.to_csv("%s_data.csv" % ticker)

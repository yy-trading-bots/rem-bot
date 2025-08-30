from typing import Tuple, Sequence, List, Optional
import copy


class MarketSnapshot:
    """
    Container for a single snapshot of technical indicators.

    This structure captures the timestamp, current price, and commonly-used
    indicators (MACD, EMA, RSI), along with a list of recent OHLC bars.
    """

    def __init__(
        self,
        date: str,
        price: float,
        macd_12: float,
        macd_26: float,
        ema_100: float,
        rsi_6: float,
        bar_list: Optional[Sequence[Tuple[float, float, float, float]]] = None,
    ) -> None:
        """
        Initialize an IndicatorSnapshot.

        Args:
            date (str): Snapshot timestamp as a formatted string.
            price (float): Latest market price.
            macd_12 (float): MACD fast/line value (12-period).
            macd_26 (float): MACD signal/line value (26-period).
            ema_100 (float): Exponential Moving Average over 100 periods.
            rsi_6 (float): Relative Strength Index over 6 periods.
            bar_list (Optional[Sequence[Tuple[float, float, float, float]]], optional):
                Recent OHLC bars as (open, close, low, high) tuples. Defaults to None.

        Notes:
            - Internally, `bar_list` is stored as a list to avoid accidental
              mutation of the input sequence.
        """
        self.date: str = date
        self.price: float = float(price)
        self.macd_12: float = float(macd_12)
        self.macd_26: float = float(macd_26)
        self.ema_100: float = float(ema_100)
        self.rsi_6: float = float(rsi_6)
        self.bar_list: List[Tuple[float, float, float, float]] = (
            list(bar_list) if bar_list else []
        )

    def __str__(self) -> str:
        """
        Return a compact, human-readable summary of key indicators.

        Returns:
            str: A single-line summary string.
        """
        return (
            f"PRICE: {self.price:.2f} | "
            f"MACD_12: {self.macd_12:.2f} | "
            f"MACD_26: {self.macd_26:.2f} | "
            f"EMA_100: {self.ema_100:.2f} | "
            f"RSI_6: {self.rsi_6:.2f}"
        )

    def clone(self) -> "MarketSnapshot":
        """
        Create a deep copy of the snapshot, including the OHLC bar list.

        Returns:
            MarketSnapshot: A new snapshot instance with the same values.
        """
        return MarketSnapshot(
            date=self.date,
            price=self.price,
            macd_12=self.macd_12,
            macd_26=self.macd_26,
            ema_100=self.ema_100,
            rsi_6=self.rsi_6,
            bar_list=copy.deepcopy(self.bar_list),
        )

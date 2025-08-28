from __future__ import annotations
from abc import ABC, abstractmethod
from typing import final
from utils.logger import Logger
from bot.rem_bot import RemBot


class PositionState(ABC):
    """
    Abstract base class representing a trading position state.

    This class defines the interface and core workflow for handling position states.
    Each concrete state (e.g., Long, Short, NoPosition) must implement the `apply` method
    to define specific trading logic.
    """

    def __init__(self, parent: RemBot) -> None:
        """
        Initialize a PositionState.

        Args:
            parent (RemBot): The RemBot instance that manages trading logic,
                             containing shared resources like DataManager and BinanceAdapter.
        """
        self.parent: RemBot = parent

    @final
    def step(self) -> None:
        """
        Execute one step of the position state.

        This method refreshes market indicators and applies the logic
        of the current position state. It also includes exception handling
        to prevent interruptions in the trading loop.
        """
        try:
            self._refresh_indicators()
            self.apply()
        except Exception as e:
            Logger.log_exception(str(e))

    @abstractmethod
    def apply(self) -> None:
        """
        Apply the trading logic for this position state.

        Subclasses must override this method to implement specific
        entry/exit conditions and state transitions.
        """
        pass

    def _refresh_indicators(self) -> None:
        """
        Refresh the latest market indicators.

        Updates the parent's DataManager with a fresh snapshot
        of indicators fetched from the BinanceAdapter.
        """
        self.parent.data_manager.indicator_snapshot = (
            self.parent.binance_adapter.indicator_manager.fetch_indicators()
        )

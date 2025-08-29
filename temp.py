from __future__ import annotations

"""
Configuration model and helpers for RemBot runtime and trading parameters.
Provides a frozen dataclass with validation and convenience constructors
to load settings from a TOML file or a generic mapping.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Pattern
from utils.file_utils import FileUtils
import re

# Valid interval pattern such as "15m", "1h", "4h", "1d", etc.
INTERVAL_RE: Pattern[str] = re.compile(r"^\d+(s|m|h|d|w)$")


@dataclass(frozen=True)
class BotSettings:
    """
    Immutable configuration for the trading bot.

    Attributes:
        API_PUBLIC_KEY (str): Public API key for the exchange.
        API_SECRET_KEY (str): Secret API key for the exchange.
        SYMBOL (str): Trading symbol, e.g., "ETHUSDT".
        COIN_PRECISION (int): Number of decimal places to round prices/amounts.
        TP_RATIO (float): Take-profit ratio applied to entry price.
        SL_RATIO (float): Stop-loss ratio applied to entry price.
        LEVERAGE (int): Futures leverage multiplier (>= 1).
        TEST_MODE (bool): If True, orders are not placed on the exchange.
        INTERVAL (str): Candle interval (e.g., "15m", "1h").
        SLEEP_DURATION (float): Loop sleep duration in seconds.
        OUTPUT_CSV_PATH (str): Path to the CSV file where results are appended.
    """

    API_PUBLIC_KEY: str
    API_SECRET_KEY: str
    SYMBOL: str = "ETHUSDT"
    COIN_PRECISION: int = 2
    TP_RATIO: float = 0.0050
    SL_RATIO: float = 0.0050
    LEVERAGE: int = 1
    TEST_MODE: bool = True
    INTERVAL: str = "15m"
    SLEEP_DURATION: float = 20.0
    OUTPUT_CSV_PATH: str = "./results.csv"

    @classmethod
    def from_toml(cls, path: str | Path = "settings.toml") -> "BotSettings":
        """
        Create a BotSettings instance from a TOML file.

        Args:
            path (str | Path): Path to the TOML configuration file.

        Returns:
            BotSettings: A validated, immutable settings instance.
        """
        cfg = FileUtils.read_toml_file(str(path))
        return cls.from_mapping(cfg)

    @classmethod
    def from_mapping(cls, cfg: Mapping[str, Any]) -> "BotSettings":
        """
        Create a BotSettings instance from a generic mapping (dict-like).

        The mapping is expected to contain the following optional sections:
        "api", "position", "runtime", and "output".

        Args:
            cfg (Mapping[str, Any]): Source mapping containing configuration.

        Returns:
            BotSettings: A validated, immutable settings instance.

        Raises:
            TypeError: If a field has an invalid type (e.g., test_mode not bool).
        """
        api = cfg.get("api", {}) or {}
        position = cfg.get("position", {}) or {}
        runtime = cfg.get("runtime", {}) or {}
        output = cfg.get("output", {}) or {}

        tm = runtime.get("test_mode", True)
        if not isinstance(tm, bool):
            raise TypeError("test_mode must be a boolean.")

        return cls(
            API_PUBLIC_KEY=str(api.get("public_key", "")),
            API_SECRET_KEY=str(api.get("secret_key", "")),
            SYMBOL=str(position.get("symbol", "ETHUSDT")),
            COIN_PRECISION=int(position.get("coin_precision", 2)),
            TP_RATIO=float(position.get("tp_ratio", 0.0050)),
            SL_RATIO=float(position.get("sl_ratio", 0.0050)),
            LEVERAGE=int(position.get("leverage", 1)),
            TEST_MODE=tm,
            INTERVAL=str(runtime.get("interval", "15m")),
            SLEEP_DURATION=float(runtime.get("sleep_duration", 20.0)),
            OUTPUT_CSV_PATH=str(output.get("csv_path", "./results.csv")),
        )

    def __post_init__(self) -> None:
        """
        Validate settings fields after dataclass initialization.

        Raises:
            ValueError: If any field fails validation (e.g., empty SYMBOL,
                        non-positive ratios, invalid interval format, etc.).
        """
        if not self.SYMBOL or not self.SYMBOL.strip():
            raise ValueError("SYMBOL cannot be empty.")
        if self.COIN_PRECISION < 0:
            raise ValueError("COIN_PRECISION cannot be negative.")
        if self.LEVERAGE < 1:
            raise ValueError("LEVERAGE must be at least 1.")
        if self.TP_RATIO <= 0:
            raise ValueError("TP_RATIO must be greater than 0.")
        if self.SL_RATIO <= 0:
            raise ValueError("SL_RATIO must be greater than 0.")
        if not INTERVAL_RE.match(self.INTERVAL):
            raise ValueError(
                f"Invalid INTERVAL: '{self.INTERVAL}'. Examples: '15m', '1h', '4h', '1d'."
            )
        if self.SLEEP_DURATION <= 0:
            raise ValueError("SLEEP_DURATION must be greater than 0.")
        if not self.TEST_MODE and (not self.API_PUBLIC_KEY or not self.API_SECRET_KEY):
            raise ValueError("API keys must not be empty when TEST_MODE is False.")
        if not self.OUTPUT_CSV_PATH or not str(self.OUTPUT_CSV_PATH).strip():
            raise ValueError("OUTPUT_CSV_PATH cannot be empty.")


# Eagerly load settings from the default TOML file path.
SETTINGS: BotSettings = BotSettings.from_toml("settings.toml")

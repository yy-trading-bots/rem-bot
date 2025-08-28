from bot.rem_bot import RemBot

def main() -> None:
    """
    Entry point of the trading bot.

    Initializes the RemBot instance and starts its execution loop.
    """
    rembot: RemBot = RemBot()
    rembot.run()

if __name__ == "__main__":
    main()

import logging

def setup_logger():
    """Setup the logger for the application.
    This function configures the logging settings for the application, including log level, format, and handlers.
    It sets up both console and file handlers to capture logs.
    The log level is set to INFO, and logs are formatted to include the timestamp, logger name, log level, and message.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log")
        ]
    )
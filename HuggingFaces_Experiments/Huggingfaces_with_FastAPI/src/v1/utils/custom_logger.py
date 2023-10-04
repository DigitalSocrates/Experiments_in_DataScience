import logging

class CustomLogger:
    """
    A class for initializing and managing a logger for a Python script.

    This class simplifies the process of setting up a logger with 
    a specified script name.

    Usage:
        script_name = "simple_example"
        logger_initializer = ScriptLogger(script_name)
        logger = logger_initializer.get_logger()

        # Now you can use the logger for logging messages
        logger.debug("This is a debug message.")
        logger.info("This is an info message.")
        logger.warning("This is a warning message.")
        logger.error("This is an error message.")
        logger.critical("This is a critical message.")
    """
    def __init__(self, script_name):
        """
        Initialize a logger with the given script name.

        Args:
            script_name (str): The name of the script or logger.

        Returns:
            None
        """
        self.logger = logging.getLogger(script_name)
        self.logger.setLevel(logging.DEBUG)
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s : %(message)s')
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def get_logger(self):
        """
        Get the initialized logger instance.

        Returns:
            logging.Logger: The logger instance.
        """
        return self.logger

if __name__ == "__main__":
    script_name = "set_logger"
    logger_initializer = Logger_Custom(script_name)
    logger = logger_initializer.get_logger()

    # Now you can use the logger for logging messages
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")

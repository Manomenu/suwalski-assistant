import logging
import os
from logging.handlers import TimedRotatingFileHandler

def setup_logging():
    """
    Configures logging to output to both console and a rotating file.
    Logs in the 'logs' folder are kept for 3 days.
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "suwalski_assistant.log")

    # Formatter for logs
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # Timed Rotating File Handler: rotates every day ('D'), keeps 3 backups (backupCount=3)
    file_handler = TimedRotatingFileHandler(
        log_file, 
        when="D", 
        interval=1, 
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers to avoid duplicates if setup is called multiple times
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.info("Logging initialized. Logs are stored in 'logs/' and kept for 3 days.")

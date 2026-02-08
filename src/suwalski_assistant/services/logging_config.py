import logging
import os
from logging.handlers import TimedRotatingFileHandler

def setup_logging():
    """
    Configures logging:
    - Console: INFO level and above.
    - logs/debug.log: DEBUG level and above (full logs).
    - logs/info.log: INFO level and above.
    Logs are kept for 3 days.
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Formatter for logs
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # DEBUG File Handler (Full logs)
    debug_file = os.path.join(log_dir, "debug.log")
    debug_handler = TimedRotatingFileHandler(
        debug_file, when="D", interval=1, backupCount=3, encoding="utf-8"
    )
    debug_handler.setFormatter(formatter)
    debug_handler.setLevel(logging.DEBUG)

    # INFO File Handler (Info and above)
    info_file = os.path.join(log_dir, "info.log")
    info_handler = TimedRotatingFileHandler(
        info_file, when="D", interval=1, backupCount=3, encoding="utf-8"
    )
    info_handler.setFormatter(formatter)
    info_handler.setLevel(logging.INFO)

    # Console Handler (Info and above)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        
    root_logger.addHandler(debug_handler)
    root_logger.addHandler(info_handler)
    root_logger.addHandler(console_handler)

    logging.info("Logging initialized: Console (INFO), debug.log (DEBUG), info.log (INFO).")

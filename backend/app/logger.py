import logging

# Create a custom logger

logger = logging.getLogger(__name__)
logger.handlers = logger.handlers

# Create handler and formatter
c_format = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
)
c_handler = logging.StreamHandler()

# Set formatter handler
c_handler.setFormatter(c_format)

# Add handler to logger
logger.addHandler(c_handler)

# Set level
logger.setLevel(logging.INFO)

logger.propagate = False

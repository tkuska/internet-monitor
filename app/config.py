import os

MINIMAL_SPEED = float(os.getenv("MINIMAL_SPEED", 300))
ACCEPTABLE_SPEED = float(os.getenv("ACCEPTABLE_SPEED", 700))
MAX_SPEED = float(os.getenv("MAX_SPEED", 1000))

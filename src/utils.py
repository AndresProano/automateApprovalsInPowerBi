import logging, os, sys
def setup_logging():
    level = getattr(logging, os.getenv("LOG_LEVEL","INFO").upper(), logging.INFO)
    logging.basicConfig(stream=sys.stdout, level=level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
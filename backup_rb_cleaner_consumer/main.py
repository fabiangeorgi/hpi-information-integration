import logging
import os

from rb_cleaner import RbCleaner

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
log = logging.getLogger(__name__)


def run():
    RbCleaner()


if __name__ == "__main__":
    run()

from datetime import date
from manager import book_paddle_automated
import os
import logging
import traceback
from data import data
from Util import Util

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("paddle.log", mode="w"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info("Started paddle reservation script")


# Read inputs from GitHub Actions
input_time = os.environ.get("INPUT_TIMESLOT", "16:30")  # fallback to default
input_days = int(os.environ.get("INPUT_DAYS_IN_ADVANCE", "7"))

logger.info(f"Input time slot: {input_time}")
logger.info(f"Booking days in advance: {input_days}")

# Set values dynamically from inputs
for court in [data.COURT1, data.COURT2]:
    court.time = Util(is_tennis=False).calc_time(input_time)
    court.days_in_advance = input_days


def make_res(res):
    logger.info(
        f"--- Attempting reservation ---\n"
        f"Court: {res.court}\n"
        f"Names: {res.names}\n"
        f"Code: {res.code}\n"
        f"Days in advance: {res.days_in_advance}\n"
    )

    try:
        court = book_paddle_automated(res)
        logger.info(f"✅ First attempt successful: {court}")

    except Exception as e:
        logger.warning(f"⚠️ First attempt failed: {e}. Retrying...")
        try:
            court = book_paddle_automated(res)
            logger.info(f"✅ Retry successful: {court}")
        except Exception as e:
            logger.error("❌ Retry failed", exc_info=True)
            raise

    logger.info(f"✔ Final reservation status: {court}")
    logger.info("-" * 50)


def court1():
    make_res(data.COURT1)


def court2():
    make_res(data.COURT2)


if __name__ == "__main__":
    logger.info(f"\nRunning on {date.today()}\n")

    try:
        court1()
    except Exception as e:
        logger.error("❌ Court 1 reservation failed", exc_info=True)

    try:
        court2()
    except Exception as e:
        logger.error("❌ Court 2 reservation failed", exc_info=True)

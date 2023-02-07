#!/bin/env python3

import emoji
import logging
import sqlalchemy as sa
import time
from anbot.chat import session

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    while True:
        time.sleep(0.25)

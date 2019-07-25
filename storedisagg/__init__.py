#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 20:09:56 2018

@author: mcsoini
"""

import logging

def _get_logger(name):
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        f_handler = logging.StreamHandler()
        f_handler.setLevel(0)
        format_str = '> %(asctime)s - %(levelname)s - %(name)s - %(message)s'
        f_format = logging.Formatter(format_str, "%H:%M:%S")
        f_handler.setFormatter(f_format)
        logger.addHandler(f_handler)

    return logger

logger = _get_logger(__name__)


from storedisagg.compcalc import ComponentCalculator
from storedisagg.storagedisaggregator import StDisaggregator

from storedisagg.example.example_data import get_example_data_100


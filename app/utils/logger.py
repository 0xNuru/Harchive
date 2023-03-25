#!/usr/bin/python3
from loguru import logger
from os.path import abspath, join, dirname
import os
import sys


"""Establishes the log format"""

base_dir = abspath("..")

log_dir = base_dir+ "/logs"
# create folder if not existing
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger.remove(0)
logger.add("logs/log_file.log", format = "{time:YYYY MMM D  HH:mm:ss.SS} | {file} took {elapsed} to execute | {level} | {message}", colorize=True)
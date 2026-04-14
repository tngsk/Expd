"""
Exploratory Design Process Support Tool (EXPD)

A tool for parameter exploration and experimentation with external applications.
"""

__version__ = "0.1.0"
__author__ = "EXPD Development Team"

from expd.config import Config
from expd.core import ExperimentRunner
from expd.interface import AppInterface

__all__ = ["ExperimentRunner", "AppInterface", "Config", "__version__"]

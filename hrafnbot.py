#!/usr/bin/env python3
"""
HrafnBot entry point script
"""
import sys
import os

# Add the hrafnbot package to the path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from hrafnbot.main import cli

if __name__ == "__main__":
    cli()
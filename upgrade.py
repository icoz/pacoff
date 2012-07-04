#!/usr/bin/env python3

import os

print("Running upgrade...")
os.system("sudo pacman -Suyp > download.info")

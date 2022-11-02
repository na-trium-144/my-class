#!/usr/bin/env python3
from tkinter import filedialog
import sys
print(filedialog.askdirectory(initialdir=sys.argv[1]), end="")

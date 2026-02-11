#!/usr/bin/env python3

import sys
from pathlib import Path

CURDIR = Path(__file__).parent
sys.path.insert(0, str(CURDIR))

# pylint: disable=wrong-import-position
from jimlet.app import JimletApp

app = JimletApp()
app.run(start_mainloop=True)
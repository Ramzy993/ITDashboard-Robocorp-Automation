#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ˅

import pathlib
import os

ROOT_FOLDER = pathlib.Path(__file__).parent.absolute().parent.absolute()
COMMON_FOLDER = pathlib.Path(__file__).parent.absolute()
DOWNLOAD_FOLDER = os.path.join(ROOT_FOLDER, 'output')

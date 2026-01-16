#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of morss
#
# Copyright (C) 2013-2020 pictuga <contact@pictuga.com>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>.

"""
Vercel serverless function entry point for Morss
This module adapts the WSGI application for Vercel's serverless environment
"""

# Import sys and os inside a function to avoid Vercel's issubclass() TypeError
# Vercel's runtime inspects module-level objects, and calling issubclass() on
# non-class objects like sys and os modules causes a TypeError
def _setup_path():
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

_setup_path()

# Import the WSGI application as 'handler' for Vercel
# Note: Only export 'handler' to avoid Vercel's issubclass() TypeError
from morss.wsgi import application as handler

# Explicitly define what should be exported from this module
# This prevents Vercel's runtime from inspecting other imports
__all__ = ['handler']

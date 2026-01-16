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

# Set up the path to import morss module
import sys
import os
_parent_dir = os.path.join(os.path.dirname(__file__), '..')
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

# Import and re-export as handler for Vercel
# Only export 'handler' to avoid confusing Vercel's runtime inspection
from morss.wsgi import application as handler

# Clean up namespace to prevent Vercel's issubclass() TypeError
# Delete module-level imports that aren't needed as exports
del sys, os, _parent_dir

# Explicitly define exports to avoid Vercel's runtime inspection issues
__all__ = ['handler']

#!/usr/bin/env python3

# Copyright (c) 2009 Giampaolo Rodola'. All rights reserved.
# Use of this source code is governed by a BSD-style license

"""
Purge mptcplib installation by removing mptcplib-related files and
directories found in site-packages directories. This is needed mainly
because sometimes "import mptcplib" imports a leftover installation
from site-packages directory instead of the main working directory.
"""

import os
import shutil
import site

PKGNAME = "mptcplib"

def rmpath(path):
    if os.path.isdir(path):
        print("rmdir " + path)
        shutil.rmtree(path)
    else:
        print("rm " + path)
        os.remove(path)


def main():
    locations = [site.getusersitepackages()]
    locations.extend(site.getsitepackages())
    for root in locations:
        if os.path.isdir(root):
            for name in os.listdir(root):
                if PKGNAME in name:
                    abspath = os.path.join(root, name)
                    rmpath(abspath)

main()

#!/usr/bin/env python3

# -*- encoding: utf-8 -*-
#
# Copyright 2022 LIP
#
# Author: Mario David <mariojmdavid@gmail.com>
#

"""upload packages to nexus oss repositories
"""

import sys
import utils


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage:', sys.argv[0], '<package_name_version> (without extension .json)')
        sys.exit(1)

    prod_name = sys.argv[1]
    utils.upload_pkg(prod_name)
    sys.exit(0)

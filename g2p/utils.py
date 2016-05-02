#!/usr/bin/env python
#-*- encoding:utf-8 -*-

# utils.py - Extra functions
# Copyright (C) 2015  Alessandro Bokan
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:  Alessandro Bokan <alessandro.bokan@gmail.com>

import codecs


def load_prefixes(PATH_PREFIXES):
    """
    Return a list of prefixes and their phonemes.

    Args:
        PATH_PREFIXES: Prefixes file path

    Returns: List of prefixes and their phonemes, e.g, "crip-to	kɾipɪ-to"

    """
    # Open file
    f = codecs.open(PATH_PREFIXES, 'r', 'utf-8')
    # Get prefixes
    prefixes = [tuple(line.strip().split('\t')) for line in f.readlines()]
    # Close file
    f.close()

    return prefixes


def load_homographs_heterophones(PATH_HOMOGRAPHS_HETEROPHONES):
    """
    Return a dictionary of phonemes of the Homographs Heterophones (HHs).

    Args:
        PATH_HOMOGRAPHS_HETEROPHONES: HHs file path

    Returns: Dictionary of phonemes of HHs, e.g. "molho -> ˈmo.ʎʊ | ˈmɔ.ʎʊ"

    """
    # Open file
    f, dct = codecs.open(PATH_HOMOGRAPHS_HETEROPHONES, 'r', 'utf-8'), {}
    # Get HHs
    for line in f.readlines():
        spl = line.strip().split('|')
        if dct.get(spl[0]) and spl[2] not in dct.get(spl[0]):
            dct[spl[0]] = dct[spl[0]] + '|' + spl[2]
        else:
            dct[spl[0]] = spl[2]
    # Close file
    f.close()

    return dct
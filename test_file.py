#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from __future__ import unicode_literals

from argparse import ArgumentParser

from syllables.ceci import CECISyllableSeparator
from syllables.silva2011 import Silva2011SyllableSeparator

from stress.tonic import StressDetector

from g2p.g2p import G2PTranscriber

import os
import codecs


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("the file \"%s\" does not exist!" % arg)
    elif not arg.endswith(".txt"):
        parser.error("\"%s\" is not a text file!" % arg)
    else:
        return codecs.open(arg, 'r', 'utf-8')  # return an open file handle

if __name__ == '__main__':
    # Initialize ArgumentParser class
    parser = ArgumentParser()
    # Parse command line arguments
    parser.add_argument(
        '-s', '--separator',
        dest='separator',
        required=True,
        type=str,
        choices=['silva', 'ceci'],
        help=u'Select the separator/syllabification algorithm',
    )
    parser.add_argument(
        '-f', '--file',
        dest='file',
        required=True,
        help=u'Text file',
        type=lambda x: is_valid_file(parser, x),
    )
    args = parser.parse_args()

    # Open output file
    f = codecs.open('output.txt', 'w', 'utf-8')
    # Iterate input file
    for line in args.file.readlines():
        # Get input word
        word = line.strip()
        # Initialize syllable separator
        separator = Silva2011SyllableSeparator(word) if args.separator == 'silva2011' else CECISyllableSeparator(word)
        # Initialize stress detector
        stress = StressDetector(word)
        # Separate syllables
        syllables = separator.separate()
        # Transform list of syllables, e.g. [u'co', u'mi', u'da'] -> 'co-mi-da'
        syllables = ('-').join(syllables)
        # Get stress syllable positions
        a, b = stress.get_stress_syllable_with_hyphen(syllables)
        # Initialize g2p transcriber
        transcriber = G2PTranscriber(word, syllables)
        # Transcribe to phonemes
        phonemes = transcriber.transcriber(stress)

        f.write('{0} -> [{1}] | {2}[{3}]{4}\r\n'.format(word, phonemes, syllables[:a], syllables[a:b], syllables[b:]))

    # Close output file
    f.close()

    print '\nSuccess!!! Open the "output.txt" file to see the result.\n'
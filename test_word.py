#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from __future__ import unicode_literals

from argparse import ArgumentParser

from syllables.ceci import CECISyllableSeparator
from syllables.silva2011 import Silva2011SyllableSeparator

from stress.tonic import StressDetector

from g2p.g2p import G2PTranscriber


if __name__ == '__main__':
    # Initialize ArgumentParser class
    parser = ArgumentParser()
    # Parse command line arguments
    parser.add_argument(
        '-s', '--separator',
        dest="separator",
        required=True,
        type=str,
        choices=['silva', 'ceci'],
        help=u'Select the separator/syllabification algorithm',
    )
    parser.add_argument(
        '-w', '--word',
        dest="word",
        required=True,
        help=u'Word',
    )
    args = parser.parse_args()
    # Get the input word
    word = args.word.decode('utf-8')
    # Initialize the syllable separator
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

    print '\n{0} -> [{1}] | {2}[{3}]{4}\n'.format(word, phonemes, syllables[:a], syllables[a:b], syllables[b:])

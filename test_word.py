#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from __future__ import unicode_literals

from argparse import ArgumentParser

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
    word = args.word.decode('utf-8').lower()
    # Initialize G2P transcriber
    g2p = G2PTranscriber(word, algorithm=args.separator)

    print '\n{0} -> [{1}] | {2} | {3}\n'.format(
        word,
        g2p.transcriber(),
        g2p.get_syllables_with_hyphen(),
        g2p.get_syllables_with_stress_boundaries()
    )
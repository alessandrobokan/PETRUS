#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from __future__ import unicode_literals

from argparse import ArgumentParser

from g2p.g2p import G2PTranscriber

import os
import codecs


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error('the file "%s" does not exist!' % arg)
    elif not arg.endswith(".txt"):
        parser.error('"%s" is not a text file!' % arg)
    else:
        return codecs.open(arg, "r", "utf-8")  # return an open file handle


if __name__ == "__main__":
    # Initialize ArgumentParser class
    parser = ArgumentParser()
    # Parse command line arguments
    parser.add_argument(
        "-s",
        "--separator",
        dest="separator",
        required=True,
        type=str,
        choices=["silva", "ceci"],
        help="Select the separator/syllabification algorithm",
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="file",
        required=True,
        help="Text file",
        type=lambda x: is_valid_file(parser, x),
    )
    args = parser.parse_args()

    # Open output file
    f = codecs.open("output.txt", "w", "utf-8")
    # Iterate input file
    for line in args.file.readlines():
        # Get input word
        word = line.strip().lower()
        # Initialize g2p transcriber
        g2p = G2PTranscriber(word, algorithm=args.separator)
        # Write file
        f.write(
            "{0} -> [{1}] | {2} | {3}\r\n".format(
                word,
                g2p.transcriber(),
                g2p.get_syllables_with_hyphen(),
                g2p.get_syllables_with_stress_boundaries(),
            )
        )
    # Close output file
    f.close()

    print('\nSuccess!!! Open the "output.txt" file to see the result.\n')

#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# g2p.py - Grapheme to phoneme transcriber algorithm based on the Thesis
# of Marquiafavel [2014].
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

from __future__ import unicode_literals

from .utils import load_prefixes, load_homographs_heterophones

from stress.tonic import StressDetector

from syllables.silva2011 import Silva2011SyllableSeparator
from syllables.ceci import CECISyllableSeparator

import re
import os
import sys

if sys.version_info[0] == 3:
    unichr = chr

PATH_PREFIXES = os.path.dirname(__file__) + "/resources/prefixes.txt"

PATH_HOMOGRAPHS_HETEROPHONES = (
    os.path.dirname(__file__) + "/resources/homographs_heterophones.txt"
)

# Load prefixes with their phonemes
PREFIXES = load_prefixes(PATH_PREFIXES)

# Load Homographs Heterophones (HHs)
HHs = load_homographs_heterophones(PATH_HOMOGRAPHS_HETEROPHONES)

# Consonants
C = [
    "b",
    "c",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "m",
    "n",
    "p",
    "q",
    "r",
    "s",
    "t",
    "v",
    "w",
    "x",
    "y",
    "z",
]

# Vowels
V = ["a", "e", "o", "á", "é", "í", "ó", "ú", "ã", "õ", "â", "ê", "ô", "à", "ü"]


class G2PTranscriber(object):
    """
    This class implements the G2P transcriber algorithm presented in the
    Phd thesis of Marquiafavel [2014]

    """

    def __init__(self, word, algorithm="silva"):
        # Initialize word
        try:
            self.word = word.decode("utf-8").lower()
        except:
            self.word = word.lower()

        # Initialize stress detector
        self.stress = StressDetector(self.word)

        # Initialize syllable separator
        if algorithm == "silva":
            self.separator = Silva2011SyllableSeparator(
                self.word, self.stress.get_stress_vowel()
            )
        else:
            self.separator = CECISyllableSeparator(self.word)

        # Initialize syllables
        self.syllables = self.get_syllables_with_hyphen()

    def get_syllables(self):
        """
        Returns a list of syllables

        Returns: List of syllables, e.g. ['cho', 'co', 'la', 'te']

        """
        try:
            return self.separator.separate()
        except (ValueError, IndexError):
            return [self.word]

    def get_syllables_with_hyphen(self):
        """
        Returns syllables with hyphen

        Returns: syllables, e.g, "cho-co-la-te"

        """
        return ("-").join(self.get_syllables())

    def get_syllables_with_stress_boundaries(self):
        """
        Returns syllables divided by '-' pointing the stress syllable with '[]'

        Returns: syllables with stress boundaries, e.g "cho-co-[la]-te"

        """
        a, b = self.stress.get_stress_syllable_with_hyphen(self.syllables)

        return "{0}[{1}]{2}".format(
            self.syllables[:a], self.syllables[a:b], self.syllables[b:]
        )

    def is_tonic_syllable(self, a, b, i):
        return True if a <= i and i <= b else False

    def is_last_syllable(self, i):
        mth = [m.start() for m in re.finditer("-", self.syllables)]
        a, b = mth[-1] if mth else 0, len(self.syllables) - 1

        return True if a <= i and i <= b else False

    def is_oxytone(self, ts1, ts2, i):
        return (
            True
            if self.is_tonic_syllable(ts1, ts2, i) and self.is_last_syllable(i)
            else False
        )

    def pre_transcriber(self):
        i, j, tam, w = 0, 0, len(self.syllables), self.syllables
        for prefix, phones in PREFIXES:
            if self.syllables.find(prefix) == 0:
                if self.syllables in ["e-co-cha-to", "e-co-rre-no-va-ção"]:
                    phones = "ɛ-ko"
                elif self.syllables in ["e-le-tro-do", "e-le-trô-ni-co"]:
                    phones = "e-le-tɾo"
                elif self.syllables.find("te-le-fo-ne") == 0:
                    phones = "te-le"
                i, j = len(prefix), len(phones)
                w = phones + w[i:]

                return i, j, tam, self.syllables, w
        return i, j, tam, self.syllables, w

    def transcriber(self):
        """
        Transcribe graphemes to phonemes.

        Args:
            stress: StressDetector object

        Returns: Phonemes, e.g. ʃo.ko.ˈla.ʧɪ

        """
        # Verify if the word is a Homograph Heterophone (HH)
        if HHs.get(self.word):
            return HHs.get(self.word).replace("|", ", ")

        # Initialize variables
        i, j, tam, word, w = self.pre_transcriber()

        # Get stress syllable boundaries
        ts1, ts2 = self.stress.get_stress_syllable_with_hyphen(self.syllables)

        # TODO Translate commentaries from Portuguese to English

        while i < tam:
            # ---------------------------------------------------------------------
            # ----------------------------CONSOANTES-------------------------------
            # ---------------------------------------------------------------------
            if word[i] == "p":
                T = ["b", "c", "ç", "f", "g", "n", "s", "t"]
                # Quando é seguido das consontes 'b,c,ç,f,g,b,s,t' na mesma sílaba
                if (tam - 1 > i and word[i + 1] in T) or (
                    tam - 2 > i and word[i + 1] == "-" and word[i + 2] in T
                ):
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + w[j + 1 :]
                    j += 1
                # Caso contrario fica com 'p'

            elif word[i] == "b":
                T = ["c", "d", "j", "m", "n", "p", "t", "v", "s"]
                # Quando seguido das consontes 'c,d,j,m,n,p,t,v,s' na mesma sílaba
                if tam - 1 > i and word[i + 1] in T:
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + w[j + 1 :]
                    j += 1
                # Quando é seguida de consoante na sílaba tônica seguinte
                elif (
                    tam - 2 > i
                    and word[i + 1] == "-"
                    and word[i + 2] == "s"
                    and self.is_tonic_syllable(ts1, ts2, i + 2)
                ):
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + "-" + "s" + w[j + 3 :]
                    j += 3
                    i += 2
                # Quando é seguida de consoante na sílaba não tônica seguinte
                elif (
                    tam - 2 > i
                    and word[i + 1] == "-"
                    and word[i + 2] in T
                    and not self.is_tonic_syllable(ts1, ts2, i + 2)
                ):
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + "-" + w[j + 2 :]
                    j += 2
                    i += 1
                # Quando for final de palavra
                if tam - 1 == i:
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + w[j + 1 :]
                    j += 1

            elif word[i] == "c":
                T = ["e", "é", "ê", "i", "í"]
                # Quando predecer e, é, ê, i, í, na mesma sílaba
                if tam - 1 > i and word[i + 1] in ["e", "é", "ê", "i", "í"]:
                    w = w[:j] + "s" + w[j + 1 :]
                # Quando a sílaba seguinte inicia com consoante, sem 'r' e 'l'
                elif (
                    tam - 2 > i
                    and word[i + 1] == "-"
                    and word[i + 2] in C
                    and not word[i + 2] in ["r", "l"]
                ):
                    ipa = unichr(int("026A", 16))
                    w = w[:j] + "k" + ipa + w[j + 1 :]
                    j += 1
                # Quando é a última letra da palavra
                elif tam - 1 == i:
                    ipa = unichr(int("026A", 16))
                    w = w[:j] + "k" + ipa
                # Quando tem cç
                elif tam - 2 > i and word[i + 1] == "-" and word[i + 2] == "ç":
                    ipa = unichr(int("026A", 16))
                    w = w[:j] + "k" + ipa + w[j + 1 :]
                    j += 1
                # Quando for seguida de h
                elif tam - 1 > i and word[i + 1] == "h":
                    ipa = unichr(int("0283", 16))
                    w = w[:j] + ipa + w[j + 2 :]
                    i += 1
                # Quando não predecer e, é, ê, i, í
                elif tam - 1 > i and not word[i + 1] in T:
                    w = w[:j] + "k" + w[j + 1 :]

            elif word[i] == "ç":
                # Sempre reemplazar por 's'
                w = w[:j] + "s" + w[j + 1 :]

            elif word[i] == "t":
                # Antes de 'i'
                if tam - 1 > i and word[i + 1] in ["i", "í"]:
                    ipa = unichr(int("02A7", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Antes de 'e' ao final da palavra
                elif tam - 2 == i and word[i + 1] == "e":
                    ipa = unichr(int("02A7", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Antes de 'es' ao final da palavra
                elif tam - 3 == i and word[i + 1 : i + 3] == "es":
                    ipa = unichr(int("02A7", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando for seguida por consonante em sílaba consecutiva
                elif tam - 2 > i and word[i + 1] == "-" and word[i + 2] in C:
                    ipa = unichr(int("02A7", 16)) + unichr(int("026A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                    j += 1
                # Quando for seguida por 'm, n' na mesma sílaba
                elif tam - 1 > i and word[i + 1] in ["m", "n"]:
                    ipa = unichr(int("02A7", 16)) + unichr(int("026A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                    j += 1

            elif word[i] == "d":
                tmp = ["a", "â", "ã", "à", "á", "é", "ê", "ô", "ó", "o", "u", "ú"]
                # Quando for seguida de 's' na mesma sílaba
                if tam - 1 > i and word[i + 1] == "s":
                    ipa = unichr(int("02A4", 16)) + unichr(int("026A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                    j += 1
                # Quanto for seguida da vogal a,â,ã,à,á,é,ê,ô,ó,o,u,ú ou
                # seguida de uma consonante na mesma sílaba
                elif tam - 1 > i and word[i + 1] in tmp + C:
                    w = w[:j] + "d" + w[j + 1 :]
                # Quando for antes de 'i'
                elif tam - 1 > i and word[i + 1] == "i":
                    ipa = unichr(int("02A4", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando 'e' é átono em finais de palavras
                elif tam - 2 == i and word[i + 1] == "e":
                    ipa = unichr(int("02A4", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Antes de 'es' ao final da palavra
                elif tam - 3 == i and word[i + 1 : i + 3] == "es":
                    ipa = unichr(int("02A4", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando for seguida por consonante em sílaba consecutiva
                elif tam - 1 > i and word[i + 1] == "-" and word[i + 2] in C:
                    ipa = unichr(int("02A4", 16)) + unichr(int("026A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                    j += 1
                # Quando for ultima letra
                elif tam - 1 == i:
                    ipa = unichr(int("02A4", 16))
                    w = w[:j] + ipa + w[j + 1 :]

            elif word[i] == "f":
                # Quando for seguida por consonante em sílaba consecutiva
                if tam - 2 > i and word[i + 1] == "-" and word[i + 2] in C:
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + w[j + 1 :]
                    j += 1
                # Quando é final de palavra
                elif tam - 1 == i:
                    ipa = unichr(int("026A", 16))
                    w = w + ipa

            elif word[i] == "g":
                # Quando for seguida de 'a,â,ã,à,á,ô,ó,o,u,ú,l,r'
                T1 = ["a", "â", "ã", "à", "á", "ô", "ó", "o", "u", "ú", "l", "r"]
                T2 = ["e", "é", "ê", "i", "í"]
                T3 = ["a", "o"]
                T4 = ["e", "i"]
                # Quando for seguida por 'e,é,ê,i,í'
                if tam - 1 > i and word[i + 1] in T2:
                    ipa = unichr(int("0292", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando for seguido de consoante
                elif tam - 1 > i and word[i + 1] in C and word[i + 1] not in ["l", "r"]:
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + w[j + 1 :]
                    j += 1
                # Quando for seguido de consoante na seguinte sílaba
                elif (
                    tam - 2 > i
                    and word[i + 1] == "-"
                    and word[i + 2] in C
                    and word[i + 2] not in ["l", "r"]
                ):
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + w[j + 1 :]
                    j += 1
                # Quando 'qu' for seguido de 'e' seguido 'n'
                elif (
                    len(word) - 3 > i
                    and word[i + 1] == "u"
                    and word[i + 2] in ["e", "é", "ê"]
                    and word[i + 3] == "n"
                ):
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + "g" + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando 'gu' for seguido de 'a, o'
                elif tam - 1 > i and word[i + 1] == "u" and word[i + 2] in T3:
                    ipa = unichr(int("028A", 16))
                    w = w[: j + 1] + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando 'gu' for seguido de 'e, i'
                elif tam - 1 > i and word[i + 1] == "u" and word[i + 2] in T4:
                    w = w[: j + 1] + w[j + 2 :]
                    i += 1

            elif word[i] == "h":
                # No início da palavra não tem som
                if i == 0:
                    w = w[j + 1 :]
                    j -= 1

            elif word[i] == "v":
                # Quando for seguida de 'n' na seguinte silaba
                if tam - 2 > i and word[i + 1] == "-" and word[i + 2] in C:
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + w[j + 1 :]
                    j += 1
                # Quando for seguida de 'n' na mesma silaba
                if tam - 1 > i and word[i + 1] in C:
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + w[j + 1 :]
                    j += 1
                # Caso contrario fica com 'v'

            elif word[i] == "w":
                # Quando for seguida de 'h'
                if tam - 1 > i and word[i + 1] == "h":
                    w = w[:j] + "u" + w[j + 2 :]
                    j -= 1
                else:
                    w = w[:j] + "u" + w[j + 1 :]

            elif word[i] == "s":
                T1 = ["n", "r", "z", "v", "g", "d", "b", "m", "l"]
                T2 = ["s", "ç"]
                T3 = ["e", "é", "ê", "i", "í", "î"]
                T4 = ["a", "á", "à", "â", "o", "ó", "ô", "u", "ú", "û"]
                # Quando estiver sempre entre vogais
                if (
                    tam - 1 > i
                    and tam - 2 >= 0
                    and word[i - 1] == "-"
                    and word[i - 2] in V + ["i", "u"]
                    and word[i + 1] in V + ["i", "u"]
                ):
                    w = w[:j] + "z" + w[j + 1 :]
                # Quando for seguido por um consoante vozeada
                elif tam - 2 > i and word[i + 1] == "-" and word[i + 2] in T1:
                    w = w[:j] + "z" + w[j + 1 :]
                # Quando for seguido de 's,ç', só ficaria uma 's'
                elif tam - 2 > i and word[i + 1] == "-" and word[i + 2] in T2:
                    w = w[:j] + "-" + "s" + w[j + 3 :]
                    j += 1
                    i += 2
                # Quando for seguido de 's' na mesma sílaba
                elif tam - 2 > i and word[i + 1] == "s":
                    w = w[: j + 1] + w[j + 2 :]
                    i += 1
                # Quando 'sc' for seguido de 'e,i,é,ê,í,î'
                elif (
                    tam - 3 > i
                    and word[i + 1] == "-"
                    and word[i + 2] == "c"
                    and word[i + 3] in T3
                ):
                    w = w[:j] + "-" + "s" + w[j + 3 :]
                    j += 1
                    i += 2
                # Quando 'sc' for seguido de 'a,á,à,â,o,ó,ô,u,ú,û'
                elif (
                    tam - 3 > i
                    and word[i + 1] == "-"
                    and word[i + 2] == "c"
                    and word[i + 3] in T4
                ):
                    w = w[: j + 1] + "-" + "k" + w[j + 3 :]
                    j += 2
                    i += 2
                # Quando for seguida de h
                elif tam - 1 > i and word[i + 1] == "h":
                    ipa = unichr(int("0283", 16))
                    w = w[:j] + ipa + w[j + 2 :]
                    i += 1
                # Fica com 's':
                #   em início de palavras ou após as consonantes r,l,p,b,n ou
                #   em final de sílaba seguido por consoante desvozeada s,t,p,k,f
                #   ou da consoante alveolar t,d,n,l ou no final das palavras

            elif word[i] == "j":
                # Para todos os casos
                ipa = unichr(int("0292", 16))
                w = w[:j] + ipa + w[j + 1 :]

            elif word[i] == "z":
                # Quando for no final das palavras
                if tam - 1 == i:
                    w = w[:j] + "s"
                # Fica com 'z':
                #   em início de palavra seguido de vogal ou
                #   quando não for final de palavra

            elif word[i] == "r":
                T1 = ["b", "d", "g", "p", "t", "c", "f", "v"]
                T2 = ["b", "d", "g", "v", "z", "j", "m", "n", "l"]
                # Ao ínicio de palavras
                if i == 0:
                    w = w[:j] + "x" + w[j + 1 :]
                # Quando for final de palavra
                elif tam - 1 == i:
                    w = w[:j] + "x"
                # Precedido por consoante s,z,n,l da sílaba anterior
                elif word[i - 1] == "-" and word[i - 2] in ["s", "n", "l"]:
                    w = w[:j] + "x" + w[j + 1 :]
                # Antes das consoantes p,t,c,q,f
                elif word[i + 1] == "-" and word[i + 2] in ["p", "t", "c", "f", "q"]:
                    w = w[:j] + "x" + w[j + 1 :]
                # Quando estiver entre vogais
                elif (
                    tam - 1 > i
                    and word[i + 1] in V + ["i", "u"]
                    and word[i - 1] == "-"
                    and word[i - 2] in V + ["i", "u"]
                ):
                    ipa = unichr(int("027E", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando acontece en encontros consoantes 'br,dr,gr,tr,cr,fr,vr'
                elif i - 1 >= 0 and word[i - 1] in T1:
                    ipa = unichr(int("027E", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando for seguido de 'r', só ficaria uma 'r'
                elif tam - 2 > i and word[i + 1] == "-" and word[i + 2] == "r":
                    w = w[:j] + "-" + "x" + w[j + 3 :]
                    j += 1
                    i += 2
                # Quando for seguida de 'r'
                elif tam - 1 > i and word[i + 1] == "r":
                    w = w[:j] + "x" + w[j + 2 :]
                    i += 1
                # Quando for final de sílaba seguido de uma consoante
                elif tam - 1 > i and word[i + 1] == "-" and word[i + 2] in T2:
                    ipa = unichr(int("0263", 16))
                    w = w[:j] + ipa + w[j + 1 :]

                # Caso contraŕio
                else:
                    ipa = unichr(int("027E", 16))
                    w = w[:j] + ipa + w[j + 1 :]

            elif word[i] == "m":
                # Quando for 'muito, muita, muitos, muitas'
                if word in ["mui-ta", "mui-tas", "mui-to", "mui-tos"]:
                    w = w[: j + 2] + "ĩ" + w[j + 3 :]
                    j += 4
                    i += 3
                # Quando for final de sílaba seguida de uma consoante, sem
                # considerar 'p' e 'b'
                elif (
                    tam - 1 > i
                    and word[i + 1] == "-"
                    and word[i + 2] in C
                    and not word[i + 2] in ["p", "b"]
                ):
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + word[j + 1 :]
                    j += 1
                # Fica com 'm':
                #   em início de palavra seguida de vogal ou
                #   se for seguida de consoante na proxima sílaba ou
                #   na sequência vogal + m + vogal (posição intervocálica)
                #   Não usar 'm,n,nh' diante de 'f,v,s,ç,z,s,ch,j,r,l,lh'

            elif word[i] == "n":
                T = ["a", "e", "i", "o", "u"]
                # A consonante nasal velar [n] ocorre apenas em posição de coda
                # medial entre uma vogal nasal 'a,e,i,o,u' e uma consoante velar
                # 'c,g'
                if (
                    tam - 1 > i
                    and word[i - 1] in T
                    and word[i + 1] == "-"
                    and word[i + 2] in ["c", "g", "r"]
                ):
                    ipa = unichr(int("0273", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando não for seguida por 'hia'
                elif (
                    tam - 2 > i and word[i + 1] == "h" and word[i + 2 : i + 5] != "i-a"
                ):
                    ipa = unichr(int("0272", 16))
                    w = w[:j] + ipa + w[j + 2 :]
                    i += 1
                # Quando não for seguida por 'hia'
                elif (
                    tam - 2 > i and word[i + 1] == "h" and word[i + 2 : i + 5] == "i-a"
                ):
                    ipa = unichr(int("0272", 16))
                    w = w[: j + 1] + w[j + 2 :]
                    i += 1
                # Fica com 'n':
                #   No início da palavra ou
                #   seguido de consoante em sílaba distinta ou
                #   em posição intervocálica ou diante de 't,d' ou
                #   quando for seguida de 'hia'
                #   Não usar 'm,n,nh' diante de 'f,v,s,ç,z,s,ch,j,r,l.lh'

            elif word[i] == "l":
                T = ["a", "e", "o", "u", "ã", "ẽ", "õ", "ũ"]
                # Quando for final da palavra
                if tam - 1 == i:
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando for final de sílaba seguido de uma consoante
                elif tam - 1 > i and word[i + 1] == "-" and word[i + 2] in C:
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando for seguido de 'h'
                elif tam - 2 > i and word[i + 1] == "h":
                    ipa = unichr(int("028E", 16))
                    w = w[:j] + ipa + w[j + 2 :]
                    i += 1
            # Fica com 'l':
            #   quando for início de sílaba e palavra ou
            #   seguido da consoante na mesma sílaba 'bl,cl,fl,gl,pl,vl' ou
            #   em posição intervocálica

            elif word[i] == "x":
                T1 = ["f", "k", "p", "q", "t", "s"]
                T2 = ["c", "f", "p", "t"]
                T3 = ["e", "é", "ê", "i", "í"]
                # Quando for no início da palavra
                if i == 0:
                    ipa = unichr(int("0283", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando ocorre após 'en' e os ditongos 'ai,ei,ou'
                elif word[i - 3 : i - 1] in ["en", "ai", "ei", "ou"]:
                    ipa = unichr(int("0283", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando a palavra tem 'f, m' + i + x
                elif (
                    tam - 3 > 1
                    and word[i - 1] == "-"
                    and word[i - 2] == "i"
                    and word[i - 3] in ["f", "m"]
                ):
                    w = w[:j] + "ks" + w[j + 1 :]
                    j += 1
                # Quando a palavra tem 'fl' + 'e, u' + x
                elif (
                    tam - 4 > 1
                    and word[i - 1] == "-"
                    and word[i - 2] in ["e", "u"]
                    and word[i - 4 : i - 2] == "fl"
                ):
                    w = w[:j] + "ks" + w[j + 1 :]
                    j += 1
                # Quando ocorre no final da palavra
                elif tam - 1 == i:
                    ipa = unichr(int("026A", 16))
                    w = w[:j] + "k" + ipa + "s"
                # Quando 'xc' for seguida por 'e,é,ê,i,í'
                elif (
                    tam - 3 > i
                    and word[i + 1] == "-"
                    and word[i + 2] == "c"
                    and word[i + 3] in T3
                ):
                    w = w[:j] + "s" + w[j + 3 :]
                    i += 2
                # Quando a palavra começa en 'f, m' + i + x
                elif (
                    i - 3 == 0
                    and word[i - 1] == "-"
                    and word[i - 2] == "i"
                    and word[i - 3] in ["f", "m"]
                ):
                    ipa = unichr(int("026A", 16))
                    w = w[:j] + "k" + ipa + "s" + w[j + 1 :]
                    j += 2
                # Quando ocorre 'e' no início da palavra + x + 'c,f,p,t'
                elif (
                    tam - 1 > i
                    and i - 1 == 0
                    and word[i - 1] == "e"
                    and word[i + 1] == "-"
                    and word[i + 2] in T2
                ):
                    w = w[:j] + "s" + w[j + 1 :]
                # Quando a palavra inicia com 'e, ê' + x + vogal + consoante
                elif (
                    tam - 3 > i
                    and i - 2 == 0
                    and word[i - 2] in ["e", "ê"]
                    and word[i + 1] in V
                    and word[i + 2] in C
                ):
                    w = w[:j] + "z" + w[j + 1 :]
                # Quando a palavra inicia com 'e, ê' + x + vogal + consoante
                elif (
                    tam - 3 > i
                    and i - 2 == 0
                    and word[i - 2] in ["e", "ê"]
                    and word[i + 1] in V
                    and word[i + 2] == "-"
                    and word[i + 3] in C
                ):
                    w = w[:j] + "z" + w[j + 1 :]
                # Quando a palavra inicia com 'ine' + x + vogal + consoante
                elif (
                    tam - 3 > i
                    and i - 5 == 0
                    and word[i - 5 : i - 1] == "i-ne"
                    and word[i + 1] in V + ["i"]
                    and word[i + 2] in C
                ):
                    w = w[:j] + "z" + w[j + 1 :]
                # Quando a palavra inicia com 'ine' + x + vogal + consoante
                elif (
                    tam - 3 > i
                    and i - 5 == 0
                    and word[i - 5 : i - 1] == "i-ne"
                    and word[i + 1] in V
                    and word[i + 2] == "-"
                    and word[i + 3] in C
                ):
                    w = w[:j] + "z" + w[j + 1 :]
                # Quando for seguida de consoante desvozeada 'f,k,p,q,t,s'
                elif tam - 1 > i and word[i + 1] == "-" and word[i + 2] in T1:
                    w = w[:j] + "s" + w[j + 1 :]
                # Quando a palavra inicia com 'e, ê' + x + consoante (exceto 'v')
                elif (
                    tam - 1 > i
                    and i - 1 == 0
                    and word[i - 1] in ["e", "ê"]
                    and word[i + 1] == "-"
                    and word[i + 2] in C
                    and word[i + 2] != "v"
                ):
                    w = w[:j] + "z" + w[j + 1 :]
                # Quando a palavra inicia com 'ine' + x + consoante (exceto 'v')
                elif (
                    tam - 1 > i
                    and i - 4 == 0
                    and word[i - 4 : i] == "i-ne"
                    and word[i + 1] == "-"
                    and word[i + 2] in C
                    and word[i + 2] != "v"
                ):
                    w = w[:j] + "z" + w[j + 1 :]
                else:
                    ipa = unichr(int("0283", 16))
                    w = w[:j] + ipa + w[j + 1 :]

            elif word[i] == "q":
                T1 = ["a", "à", "á", "â", "o", "ó"]
                T2 = ["e", "é", "ê", "i", "í"]
                # Quando 'qu' for seguido de 'e' seguido 'n'
                if (
                    len(word) - 3 > i
                    and word[i + 1] == "u"
                    and word[i + 2] in ["e", "é", "ê"]
                    and word[i + 3] == "n"
                ):
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + "k" + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando 'qu' for seguido de 'a,à,á,â,o,ó'
                elif len(word) - 2 > i and word[i + 1] == "u" and word[i + 2] in T1:
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + "k" + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando 'qu' for seguido de 'e,é,ê,i,í'
                elif len(word) - 2 > i and word[i + 1] == "u" and word[i + 2] in T2:
                    w = w[:j] + "k" + w[j + 2 :]
                    i += 1

            elif word[i] == "y":
                # Sempre vira 'i'
                w = w[:j] + "i" + w[j + 1 :]

            elif word[i] == "k":
                # Quando for a última letra da sílaba ou palavra
                if len(word) - 1 == i or word[i + 1] == "-":
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + w[j + 1 :]
                    j += 1
                # Caso contrario fica com 'k'

            # ---------------------------------------------------------------------
            # -------------------------------VOGAIS--------------------------------
            # ---------------------------------------------------------------------
            elif word[i] == "a":
                T1 = ["n", "m"]
                T2 = ["p", "t", "k", "b", "d"]
                T3 = ["f", "v", "s", "z", "j"]
                T4 = ["c", "g"]
                # -----------------------------------------------------------------
                # --------------------------VOGAIS NASAIS--------------------------
                # -----------------------------------------------------------------

                # Quando for seguido de 'm' apenas em final de palavra
                if tam - 1 > i and word[i + 1] == "m" and i + 1 == len(word) - 1:
                    # w = w[:j] + 'ãʊ̃' + w[j + 2:]
                    w = w[:j] + "ɐ͂ʊ̃" + w[j + 2 :]
                    i += 1
                    j += 3
                # Quando for seguido de 'm' apenas em final de palavra
                elif tam - 1 > i and word[i + 1] in T1:
                    # w = w[:j] + 'ã' + w[j + 2:]
                    w = w[:j] + "ɐ͂" + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for seguida de 'm,n' na proxima sílaba
                elif (
                    tam - 2 > i
                    and word[i + 1] == "-"
                    and word[i + 2] in T1
                    and self.is_tonic_syllable(ts1, ts2, i)
                ):
                    # w = w[:j] + 'ã' + w[j + 1:]
                    w = w[:j] + "ɐ͂" + w[j + 1 :]
                    j += 1
                # Quando for seguido de 'm' e seguido de 'p,b' na segunte sílaba
                elif (
                    tam - 3 > i
                    and word[i + 1] == "m"
                    and word[i + 2] == "-"
                    and word[i + 3] in ["p", "b"]
                ):
                    ipa = unichr(int("0250", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                    i += 1
                    j += 1
                # Quando for final de sílaba tônica seguida por outra sílaba
                # iniciada por 'm, n'
                elif (
                    tam - 2 > i
                    and word[i + 1] == "-"
                    and word[i + 2] in T1
                    and self.is_tonic_syllable(ts1, ts2, i)
                ):
                    w = w[:j] + "ɐ͂" + w[j + 1 :]
                    j += 1

                # -----------------------------------------------------------------
                # --------------------------DITONGOS ORAIS-------------------------
                # -----------------------------------------------------------------
                # Quando for seguido de 'o'
                elif tam - 1 > i and word[i + 1] == "o":
                    ipa = unichr(int("028A", 16))
                    w = w[: j + 1] + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for seguido de 'i'
                elif tam - 1 > i and word[i + 1] == "i":
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + w[j + 2 :]
                    i += 1
                    j += 1

                # Quando for seguida de 'í' fica igual

                # Quando for seguido de 'u'
                elif tam - 1 > i and word[i + 1] == "u":
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + "a" + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for seguido 'l' seguido de consoante na sílaba seguinte
                elif (
                    tam - 3 > i
                    and word[i + 1] == "l"
                    and word[i + 2] == "-"
                    and word[i + 3] in C
                ):
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + "a" + ipa + w[j + 2 :]
                    i += 1
                    j += 1

                # Quando for seguido de 'lh' fica igual

                # Quando for seguido de 'ú' fica igual (olhar as regras da 'ú')

                # -----------------------------------------------------------------
                # -----------------------------------------------------------------
                # Quando for 'aa'
                elif tam - 1 > i and word[i + 1] == "-" and word[i + 2] == "a":
                    w = w[: j + 1] + w[j + 3 :]
                    i += 2
                # Quando for no final da sílaba tônica seguida por outra sílaba
                # iniciada por 'm, n'
                elif (
                    len(word) - 1 > i
                    and i == ts2 - 1
                    and word[i + 1] == "-"
                    and word[i + 2] in ["m", "n"]
                ):
                    ipa = unichr(int("0250", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Caso contrario fica com 'a'

            elif word[i] == "â":
                T1 = ["n", "m"]
                T2 = ["p", "t", "k", "b", "d"]
                T3 = ["f", "v", "s", "z", "j"]
                T4 = ["c", "g"]
                # -----------------------------------------------------------------
                # --------------------------VOGAIS NASAIS--------------------------
                # -----------------------------------------------------------------
                # Quando for seguido de 'n' apenas em final de palavra
                if tam - 1 > i and word[i + 1] in T1:
                    w = w[:j] + "ɐ͂" + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for final de sílaba tônica seguida por outra sílaba
                # iniciada por 'm, n'
                elif (
                    tam - 2 > i
                    and word[i + 1] == "-"
                    and word[i + 2] in T1
                    and self.is_tonic_syllable(ts1, ts2, i)
                ):
                    w = w[:j] + "ɐ͂" + w[j + 1 :]
                    j += 1
                # Quanfo for seguido de 'm,n' diante consoante oclusiva 'p,t,b,d'
                elif tam - 1 > i and word[i + 1] in T1 and word[i - 1] in T2:
                    w = w[:j] + "ɐ͂" + w[j + 1 :]
                    i += 1
                    j += 2
                # Quanfo for seguido de 'm,n' diante consoante oclusiva 'f,v,s,z,j'
                elif tam - 1 > i and word[i + 1] in T1 and word[i - 1] in T3:
                    w = w[:j] + "ɐ͂" + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for começo de sílaba seguido de 'm,n'
                elif (
                    tam - 1 > i and (i == 0 or word[i - 1] == "-") and word[i + 1] in T1
                ):
                    w = w[:j] + "ɐ͂" + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando estiver em sílaba tônica
                elif self.is_tonic_syllable(ts1, ts2, i):
                    w = w[:j] + "ɐ͂" + w[j + 1 :]
                    j += 1

                # Caso contrario fica com 'a'

            elif word[i] == "à":
                w = w[:j] + "a" + w[j + 1 :]

            elif word[i] == "á":
                w = w[:j] + "a" + w[j + 1 :]

            elif word[i] == "e":
                T = ["e-la", "e-las", "es-ta", "es-tas"]
                T1 = ["n", "m"]
                T2 = ["t", "k", "d"]
                T3 = ["c", "g", "r"]
                T4 = ["f", "v", "s", "z", "j"]
                # No inicio da palavra
                if tam - 1 > i and i == 0 and word[i + 1] in ["s", "z"]:
                    w = "i" + w[j + 1 :]
                # Quando é posição inicial da palavra seguida de 'xa'
                elif (
                    tam - 3 > i
                    and i == 0
                    and word[i + 1] == "-"
                    and word[i + 2 : i + 4] == "xa"
                ):
                    w = "i" + w[j + 1 :]
                # Quando fo
                elif (
                    tam - 3 > i
                    and i == 0
                    and word[i + 1] == "x"
                    and word[i + 2] == "-"
                    and word[i + 3] in ["p", "t"]
                ):
                    w = "i" + w[j + 1 :]

                # -----------------------------------------------------------------
                # --------------------------VOGAIS NASAIS--------------------------
                # -----------------------------------------------------------------
                # Quando for seguido de 'm,n' diante consoante oclusiva 't,k,d'
                if (
                    tam - 3 > i
                    and word[i + 1] in T1
                    and word[i + 2] == "-"
                    and word[i + 3] in T2
                ):
                    w = w[:j] + "ẽɪ̃" + w[j + 2 :]
                    i += 1
                    j += 3
                # Quando for seguido de 'm,n' na mesma sílaba
                elif tam - 1 > i and word[i + 1] in T1:
                    w = w[:j] + "ẽɪ̃" + w[j + 2 :]
                    i += 1
                    j += 3
                # Quando for seguida de 'm,n' na proxima sílaba
                elif (
                    tam - 2 > i
                    and word[i + 1] == "-"
                    and word[i + 2] in T1
                    and self.is_tonic_syllable(ts1, ts2, i)
                ):
                    w = w[:j] + "ẽ" + w[j + 1 :]
                    j += 1

                # -----------------------------------------------------------------
                # --------------------------DITONGOS ORAIS-------------------------
                # -----------------------------------------------------------------
                # Quando for seguido de 'a' na sílaba seguinte
                elif tam - 2 > i and word[i + 1] == "-" and word[i + 2] == "a":
                    ipa = unichr(int("026A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                    i += 2
                    j += 2
                # Quando for seguido de 'i'
                elif tam - 1 > i and word[i + 1] == "i":
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for seguido de 'o' no final da palavra
                elif tam - 3 == i and word[i + 1] == "-" and word[i + 2] == "o":
                    ipa = unichr(int("026A", 16)) + unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 3 :]
                    i += 2
                    j += 2
                # Quando for seguido de 'u'
                elif tam - 1 > i and word[i + 1] == "u":
                    ipa = unichr(int("028A", 16))
                    w = w[: j + 1] + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for vogal tônica seguido de "l" em final de silaba
                # (palavras oxítonas)
                elif (
                    tam - 1 > i
                    and self.is_tonic_syllable(ts1, ts2, i)
                    and word[i + 1] == "l"
                    and len(word) - 2 == i
                ):
                    ipa = unichr(int("025B", 16)) + unichr(int("028A", 16))
                    w = w[:j] + ipa
                    i += 1
                    j += 1
                # Quando for seguida de 'í' na seguinte sílaba, fica igual (olhar
                # as regras da 'í')

                # Quando for seguida de 'ú' na seguinte sílaba, fica igual (olhar
                # as regras da 'ú')

                # -----------------------------------------------------------------
                # -----------------------------------------------------------------
                # Quando for tônica e for seguida por 'l' na mesma sílaba
                elif (
                    tam - 1 > i
                    and self.is_tonic_syllable(ts1, ts2, i)
                    and word[i + 1] == "l"
                ):
                    ipa = unichr(int("025B", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando for pronome feminino e vogal tônica
                elif word in T and self.is_tonic_syllable(ts1, ts2, i):
                    ipa = unichr(int("025B", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando for vogal tônica e a seguinte silaba for 'la, lo', excepto
                # nas palavras 'pelo, pela'
                elif (
                    tam - 3 > i
                    and self.is_tonic_syllable(ts1, ts2, i)
                    and word[i + 1] == "-"
                    and word[i + 2 : i + 4] in ["la", "lo"]
                    and not word in ["pe-lo", "pe-la"]
                ):
                    ipa = unichr(int("025B", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando for final da palavra
                elif tam - 1 == i:
                    ipa = unichr(int("026A", 16))
                    w = w[:j] + ipa
                # Quando for final de palavra seguido de 's'
                elif tam - 2 == i and word[i + 1] == "s":
                    ipa = unichr(int("026A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando está em posição inicial da palavra e ocorro diante das
                # fricativas 's,z'
                elif tam - 1 > i and i == 0 and word[i + 1] in ["s", "z"]:
                    ipa = unichr(int("026A", 16))
                    w = w[:j] + ipa + w[j + 1 :]

                # Caso contrario fica com 'e'

            elif word[i] == "é":
                T1 = ["n", "m"]
                T2 = ["p", "t", "k", "b", "d"]
                # -----------------------------------------------------------------
                # --------------------------VOGAIS NASAIS--------------------------
                # -----------------------------------------------------------------
                # Quanfo for seguido de 'm,n' diante consoante oclusiva 'p,t,k,b,d'
                if (
                    tam - 3 > i
                    and word[i + 1] in T1
                    and word[i + 2] == "-"
                    and word[i + 3] in T2
                ):
                    w = w[:j] + "ẽɪ̃" + w[j + 2 :]
                    i += 1
                    j += 2
                # Quando ocorre antes de 'm, n'
                elif tam - 1 > i and word[i + 1] in T1:
                    w = w[:j] + "ẽɪ̃" + w[j + 2 :]
                    i += 1
                    j += 2

                # -----------------------------------------------------------------
                # --------------------------DITONGOS ORAIS-------------------------
                # -----------------------------------------------------------------
                # Quando for seguido de 'i'
                elif tam - 1 > i and word[i + 1] == "i":
                    ipa = unichr(int("025B", 16)) + unichr(int("026A", 16))
                    w = w[:j] + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for seguido de 'o'
                elif tam - 1 > i and word[i + 1] == "o":
                    ipa = unichr(int("025B", 16)) + unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for seguido de 'u'
                elif tam - 1 > i and word[i + 1] == "u":
                    ipa = unichr(int("025B", 16)) + unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 2 :]
                    i += 1
                    j += 1

                # -----------------------------------------------------------------
                # -----------------------------------------------------------------
                # Caso contrário
                else:
                    ipa = unichr(int("025B", 16))
                    w = w[:j] + ipa + w[j + 1 :]

            elif word[i] == "ê":
                T1 = ["n", "m"]
                T2 = ["p", "t", "k", "b", "d"]
                T3 = ["c", "g", "r"]
                # -----------------------------------------------------------------
                # --------------------------VOGAIS NASAIS--------------------------
                # -----------------------------------------------------------------
                # Quanfo for seguido de 'm,n' diante consoante oclusiva 'p,t,k,b,d'
                if (
                    tam - 3 > i
                    and word[i + 1] in T1
                    and word[i + 2] == "-"
                    and word[i + 3] in T2
                ):
                    w = w[:j] + "ẽɪ̃" + w[j + 2 :]
                    i += 1
                    j += 2
                # Quando for seguido de 'm,n' na mesma sílaba
                elif tam - 1 > i and word[i + 1] in T1:
                    w = w[:j] + "ẽɪ̃" + w[j + 2 :]
                    i += 1
                    j += 3
                # Quanfo for seguido de 'm,n' diante consoante velar 'c,g,r'
                elif (
                    tam - 3 > i
                    and word[i + 1] in T1
                    and word[i + 2] == "-"
                    and word[i + 3] in T3
                ):
                    ipa = unichr(int("014B", 16))
                    w = w[:j] + "e" + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for seguido de 'm, n' na seguinte sílaba
                elif tam - 2 > i and word[i + 1] == "-" and word[i + 2] in T1:
                    w = w[:j] + "ẽ" + w[j + 1 :]
                    j += 1
                # -----------------------------------------------------------------
                # -----------------------------------------------------------------
                # Caso contrário
                else:
                    w = w[:j] + "e" + w[j + 1 :]

            elif word[i] == "i":
                T1 = ["n", "m"]
                T2 = ["c", "g", "r"]
                # -----------------------------------------------------------------
                # --------------------------VOGAIS NASAIS--------------------------
                # -----------------------------------------------------------------
                # Quando for seguido de 'm,n' na mesma sílaba
                if tam - 1 > i and word[i + 1] in T1:
                    w = w[:j] + "ĩ" + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for seguida de 'm,n' na proxima sílaba
                elif (
                    tam - 2 > i
                    and word[i + 1] == "-"
                    and word[i + 2] in T1
                    and self.is_tonic_syllable(ts1, ts2, i)
                ):
                    w = w[:j] + "ĩ" + w[j + 1 :]
                    j += 1

                # -----------------------------------------------------------------
                # --------------------------DITONGOS ORAIS-------------------------
                # -----------------------------------------------------------------
                # Quando for seguido de 'e' no final da palavra
                elif tam - 3 == i and word[i + 1] == "-" and word[i + 2] == "e":
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + w[j + 3 :]
                    i += 2
                    j += 2
                # Quando for seguido de 'u' no final da palavra
                elif tam - 2 == i and word[i + 1] == "u":
                    ipa = unichr(int("028A", 16))
                    w = w[: j + 1] + ipa + w[j + 3 :]
                    i += 2
                    j += 2
                # Quando for precedido de 'a, e, o' e seguido de 'o'
                elif (
                    tam - 3 == i
                    and word[i - 1] == "-"
                    and word[i - 2] in ["e", "o"]
                    and word[i + 1] == "-"
                    and word[i + 2] == "o"
                ):
                    ipa = unichr(int("026A", 16)) + "-" + unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 3 :]
                    i += 2
                    j += 2
                # Quando for precedido de 'a, e, o' e seguido de 'o'
                elif (
                    tam - 2 > i
                    and word[i - 1] == "-"
                    and word[i - 2] in ["a", "e"]
                    and word[i + 1] == "-"
                    and word[i + 2] == "o"
                ):
                    ipa = unichr(int("026A", 16)) + "-" + "u"
                    w = w[:j] + ipa + w[j + 3 :]
                    i += 2
                    j += 2
                # Quando for seguido de 'o' no final
                elif tam - 3 == i and word[i + 1] == "-" and word[i + 2] == "o":
                    ipa = "i" + "-" + unichr(int("028A", 16))
                    w = w[:j] + ipa
                    i += 2
                    j += 2
                # Quando for precedido  de 'c, s' seguido de 'on' no final
                elif (
                    tam - 4 > i
                    and word[i - 1] in ["c", "s"]
                    and word[i + 1] == "-"
                    and word[i + 2] == "o"
                    and word[i + 3] == "-"
                    and word[i + 4] == "n"
                ):
                    ipa = unichr(int("026A", 16)) + "-" + "o"
                    w = w[:j] + ipa + w[j + 3 :]
                    i += 2
                    j += 2
                # Quando for seguido de 'u' na seguinte sílaba
                elif tam - 1 > i and word[i + 1] == "-" and word[i + 2] == "u":
                    ipa = unichr(int("028A", 16))
                    w = w[: j + 2] + ipa + w[j + 3 :]
                    i += 2
                    j += 2
                # Quando for seguido de 'l'
                elif tam - 1 > i and word[i + 1] == "l":
                    ipa = unichr(int("028A", 16))
                    w = w[: j + 1] + ipa + w[j + 2 :]
                    i += 1
                    j += 1

                # -----------------------------------------------------------------
                # -----------------------------------------------------------------
                # Quando for final de palavra e for atono
                elif tam - 1 == i and not self.is_tonic_syllable(ts1, ts2, i):
                    ipa = unichr(int("026A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Caso contrario fica com 'i'

            elif word[i] == "í":
                T1 = ["n", "m"]
                T2 = ["c", "g", "r"]
                # -----------------------------------------------------------------
                # --------------------------VOGAIS NASAIS--------------------------
                # -----------------------------------------------------------------
                # Quando for seguido de 'm,n' na mesma sílaba
                if tam - 1 > i and word[i + 1] in T1:
                    w = w[:j] + "ĩ" + w[j + 2 :]
                    i += 1
                    j += 1
                # Quanfo for seguido de 'm,n' diante consoante velar 'c,g,r'
                elif (
                    tam - 3 > i
                    and word[i + 1] in T1
                    and word[i + 2] == "-"
                    and word[i + 3] in T2
                ):
                    ipa = unichr(int("014B", 16))
                    w = w[:j] + "i" + ipa + w[j + 2 :]
                    i += 1
                    j += 1

                # -----------------------------------------------------------------
                # -----------------------------------------------------------------
                # Caso contrário
                else:
                    w = w[:j] + "i" + w[j + 1 :]

            elif word[i] == "o":
                T1 = ["n", "m"]
                T2 = ["c", "g", "r"]
                # -----------------------------------------------------------------
                # --------------------------VOGAIS NASAIS--------------------------
                # -----------------------------------------------------------------
                # Quando for seguido de 'm,n'
                if tam - 1 > i and word[i + 1] in T1:
                    # w = w[:j] + 'õʊ͂' + w[j + 2:]
                    w = w[:j] + "õʊ̃" + w[j + 2 :]
                    i += 1
                    j += 3
                # Quando for seguida de 'm,n' na proxima sílaba
                elif (
                    tam - 2 > i
                    and word[i + 1] == "-"
                    and word[i + 2] in T1
                    and self.is_tonic_syllable(ts1, ts2, i)
                ):
                    w = w[:j] + "õ" + w[j + 1 :]
                    j += 1
                # Quando for seguido de 'o'
                elif tam - 1 > i and (
                    word[i + 1] == "o" or word[i + 1 : i + 3] == "-o"
                ):
                    w = w[:j] + w[j + 2 :]
                    i += 1
                    j -= 1
                # Quando é posição inicial da palavra seguida de 'ra'
                elif tam - 3 > i and word[i + 1] == "-" and word[i + 2 : i + 4] == "ra":
                    ipa = unichr(int("0254", 16))
                    w = w[:j] + ipa + w[j + 1 :]

                # -----------------------------------------------------------------
                # --------------------------DITONGOS ORAIS-------------------------
                # -----------------------------------------------------------------
                # Quando for vogal tônica seguido de "l" em final de silaba
                # (palavras oxítonas)
                elif (
                    tam - 2 == i
                    and self.is_tonic_syllable(ts1, ts2, i)
                    and word[i + 1] == "l"
                ):
                    ipa = unichr(int("0254", 16)) + unichr(int("028A", 16))
                    w = w[:j] + ipa
                    i += 1
                    j += 1
                # Quando for seguido de 'i'
                elif tam - 1 > i and word[i + 1] == "i":
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for seguido de 'e'
                elif tam - 1 > i and word[i + 1] == "e":
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for seguido de 'a'
                elif tam - 1 > i and word[i + 1] == "a":
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                    i += 1
                    j += 1
                # Quando for seguido de 'a' na seguinte sílaba
                elif tam - 2 > i and word[i + 1] == "-" and word[i + 2] == "a":
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                    i += 2
                    j += 2
                # Quando for seguido de 'ou' na ultima sílaba
                elif (
                    tam - 4 == i
                    and word[i + 1] == "-"
                    and word[i + 2] == "o"
                    and word[i + 3] == "u"
                ):
                    ipa = unichr(int("028A", 16))
                    w = w[: j + 3] + ipa
                    i += 3
                    j += 3
                # Quando for seguido de 'o' na seguinte sílaba
                elif tam - 2 > i and word[i + 1] == "-" and word[i + 2] == "o":
                    w = w[: j + 1] + w[j + 3 :]
                    i += 3
                    j += 1
                # Quando for seguido de 'ó' na seguinte sílaba
                elif tam - 2 > i and word[i + 1] == "-" and word[i + 2] == "ó":
                    ipa = unichr(int("0254", 16))
                    w = w[:j] + ipa + w[j + 3 :]
                    i += 3
                    j += 1
                # Quando for seguido de 'u'
                elif tam - 1 > i and word[i + 1] == "u":
                    ipa = unichr(int("028A", 16))
                    w = w[: j + 1] + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for seguido de 'ú' na seguinte sílaba
                elif tam - 2 > i and word[i + 1] == "-" and word[i + 2] == "ú":
                    w = w[: j + 2] + "u" + w[j + 3 :]
                    i += 2
                    j += 2
                # Quando for seguida de 'sos' na sílaba final
                elif (
                    tam - 5 == i and word[i + 1] == "-" and word[i + 2 : i + 5] == "sos"
                ):
                    ipa = unichr(int("0254", 16)) + "-z" + unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 4 :]
                    i += 4
                    j += 4
                # Quando for seguido de s no final
                elif tam - 1 > i and tam - 2 == i and word[i + 1] == "s":
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                    i += 2
                    j += 2

                # -----------------------------------------------------------------
                # -----------------------------------------------------------------
                # Quando for seguido da silaba 'sa' em final de palavra
                elif (
                    tam - 4 == i and word[i + 1] == "-" and word[i + 2 : i + 4] == "sa"
                ):
                    ipa = unichr(int("0254", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando for seguido por 'z' em final de palavra
                elif tam - 2 == i and word[i + 1] == "z" and word != "ar-roz":
                    ipa = unichr(int("0254", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando for vogal atona em final da palavra
                elif tam - 1 == i and not self.is_tonic_syllable(ts1, ts2, i):
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Caso contrario fica com 'o'

            elif word[i] == "ó":
                # Quando for seguido de 'i'
                if tam - 1 > i and word[i + 1] == "i":
                    ipa = unichr(int("0254", 16)) + unichr(int("026A", 16))
                    w = w[:j] + ipa + w[j + 2 :]
                    i += 2
                    j += 2
                # Caso contrário
                else:
                    ipa = unichr(int("0254", 16))
                    w = w[:j] + ipa + w[j + 1 :]

            elif word[i] == "ô":
                T1 = ["n", "m"]
                T2 = ["c", "g", "r"]
                # -----------------------------------------------------------------
                # --------------------------VOGAIS NASAIS--------------------------
                # -----------------------------------------------------------------
                # Quando for seguida de 'm,n' na proxima sílaba
                if (
                    tam - 2 > i
                    and word[i + 1] == "-"
                    and word[i + 2] in T1
                    and self.is_tonic_syllable(ts1, ts2, i)
                ):
                    w = w[:j] + "õ" + w[j + 1 :]
                    j += 1
                # Quanfo for seguido de 'm,n' diante consoante velar 'c,g,r'
                elif (
                    tam - 3 > i
                    and word[i + 1] in T1
                    and word[i + 2] == "-"
                    and word[i + 3] in T2
                ):
                    ipa = unichr(int("014B", 16))
                    w = w[:j] + "o" + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quanfo for seguido de 'm,n'
                elif tam - 1 > i and word[i + 1] in T1:
                    w = w[:j] + "õʊ͂" + w[j + 2 :]
                    i += 1
                    j += 2

                # -----------------------------------------------------------------
                # -----------------------------------------------------------------
                # Quando for seguido de 'o'
                elif tam - 1 > i and word[i + 1] == "o":
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + "o" + ipa + w[j + 2 :]
                    i += 2
                    j += 2
                # Caso contrário
                else:
                    w = w[:j] + "o" + w[j + 1 :]

            elif word[i] == "u":
                T = ["c", "g", "q"]
                T1 = ["n", "m"]
                T2 = ["c", "g", "r"]
                # -----------------------------------------------------------------
                # --------------------------VOGAIS NASAIS--------------------------
                # -----------------------------------------------------------------
                # Quanfo for seguido de 'm,n'
                if tam - 1 > i and word[i + 1] in T1:
                    # w = w[:j] + 'ũʊ͂' + w[j + 2:]
                    w = w[:j] + "ũ" + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for seguida de 'm,n' na proxima sílaba
                elif (
                    tam - 2 > i
                    and word[i + 1] == "-"
                    and word[i + 2] in T1
                    and self.is_tonic_syllable(ts1, ts2, i)
                ):
                    w = w[:j] + "ũ" + w[j + 1 :]
                    j += 1

                # -----------------------------------------------------------------
                # --------------------------DITONGOS ORAIS-------------------------
                # -----------------------------------------------------------------
                # Quando for seguido de 'a' e após as consoantes oclusivas 'c,g,q'
                elif tam - 1 > i and word[i + 1] == "a" and word[i - 1] in T:
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                    i += 1
                    j += 1
                # Quando for seguido de 'a' e não suceder as consoantes 'c,g,q'
                elif tam - 1 > i and word[i + 1] == "a" and not word[i - 1] in T:
                    w = w[: j + 1] + w[j + 1 :]
                    i += 1
                    j += 1
                # Quando for seguido de 'e' e após as consoantes oclusivas 'c,g,q'
                elif tam - 1 > i and word[i + 1] == "e" and word[i - 1] in T:
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                    i += 1
                    j += 1
                # Quando for seguido de 'e' e não suceder as consoantes 'c,g,q'
                elif tam - 1 > i and word[i + 1] == "e" and not word[i - 1] in T:
                    w = w[: j + 1] + w[j + 1 :]
                    i += 1
                    j += 1
                # Apenas na palavra 'muito'
                elif word == "mui-to":
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for seguido de 'i' em final de sílaba
                elif tam - 2 > i and word[i + 1] == "i" and word[i + 2] == "-":
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for seguido de 'i' no final da palavra
                elif tam - 2 == i and word[i + 1] == "i":
                    ipa = unichr(int("026A", 16))
                    w = w[: j + 1] + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for seguido de 'o' e se suceder 'q'
                elif tam - 1 > i and word[i - 1] == "q" and word[i + 1] == "o":
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                    i += 1
                    j += 1
                # Quando for seguido de 'l' em final de sílaba
                elif tam - 2 > i and word[i + 1] == "l" and word[i + 2] == "-":
                    ipa = unichr(int("028A", 16))
                    w = w[: j + 1] + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for seguido de 'l' no da palavra
                elif tam - 2 == i and word[i + 1] == "l":
                    ipa = unichr(int("028A", 16))
                    w = w[: j + 1] + ipa + w[j + 2 :]
                    i += 1
                    j += 1
                # Quando for seguido de s no final
                elif (
                    tam - 1 > i
                    and tam - 2 == i
                    and word[i + 1] == "s"
                    and not self.is_tonic_syllable(ts1, ts2, i)
                ):
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                    i += 2
                    j += 2
                # -----------------------------------------------------------------
                # -----------------------------------------------------------------
                # Quando for silaba átona no final da palavra
                elif self.is_last_syllable(i) and not self.is_tonic_syllable(
                    ts1, ts2, i
                ):
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Na sequência 'k, g' + 'u' + vogal ou se for ditongo
                elif tam - 1 > i and word[i - 1] in ["k", "g"] and word[i + 1] in V:
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Quando for vogal + 'u' + vogal
                elif (
                    tam - 1 > i
                    and word[i - 1] in V
                    and word[i + 1] == "-"
                    and word[i + 2] in V
                ):
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                elif (
                    tam - 1 > i
                    and word[i - 1] == "-"
                    and word[i - 2] in V
                    and word[i + 1] == "-"
                    and word[i + 2] in V
                ):
                    ipa = unichr(int("028A", 16))
                    w = w[:j] + ipa + w[j + 1 :]
                # Caso contrario fica com 'u'

            elif word[i] == "ú":
                T1 = ["n", "m"]
                T2 = ["c", "g", "r"]
                # -----------------------------------------------------------------
                # --------------------------VOGAIS NASAIS--------------------------
                # -----------------------------------------------------------------
                # Quanfo for seguido de 'm,n' diante consoante velar 'c,g,r'
                if (
                    tam - 3 > i
                    and word[i + 1] in T1
                    and word[i + 2] == "-"
                    and word[i + 3] in T2
                ):
                    w = w[:j] + "ũ" + w[j + 2 :]
                    i += 1
                    j += 1
                # Quanfo for seguido de 'm,n'
                elif tam - 1 > i and word[i + 1] in T1:
                    w = w[:j] + "ũʊ͂" + w[j + 2 :]
                    i += 1
                    j += 2

                # -----------------------------------------------------------------
                # -----------------------------------------------------------------
                # Caso contrário
                else:
                    w = w[:j] + "u" + w[j + 1 :]

            elif word[i] == "ã":
                # -----------------------------------------------------------------
                # -------------------------DITONGOS NASAIS-------------------------
                # -----------------------------------------------------------------
                # Quando for seguida de 'e'
                if tam - 1 > i and word[i + 1] == "e":
                    # w = w[:j] + 'ãĩ' + w[j + 2:]
                    w = w[:j] + "ɐ͂ɪ̃" + w[j + 2 :]
                    i += 1
                    j += 3
                # Quando for seguida de 'o'
                elif tam - 1 > i and word[i + 1] == "o":
                    # w = w[:j] + 'ãʊ̃' + w[j + 2:]
                    w = w[:j] + "ɐ͂ʊ̃" + w[j + 2 :]
                    i += 1
                    j += 3

                # -----------------------------------------------------------------
                # ---------------------------VOGAIS NASAIS-------------------------
                # -----------------------------------------------------------------
                # Quando for em final da palavra
                elif tam - 1 == i:
                    w = w[:j] + "ɐ͂"

                else:
                    w = w[:j] + "ɐ͂" + w[j + 1 :]
                    j += 1

            elif word[i] == "õ":
                # -----------------------------------------------------------------
                # -------------------------DITONGOS NASAIS-------------------------
                # -----------------------------------------------------------------
                # Quando for seguida de 'e'
                if tam - 1 > i and word[i + 1] == "e":
                    # w = w[:j] + 'õĩ' + w[j + 2:]
                    w = w[:j] + "õɪ̃" + w[j + 2 :]
                    i += 2
                    j += 2

                # -----------------------------------------------------------------
                # -----------------------------------------------------------------

            i += 1
            j += 1

        # Get stress phonetic syllable boundaries
        a, b = self.stress.get_stress_phonetic_syllable(self.syllables, w)

        return (w[:a] + "ˈ" + w[a:]).replace("-", ".")

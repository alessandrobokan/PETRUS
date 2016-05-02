#!/usr/bin/env python
#-*- encoding:utf-8 -*-

# tonic.py - Determine the tonic vowel position in a word using the algorithm
# described in chapter 3 of Silva [2011].
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

import re


class StressDetector(object):
    """
    This class implements the tonic/stress detection presented in
    the third chapter of the PhD thesis:

        Silva, D.C. (2011) Algoritmos de Processamento da Linguagem e Síntese
        de Voz com Emoções Aplicados a um Conversor Text-Fala Baseado
        em HMM. PhD dissertation, COPPE, UFRJ.

    """
    def __init__(self, word):
        try:
            self.word = word.decode('utf-8').lower()
        except (UnicodeDecodeError, UnicodeEncodeError):
            self.word = word.lower()

    def get_stress_vowel(self):
        """
        Identify the tonic vowel in a word.

        Args:
            word: Input word, e.g. "chocolate"

        Returns: The position of the tonic vowel in the word, e.g. 6 -> 'o'

        """
        # Rule 1:
        # If the vowel has an accent then it is a tonic vowel
        match = re.search('á|é|í|ó|ú|â|ê|ô|à|ã|õ', self.word, re.UNICODE)
        if match: return match.start()

        # TODO Word with len(word) > 2

        # Rule 2: if ^(0) = {r,l,z,x,n} then T = 1
        if re.search('[rlzxn]$', self.word, re.UNICODE):
            return len(self.word) - 2

        # Rule 3:
        # if ^(0) = {m} & ^(1) = {i,o,u} then T = 1
        if re.search('[iou]m$', self.word, re.UNICODE):
            return len(self.word) - 2

        # Rule 4:
        # if ^(0) = {s} & ^(1) = {n} & ^(2) = {i,o,u} then T = 1
        if re.search('[iou]ns$', self.word, re.UNICODE):
            return len(self.word) - 3

        # Rule 5:
        # if ^(0) = {i} & ^(1) = {u,ü} & ^(2) = {q,g} then T = 0
        if re.search('[qg][uü]i$', self.word, re.UNICODE):
            return len(self.word) - 1

        # Rule 6:
        # if ^(0) = {s} & ^(1) = {i} & ^(2) = {u,ü} & ^(3) = {q,g} then T = 1
        if re.search('[qg][uü]is$', self.word, re.UNICODE):
            return len(self.word) - 2

        # Rule 7:
        # if ^(0) = {i,u} & ^(1) = {a,e,i,o,u} then T = 1
        if re.search('[aeiou][iu]$', self.word, re.UNICODE):
            return len(self.word) - 2
        # if ^(0) = {i,u} & ^(1) != {a,e,i,o,u} then T = 0
        if re.search('[^aeiou][iu]$', self.word, re.UNICODE):
            return len(self.word) - 1

        # Rule 8:
        # if ^(0) = {s} & ^(1) = {i,u} & ^(2) = {a,e,i,o,u} then T = 2
        if re.search('[aeiou][iu]s$', self.word, re.UNICODE):
            return len(self.word) - 3

        # Rule 9:
        # if ^(0) = {s} & ^(1) = {i,u} & ^(2) != {a,e,i,o,u} then T = 2
        if re.search('[^aeiou][iu]s$', self.word, re.UNICODE):
            return len(self.word) - 2

        # Rule 10:
        # if ^(0) = {e} & ^(1) = {u} & ^(2) = {q} & ^(3) = {r} & ^(4) = {o} &
        # ^(4) = {p} then T = 0
        if self.word == "porque":
            return len(self.word) - 1

        # Rule 11
        # if ^(0) = {e} & ^(1) = {u} & ^(2) = {qg} & ^(3) = {a,e,i,o,u} then T = 3
        if re.search('[aeiou][qg]ue$', self.word, re.UNICODE):
            return len(self.word) - 4
        # if ^(0) = {e} & ^(1) = {u} & ^(2) = {qg} & ^(3) != {a,e,i,o,u} then T = 4
        if re.search('[^aeiou][qg]ue$', self.word, re.UNICODE):
            return len(self.word) - 5

        # Rule 12
        # if ^(0)={e} & ^(1)={e} & ^(2)={u} & ^(3)={qg} & ^(4)={aeiou} then T = 4
        if re.search('[aeiou][qg]ues$', self.word, re.UNICODE):
            return len(self.word) - 5
        # if ^(0)={e} & ^(1)={e} & ^(2)={u} & ^(3)={qg} & ^(4)!={aeiou} then T = 5
        if re.search('[^aeiou][qg]ues$', self.word, re.UNICODE):
            return len(self.word) - 6

        # Rule 13:
        # if ^(0) = {a,e,i,o,u} & ^(2) = {i,u} & ^(3) = {a,e,i,o,u} then T = 2
        if re.search('[aeiou][iu][aeiou]$', self.word, re.UNICODE):
            return len(self.word) - 3

        # Rule 14:
        # if ^(0) & ^(3) = {a,e,i,o,u} & ^(2) = {i,u} & ^(1) != {a,e,i,o,u} &
        # ^(4) != {q,g} then T = 3
        if re.search('[^qg][aeiou][iu][^aeiou][aeiou]$', self.word, re.UNICODE):
            return len(self.word) - 4

        # Rule 15:
        # if ^(0) = {s} & ^(1) & ^(4) = {a,e,i,o,u} & ^(3) = {i,u} &
        # ^(2) != {a,e,i,o,u} & ^(5) != {q,g} then T = 4
        if re.search('[^qg][aeiou][iu][^aeiou][aeiou]s$', self.word, re.UNICODE):
            return len(self.word) - 5

        # Rule 16:
        # if ^(0) = {a,e,o} & ^(1) = cons & ^(2) = {n} & ^(3) = {i,u} &
        # ^(4) = {a,e,i,o,u} then T = 3
        consts = 'bdfghjklmnñpqrstvxyz'
        if re.search('[aeiou][iu]n[' + consts + '][aeo]$', self.word, re.UNICODE):
            return len(self.word) - 4

        # Rule 17:
        matches = [m.start() for m in re.finditer('a|e|i|o|u', self.word, re.UNICODE)]
        if len(matches) >= 2:
            k = matches[-2]
            v = ['a', 'e', 'i', 'o', 'u']
            if self.word[k] in ['i', 'u'] and self.word[k - 1] in v and not self.word[k + 1] in v:
                if k - 2 < 0:
                    return 0
                if not self.word[k - 2] in ['q', 'g']:
                    return k - 1

        # Rule 18:
        # if ^(0) = {m} & ^(1) = {e} & ^(2) = {u} & ^(3) = {q} then T = 1
        if self.word == "quem":
            return len(self.word) - 2

        # Rule 19:
        # Penultimate vowel of the word
        matches = [m.start() for m in re.finditer('a|e|i|o|u', self.word, re.UNICODE)]
        if len(matches) >= 2:
            return matches[-2]

        return -1

    def get_stress_vowel_with_hyphen(self, syllables):
        """
        Identify the tonic vowel in a word separate by syllables.

        Args:
            word: Syllables, e.g. "cho-co-la-te"

        Returns: Position of the tonic vowel in syllables, e.g. 8 -> 'o'

        """
        a, b, stress = 0, 0, self.get_stress_vowel()
        while a < len(syllables):
            if syllables[a] != self.word[b]:
                a += 1
            if stress == b:
                return a
            a, b = a + 1, b + 1

        return -1

    def get_stress_syllable(self, syllables):
        """
        Returns the stress syllable positions.

        Args:
            syllables: Word syllables, e.g. ['ca', 'cho', 'rro']

        Returns: Stress syllable position, e.g. (2, 5) -> 'cho'

        """
        a, b, stress = 0, 0, self.get_stress_vowel()
        for it in syllables:
            b += len(it)
            if stress >= a and stress < b:
                return a, b
            else:
                a += len(it)

        return 0, len(syllables[0])


    def get_stress_syllable_with_hyphen(self, syllables):
        """
        Returns the stress syllable positions

        Args:
            syllables: Word syllables with hyphen , e.g. 'ca-cho-rro'

        Returns: Stress syllable position, e.g. (3, 6) -> 'cho'

        """
        mtch = [match.start() for match in re.finditer('-', syllables)]
        stress = self.get_stress_vowel_with_hyphen(syllables)
        tmp1, tmp2 = 0, len(syllables)
        for i in range(len(mtch)):
            if mtch[i] < stress:
                tmp1 = mtch[i]
            else:
                tmp2 = mtch[i]
                break
        tmp1 += 1 if tmp1 != 0 else tmp1

        return tmp1, tmp2


    def get_stress_phonetic_syllable(self, syllables, phonemes):
        """
        Returns the stress phonetic syllable positions based on tonic syllable.

        Args:
            syllables: Word syllables, e.g. "cho-co-la-te"
            phoneme: Word phonemes, e.g. "ʃo-ko-la-ʧɪ"

        Returns: Stress phonetic syllable positions, e.g.

        """
        syl = sorted([m.start() for m in re.finditer('-', syllables)] + [-1, len(syllables)])
        pho = sorted([m.start() for m in re.finditer('-', phonemes)] + [-1, len(phonemes)])
        a, b = self.get_stress_syllable_with_hyphen(syllables)
        i, j, k = 0, 0, 0
        if len(syl) == len(pho):
            while (k < len(syl) - 1):
                if syl[k] <= a and syl[k + 1] >= b:
                    i = k
                    j = k + 1
                    break
                k += 1
            return pho[i] + 1, pho[j]

        return 0, len(phonemes)

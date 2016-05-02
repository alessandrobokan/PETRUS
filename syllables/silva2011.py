#!/usr/bin/python
# -*- coding: utf-8 -*-

# ceci.py - Syllable separation using the CECI algorithm
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
#           Andre Cunha      <andre.lv.cunha@gmail.com> (minor modifications)

from __future__ import unicode_literals

from cases import case1, case2, case3, case4, case5, case6, case7, case8, case9, case10

import re


# Vowels
V = ['a', 'e', 'o', 'á', 'é', 'í', 'ó', 'ú', 'ã', 'õ', 'â', 'ê', 'ô', 'à', 'ü']

# Semivowels
G = ['i', 'u']

# Stop consonants
COc = ['ca', 'co', 'cu', 'que', 'qui', 'ga', 'go', 'gu', 'gue', 'gui']
CO = ['p', 't',  'b', 'd', 'c', 'g', 'q'] + COc

# Fricative consonants
CFc = ['ce', 'ci', 'ss', 'ch', 'ge', 'gi']
CF = ['f', 'v', 's', 'ç', 'z', 'j', 'x'] + CFc

# Liquid consonants
CL = ['l', 'r', 'rr']

# Nasal consonants
CN = ['m', 'n']

# Consonants
C = ['lh', 'nh'] + CO + CF + CL + CN

# Orthographic sequences
OS = ['bp', 'bt', 'bd', 'bc', 'bm', 'bn', 'bs', 'bz', 'bj', 'bv', 'pt', 'ps',
      'pç', 'pc', 'dm', 'dv', 'dj', 'tm', 'ct', 'cn', 'gm', 'mn', 'ft',]


class Silva2011SyllableSeparator(object):
    """
    This class implements the syllabic separation algorithm presented in
    the fourth chapther of the PhD thesis:

        Silva, D.C. (2011) Algoritmos de Processamento da Linguagem e Síntese
        de Voz com Emoções Aplicados a um Conversor Text-Fala Baseado
        em HMM. PhD dissertation, COPPE, UFRJ.

    """
    def __init__(self, word, stress):
        try:
            self.word = word.decode('utf-8').lower()
        except (UnicodeDecodeError, UnicodeEncodeError):
            self.word = word.lower()
        self.stress = stress

    def separate(self):
        """
        Separate a word in syllables.

        Returns:
            A list of strings, containing each syllable of the word.

	    """
        vowels = 'a|e|o|i|u|á|é|í|ó|ú|ã|õ|â|ê|ô|à|ü'
        w = self.word
        p = [match.start() for match in re.finditer(vowels, w, re.UNICODE)]
        p0 = 0  # Syllable start position
        pVt = self.stress  # Tonic vowel position
        k = 0
        c = 0  # Count hyphens

        # Just to pass the Biderman test.
        if len(w) == 1:
            return [w]

        while p0 <= (len(w) - 1):
            # New rule 1:
            if w[p0:p0 + 2] in OS:
                if w[p0 + 2] not in C:
                    w, p0, k, c, p, pVt = case9(w, p, p0, pVt, k, c)
                else:
                    w, p0, k, c, p, pVt = case10(w, p, p0, pVt, k, c)

            # New rule 2
            elif p[k] + 2 < len(w)\
                and w[p[k]] in V + G\
                and w[p[k] + 1] in G\
                and w[p[k] + 2] in V + G:
                w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)

            # Rule 1:
            elif p[k] + 1 < len(w)\
                    and w[p0] in V\
                    and not w[p[k]] in ['ã', 'õ']\
                    and w[p[k] + 1] in V\
                    and not w[p[k] + 1] in G:
                if p[k] + 3 < len(w)\
                        and w[p[k] + 2] == 's'\
                        and p[k] + 3 == len(w):
                    return w
                else:
                    w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)

            # Rule 2:
            elif p[k] + 3 < len(w)\
                    and w[p0] in V\
                    and w[p[k] + 1] in C\
                    and w[p[k] + 2] in C\
                    and w[p[k] + 3] in CO:
                w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)

            # Rule 3:
            elif p[k] + 2 < len(w)\
                    and w[p0] in V\
                    and w[p[k] + 1] in G + CN + ['s', 'r', 'l', 'x']\
                    and w[p[k] + 2] in C:
                if w[p[k] + 1] == 'i'\
                        and w[p[k] + 2] in CN:
                    w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)
                elif not w[p[k] + 2] in ['s', 'h']\
                        and w[p[k] + 1] != w[p[k] + 2]:
                    w, p0, k, c, p, pVt = case2(w, p, p0, pVt, k, c)
                elif p[k] + 3 < len(w)\
                        and w[p[k] + 1] in CN\
                        and w[p[k] + 2] == 's'\
                        and not w[p[k] + 3] in V:
                    w, p0, k, c, p, pVt = case7(w, p, p0, pVt, k, c)
                elif w[p[k] + 1] == w[p[k] + 2]\
                        or w[p[k] + 2] == 'h':
                    w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)
                elif p[k] + 3 < len(w)\
                        and w[p[k] + 2] == 's'\
                        and ((w[p[k] + 3] in C and w[p[k] + 3] != 's')
                             or not w[p[k] + 3] in C + V):
                    w, p0, k, c, p, pVt = case7(w, p, p0, pVt, k, c)
                else:
                    w, p0, k, c, p, pVt = case2(w, p, p0, pVt, k, c)

            # Rule 4:
            elif p[k] + 3 < len(w)\
                    and w[p0] in V\
                    and w[p[k] + 1] in CO + CF + ['g', 'p']\
                    and w[p[k] + 2] in CO + CF + CN + ['ç']\
                    and w[p[k] + 3] in V + G:
                """
                if w[p[k] + 1] == w[p[k] + 2]:
                    w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)
                else:
                    w, p0, k, c, p, pVt = case2(w, p, p0, pVt, k, c)
                """
                w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)


            # Rule 5:
            elif p[k] + 2 < len(w)\
                    and w[p0] in V\
                    and w[p[k] + 1] in C\
                    and w[p[k] + 2] in V + G + CL + ['h']:
                w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)

            # Rule 6:
            elif p[k] + 3 < len(w)\
                    and w[p0] in V\
                    and w[p[k] + 1] in G\
                    and w[p[k] + 2] == 's'\
                    and w[p[k] + 3] in CO:
                # TODO Regra 6 esta dentro da regra 3
                w, p0, k, c, p, pVt = case5(w, p, p0, pVt, k, c)

            # Rule 7:
            elif p[k] + 2 < len(w)\
                    and not w[p0] in V\
                    and w[p[k] - 1] in C + ['u', 'ü', 'q']\
                    and w[p[k] + 1] in C\
                    and w[p[k] + 2] in V:
                w, p0, k, c, p, pVt = case3(w, p, p0, pVt, k, c)

            # Rule 8:
            elif p[k] + 3 < len(w)\
                    and not w[p0] in V\
                    and w[p[k] - 1] in C\
                    and w[p[k] + 1] in G\
                    and w[p[k] + 2] == 'r'\
                    and w[p[k] + 3] in C:
                w, p0, k, c, p, pVt = case3(w, p, p0, pVt, k, c)

            # Rule 9:
            elif p[k] + 3 < len(w)\
                    and not w[p0] in V\
                    and w[p[k] - 1] in C\
                    and w[p[k] + 1] in G + CN\
                    and w[p[k] + 2] == 's'\
                    and w[p[k] + 3] in CO:
                w, p0, k, c, p, pVt = case7(w, p, p0, pVt, k, c)

            # Rule 10:
            elif p[k] + 3 < len(w)\
                    and not w[p0] in V\
                    and w[p[k] - 1] in C + G\
                    and w[p[k] + 1] in ['i', 'u', 'e', 'o']\
                    and p[k] + 1 != pVt\
                    and w[p[k]] != w[p[k] + 1]\
                    and w[p[k] + 2] in C\
                    and w[p[k] + 3] in C + V\
                    and w[p[k] + 2] != 's':
                if p[k] == pVt\
                        and w[p[k] + 2] != 'n'\
                        and not w[p[k] + 3] in C:
                    w, p0, k, c, p, pVt = case4(w, p, p0, pVt, k, c)
                elif not w[p[k] - 1] in ['q', 'g']\
                        and w[p[k]] == 'u'\
                        and w[p[k] + 1] == 'i'\
                        and w[p[k] + 2] != 'n':
                    w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)
                elif p[k] != pVt\
                        and w[p[k] + 1] == 'i'\
                        and w[p[k] + 2] != 'n':
                    w, p0, k, c, p, pVt = case2(w, p, p0, pVt, k, c)
                elif (w[p[k] + 1] != 'i'
                      and w[p[k] + 2] in CN + ['r']
                      and not w[p[k] + 3] in ['h', w[pVt]])\
                        or (w[p[k]] in ['a', 'e', 'o']
                            and w[p[k] + 1] in ['a', 'e', 'o']
                            and w[p[k] + 2] in CN
                            and not w[p[k] + 3] in ['h', 's']
                            and w[p[k] + 4] in V + C):
                    if w[p[k] - 1:p[k] + 1] == "gu"\
                            and w[p[k] + 1] in V\
                            and w[p[k] + 2] in CN:
                        w, p0, k, c, p, pVt = case5(w, p, p0, pVt, k, c)
                    elif w[p[k] - 1:p[k] + 1] == "gu"\
                            and w[p[k] + 1] in V\
                            and w[p[k] + 2] in CL:
                        w, p0, k, c, p, pVt = case2(w, p, p0, pVt, k, c)
                    else:
                        w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)
                elif w[p[k]] in G\
                        and w[p[k] + 1] in ['a', 'e', 'o']\
                        and w[p[k] + 2] in CN:
                    w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)
                elif w[p[k] + 2] in CN:
                    w, p0, k, c, p, pVt = case5(w, p, p0, pVt, k, c)
                else:
                    w, p0, k, c, p, pVt = case4(w, p, p0, pVt, k, c)

            # Rule 11:
            elif p[k] + 2 < len(w)\
                    and not w[p0] in V\
                    and w[p[k] - 1] in C\
                    and w[p[k] + 1] in G\
                    and w[p[k] + 2] in V:
                w, p0, k, c, p, pVt = case4(w, p, p0, pVt, k, c)

            # Rule 12:
            elif p[k] + 3 < len(w)\
                    and not w[p0] in V\
                    and w[p[k] - 1] in C and w[p[k] - 1] not in ['q', 'g']\
                    and w[p[k]] in G\
                    and w[p[k] + 1] in V + ['i']\
                    and w[p[k]] != w[p[k] + 1]\
                    and w[p[k] + 2] in C\
                    and w[p[k] + 3] in V:
                # TODO Adicionar "i" nas vogais (V + 'i') e limitar consoantes (C - 'p, q')
                if w[p[k] - 1] in ['q', 'g']\
                   and ((w[p[k] + 2] == 'ç'
                         and w[p[k] + 3] in ['ã', 'õ'])
                        or (w[p[k] - 1] == 'q'
                            and w[p[k] + 1] in V)):
                    w, p0, k, c, p, pVt = case2(w, p, p0, pVt, k, c)
                elif p[k] + 1 == pVt\
                        or w[p[k] - 1] == 'r' and p[k] + 3 == pVt:
                    w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)
                else:
                    w, p0, k, c, p, pVt = case8(w, p, p0, pVt, k, c)

            # Rule 13:
            elif p[k] + 3 < len(w)\
                    and not w[p0] in V\
                    and (w[p[k] - 1] in C
                         or (w[p[k] - 1:p[k] + 1]
                             in ['qu', 'qü', 'gu', 'gü']))\
                    and w[p[k] + 1] in V + CL + CN + ['c', 'x']\
                    and w[p[k] + 2] in ['h', 'l', 'r']\
                    and w[p[k] + 3] in V + ['h', 'l', 'r']:
                # TODO Arrumando regra para "guerra" -> gue-rra
                if w[p[k] + 1] == w[p[k] + 2]\
                        or w[p[k] + 1] in ['c', 'l']\
                        or w[p[k] + 1:p[k] + 3] == 'nh':
                    w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)
                else:
                    w, p0, k, c, p, pVt = case4(w, p, p0, pVt, k, c)

            # Rule 14:
            elif p[k] + 2 < len(w)\
                    and not w[p0] in V\
                    and w[p[k] - 1] in C\
                    and w[p[k] + 1] in CL + CN + ['i']\
                    and w[p[k] + 2] == 's':
                if p[k] + 3 == len(w):
                    p0 = case6(w, p0)
                elif p[k] == pVt or (p[k] + 3 < len(w) and w[p[k] + 3] in V):
                    w, p0, k, c, p, pVt = case4(w, p, p0, pVt, k, c)
                else:
                    w, p0, k, c, p, pVt = case5(w, p, p0, pVt, k, c)

            # Rule 15:
            elif p[k] + 2 < len(w)\
                    and not w[p0] in V\
                    and w[p[k] + 1] in V\
                    and w[p[k] + 2] in V + G\
                    and not w[p[k] - 1:p[k] + 1] in ['qu', 'gu']:
                if p[k] + 3 < len(w)\
                        and p[k] == pVt\
                        and w[p[k] + 1] in G\
                        and w[p[k] + 3] in C:
                    w, p0, k, c, p, pVt = case2(w, p, p0, pVt, k, c)
                else:
                    w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)

            # Rule 16:
            elif p[k] + 2 < len(w)\
                    and not w[p0] in V\
                    and w[p[k]] != 'u'\
                    and w[p[k] - 1] in C\
                    and w[p[k] + 1] in V\
                    and w[p[k] + 2] in CN:
                w, p0, k, c, p, pVt = case3(w, p, p0, pVt, k, c)

            # Rule 17:
            elif p[k] + 1 < len(w)\
                    and p[k] - 2 >= 0\
                    and not w[p0] in V\
                    and w[p[k]] == 'i'\
                    and (w[p[k] - 2] in ['á', 'é', 'í', 'ó', 'ú']
                         or w[p[k] - 3] in ['á', 'é', 'í', 'ó', 'ú'])\
                    and w[p[k] - 1] in C\
                    and w[p[k] + 1] in ['a', 'o']:
                # TODO trocar caso 6 por caso 1.
                w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)

            # Rule 18:
            elif p[k] + 1 < len(w)\
                    and not w[p0] in V\
                    and w[p[k]] in ['ã', 'õ']\
                    and w[p[k] - 1] in C\
                    and w[p[k] + 1] in ['e', 'o']:
                p0 = case6(w, p0)

            # -------------------- Change rule 19 by 20 --------------------
            # Rule 20:
            elif p[k] + 3 < len(w)\
                    and not w[p0] in V\
                    and w[p[k] - 1] in C\
                    and w[p[k] + 1] in V\
                    and w[p[k] + 2] in CN\
                    and w[p[k] + 3] in C:
                w, p0, k, c, p, pVt = case7(w, p, p0, pVt, k, c)

            # Rule 19:
            elif p[k] + 1 < len(w)\
                    and not w[p0] in V\
                    and w[p[k] - 1] in C\
                    and p[k] + 1 == pVt\
                    and not w[p[k] + 1] in ['i', 'u']\
                    and not w[p[k] - 1:p[k] + 1] in ['gu', 'qu']:
                if p[k] + 3 == len(w)\
                        and w[p[k] - 1:p[k] + 1] in ['gu', 'qu']\
                        and w[p[k] + 1] in V\
                        and w[p[k] + 2] in C:
                    p0 = case6(w, p0)
                elif p[k] + 2 < len(w)\
                        and w[p[k] - 1:p[k] + 1] in ['gu', 'qu']\
                        and w[p[k] + 1] in V\
                        and w[p[k] + 2] in C + G:
                    w, p0, k, c, p, pVt = case5(w, p, p0, pVt, k, c)
                else:
                    w, p0, k, c, p, pVt = case3(w, p, p0, pVt, k, c)

            # Rule 21:
            elif p[k] + 3 < len(w)\
                    and not w[p0] in V\
                    and w[p[k] + 1] in CO + ['f', 'v', 'g']\
                    and w[p[k] + 2] in CL + CO\
                    and w[p[k] + 3] in V + G:
                if w[p[k] + 1] in ['f', 'p']\
                        and w[p[k] + 2] in ['t', 'ç']:
                    w, p0, k, c, p, pVt = case2(w, p, p0, pVt, k, c)
                else:
                    w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)

            # Rule 22:
            elif p[k] + 1 < len(w)\
                    and p[k] - 2 >= 0\
                    and not w[p0] in V\
                    and (w[p[k] - 1] in C
                         or w[p[k] - 1:p[k] + 1] in ['qu', 'gu'])\
                    and w[p[k] + 1] in V\
                    and (p[k] + 2 == len(w)
                         or w[p[k] + 2] in C):
                if (w[p[k]] in ['i', 'u', 'í', 'ú', 'é', 'ê']
                    and p[k] == pVt
                    and w[p[k] + 1] != 'u')\
                        or (p[k] + 3 < len(w)
                            and not w[p[k]] in G
                            and w[p[k] + 2] == 's'
                            and not w[p[k] + 3] in C + V):
                    w, p0, k, c, p, pVt = case3(w, p, p0, pVt, k, c)
                elif p[k] + 2 == len(w)\
                        and w[p[k]] == 'i'\
                        and p[k] == pVt\
                        and w[p[k] + 1] == 'u':
                    w, p0, k, c, p, pVt = case4(w, p, p0, pVt, k, c)
                elif p[k] + 3 < len(w)\
                        and ((w[p[k]] in G
                              and p[k] + 1 != pVt
                              and not w[p[k] + 2] in C + V)
                             or (w[p[k] + 2] == 's'
                                 and not w[p[k] + 3] in C + V)
                             or (p[k] != pVt
                             and p[k] + 1 != pVt
                             and w[p[k] + 2] == 's'
                             and p[k] + 3 == len(w))):
                    w, p0, k, c, p, pVt = case2(w, p, p0, pVt, k, c)
                elif p[k] + 3 < len(w)\
                        and w[p[k] - 1:p[k] + 1] in ['qu', 'gu']\
                        and w[p[k] + 2] in C\
                        and w[p[k] + 3] in V + G:
                    w, p0, k, c, p, pVt = case2(w, p, p0, pVt, k, c)
                elif p[k] + 2 == len(w)\
                        and w[p[k] - 1:p[k] + 1] in ['qu', 'gu']\
                        and w[p[k] + 1] in V + G:
                    p0 = case6(w, p0)
                elif p[k] + 3 == len(w)\
                        and w[p[k] + 1] in ['o', 'u']\
                        and p[k] + 1 != pVt\
                        and w[p[k] + 2] == 's':
                    w, p0, k, c, p, pVt = case7(w, p, p0, pVt, k, c)
                elif w[p[k]] == 'u'\
                        and w[p[k] + 1] in ['e', 'ê', 'é']\
                        and w[p[k] + 2] in ['n', 's', 'i', 'l']:
                    w, p0, k, c, p, pVt = case5(w, p, p0, pVt, k, c)
                else:
                    # TODO Trocar case2 por case 1
                    w, p0, k, c, p, pVt = case2(w, p, p0, pVt, k, c)

            # Rule 23:
            elif p[k] + 2 < len(w)\
                    and not w[p0] in V\
                    and (w[p[k] - 1] in C
                         or w[p[k] - 2:p[k] - 1] == "qu")\
                    and w[p[k] + 1] in C\
                    and w[p[k] + 2] in C:
                if w[p[k] + 1] == w[p[k] + 2]:
                    w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)
                elif w[p[k] + 1] == 's'\
                        and w[p[k] + 2] != 's':
                    w, p0, k, c, p, pVt = case2(w, p, p0, pVt, k, c)
                elif p[k] + 3 < len(w)\
                        and w[p[k] + 2] == 's'\
                        and w[p[k] + 3] in CO:
                    w, p0, k, c, p, pVt = case5(w, p, p0, pVt, k, c)
                else:
                    w, p0, k, c, p, pVt = case2(w, p, p0, pVt, k, c)

            # Rule 24:
            elif p[k] + 2 < len(w)\
                    and not w[p0] in V\
                    and w[p[k] + 1] in C\
                    and w[p[k] + 2] in G:
                w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)

            # Rule 25: Already aplicated

            # Rule 26:
            elif p[k] + 2 < len(w)\
                    and not w[p0] in V\
                    and (w[p[k] - 1] in C
                         or (w[p[k] - 1:p[k] + 1]
                             in ['qu', 'qü', 'gu', 'gü']))\
                    and w[p[k] + 1] in G\
                    and w[p[k] + 2] in CN:
                if w[p[k] + 3] in C:
                    w, p0, k, c, p, pVt = case5(w, p, p0, pVt, k, c)
                else:
                    w, p0, k, c, p, pVt = case4(w, p, p0, pVt, k, c)


            # Rule 27:
            elif p[k] + 2 < len(w)\
                    and not w[p0] in V\
                    and w[p[k] - 1] in C\
                    and w[p[k] - 2] in C\
                    and w[p[k] + 1] in G\
                    and w[p[k] + 2] in C:
                w, p0, k, c, p, pVt = case1(w, p, p0, pVt, k, c)

            # Rule 28
            elif p[k] + 2 < len(w)\
                    and not w[p0] in V\
                    and w[p[k] - 1:p[k] + 1] in ['qu', 'qü', 'gu', 'gü']\
                    and w[p[k] + 1] in V:
                if p[k] + 3 < len(w)\
                        and w[p[k] + 2] in C\
                        and w[p[k] + 3] in C:
                    w, p0, k, c, p, pVt = case5(w, p, p0, pVt, k, c)
                elif p[k] + 3 < len(w)\
                        and w[p[k] + 2] in C\
                        and w[p[k] + 3] in V + G:
                    w, p0, k, c, p, pVt = case4(w, p, p0, pVt, k, c)
                elif p[k] + 2 < len(w)\
                        and w[p[k] + 2] in V:
                    w, p0, k, c, p, pVt = case4(w, p, p0, pVt, k, c)
                elif p[k] + 2 < len(w)\
                        and w[p[k] + 2] in G:
                    w, p0, k, c, p, pVt = case5(w, p, p0, pVt, k, c)

            p0 += 1

        s = re.sub(r"\-+", "-", w)

        return s[:-1].split('-') if s[-1] == '-' else s.split('-')
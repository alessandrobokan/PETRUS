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
# Authors:  Andre Cunha      <andre.lv.cunha@gmail.com>
#           Alessandro Bokan <alessandro.bokan@gmail.com> (minor modifications)


from __future__ import unicode_literals


class CECISyllableSeparator(object):
    def __init__(self, word):
        try:
            self.word = word.decode('utf-8').lower()
        except (UnicodeDecodeError, UnicodeEncodeError):
            self.word = word.lower()

    def _get(self, la, le):
        letters = self.tab_ceci[0]
        line = letters.index(la)
        column = letters.index(le)
        return self.tab_ceci[line][column]

    def _get_action(self, la, le):
        if not la.isalpha():
            return 2
        if not le.isalpha():
            return 3
        t = self._get(la, le)
        if t.isspace():
            return 0
        return int(t)

    def separate(self):
        if self.word[0] == 'à':
            has_crasis = True
            word = 'a' + self.word[1:]
        else:
            has_crasis = False

        self.word += ' '
        no_syllables = 1
        start_syllable = True
        result = self.word[0]
        _le = 1
        _la = 0

        is_vowel = lambda x: x.lower() in 'aáãâeéêiíoóôõuúü'
        is_consonant = lambda x: not is_vowel(x)

        stop = False
        while not stop:
            action = self._get_action(self.word[_la].lower(), self.word[_le].lower())

            if action == 0:
                result += self.word[_le]
                start_syllable = False
            elif action == 1:
                result += ' '
                no_syllables += 1
                result += self.word[_le]
                start_syllable = True
            elif action == 2:
                if start_syllable and no_syllables > 1:
                    result = result[:-2] + result[-1]
                    no_syllables -= 1
                result += ' '
                no_syllables += 1
                result += self.word[_le]
                start_syllable = True
            elif action == 3:
                if start_syllable\
                        and is_consonant(self.word[_la])\
                        and no_syllables != 1:
                    if len(result) > 2:
                        result = result[:-2] + result[-1]
                    no_syllables -= 1
                result += ' '
                no_syllables += 1
                result += self.word[_le]
                start_syllable = True
            elif action == 4:
                if start_syllable and no_syllables == 1:
                    result += self.word[_le]
                    start_syllable = False
                else:
                    if start_syllable and no_syllables > 1:
                        result = result[:-2] + result[-1]
                        no_syllables -= 1
                    result += ' '
                    no_syllables += 1
                    result += self.word[_le]
                    start_syllable = True
            else:
                raise Exception(u'Unknown action code')
            _le += 1
            _la += 1
            stop = (_le == len(self.word))

        if has_crasis:
            result = 'à' + result[1:]

        #print "KADSKLASDKALS", result
        #result = result.strip().replace(u' ', u'-')

        return result.split()

    def no_syllables(self, word):
        if word[0] == u'à':
            word = u'a' + word[1:]

        word += u' '
        no_syllables = 1
        start_syllable = True
        _le = 1
        _la = 0

        is_vowel = lambda x: x.lower() in 'aáãâeéêiíoóôõuúü'
        is_consonant = lambda x: not is_vowel(x)

        stop = False
        while not stop:
            action = self._get_action(word[_la].lower(), word[_le].lower())

            if action == 0:
                start_syllable = False
            elif action == 1:
                no_syllables += 1
                start_syllable = True
            elif action == 2:
                if start_syllable and no_syllables > 1:
                    no_syllables -= 1
                no_syllables += 1
                start_syllable = True
            elif action == 3:
                if start_syllable\
                        and is_consonant(word[_la])\
                        and no_syllables != 1:
                    no_syllables -= 1
                no_syllables += 1
                start_syllable = True
            elif action == 4:
                if start_syllable and no_syllables == 1:
                    start_syllable = False
                else:
                    if start_syllable and no_syllables > 1:
                        no_syllables -= 1
                    no_syllables += 1
                    start_syllable = True
            else:
                raise Exception(u'Unknown action code')
            _le += 1
            _la += 1
            stop = (_le == len(word))

        return no_syllables - 1

    tab_ceci = [
        ' aáãâbcçdeéêfghiíjklmnoóôõpqrstuúüvwxyz',
        'a11113311011111111111101101111101 1 101',
        'á    11110  11 0 111110   111111  1 101',
        'ã        0            0      0       0 ',
        'â    11110     11111110   11111 1 1 101',
        'b000022 200022 002 0220000220220002  0 ',
        'c0000 22 000  000  0240000  002000   0 ',
        'ç0000    000   0      0000     000   0 ',
        'd0000222200022200222220000220220002  00',
        'e1  1111111 11 0111111111 111110101 101',
        'é0   1111   11 0 1 1110   111110  1 101',
        'ê0   1111   11   1 1110   111110  1 101',
        'f0000    000   00  0 20000  0 2000   0 ',
        'g0000    000  000  0240000  0  000   0 ',
        'h0000    000   00     0000     000   0 ',
        'i1111111111111 111 11111111111111 1 101',
        'í1   11111  11 1 111111   11111   1 101',
        'j0000    000   00     0000     000   0 ',
        'k0000    000   00  0 40000  0  000   0 ',
        'l0000222200022000220220000222220002 202',
        'm00002   000   00   2400002    000   0 ',
        'n0000 22200022000222220000 22220002 202',
        'o0111311101111 011111111111111101 11101',
        'ó0   1111   11 0 111111   11111   1 101',
        'ô0   1111   11   1 111    11111   1 101',
        'õ        0                           0 ',
        'p0000 22 000  000  0 40000  044000   0 ',
        'q0000    000   00  0  0000  0  000   0 ',
        'r0000222200022000222220000222220002 202',
        's00002222000220002222200002222200022202',
        't0000    000  000  0020000  020000   0 ',
        'u0111111101111 011111101101111111 1 101',
        'ú1   11111  11 1 111111   11101   1 101',
        'ü        000   00     0000           0 ',
        'v0000    000  000  0  0000  0  000   0 ',
        'w0000    000  000  0  0000  0  000   0 ',
        'x0000222200022 002222200002222200022202',
        'y00001111000110001111100001111100011111',
        'z00002222000220002222200002222200022222',
    ]

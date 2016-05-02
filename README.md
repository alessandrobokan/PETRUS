Pɛtɾʊs (PhonEtic TRanscriber for User Support)
=========================

Pɛtɾʊs is a an online automatic phonetic transcription system for **Brazilian Portuguese**. For example, Pɛtɾʊs
automatically converts a sequence of letters like "descrédito" into a sequence of phones [ʤiskɾɛʤɪtʊ].

In order to represent the pronunciation of a word, the [IPA](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet)
(International Phonetic Alphabet), a latin-based alphabetical system for phonetic notation, is utilized.
Beyond phonetic transcription, Pɛtɾʊs offers more information to users like: stressed syllable identification and
syllabification. Also, it transcribes hetereophonic homographs (words with the same spelling, but different
pronunciation), generating both forms as output.

If you would like to transcribe a single word or a file, just go to the main [website](http://54.232.255.128/).


What's syllabification?
=====
The syllabic division consists in the identification and delimitation of the syllables that constitute each word.
To perform this task automatically by Pɛtɾʊs, we adopted two algorithms: a rule-based algorithm described in Silva (2011)
and the CECI algorithm.

The syllabification algorithm proposed by Silva (2011, p. 39) was developed on the basis of the Brazilian Portuguese
spelling, but **predominating** phonology of words. Thus, the words "obstrução" (occlusion), "arredondar" (to round) and
"assado" (roasted) are divided into syllables as follows, respectively: (o.bs.tru.ção), (a.rre.don.dar) and (a.ssa.do).


About
=====
The automatic phonetic transcription called Pɛtɾʊs is a project carried out in "Instituto de Biociências, Letras e
Ciências Exatas da UNESP" ([IBILCE](http://www.ibilce.unesp.br/)), by the doctoral student in linguistic
[Vanessa Marquiafavel Serrani](http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K4771845J5), under the
supervision of Prof. Dra. [Claudia Zavaglia](http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K4790044E8).
Pɛtɾʊs is dedicated to the automatic phonetic transcription of simple words from Brazilian Portuguese, having as
reference **São Paulo** state standard pronunciation.


***
Usage
=====

* Test by word using the Silva (2011) algorithm:

```
$ python test_word.py -s silva -w guerra

guerra -> [ˈge.xa] | gue-rra | [gue]-rra

```

* Test by word using the CECI algorithm:

```
$ python test_word.py -s ceci -w guerra

guerra -> [ˈge.xa] | guer-ra | [guer]-ra

```

* Example transcribing transcribes Hetereophonic Homographs (HHs):

```
$ python test_word.py -s silva -w molho

molho -> [ˈmo.ʎʊ, ˈmɔ.ʎʊ] | mo-lho | [mo]-lho

```

* Test by file:

```
$ python test_file.py -s silva -f example.txt
```

or:

```
$ python test_file.py -s ceci -f example.txt
```


***
References
=========

* Marquiafavel, V.; Bokan, A. and Zavaglia, C. (2014). "PETRUS: A rule-based grapheme-to-phone converter for Brazilian Portuguese". In: J. Baptista et al. (Eds.): PROPOR 2014, LNAI 8776, Springer, Heidelberg (2014).
* Cristófaro-Silva, T. (2000). "Fonética e fonologia dos português: roteiro de estudos e guia de exercícios". 3a ed., São Paulo: Contexto.
* Cagliari, L. (2009). "Elementos de fonética do português brasileiro". São Paulo: Paulistana.
* Silva, D. (2011). "Algoritmos de processamento da linguagem e síntese de voz com emoções aplicados a um conversor texto-fala baseado em HMM". Tese de Doutorado. Programa de Pós-Graduação em Engenharia Elétrica, COPPE, Universidade Federal do Rio de Janeiro, RJ, 2011

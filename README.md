Pɛtɾʊs (PhonEtic TRanscriber for User Support.)
=========================

Pɛtɾʊs is a an online automatic phonetic transcription system for Brazilian Portuguese. For example, Pɛtɾʊs
automatically converts a sequence of letters like <descrédito> into a sequence of phones [ʤiskɾɛʤɪtʊ]


See the website: http://54.232.255.128/

***
Usage
=====

* Test by word using the Silva2011 algorithm:

```
$ python test_word.py -s silva -w chocolate
```

or using the CECI algorithm:

```
$ python test_word.py -s ceci -w chocolate
```


* Test by file:

```
$ python test_file.py -s silva -f example.txt
```

or using the CECI algorithm:

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

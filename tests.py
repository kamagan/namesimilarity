#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import unittest
from namesimilarity import NameSimilarity


class Names(unittest.TestCase):

    # имена одинаковы
    def test_equals(self):
        self.assertEqual(NameSimilarity(
            "Гримо Мишель",
            "Гримо Мишель"
        ).check(), 100)

    # имена разные
    def test_non_equals(self):
        self.assertEqual(NameSimilarity(
            "Пушкин Александр Сергеевич",
            "Толстой Лев Николаевич"
        ).check(), 0)

    # имена похожи, отличаются символом апострофа
    def test_non_letter_symbol(self):
        self.assertEqual(NameSimilarity(
            "О'Лири Патрик",
            "О’Лири Патрик"
        ).check(), 97)

    # имена похожи, отличаются регистром
    # Буджолд Лоис МакМастер => Буджолд Лоис Макмастер
    # де Линт Чарльз => Де Линт Чарльз
    def test_register_symbol(self):
        self.assertEqual(NameSimilarity(
            "Буджолд Лоис МакМастер",
            "Буджолд Лоис Макмастер"
        ).check(), 98)

    # имена похожи, отличаются удвоенным символом
    def test_repeat_symbol(self):
        self.assertEqual(NameSimilarity(
            "Мьевилль Чайна",
            "Мьевиль Чайна"
        ).check(), 95)

    def test_repeat_symbol_invert(self):
        self.assertEqual(NameSimilarity(
            "Мьевиль Чайна",
            "Мьевилль Чайна"
        ).check(), 95)
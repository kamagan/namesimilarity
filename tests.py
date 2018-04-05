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

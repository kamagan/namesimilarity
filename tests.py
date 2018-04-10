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

    # 'э': ['е', 3],
    def test_similar_sound_1(self):
        self.assertEqual(NameSimilarity(
            "Нортон Андрэ",
            "Нортон Андре"
        ).check(), 97)

    def test_similar_sound_1_invert(self):
        self.assertEqual(NameSimilarity(
            "Нортон Андре",
            "Нортон Андрэ"
        ).check(), 97)

    def test_similar_sound_2(self):
        self.assertEqual(NameSimilarity(
            "Найт Дэймон",
            "Найт Деймон"
        ).check(), 97)

    def test_similar_sound_3(self):
        self.assertEqual(NameSimilarity(
            "Нэвилл Кэтрин",
            "Невилл Кэтрин"
        ).check(), 97)

    # 'я': ['а', 3],
    def test_similar_sound_4(self):
        self.assertEqual(NameSimilarity(
            "Маркес Габриэль Гарсия",
            "Маркес Габриэль Гарсиа"
        ).check(), 97)

    # 'ё': ['е', 2],
    def test_similar_sound_5(self):
        self.assertEqual(NameSimilarity(
            "Ладыженский Олег Семенович",
            "Ладыженский Олег Семёнович"
        ).check(), 98)

    # Херберт Фрэнк => Герберт Фрэнк
    # Андерсен Ганс Христиан => Андерсен Ханс Кристиан
    # Джерролд Дэвид => Герролд Дэвид
    # 'г': ['х', 3],
    def test_similar_sound_6(self):
        self.assertEqual(NameSimilarity(
            "Херберт Фрэнк",
            "Герберт Фрэнк"
        ).check(), 97)

    # Андерсен Ганс Христиан => Андерсен Ханс Кристиан
    # 'к': ['х', 3],
    def test_similar_sound_6(self):
        self.assertEqual(NameSimilarity(
            "Андерсен Ханс Христиан",
            "Андерсен Ханс Кристиан"
        ).check(), 97)

    def test_similar_sound_6_double(self):
        self.assertEqual(NameSimilarity(
            "Андерсен Ганс Христиан",
            "Андерсен Ханс Кристиан"
        ).check(), 91)

    # 'дж': ['г', 3]
    def test_similar_sound_7(self):
        self.assertEqual(NameSimilarity(
            "Джерролд Дэвид",
            "Герролд Дэвид"
        ).check(), 97)

    # Конан Дойль Артур => Дойл Артур Конан
    # Уайлд Оскар => Уайльд Оскар
    # 'ь': ['', 2]
    def test_similar_sound_8(self):
        self.assertEqual(NameSimilarity(
            "Конан Дойль Артур",
            "Конан Дойл Артур"
        ).check(), 98)

    def test_similar_sound_8_invert(self):
        self.assertEqual(NameSimilarity(
            "Конан Дойл Артур",
            "Конан Дойль Артур"
        ).check(), 98)

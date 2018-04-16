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

    # имена разные, по одному слову в каждом
    def test_non_equals_one_word_per_name(self):
        self.assertEqual(NameSimilarity(
            "Пушкин",
            "Толстой"
        ).check(), 0)

    # одно из имён пустое
    def test_non_equals_one_word_end_empty(self):
        self.assertEqual(NameSimilarity(
            "Пушкин",
            ""
        ).check(), 0)

    # имена пустые
    def test_empty_names(self):
        self.assertEqual(NameSimilarity(
            "",
            ""
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

    # имена похожи, отличаются удвоенным символом расположенном в конце
    def test_repeat_symbol_end(self):
        self.assertEqual(NameSimilarity(
            "Чайна Мьевилль",
            "Чайна Мьевиль"
        ).check(), 95)

    def test_repeat_symbol_end_invert(self):
        self.assertEqual(NameSimilarity(
            "Чайна Мьевиль",
            "Чайна Мьевилль"
        ).check(), 95)

    #
    # имена похожи, отличаются буквами, дающими похожие звуки...

    # ...
    # 'э': ['е', 3],
    # Нортон Андрэ => Нортон Андре
    # Найт Дэймон => Найт Деймон
    # Нэвилл Кэтрин => Невилл Кэтрин
    def test_similar_sound_e_to_ie(self):
        self.assertEqual(NameSimilarity(
            "Нортон Андрэ",
            "Нортон Андре"
        ).check(), 97)

    def test_similar_sound_e_to_ie_invert(self):
        self.assertEqual(NameSimilarity(
            "Нортон Андре",
            "Нортон Андрэ"
        ).check(), 97)

    # ...
    # 'я': ['а', 3],
    def test_similar_sound_ya_to_a(self):
        self.assertEqual(NameSimilarity(
            "Маркес Габриэль Гарсия",
            "Маркес Габриэль Гарсиа"
        ).check(), 97)

    # ...
    # 'ё': ['е', 2],
    def test_similar_sound_io_to_ie(self):
        self.assertEqual(NameSimilarity(
            "Ладыженский Олег Семенович",
            "Ладыженский Олег Семёнович"
        ).check(), 98)

    # ...
    # 'г': ['х', 3],
    # Херберт Фрэнк => Герберт Фрэнк
    # Андерсен Ганс Христиан => Андерсен Ханс Кристиан
    # Джерролд Дэвид => Герролд Дэвид
    def test_similar_sound_ghe_to_ha(self):
        self.assertEqual(NameSimilarity(
            "Херберт Фрэнк",
            "Герберт Фрэнк"
        ).check(), 97)

    # ...
    # 'к': ['х', 3],
    def test_similar_sound_ka_to_ha(self):
        self.assertEqual(NameSimilarity(
            "Андерсен Ханс Христиан",
            "Андерсен Ханс Кристиан"
        ).check(), 97)

    def test_similar_sound_ka_to_ha_double(self):
        self.assertEqual(NameSimilarity(
            "Андерсен Ганс Христиан",
            "Андерсен Ханс Кристиан"
        ).check(), 91)

    # ...
    # 'дж': ['г', 3]
    def test_similar_sound_de_zhe_to_ghe(self):
        self.assertEqual(NameSimilarity(
            "Джерролд Дэвид",
            "Герролд Дэвид"
        ).check(), 97)

    # ...
    # 'ь': ['', 2]
    # Конан Дойль Артур => Дойл Артур Конан
    # Уайлд Оскар => Уайльд Оскар
    def test_similar_sound_soft_sign_to_empty(self):
        self.assertEqual(NameSimilarity(
            "Конан Дойль Артур",
            "Конан Дойл Артур"
        ).check(), 98)

    def test_similar_sound_soft_sign_to_empty_invert(self):
        self.assertEqual(NameSimilarity(
            "Конан Дойл Артур",
            "Конан Дойль Артур"
        ).check(), 98)

    # различается порядок слов...
    # ...имена одинаковы, состоят из двух слов
    def test_transposition_two_words_per_name(self):
        self.assertEqual(NameSimilarity(
            "Гримо Мишель",
            "Мишель Гримо"
        ).check(), 100)

    # ...имена одинаковы, состоят из трёх слов
    def test_transposition_three_words_per_name_1(self):
        self.assertEqual(NameSimilarity(
            "Трэверс Памела Линдон",
            "Памела Линдон Трэверс"
        ).check(), 100)

    # ...имена одинаковы, состоят из трёх слов
    def test_transposition_three_words_per_name_2(self):
        self.assertEqual(NameSimilarity(
            "Трэверс Линдон Памела",
            "Памела Трэверс Линдон"
        ).check(), 100)

    # ...имена похожи (Гарсия => Гарсиа)
    def test_transposition_similar(self):
        self.assertEqual(NameSimilarity(
            "Маркес Габриэль Гарсия",
            "Гарсиа Маркес Габриэль"
        ).check(), 97)

    # одно или несколько частей имени не похожи или отсутствуют...
    # ... различается количество слов в именах: 2 => 3
    def test_transposition_diff_count_two_and_three(self):
        self.assertEqual(NameSimilarity(
            "Лев Толстой",
            "Толстой Лев Николаевич"
        ).check(), 95)

    # ... различается количество слов в именах: 3 => 2
    def test_transposition_diff_countthree_and_two(self):
        self.assertEqual(NameSimilarity(
            "Лев Николаевич Толстой",
            "Толстой Лев"
        ).check(), 95)

    # ... различается количество слов в именах: 1 => 2
    def test_transposition_diff_count_one_and_two(self):
        self.assertEqual(NameSimilarity(
            "Толстой",
            "Толстой Алексей"
        ).check(), 80)

    # похожи только фамилии
    def test_transposition_same_only_family(self):
        self.assertEqual(NameSimilarity(
            "Толстой Лев",
            "Толстой Алексей"
        ).check(), 20)

#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import difflib
import re


class NameSimilarity:

    def __init__(self, name, check_name):
        self.factors = {
            'non_letter': 3,
            'register': 2,
            'repeat_letter': 5,
            'discarding_base': 5,
            'discarding_both': 2,
            'only_one_after_discarding': 4,
            'substitutes': {
                # Нортон Андрэ => Нортон Андре
                'э': ['е', 3],

                # Маркес Габриэль Гарсия => Гарсиа Маркес Габриэль
                'я': ['а', 3],

                # Ладыженский Олег Семенович => Ладыженский Олег Семёнович
                'ё': ['е', 2],

                # Херберт Фрэнк => Герберт Фрэнк
                # Андерсен Ганс Христиан => Андерсен Ханс Кристиан
                'г': ['х', 3],

                # Андерсен Ганс Христиан => Андерсен Ханс Кристиан
                'к': ['х', 3],

                # Джерролд Дэвид => Герролд Дэвид
                'дж': ['г', 3],

                # Конан Дойль Артур => Дойл Артур Конан
                'ь': ['', 2]
            }
        }

        self.uncertainty = 1

        self.name = name
        self.name_init = name

        self.check_name = check_name
        self.check_name_init = check_name

    def check(self, transposition=True):
        if transposition:
            self.check_transposition()

        self.check_diff_non_letter()
        self.check_diff_register()
        self.check_diff_repeat()
        self.check_diff_similar_sound()

        if (
            self.name != self.check_name
            or self.uncertainty > 100
            or self.name == ''
            or self.check_name == ''
        ):
            self.uncertainty = 100

        if self.uncertainty == 1:
            self.uncertainty = 0

        similarity = 100 - self.uncertainty
        return similarity

    def check_transposition(self):
        if self.name == self.check_name:
            return

        list_name = self.name.split()
        list_check_name = self.check_name.split()
        out_list_name = []
        out_list_check_name = []

        for item in list_name:
            found = False

            for check_item in list_check_name:
                if check_item == item:
                    out_list_name.append(item)
                    out_list_check_name.append(check_item)
                    list_check_name.remove(check_item)
                    found = True
                    break

            if not found:
                sim_max = 0
                sim_max_index = None
                index = 0
                for check_item in list_check_name:
                    sim = NameSimilarity(item, check_item).check(transposition=False)
                    if sim > sim_max:
                        sim_max = sim
                        sim_max_index = index

                    index += 1

                if sim_max > 0:
                    out_list_name.append(item)
                    sim_check_item = list_check_name.pop(sim_max_index)
                    out_list_check_name.append(sim_check_item)

        rest_name = len(list_name) - len(out_list_name)
        rest_check_name = len(list_check_name)
        rest = rest_name + rest_check_name

        # влияющие факторы:
        #   кол-во похожих слов в имени
        #   кол-во не-похожих слов в имени
        #   был ли остаток только в name или check_name или в обоих
        #       если только в одном, то это может быть различие
        #       в наличии или отсутсвии отчества,
        #       если осталось что-то и там и там,
        #       то это уже сильно подозрительно

        multiplier = 1
        if len(out_list_check_name) < 2:
            multiplier *= self.factors['only_one_after_discarding']

        if rest_name > 0 and rest_check_name > 0:
            multiplier *= self.factors['discarding_both']

        if rest > 0:
            self.uncertainty *= self.factors['discarding_base'] * rest * multiplier

        self.name = ' '.join(out_list_name)
        self.check_name = ' '.join(out_list_check_name)

    def check_diff_non_letter(self):
        self.check_diff_base(
            replace_condition=self.non_letter
        )

    def check_diff_register(self):
        self.check_diff_base(
            replace_condition=self.register
        )

    def check_diff_repeat(self):
        self.check_diff_base(
            insert_condition=self.repeat_letter,
            delete_condition=self.repeat_letter
        )

    def check_diff_similar_sound(self):
        self.check_diff_base(
            replace_condition=self.similar_sound_replace,
            insert_condition=self.similar_sound_replace,
            delete_condition=self.similar_sound_replace
        )

    def check_diff_base(
        self,
        replace_condition=None,
        insert_condition=None,
        delete_condition=None
    ):
        if self.name == self.check_name:
            return

        conditions = {
            'equal': None,
            'replace': replace_condition,
            'insert': insert_condition,
            'delete': delete_condition
        }

        check_name_tmp = ''
        sequence = difflib.SequenceMatcher(None, self.name, self.check_name)
        for diff in sequence.get_opcodes():

            operation,\
                sub_str_index_start_name, sub_str_index_end_name,\
                sub_str_index_start_check_name, sub_str_index_end_check_name\
                = diff

            name_sub_str = self.name[
                sub_str_index_start_name:sub_str_index_end_name
            ]
            check_name_sub_str = self.check_name[
                sub_str_index_start_check_name:sub_str_index_end_check_name
            ]

            try:
                # если условие корректно ...
                if (
                    conditions[operation] is not None
                    and
                    conditions[operation](
                        name_sub_str,
                        check_name_sub_str,
                        diff
                    )
                ):
                    # ... зменяем подстроку для проверяемого имени
                    # на подстроку имени
                    check_name_tmp += name_sub_str
                else:
                    # ... иначе берём подстроку из проверяемого имени
                    check_name_tmp += check_name_sub_str
            except KeyError as e:
                raise ValueError('Undefined operation: {}'.format(e.args[0]))

        self.check_name = check_name_tmp

    def non_letter(self, a, b, diff):
        if (
            re.match('^[^\w]*$', a) is not None
            and
            re.match('^[^\w]*$', b) is not None
        ):
            self.uncertainty *= self.factors['non_letter']
            return True

        return False

    def register(self, a, b, diff):
        if (
            re.match('^[\w]*$', a) is not None
            and
            re.match('^[\w]*$', b) is not None
            and
            a.lower() == b.lower()
        ):
            self.uncertainty *= self.factors['register']
            return True
        else:
            return False

    def repeat_letter(self, a, b, diff):
        operation, \
            sub_str_index_start_a, ___, \
            sub_str_index_start_b, ___ \
            = diff

        a_full = self.name
        b_full = self.check_name

        if operation == 'insert':
            a, b = b, a
            a_full, b_full = b_full, a_full
            sub_str_index_start_a, sub_str_index_start_b\
                = sub_str_index_start_b, sub_str_index_start_a

        a_next = None
        a_next_index = sub_str_index_start_a + 1
        if len(a_full) > a_next_index:
            a_next = a_full[a_next_index]

        a_pre = None
        a_pre_index = sub_str_index_start_a - 1
        if a_pre_index > 0:
            a_pre = a_full[a_pre_index]

        if (
            (a_next is not None and a == a_next)
            or
            (a_pre is not None and a == a_pre)
        ):
            self.uncertainty *= self.factors['repeat_letter']
            return True
        else:
            return False

    def similar_sound_replace(self, a, b, diff):
        a = a.lower()
        b = b.lower()

        substitutes = self.factors['substitutes']
        sub_a = substitutes.get(a)
        sub_b = substitutes.get(b)

        if ((
            sub_a is not None
            and
            sub_a[0] == b
        ) or (
            sub_b is not None
            and
            sub_b[0] == a
        )):
            if sub_a is not None:
                self.uncertainty *= sub_a[1]
            else:
                self.uncertainty *= sub_b[1]

            return True
        else:
            return False

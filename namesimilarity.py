#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import difflib
import re


class NameSimilarity:

    def __init__(self, name, check_name):
        self.factors = {
            'non_letter': 3,
            'register': 2,
            'repeat_letter': 5
        }

        self.uncertainty = 1

        self.name = name
        self.name_init = name

        self.check_name = check_name
        self.check_name_init = check_name

    def check(self):
        self.check_diff_non_letter()
        self.check_diff_register()
        self.check_diff_repeat()

        if self.name != self.check_name:
            self.uncertainty = 100

        if self.uncertainty == 1:
            self.uncertainty = 0

        similarity = 100 - self.uncertainty
        return similarity

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

        a_next = a_full[sub_str_index_start_a + 1]

        if a == a_next:
            self.uncertainty *= self.factors['repeat_letter']
            return True
        else:
            return False

#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import unittest
from namesimilarity import nameSimilarity


class Names(unittest.TestCase):

    def test_equals(self):
        self.assertEqual(nameSimilarity().check('Гримо Мишель', 'Гримо Мишель'), 100)

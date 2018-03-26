#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class nameSimilarity:

    def __init__(self):
        self.uncertainty = None

        self.name = None
        self.name_init = None

        self.check_name = None
        self.check_name_init = None

    def check(self, name, check_name):
        if name == check_name:
            self.uncertainty = 0
        else:
            self.uncertainty = 100

        similarity = 100 - self.uncertainty
        return similarity

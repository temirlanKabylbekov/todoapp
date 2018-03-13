from django.test import TestCase


class FixtureReaderMixin:

    @classmethod
    def read_fixture(cls, src, binary=False):
        mode = 'r'
        if binary:
            mode = 'rb'
        with open(src, mode) as f:
            return f.read()


class TestCase(FixtureReaderMixin, TestCase):
    pass

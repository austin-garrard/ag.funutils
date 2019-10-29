from unittest import TestCase
from ag.funutils import maybe

class TestMaybe(TestCase):
    
    def test_just(self):
        result = maybe.chain(
            5,
            lambda v: v + 1,
            just=lambda v: v / 2,
            none=99
        )

        self.assertEqual(result, 3)

    def test_just_value(self):
        result = maybe.chain(
            5,
            lambda v: v,
            just=555,
            none=99
        )

        self.assertEqual(result, 555)
    
    def test_none(self):
        result = maybe.chain(
            None,
            lambda v: v + 1,
            just=lambda v: v / 2,
            none=lambda: 1 + 2
        )

        self.assertEqual(result, 3)
    
    def test_none_value(self):
        result = maybe.chain(
            5,
            lambda v: None,
            just=555,
            none=99
        )

        self.assertEqual(result, 99)


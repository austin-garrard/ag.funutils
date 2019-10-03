from unittest import TestCase

import ag.funutils as fun

class TestDicts(TestCase):
    def setUp(self):
        self.log = []
        self.data = {
            "rover1": {
                "pos": (1, 0),
                "dir": "N"
            },
            "rover2": {
                "pos": (2, 3),
                "dir": "W"
            }
        }

    def log_y_pos(self, rover_id, rover):
        self.log.append((rover_id, rover["pos"][1]))

    def move_north(rover_id, rover):
        return (
            rover_id,
            {
                "pos": (rover['pos'][0], rover['pos'][1] + 1),
                "dir": rover["dir"]
            }
        )

    def above_equator(rover_id, rover):
        return rover['pos'][1] > 2

    def collect_directions(dirs, rover_id, rover):
        return dirs + [(rover_id, rover["dir"])]

    def test_map(self):
        mapper = fun.map(TestDicts.move_north)

        result = mapper(self.data.items())

        self.assertEqual(dict(result), {
            "rover1": {
                "pos": (1, 1),
                "dir": "N"
            },
            "rover2": {
                "pos": (2, 4),
                "dir": "W"
            }
        })

    def test_filter(self):
        mapper = fun.filter(TestDicts.above_equator)

        result = mapper(self.data.items())

        self.assertEqual(dict(result), {
            "rover2": {
                "pos": (2, 3),
                "dir": "W"
            }
        })

    def test_reduce(self):
        reducer = fun.reduce(TestDicts.collect_directions, [])

        result = reducer(self.data.items())

        self.assertTrue(("rover1", "N") in result)
        self.assertTrue(("rover2", "W") in result)
        self.assertEqual(len(result), 2)

    def test_chain(self):
        result = fun.chain(
            self.data.items(),
            fun.map(TestDicts.move_north),
            fun.tap_each(self.log_y_pos),
            fun.filter(TestDicts.above_equator),
            dict
        )

        self.assertEqual(result, {
            "rover2": {
                "pos": (2, 4),
                "dir": "W"
            }
        })
    
    def test_boop(self):
        data = {
            'beep': 1,
            'boop': 2,
            'buup': 3,
        }

        add_one = fun.map(lambda k, v: (k, v + 1))
        evens = fun.filter(lambda k, v: v % 2 == 0)
        beep_buup = fun.reduce(lambda acc, k, v: f'{acc}{k}{v}', '')

        result = fun.chain(
            data.items(),
            add_one,
            evens,
            add_one,
            beep_buup
        )

        self.assertEqual(result, 'beep3buup5')


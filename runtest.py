#!/usr/bin/env python3

import unittest

if __name__ == "__main__":
    suite = unittest.TestLoader().discover('tests', pattern = "test_*.py")
    unittest.TextTestRunner().run(suite)


#!/usr/bin/env python3

import unittest
import sys

if __name__ == "__main__":
	suite = unittest.TestLoader().discover('tests', pattern = "test_*.py")
	if len(sys.argv) > 1:
		if sys.argv[1] == 'verbose':
			unittest.TextTestRunner(verbosity=2).run(suite)
		else:
			unittest.TextTestRunner().run(suite)
	else:
		unittest.TextTestRunner().run(suite)


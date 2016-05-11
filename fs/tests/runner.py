import os
import sys
import unittest

VERBOSITY = 2

HERE = os.path.abspath(os.path.dirname(__file__))
testmodules = [os.path.splitext(x)[0] for x in os.listdir(HERE)
               if x.endswith('.py') and x.startswith('test_')]
suite = unittest.TestSuite()
for tm in testmodules:
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(tm))
result = unittest.TextTestRunner(verbosity=VERBOSITY).run(suite)
success = result.wasSuccessful()
sys.exit(0 if success else 1)

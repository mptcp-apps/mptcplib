import sys

if sys.version_info >= (3, 0):
    import unittest
else:
    import unittest2 as unittest # requires "pip install unittest2"
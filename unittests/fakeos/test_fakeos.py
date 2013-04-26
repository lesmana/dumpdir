
import unittest

import fakeos

class TestFakeOs(unittest.TestCase):

  def test_getcwd(self):
    fakeosmod = fakeos.fakeos(None, 'cwd')
    cwd = fakeosmod.getcwd()
    self.assertEqual(cwd, 'cwd')

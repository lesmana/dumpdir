
import unittest

from reversedumpdir import ReverseDumpDir

class TestReverseDumpDir(unittest.TestCase):

  def test_onedir(self):
    report = []
    class FakeOsMod(object):
      def mkdir(self, name):
        report.append(('mkdir', name))
    revdd = ReverseDumpDir(FakeOsMod(), None)
    revdd.reversedumpdir(['d somedir'])
    self.assertEqual(report, [
          ('mkdir', 'somedir')])

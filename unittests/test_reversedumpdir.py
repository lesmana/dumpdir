
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

  def test_onefile(self):
    report = []
    class FakeFile(object):
      def __init__(self, name):
        self.name = name
      def close(self):
        report.append(('close', self.name))
    class FakeOpen(object):
      def __call__(self, name, mode):
        report.append(('open', name, mode))
        return FakeFile(name)
    revdd = ReverseDumpDir(None, FakeOpen())
    revdd.reversedumpdir(['f somefile'])
    self.assertEqual(report, [
          ('open', 'somefile', 'w'),
          ('close', 'somefile')])

  def test_onefile2(self):
    report = []
    class FakeFile(object):
      def __init__(self, name):
        self.name = name
      def write(self, text):
        report.append(('write', self.name, text))
      def close(self):
        report.append(('close', self.name))
    class FakeOpen(object):
      def __call__(self, name, mode):
        report.append(('open', name, mode))
        return FakeFile(name)
    revdd = ReverseDumpDir(None, FakeOpen())
    revdd.reversedumpdir([
          'f somefile',
          '> line 1',
          '> line 2'])
    self.assertEqual(report, [
          ('open', 'somefile', 'w'),
          ('close', 'somefile'),
          ('open', 'somefile', 'a'),
          ('write', 'somefile', 'line 1\n'),
          ('close', 'somefile'),
          ('open', 'somefile', 'a'),
          ('write', 'somefile', 'line 2\n'),
          ('close', 'somefile')])

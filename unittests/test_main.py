
import unittest

from reversedumpdir import Main

class TestMainRunExcept(unittest.TestCase):

  def test_good(self):
    report = []
    class PartFakeMain(Main):
      def filenamefromargv(self, argv):
        report.append(('filenamefromargv', argv))
        return 'inputfilename'
      def parsefileandcreatedirs(self, inputfilename):
        report.append(('parsefileandcreatedirs', inputfilename))
    main = PartFakeMain()
    main.runexcept('argv')
    self.assertEqual(report, [
          ('filenamefromargv', 'argv'),
          ('parsefileandcreatedirs', 'inputfilename')])

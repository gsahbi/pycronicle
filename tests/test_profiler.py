import time
import io
import unittest
import unittest.mock

from pycronicle import cprofile, cprogress, cprofile_named


@cprofile
def long_call(n):
    time.sleep(n)


@cprofile_named()
def long_call_2(n):
    time.sleep(n)


class TestProfiler(unittest.TestCase):
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, n, expected_output, mock_stdout):
        long_call(n)
        self.assertRegex(mock_stdout.getvalue().strip(), expected_output)

    def test_cprofile(self):
        self.assert_stdout(2, r'{"perf": {"scale": 1000, "long_call": \d+}}')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout2(self, n, expected_output, mock_stdout):
        cprogress(n)
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    def test_progress(self):
        self.assert_stdout2(2, '{"progress": 2}')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout4(self, n, expected_output, mock_stdout):
        long_call_2(n)
        self.assertRegex(mock_stdout.getvalue().strip(), expected_output)

    def test_cprofile_named(self):
        self.assert_stdout4(2, r'{"perf": {"scale": 1000, "long_call_2": \d+}}')


if __name__ == '__main__':
    unittest.main()

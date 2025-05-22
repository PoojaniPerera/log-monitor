import unittest
from log_monitor import parse_logs

class TestLogParserUnit(unittest.TestCase):

    def test_warning_duration(self):
        logs = [
            ["08:00:00", "Job A", "START", "1"],
            ["08:06:00", "Job A", "END", "1"]
        ]
        actual_result = parse_logs(logs)
        expected_result = 'WARNING :'
        
        self.assertIn(expected_result, actual_result[0])

    def test_error_duration(self):
        logs = [
            ["08:00:00", "Job B", "START", "2"],
            ["08:15:01", "Job B", "END", "2"]
        ]
        
        actual_result = parse_logs(logs)
        expected_result = 'ERROR :'
        
        self.assertIn(expected_result, actual_result[0])

    def test_no_output_for_short_job(self):
        logs = [
            ["08:00:00", "Job C", "START", "3"],
            ["08:03:00", "Job C", "END", "3"]
        ]
        expected_result = parse_logs(logs)
        self.assertEqual(len(expected_result), 0)

if __name__ == "__main__":
    unittest.main()

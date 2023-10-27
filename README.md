import unittest
from datetime import datetime, timedelta


class TestBotFunctions(unittest.TestCase):
    def test_time_until_new_year(self):
        def time_until_new_year():
            now = datetime.now()
            new_year = datetime(now.year + 1, 1, 1, 0, 0, 0)
            time_left = new_year - now
            return time_left

        # Call the function
        result = time_until_new_year()

        # Assert that the result is a timedelta instance
        self.assertIsInstance(result, timedelta)

        # Assert that it's not a past date
        self.assertGreater(result.total_seconds(), 0)



if __name__ == '__main__':
    unittest.main()


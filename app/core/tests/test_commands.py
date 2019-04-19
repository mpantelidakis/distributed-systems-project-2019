# patch will allow us to mock the behavior of django get_db command
from unittest.mock import patch

# call_command allows us to call the command in the source code
from django.core.management import call_command
# operationalError is thrown when db is unavailable
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # mock the behavior of the __getitem__ using the patch func
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # gi.return_value and gi.call_count are options we can set
            # for the mock object
            gi.return_value = True
            call_command('wait_for_db')
            # check that gi was only called once
            self.assertEqual(gi.call_count, 1)

    # use patch as a decorator.It passes the output as
    # an argument to our function, hence the ts arg below
    # we use this to override the waiting durations of
    # our actual wait_for_db command so that test
    # is executed faster
    # replaces the behavior of time.sleep with a mock
    # function that returns true
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # forces gi to raise OperationalError 5 times
            # and on the sixth time it passes
            # side_effect is an option for mock objects
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)

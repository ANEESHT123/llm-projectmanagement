# tests/test_scheduler.py

import unittest
from unittest.mock import MagicMock
from agents.scheduling_agent import SchedulingAgent
from agents.tasks import ScheduleMeetingTask

class TestSchedulingAgent(unittest.TestCase):

    def setUp(self):
        # Create a mock google service for testing
        self.mock_google_service = MagicMock()
        self.agent = SchedulingAgent(self.mock_google_service)

    def test_check_availability(self):
        # Test that availability is being checked properly
        self.mock_google_service.events().list().execute.return_value = {
            'items': [{'start': {'dateTime': '2025-02-07T10:00:00Z'}}]
        }
        available = self.agent.check_availability()
        self.assertIn('2025-02-07T10:00:00Z', available)

    def test_propose_meeting(self):
        # Test the meeting proposal
        self.mock_google_service.events().list().execute.return_value = {
            'items': [{'start': {'dateTime': '2025-02-07T10:00:00Z'}}]
        }
        result = self.agent.propose_meeting('2025-02-07T11:00:00Z')
        self.assertEqual(result, "Meeting scheduled for 2025-02-07T11:00:00Z")

if __name__ == '__main__':
    unittest.main()

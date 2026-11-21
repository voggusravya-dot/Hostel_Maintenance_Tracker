import unittest
import os
import json
import hostel_tracker


class TestHostelTracker(unittest.TestCase):

    def setUp(self):
        # Use a temporary test file
        hostel_tracker.DATA_FILE = "test_data.json"
        hostel_tracker.BACKUP_FILE = "test_data_backup.json"
        if os.path.exists("test_data.json"):
            os.remove("test_data.json")
        if os.path.exists("test_data_backup.json"):
            os.remove("test_data_backup.json")

    def tearDown(self):
        if os.path.exists("test_data.json"):
            os.remove("test_data.json")
        if os.path.exists("test_data_backup.json"):
            os.remove("test_data_backup.json")

    def test_load_save_records(self):
        sample_records = [{"id": 1, "room": "101", "status": "Pending"}]
        hostel_tracker.save_records(sample_records)
        loaded = hostel_tracker.load_records()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["room"], "101")

    def test_backup_creation(self):
        sample_records_1 = [{"id": 1, "room": "101", "status": "Pending"}]
        hostel_tracker.save_records(sample_records_1)
        sample_records_2 = [
            {"id": 1, "room": "101", "status": "Resolved"},
            {"id": 2, "room": "102", "status": "Pending"},
        ]
        hostel_tracker.save_records(sample_records_2)
        self.assertTrue(os.path.exists("test_data_backup.json"))


if __name__ == "__main__":
    unittest.main()

import unittest
import os
from chimes._config import Config
import pandas as pd


class TestConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_file_path = os.path.join(os.path.dirname(__file__), "config.yml")
        cls.config_backup_path = cls.config_file_path + ".backup"
        if os.path.exists(cls.config_file_path):
            os.rename(cls.config_file_path, cls.config_backup_path)

    @classmethod
    def tearDownClass(cls):
        # Restore the original config file
        if os.path.exists(cls.config_backup_path):
            os.rename(cls.config_backup_path, cls.config_file_path)
        else:
            # If the backup doesn't exist, remove any created config file
            if os.path.exists(cls.config_file_path):
                os.remove(cls.config_file_path)

    def setUp(self):
        self.config = Config()

    def tearDown(self):
        if os.path.exists(self.config_file_path):
            os.remove(self.config_file_path)

    def test_get_config(self):
        config_data = self.config.get()
        self.assertIsInstance(config_data, pd.DataFrame)

    def test_set_value(self):
        # Test setting a new configuration value
        test_key = "_VERB"
        new_value = False
        self.config.set_value(test_key, new_value)
        updated_value = self.config.get_current(test_key)
        self.assertEqual(updated_value, new_value)

    def test_reset_config(self):
        # Test resetting the configuration to default values
        test_key = "_VERB"
        original_default = self.config._default_config_data[test_key]['default']
        new_value = not original_default
        self.config.set_value(test_key, new_value)
        self.config.reset()
        reset_value = self.config.get_current(test_key)
        self.assertEqual(reset_value, original_default)  # Check if reset to original default


if __name__ == "__main__":
    unittest.main()

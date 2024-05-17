import unittest
from version_compare.compare import compare_versions

class TestCompareVersions(unittest.TestCase):
    def test_compare_versions(self):
        test_cases = [
            ("1.2", "1.1", 1),
            ("1.0", "1.0", 0),
            ("2.3", "2.3.4", -1),
            ("3.0.0", "3", 0),
            ("1.0.1", "1.0.0", 1),
            ("2.0.1", "2.1", -1),
            ("4.5", "4.5.1", -1),
            ("1.2.0", "1.2", 0),
            ("1.2", "1.2.0", 0),
        ]
        
        for version1, version2, expected in test_cases:
            with self.subTest(version1=version1, version2=version2, expected=expected):
                result = compare_versions(version1, version2)
                self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()

import unittest
from bin_wise.separate import separate

class TestSeparateFunction(unittest.TestCase):
    def test_separate(self):
        text = "東京都渋谷区でペットボトルを捨てたいです。大阪市でも同じように捨てたいです。"
        expected_result = {
            "target": "ペットボトル",
            "municipalities": ["東京都渋谷区", "大阪市"]
        }
        result = separate(text)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
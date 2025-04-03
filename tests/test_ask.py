import unittest
from unittest.mock import patch
from bin_wise.ask import ask

class TestAsk(unittest.TestCase):
    # @patch('bin_wise.ask.separate.separate')
    # @patch('bin_wise.ask.material_checker.get_material_info')
    # @patch('bin_wise.ask.VectorStore')
    def test_正常(self):
        # # モックの戻り値を設定
        # mock_separate.return_value = ("ペットボトル", ["東京都渋谷区", "大阪市"])
        # mock_get_material_info.return_value = "プラスチック"
        # mock_search_item.search_item.return_value = {"result": "success"}

        # # テスト対象の関数を呼び出し
        # text = "東京都渋谷区でペットボトルを捨てたいです。大阪市でも同じように捨てたいです。"
        # result = ask(text)

        # # 結果の検証
        # self.assertEqual(result, {"result": "success"})
        # mock_separate.assert_called_once_with(text)
        # mock_get_material_info.assert_called_once_with("ペットボトル")
        # mock_search_item.search_item.assert_called_once_with(["東京都渋谷区", "大阪市"], "プラスチック")
        self.assertEqual(ask(""), "燃えるごみです。")

import pytest
from unittest.mock import patch
from unittest.mock import call
from bin_wise.material_checker import get_material_info, fetch_material_info

@patch('bin_wise.material_checker.fetch_material_info')
@patch('bin_wise.material_checker.llm_chain')
def test_get_material_info(mock_llm_chain, mock_fetch):
    # モックの設定
    mock_fetch.return_value = "Plastic, Metal"
    mock_llm_chain.invoke.return_value = '{"material": "Plastic", "recyclable": true}'

    product_name = "Sample Product"
    expected_result = {
        "material": "Plastic",
        "recyclable": True
    }

    result = get_material_info(product_name)
    assert result == expected_result

    assert mock_fetch.call_args_list == [call(product_name)]

    # fetch_material_infoが正しく呼び出されたかを確認
    mock_fetch.assert_called_once_with(product_name)
    # llm_chain.invokeが正しく呼び出されたかを確認
    mock_llm_chain.invoke.assert_called_once_with({"product_name": product_name, "material_info": "Plastic, Metal"})

@patch('bin_wise.material_checker.fetch_material_info')
def test_get_material_info_no_material_info(mock_fetch):
    # モックの設定
    mock_fetch.return_value = None

    product_name = "Unknown Product"
    expected_result = "素材情報が見つかりませんでした。"

    result = get_material_info(product_name)
    assert result == expected_result

    # fetch_material_infoが正しく呼び出されたかを確認
    mock_fetch.assert_called_once_with(product_name + " material")

@patch('bin_wise.material_checker.GoogleSearchAPIWrapper')
def test_fetch_material_info(mock_search_api):
    # モックの設定
    mock_search_api.return_value.run.return_value = "Plastic, Metal"

    product_name = "羽毛布団"
    expected_result = "Plastic, Metal"

    result = fetch_material_info(product_name)
    assert "綿" in result 

    # GoogleSearchAPIWrapperのrunメソッドが正しく呼び出されたかを確認
    # mock_search_api.return_value.run.assert_called_once_with(product_name + " material")


if __name__ == '__main__':
    pytest.main()
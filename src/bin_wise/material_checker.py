import openai
from langchain_google_community.search import GoogleSearchAPIWrapper
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

search = GoogleSearchAPIWrapper()

# プロンプトテンプレートを定義
prompt_template_str = """
以下の商品についての素材情報を提供してください。
商品名: {product_name}
素材情報: {material_info}

結果を簡潔にまとめてください。
"""


# LLMChainを作成
llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0)

# プロンプトテンプレートの作成
prompt = ChatPromptTemplate.from_messages([
    ("system", prompt_template_str),
])

llm_chain = prompt | llm

def fetch_material_info(product_name):
    search_chain = SimpleWebSearchChain()
    search_results = search.run(product_name + " material")
    return search_results

def get_material_info(product_name):
    material_info = fetch_material_info(product_name)
    if not material_info:
        return "素材情報が見つかりませんでした。"

    response = llm_chain.run({"product_name": product_name, "material_info": material_info})
    result = json.loads(response)
    return result

# テスト用のコード
if __name__ == "__main__":
    product_name = "ペットボトル"
    result = get_material_info(product_name)
    print(result)
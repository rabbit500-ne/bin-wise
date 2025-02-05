import openai
from langchain_google_community.search import GoogleSearchAPIWrapper
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from bin_wise.core.llm_utils import parse
from langchain_google_community.search import GoogleSearchAPIWrapper
from googleapiclient.discovery import build
import os

from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
search = GoogleSearchAPIWrapper()

# プロンプトテンプレートを定義
prompt_template_str = """
以下の商品についての素材情報を提供してください。
商品名: {product_name}
素材情報(検索結果): {material_info}

結果を簡潔にまとめてください。
"""


# LLMChainを作成
llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0)

# プロンプトテンプレートの作成
prompt = PromptTemplate(
    input_variables=["product_name", "material_info"],
    template=prompt_template_str
)
llm_chain = prompt | llm | parse

def fetch_material_info(product_name):
    service = build("customsearch", "v1", developerKey=os.getenv("GOOGLE_API_KEY"))
    ret = service.cse().list(
                q=product_name + " の素材",
                #q="abc",
                cx=f'{os.getenv("GOOGLE_CSE_ID")}',
                lr='lang_ja',
                num=10,
                start=1,
            ).execute()
    return ' '.join([c['snippet'] for c in ret['items']])

def get_material_info(product_name):
    material_info = fetch_material_info(product_name)
    if not material_info:
        return "素材情報が見つかりませんでした。"
    response = llm_chain.invoke({"product_name": product_name, "material_info": material_info})
    result = json.loads(response)
    return result

# テスト用のコード
if __name__ == "__main__":
    product_name = "ペットボトル"
    result = get_material_info(product_name)
    print(result)

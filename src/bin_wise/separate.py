import openai
import json
import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# .env ファイルをロード
load_dotenv()

# プロンプトテンプレートを定義
prompt_template = PromptTemplate(
    input_variables=["text"],
    template="""
    以下の文章からゴミ捨て対象と都道府県自治体名を抽出してください。
    文章: {text}

    結果をJSON形式で返してください。
    例:
    {{
        "target": "ペットボトル",
        "municipalities": ["東京都渋谷区", "大阪市"]
    }}
    """
)

# LLMモデルを設定（gpt-4-turboを使用）
llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0)

# LLMChainを作成
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt_template
)

def separate(text):
    response = llm_chain.run(text)
    result = json.loads(response)  # LLMの出力をJSONに変換
    return result

if __name__ == "__main__":
    text = "東京都渋谷区でペットボトルを捨てたいです。大阪市でも同じように捨てたいです。"
    result = separate(text)
    print(result)

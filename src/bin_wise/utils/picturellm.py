from langchain.schema import SystemMessage, HumanMessage
from langchain.schema.messages import AIMessage
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

import base64
from dotenv import load_dotenv
load_dotenv()
import os


def image_to_base64(image_path):
    """画像ファイルをBase64エンコードする"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
class PictureLLM:
    def __init__(self):
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=12522,
            top_p=1,
        )
        # システムメッセージ
        SYSTEM_MESSAGE = SystemMessage(
            content="""
            ６つの画像から文字を抽出してください。
            
            以下の6枚の画像は1つの縦長画像を6分割したものです。
            画像の配置は次のようになっています：
            1 | 2
            3 | 4
            5 | 6
            
            各画像の境界には一部重複があるため、重複部分を考慮しながらOCR結果を統合してください。
            また、日本語を正しく認識するように jpn 言語モデルを使用し、句読点や改行をできるだけ正確に保持してください。
            
            出力するテキストは、
            * 画像の順序を保ちつつ、
            * 重複部分を自動で削除し、
            * 文章の流れが自然になるように統合してください。
            """
        )

        prompt_template = ChatPromptTemplate.from_messages(
            messages=[
                SYSTEM_MESSAGE,
                MessagesPlaceholder(variable_name="square_images"),
            ]
        )

        # square_images = HumanMessagePromptTemplate.from_template(
        #     [{'image_url': {'path': '{image_path}', 'detail': '{detail_parameter}'}} for image_path in square_images]
        # )

        self.cahin = prompt_template | llm | StrOutputParser()

    def invoke(self, square_image_paths):
        square_images = HumanMessagePromptTemplate.from_template(
            [{'image_url': {'path': image_path}} for image_path in square_image_paths]
        )
        return self.chain.invoke(square_images)

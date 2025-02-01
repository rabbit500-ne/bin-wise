import os
from langchain.embeddings import OpenAIEmbeddings

# ここでは環境変数として OpenAI の APIキーを設定します。
# 直接スクリプト内にキーを埋め込みたくない場合は、ターミナル/コマンドライン等から
# export OPENAI_API_KEY="sk-xxxxxxx..." のように設定しておきましょう。
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

def get_text_embedding(text: str):
    """
    テキストをOpenAI Embeddingsを用いてベクトル化する関数
    """
    # LangChainのOpenAIEmbeddingsをインスタンス化
    embedding_model = OpenAIEmbeddings(
        # モデルの指定（任意のEmbeddingsモデルが利用可能）
        model="text-embedding-ada-002",  
        openai_api_key=os.environ["OPENAI_API_KEY"]
    )
    # テキストを埋め込みベクトルに変換（単一テキストの場合は embed_query を利用する）
    vector = embedding_model.embed_query(text)
    return vector

if __name__ == "__main__":
    sample_text = "これはベクトル化したい文章のサンプルです。"
    embedding_vector = get_text_embedding(sample_text)
    print("ベクトルの次元数:", len(embedding_vector))
    print("ベクトルの中身の一部:", embedding_vector[:10], "...")

import os
from langchain_community.embeddings import OpenAIEmbeddings
#pydantic BaseModel
from pydantic import BaseModel

class EmbeddingModel(BaseModel):
    provider: str
    model: str
    # ベクトルの次元数
    vector_dim: int

EMBEDD = EmbeddingModel(
    provider="openai", 
    model="text-embedding-ada-002", 
    vector_dim=256) 

def get_text_embedding(text: str):
    """
    テキストをOpenAI Embeddingsを用いてベクトル化する関数
    """
    # LangChainのOpenAIEmbeddingsをインスタンス化
    embedding_model = OpenAIEmbeddings(
        # モデルの指定（任意のEmbeddingsモデルが利用可能）
        model=EMBEDD.model,  
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

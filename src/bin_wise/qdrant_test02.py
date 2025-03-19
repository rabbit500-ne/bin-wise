import os
from dotenv import load_dotenv
load_dotenv()
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
#print(os.environ.get("QDRANT_URL"))
#print(os.environ.get("QDRANT_API_KEY"))
#client = QdrantClient(
#    url=os.environ.get("QDRANT_URL"),
#    api_key=os.environ.get("QDRANT_API_KEY"),
#)

client = QdrantClient(
    url="https://bd341c52-9a03-4a70-8154-cfe841f66e10.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwiZXhwIjoxNzQ2ODM5NDgxfQ.QNOP-05nlBLd7LrhxElRnX5nhetVhAxjTQbMFmj_bbA",
)

if not client.collection_exists("my_collection"):
   client.create_collection(
      collection_name="my_collection",
      vectors_config=VectorParams(size=100, distance=Distance.COSINE),
   )

if not client.collection_exists("test_collection"):
    client.create_collection(
            collection_name="test_collection",
            vectors_config=VectorParams(size=4, distance=Distance.DOT),
    )

from qdrant_client.http.models import PointStruct
# UUIDを作る
import uuid
id = uuid.uuid4()
breakpoint()
operation_info = client.upsert(
    collection_name="test_collection",
    wait=True,
    points=[
        PointStruct(id=uuid.uuid4().hex, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
        PointStruct(id=uuid.uuid4().hex, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": "London"}),
        PointStruct(id=uuid.uuid4().hex, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": "Moscow"}),
        PointStruct(id=uuid.uuid4().hex, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": "New York"}),
        PointStruct(id=uuid.uuid4().hex, vector=[0.24, 0.18, 0.22, 0.44], payload={"city": "Beijing"}),
        PointStruct(id=uuid.uuid4().hex, vector=[0.35, 0.08, 0.11, 0.44], payload={"city": "Mumbai"}),
    ]
)
print(operation_info)
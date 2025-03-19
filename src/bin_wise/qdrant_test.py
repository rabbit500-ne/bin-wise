import os
from dotenv import load_dotenv
load_dotenv()
from qdrant_client import QdrantClient
#print(os.environ.get("QDRANT_URL"))
#print(os.environ.get("QDRANT_API_KEY"))
client = QdrantClient(
    url=os.environ.get("QDRANT_URL"),
    api_key=os.environ.get("QDRANT_API_KEY"),
)
from qdrant_client import QdrantClient

#qdrant_client = QdrantClient(
#    url="https://bd341c52-9a03-4a70-8154-cfe841f66e10.europe-west3-0.gcp.cloud.qdrant.io:6333", 
#    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwiZXhwIjoxNzQ2ODM5NDgxfQ.QNOP-05nlBLd7LrhxElRnX5nhetVhAxjTQbMFmj_bbA",
#)

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(
    url="https://bd341c52-9a03-4a70-8154-cfe841f66e10.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOlt7ImNvbGxlY3Rpb24iOiJzdGFyX2NoYXJ0cyIsImFjY2VzcyI6InJ3In1dLCJleHAiOjE3NDY4Mzk4NjN9.0-A-grgfhUxCiituq9O1_S3gcHibt16ue9HS_ZQtGM0",
    grpc_port=6334,
)

print(client.collection_exists("star_charts"))

#if not client.collection_exists("my_collection"):
#   client.create_collection(
#      collection_name="my_collection",
#      vectors_config=VectorParams(size=100, distance=Distance.COSINE),
#   )
import numpy as np
from qdrant_client.models import PointStruct

#vectors = np.random.rand(100, 100)
#client.upsert(
#   collection_name="my_collection",
#   points=[
#      PointStruct(
#            id=idx,
#            vector=vector.tolist(),
#            payload={"color": "red", "rand_number": idx % 10}
#      )
#      for idx, vector in enumerate(vectors)
#   ]
#)

"""
search
{
  "vector": [0.2, 0.1, 0.9, 0.7],
  "limit": 3,
  "with_payload": true
}
"""
hits = client.search(
   collection_name="star_charts",
   query_vector=[0.2, 0.1, 0.9, 0.7],
   limit=3,
   with_payload=True
)
#query_vector = np.random.rand(100)
#hits = client.search(
#   collection_name="my_collection",
#   query_vector=query_vector,
#   limit=5  # Return 5 closest points
#)
print(hits)
breakpoint()
#print(qdrant_client.get_collections())

COLLECTION_NAME = os.environ['COLLECTION_NAME']

def crate_collection():
    
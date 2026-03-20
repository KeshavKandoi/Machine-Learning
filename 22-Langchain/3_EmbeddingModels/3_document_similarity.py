# from langchain_openai import OpenAIEmbeddings
# from dotenv import load_dotenv
# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np

# load_dotenv()

# embedding=OpenAIEmbeddings(model='text-embedding-3-large',dimensions=300)

# documents = [
#     "Virat Kohli is one of the best batsmen in the world and former captain of India.",
#     "MS Dhoni is known for his calm leadership and is one of the greatest finishers in cricket.",
#     "Sachin Tendulkar is called the 'God of Cricket' and has scored 100 international centuries.",
#     "Rohit Sharma is famous for his elegant batting and holds the record for highest ODI score.",
#     "Jasprit Bumrah is a world-class fast bowler known for his unique bowling action and accuracy."
# ]

# query='tell me about virat kohli'


# doc_embeddings=embedding.embed_documents(documents)
# query_embedding=embedding.embed_query(query)

# scores=cosine_similarity([query_embedding],doc_embeddings)[0]

# index,score=sorted(list(enumerate(scores)),key=lambda x:x[1])[-1]


# print(query)
# print(documents[index])
# print("similarity score is ",score)

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

embedding = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

documents = [
    "Virat Kohli is one of the best batsmen in the world and former captain of India.",
    "MS Dhoni is known for his calm leadership and is one of the greatest finishers in cricket.",
    "Sachin Tendulkar is called the 'God of Cricket' and has scored 100 international centuries.",
    "Rohit Sharma is famous for his elegant batting and holds the record for highest ODI score.",
    "Jasprit Bumrah is a world-class fast bowler known for his unique bowling action and accuracy."
]

query = 'tell me about virat kohli'

doc_embeddings = embedding.embed_documents(documents)
query_embedding = embedding.embed_query(query)

scores = cosine_similarity([query_embedding], doc_embeddings)[0]

index, score = sorted(list(enumerate(scores)), key=lambda x: x[1])[-1]

print(query)
print(documents[index])
print("similarity score is ", score)
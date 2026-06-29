from sentence_transformers import CrossEncoder

model = CrossEncoder("BAAI/bge-reranker-v2-m3")

print(model.predict([("What is DeepTox?", "DeepTox is a toxicity prediction model.")]))

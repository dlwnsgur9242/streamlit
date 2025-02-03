from transformers import pipeline

# 텍스트 분류
classifier = pipeline("sentiment-analysis")
result = classifier("I love using Hugging Face!")
print(result)
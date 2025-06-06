from transformers import pipeline

sentiment_pipeline = pipeline(
    "sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment"
)


def analyze_sentiment(text):
    result = sentiment_pipeline(text)[0]
    return f"{result['label']} (score: {round(result['score'], 2)})"

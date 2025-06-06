from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_name = "your-hf-account/intent-bert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
label_map = ["greet", "order_status", "cancel", "complaint", "thanks"]


def predict_intent(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    pred = torch.argmax(logits, dim=-1).item()
    return label_map[pred]

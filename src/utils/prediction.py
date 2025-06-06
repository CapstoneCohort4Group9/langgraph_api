from transformers import AutoModelForSequenceClassification
import os
import joblib
from transformers import AutoTokenizer, pipeline
from peft import PeftModel, PeftConfig


class PredictionPipeline:
    def __init__(self, text):
        self.text = text

    def predict(self):
        # Load label encoder
        label_encoder = joblib.load("models/intent/labelEncoder/label_encoder.pkl")
        peft_config = PeftConfig.from_pretrained(
            os.path.join("models", "intent", "model.h5")
        )
        base_model = AutoModelForSequenceClassification.from_pretrained(
            os.path.join("models", "intent", "base_model.h5"),
            use_safetensors=True,
            trust_remote_code=True,
        )
        peft_model = PeftModel.from_pretrained(
            base_model, os.path.join("models", "intent", "model.h5")
        )
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            os.path.join("models", "intent", "tokenizer.h5")
        )

        # Use for inference
        clf = pipeline("text-classification", model=peft_model, tokenizer=tokenizer)
        result = clf(self.text)[0]
        print(result)
        label_num = int(result["label"].split("_")[-1])
        # Convert back to label
        predicted_label = label_encoder.inverse_transform([label_num])[0]
        return {"predicted_label": predicted_label, "confidence_score": result["score"]}

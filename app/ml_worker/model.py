import random

class MockSentimentModel:

    def __init__(self, model_name : str = "mock-model") -> None:

        self.model_name = model_name

    def predict(self, text : str) -> dict:

        return   {
            "sentiment": random.choice(["positive", "neutral", "negative"]),
            "confidence": round(random.uniform(0.5, 1.0), 2),
            "is_toxic": random.choice([True, False])
        }    

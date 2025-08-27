from typing import Dict, Any
from .base import BaseClassifier

class EmotionClassifier(BaseClassifier):
    """
    EmotionClassifier is a simple rule-based classifier for detecting emotions in text.

    Args:
        labels (List[str], optional): List of emotion labels to classify. Defaults to ["felice", "triste", "arrabbiato"].

    Methods:
        predict(text: str) -> Dict[str, Any]:
            Predicts the emotion expressed in the input text.
            Returns a dictionary containing:
                - 'label': the predicted emotion label.
                - 'scores': a dictionary mapping each label to its confidence score.
                - 'text': the original input text.

    Notes:
        The classifier uses keyword matching to assign scores to each emotion label.
        If no keywords are found, it assigns default scores to all labels.
    """
    def __init__(self, labels=None):
        self.labels = labels or ["felice","triste","arrabbiato"]

    def predict(self, text: str) -> Dict[str, Any]:
        t = text.lower()
        scores = {l: 0.0 for l in self.labels}
        if any(k in t for k in ["felice","content","gioia",":)", "😀", ":d"]):
            scores["felice"] += 0.9
        if any(k in t for k in ["triste","piango","malincon","😢"]):
            scores["triste"] += 0.9
        if any(k in t for k in ["arrabbi","furios","grrr","😡"]):
            scores["arrabbiato"] += 0.9
        if all(v == 0.0 for v in scores.values()):
            scores[self.labels[0]] = 0.34
            scores[self.labels[1 % len(self.labels)]] = 0.33
            scores[self.labels[2 % len(self.labels)]] = 0.33
        label = max(scores, key=scores.get)
        return {"label": label, "scores": scores, "text": text}

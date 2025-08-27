from typing import Dict, Any
from .base import BaseClassifier

class TicketClassifier(BaseClassifier):
    """
    TicketClassifier is a simple keyword-based classifier for ticket texts.

    Attributes:
        labels (List[str]): List of possible ticket categories. Defaults to ["vendite", "supporto", "generico"].

    Methods:
        __init__(labels=None):
            Initializes the classifier with the given labels.

        predict(text: str) -> Dict[str, Any]:
            Predicts the category of the given ticket text based on keyword matching.
            Returns a dictionary containing:
                - label: The predicted category label.
                - scores: A dictionary with scores for each label.
                - text: The original input text.
    """
    def __init__(self, labels=None):
        self.labels = labels or ["vendite","supporto","generico"]

    def predict(self, text: str) -> Dict[str, Any]:
        t = text.lower()
        scores = {l: 0.1 for l in self.labels}
        if any(k in t for k in ["preventivo","offerta","sconto","acquisto","comprare","prezzo"]): #semplice keywork marching
            scores["vendite"] += 0.7
        if any(k in t for k in ["errore","bug","assistenza","aiuto","rimborso","reso","ticket"]):
            scores["supporto"] += 0.7
        if len(t.split()) < 5:
            scores["generico"] += 0.3
        label = max(scores, key=scores.get)
        return {"label": label, "scores": scores, "text": text}

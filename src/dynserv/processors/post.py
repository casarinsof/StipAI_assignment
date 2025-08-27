from typing import Dict, Any
from heapq import nlargest

class TopK:
    """
    TopK is a callable class that extracts the top-k scoring items from a prediction dictionary.

    Args:
        k (int, optional): The number of top items to select. Defaults to 3.

    Methods:
        __call__(pred: Dict[str, Any]) -> Dict[str, Any]:
            Processes the input prediction dictionary, retrieves the 'scores' mapping,
            selects the top-k items based on their scores, and adds a 'topk' key to the dictionary
            containing a list of the top-k label-score pairs.

    Returns:
        Dict[str, Any]: The updated prediction dictionary with the 'topk' field added.
    """
    def __init__(self, k: int = 3):
        self.k = k

    def __call__(self, pred: Dict[str, Any]) -> Dict[str, Any]:
        scores = pred.get("scores", {})
        top = nlargest(self.k, scores.items(), key=lambda x: x[1])
        pred["topk"] = [{"label": l, "score": float(s)} for l, s in top]
        return pred

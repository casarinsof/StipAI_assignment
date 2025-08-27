from typing import Dict, Any, List

class BaseClassifier:
    labels: List[str]

    def predict(self, text: str) -> Dict[str, Any]:
        raise NotImplementedError

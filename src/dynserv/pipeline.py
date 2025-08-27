from typing import Dict, Any
from functools import lru_cache
import yaml, os
from .config import ClientConfig
from .loader import import_from_path

CONFIG_DIR = os.environ.get("DYNCONF_DIR", os.path.join(os.getcwd(), "configs", "clients"))

class Pipeline:
    """
    Pipeline for text inference with configurable preprocessing, model, postprocessing, and rule-based actions.

    Args:
        cfg (ClientConfig): Configuration object containing preprocessing, postprocessing, model, rules, and metadata.

    Attributes:
        cfg (ClientConfig): The configuration object.
        pre (List[Callable]): List of preprocessing functions.
        post (List[Callable]): List of postprocessing functions.
        model (Any): The instantiated model object.
        rules (List[Any]): List of rule objects.

    Methods:
        run(text: str) -> Dict[str, Any]:
            Executes the pipeline on the input text, applying preprocessing, model prediction, postprocessing, and rules.
            Adds model version and client ID to the output.

        apply_rules(pred: Dict[str, Any], text: str, original_text: str) -> Dict[str, Any]:
            Applies configured rules to the prediction, potentially modifying it based on rule evaluation and actions.
    """
    def __init__(self, cfg: ClientConfig):
        self.cfg = cfg
        self.pre = [import_from_path(c.class_path)(**c.params) for c in cfg.preprocessing]
        self.post = [import_from_path(c.class_path)(**c.params) for c in cfg.postprocessing]
        ModelClass = import_from_path(cfg.model["class_path"])
        self.model = ModelClass(**cfg.model.get("params", {}))
        self.rules = [r for r in cfg.rules]

    def run(self, text: str) -> Dict[str, Any]:
        original_text = text
        for p in self.pre:
            text = p(text)
        raw_pred = self.model.predict(text)
        pred = raw_pred
        for p in self.post:
            pred = p(pred)
        pred = self.apply_rules(pred, text, original_text)
        pred["model_version"] = self.cfg.model_version
        pred["client_id"] = self.cfg.client_id
        return pred

    def apply_rules(self, pred: Dict[str, Any], text: str, original_text: str) -> Dict[str, Any]:
        from .rules.builtin import evaluate_rule, apply_actions
        for rule in self.rules:
            if evaluate_rule(rule.model_dump() if hasattr(rule, "model_dump") else rule, pred, text=text, original_text=original_text):
                pred = apply_actions(rule.model_dump() if hasattr(rule, "model_dump") else rule, pred)
        return pred

@lru_cache(maxsize=64)
def load_client_config(client_id: str) -> ClientConfig:
    path = os.path.join(CONFIG_DIR, f"{client_id}.yml")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config for client '{client_id}' not found at {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return ClientConfig(**data)

@lru_cache(maxsize=64)
def get_pipeline(client_id: str) -> Pipeline:
    cfg = load_client_config(client_id)
    return Pipeline(cfg)

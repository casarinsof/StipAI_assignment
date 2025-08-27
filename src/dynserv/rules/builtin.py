from typing import Dict, Any, List

def _pred_text_contains_any(ctx: Dict[str, Any], words: List[str], case_insensitive: bool=True):
    text = ctx.get("text","")
    if case_insensitive:
        text = text.lower()
        words = [w.lower() for w in words]
    return any(w in text for w in words)

def _pred_text_len_lt(ctx: Dict[str, Any], n: int):
    text = ctx.get("text","")
    return len(text.split()) < int(n)

def _pred_pred_is(ctx: Dict[str, Any], label: str):
    return ctx.get("pred_label") == label

PRED_HANDLERS = {
    "text_contains_any": _pred_text_contains_any,
    "text_len_lt": _pred_text_len_lt,
    "pred_is": _pred_pred_is,
}

def evaluate_rule(rule: Dict[str, Any], pred: Dict[str, Any], **kwargs) -> bool:
    text = kwargs.get("original_text") or kwargs.get("text","")
    ctx = {"text": text, "pred_label": pred.get("label")}
    results = []
    for cond in rule.get("when", []):
        cond = dict(cond)
        typ = cond.pop("type")
        handler = PRED_HANDLERS.get(typ)
        if not handler:
            results.append(False)
            continue
        results.append(handler(ctx, **cond))
    return all(results)

def _action_set_pred(pred: Dict[str, Any], label: str):
    pred["label"] = label
    if "scores" in pred and label in pred["scores"]:
        pred["scores"][label] = max(pred["scores"].values()) + 0.01
    return pred

ACTION_HANDLERS = {
    "set_pred": _action_set_pred,
}

def apply_actions(rule: Dict[str, Any], pred: Dict[str, Any]) -> Dict[str, Any]:
    for act in rule.get("then", []):
        act = dict(act)
        typ = act.pop("type")
        handler = ACTION_HANDLERS.get(typ)
        if handler:
            pred = handler(pred, **act)
    return pred

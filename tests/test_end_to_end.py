from dynserv.pipeline import get_pipeline

def test_client_a_emotion_happy():
    pipe = get_pipeline("client_a")
    res = pipe.run("   Oggi sono molto felice :D   ")
    assert res["label"] == "felice"
    assert res["client_id"] == "client_a"
    assert res["model_version"] == "1.0.0"

def test_client_b_rule_refund():
    pipe = get_pipeline("client_b")
    res = pipe.run("Vorrei informazioni prezzo ma chiedo rimborso per ordine #123")
    assert res["label"] == "supporto"
    assert res["client_id"] == "client_b"
    assert res["model_version"] == "2.1.0"

def test_client_b_rule_greeting_short():
    pipe = get_pipeline("client_b")
    res = pipe.run("ciao, grazie")
    assert res["label"] == "supporto"

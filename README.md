# Dynamic Inference Service

A configurable text-inference service built with FastAPI. For each request, the service loads the model, pre-processing steps, post-processing steps and business rules defined for the given `client_id` in a YAML file, so different clients get isolated pipelines without code changes.

## Features
- Per-client configuration in YAML (`configs/clients/<client_id>.yml`).
- Components (model, processors) are resolved dynamically from `module:Class` paths.
- Pipeline: pre-processing -> model prediction -> post-processing -> rules.
- Model versioning through the `model.version` field, returned in every response.
- In-process LRU cache of loaded configs and pipelines.
- The bundled models are keyword-based mocks, not real ML models; they are meant to be replaced.

## Repository structure
```
.
├── pyproject.toml            # package metadata and dependencies
├── configs/clients/          # one YAML file per client
├── src/dynserv/
│   ├── server.py             # FastAPI app, POST /infer
│   ├── pipeline.py           # Pipeline class, config and pipeline caching
│   ├── config.py             # pydantic config schemas
│   ├── loader.py             # "module:Class" dynamic import
│   ├── models/               # classifiers (emotion, ticket)
│   ├── processors/           # pre.py and post.py processing steps
│   └── rules/                # rule predicates and actions
└── tests/test_end_to_end.py
```

## Installation
Requires Python 3.9+.
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[test]"
```

## Usage
Run from the repository root (config directory defaults to `./configs/clients`, override with `DYNCONF_DIR`):
```bash
uvicorn dynserv.server:app --reload
```
```bash
curl -s -X POST http://127.0.0.1:8000/infer \
  -H "Content-Type: application/json" \
  -d '{"client_id":"client_a","text":"oggi sono molto felice :D"}'
```
An unknown `client_id` returns HTTP 404.

## Client configuration
Example (`configs/clients/client_b.yml`):
```yaml
client_id: client_b
model:
  class_path: dynserv.models.ticket:TicketClassifier
  version: "2.1.0"
  params: {}
preprocessing:
  - class_path: dynserv.processors.pre:Lowercase
postprocessing:
  - class_path: dynserv.processors.post:TopK
    params: {k: 3}
rules:
  - name: vendite_con_rimborso_diventa_supporto
    when:
      - {type: pred_is, label: vendite}
      - {type: text_contains_any, words: ["rimborso"]}
    then:
      - {type: set_pred, label: supporto}
```
Rule predicates: `pred_is`, `text_contains_any`, `text_len_lt`. Actions: `set_pred`. All predicates in `when` are combined with AND; OR is not supported.

## Tests
```bash
pytest -q
```
Tests must run from the repository root (they read `configs/clients`).

## Notes and limitations
- Models are mock keyword classifiers.
- No persistence layer.
- The cache is per process and lost on restart.
- Possible future work: transformer-based or external-API models.

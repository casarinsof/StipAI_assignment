# Dynamic Inference Service

Un servizio di inferenza **configurabile** che carica dinamicamente modelli, pre/post-processing e regole **per cliente** in base a `client_id`.

## Caratteristiche
- Caricamento dinamico di **modello**, **pre-processing**, **post-processing** e **regole** da file YAML.
- Supporto per **più clienti**, ciascuno con configurazione isolata.
- Pipeline: **pre → predizione → post → regole**.
- **Test** end-to-end di esempio.
- **Versioning** del modello (campo `model.version`).
- **Cache** LRU dei componenti caricati per velocizzare il runtime.

## TODO futuri:
- implementazione modelli, ad esempio utilizzando un transformer scaricando gia' il modello da Hungging Facce (accurato ma pesante)
- step intermedio: utilizzare anche un semplice classificatore
- utizzare direttamente delle API esterne (OpenAI, Azure ecc)

## Struttura
```
.
├── pyproject.toml
├── README.md
├── configs/
│   └── clients/
│       ├── client_a.yml
│       └── client_b.yml
├── src/
│   └── dynserv/
│       ├── __init__.py
│       ├── server.py
│       ├── loader.py
│       ├── pipeline.py
│       ├── config.py
│       ├── models/
│       │   ├── base.py
│       │   ├── emotion.py
│       │   └── ticket.py
│       ├── processors/
│       │   ├── pre.py
│       │   └── post.py
│       └── rules/
│           ├── base.py
│           └── builtin.py
└── tests/
    └── test_end_to_end.py
```

## Requisiti
- Python 3.9+

## Installazione (dev)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
pip install pytest
```

## Avvio del server
```bash
uvicorn src.dynserv.server:app --reload
```

## Esecuzione di esempio (HTTP)
```bash
curl -s -X POST "http://127.0.0.1:8000/infer" \
  -H "Content-Type: application/json" \
  -d '{"client_id":"client_a","text":"oggi sono molto felice :D"}'
# -> {"client_id":"client_a","model_version":"1.0.0","label":"felice", ...}

curl -s -X POST "http://127.0.0.1:8000/infer" \
  -H "Content-Type: application/json" \
  -d '{"client_id":"client_b","text":"richiesta di rimborso per ordine #123"}'
# -> regola: sales -> support
```

## Esecuzione test
```bash
pytest -q
```

## Configurazione per cliente
Esempio `configs/clients/client_b.yml`:
```yaml
client_id: client_b
model:
  class_path: dynserv.models.ticket:TicketClassifier
  version: "2.1.0"
  params: {}
preprocessing:
  - class_path: dynserv.processors.pre:Lowercase
  - class_path: dynserv.processors.pre:Strip
postprocessing:
  - class_path: dynserv.processors.post:TopK
    params: {k: 3}
rules:
  - name: vendite_con_rimborso_diventa_supporto
    when:
      - type: pred_is
        label: vendite
      - type: text_contains_any
        words: ["rimborso"]
    then:
      - type: set_pred
        label: supporto
  - name: breve_saluto_diventa_supporto
    when:
      - type: pred_is
        label: generico
      - type: text_len_lt
        n: 20
      - type: text_contains_any
        words: ["ciao","arrivederci"]
    then:
      - type: set_pred
        label: supporto
```

## Note e Assunzioni
- I modelli sono **mock** per semplicità (keyword-based): come detto sopra, i classificatori implementati non sono veri modelli di machine learning, ma versioni semplificate che si basano su semplici regole di matching di parole chiave, chiaramente da sostituire. 
- la persistenza dei dati non e' trattata: improvements possibili: PostreSQL, MongoDB
- Le regole sono **AND** fra i predicati nella lista `when`: significa che, perché una regola si attivi, tutti i predicati presenti devono essere veri contemporaneamente. Non è al momento supportata la logica OR o la combinazione di operatori più complessi, che potrebbero essere aggiunti in versioni evolute.
- La cache è in-process; Ciò implica che: la cache è valida solo per il singolo processo in esecuzione e si perde allo spegnimento del servizio. In produzione si può usare un object store (tipo S3) per garantire coerenza e scalabilita'.

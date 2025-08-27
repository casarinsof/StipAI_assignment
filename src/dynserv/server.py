from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from .pipeline import get_pipeline

app = FastAPI(title="Dynamic Inference Service")

class InferRequest(BaseModel):
    client_id: str
    text: str

@app.post("/infer")
def infer(req: InferRequest) -> Dict[str, Any]:
    """
        Handles inference requests by running the specified pipeline for a given client.

        Args:
            req (InferRequest): The inference request containing the client ID and input text.

        Returns:
            Dict[str, Any]: The result of the pipeline inference.

        Raises:
            HTTPException: If the pipeline for the specified client ID is not found (404).
    """
    try:
        pipe = get_pipeline(req.client_id)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    result = pipe.run(req.text)
    return result

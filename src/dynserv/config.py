from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

class ComponentConfig(BaseModel):
    class_path: str
    params: Dict[str, Any] = Field(default_factory=dict)

class RuleConfig(BaseModel):
    name: str
    when: List[Dict[str, Any]]
    then: List[Dict[str, Any]]

class ClientConfig(BaseModel):
    """
    Configuration for a client in the dynamic service.

    Attributes:
        client_id (str): Unique identifier for the client.
        model (Dict[str, Any]): Model configuration dictionary containing keys such as 'class_path', 'params', and 'version'.
        preprocessing (List[ComponentConfig]): List of preprocessing component configurations. Defaults to an empty list.
        postprocessing (List[ComponentConfig]): List of postprocessing component configurations. Defaults to an empty list.
        rules (List[RuleConfig]): List of rule configurations. Defaults to an empty list.

    Properties:
        model_version (str): Returns the version of the model as a string. Defaults to "0" if not specified.
    """
    client_id: str
    model: Dict[str, Any]  # {class_path, params, version}
    preprocessing: List[ComponentConfig] = Field(default_factory=list)
    postprocessing: List[ComponentConfig] = Field(default_factory=list)
    rules: List[RuleConfig] = Field(default_factory=list)

    @property
    def model_version(self) -> str:
        return str(self.model.get("version", "0"))

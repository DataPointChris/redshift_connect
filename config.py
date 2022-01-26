import json
from dataclasses import dataclass


@dataclass
class RedshiftConfig:
    config1: str
    config2: str
    config3: str


def read_config(config_file: str) -> RedshiftConfig:
    with open(config_file, 'r') as file:
        data = json.load(file)
        return RedshiftConfig(**data)

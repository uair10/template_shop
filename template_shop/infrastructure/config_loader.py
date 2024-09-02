import os
import tomllib
from typing import TypeVar

from pydantic import TypeAdapter

T = TypeVar("T")
DEFAULT_CONFIG_PATH = "./config/config.dev.toml"


def load_config(config_type: type[T], config_scope: str | None = None, path: str | None = None) -> T:
    if path is None:
        path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)

    with open(path, "rb") as f:
        data = tomllib.load(f)

    if config_scope is not None:
        data = data[config_scope]

    return TypeAdapter(type=config_type).validate_python(data)

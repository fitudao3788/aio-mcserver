import os.path

import click
import yaml
from pydantic import BaseModel, Field


class ServerConfig(BaseModel):
    version: str = ""
    path: str = "server"


class AppConfig(BaseModel):
    server: ServerConfig = Field(default_factory=ServerConfig)


class Config:
    @staticmethod
    def load_or_create(file_path: str) -> AppConfig:
        if not os.path.exists(file_path):
            click.echo("[*] Creating new configuration file...")

            config = AppConfig()
            with open(file_path, "w") as f:
                yaml.dump(config.model_dump(), f, sort_keys=False)

            return config

        with open(file_path, "r") as f:
            data = yaml.safe_load(f) or {}

        return AppConfig.model_validate(data)

    @staticmethod
    def save(config: AppConfig, file_path: str):
        with open(file_path, "w") as f:
            yaml.dump(config.model_dump(), f, sort_keys=False)

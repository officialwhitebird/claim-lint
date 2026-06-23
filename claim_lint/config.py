import os
import json

class ConfigError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code

def load_config(config_path=None):
    if config_path is None:
        config_path = os.path.join(os.getcwd(), ".claimlintrc.json")

    if not os.path.exists(config_path):
        raise ConfigError("config.missing", f"Config file not found: {config_path}")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ConfigError("config.invalid", f"Invalid JSON in config: {str(e)}")

    if not isinstance(data, dict):
        raise ConfigError("config.invalid", "Config root must be a JSON object")

    required_keys = {"prohibited_claims", "internal_names"}
    actual_keys = set(data.keys())

    if not required_keys.issubset(actual_keys) or len(actual_keys) > 2:
        raise ConfigError("config.invalid", "Config must contain exactly 'prohibited_claims' and 'internal_names'")

    for key in required_keys:
        val = data[key]
        if not isinstance(val, list):
            raise ConfigError("config.invalid", f"Key '{key}' must be an array of strings")
        for item in val:
            if not isinstance(item, str):
                raise ConfigError("config.invalid", f"All items in '{key}' must be strings")

    return data

import yaml


def read_config(path: str = "/src/config/config.yaml") -> dict:
    with open(path.strip("/"), "r") as f:
        config = yaml.safe_load(f)
    return config
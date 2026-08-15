import yaml

def load_config(path="config.yaml"):
    """Load YAML config file and return as dictionary."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


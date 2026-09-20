import yaml


def load(path):

    with open(path, "r", encoding="utf8") as f:

        return yaml.safe_load(f)


def save(path, data):

    with open(path, "w", encoding="utf8") as f:

        yaml.dump(data, f, sort_keys=False)

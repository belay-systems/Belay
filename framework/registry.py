import json

from pathlib import Path


class Registry:

    def __init__(self, file):

        self.file = Path(file)

        if not self.file.exists():

            self.file.write_text("{}")

    def load(self):

        return json.loads(self.file.read_text())

    def save(self, data):

        self.file.write_text(

            json.dumps(data, indent=4)

        )

from framework.registry import Registry


class Librarian:

    def __init__(self):

        self.registry = Registry(

            "memory/knowledge_registry.json"

        )

    def register(self, artifact):

        db = self.registry.load()

        db[artifact["id"]] = artifact

        self.registry.save(db)

    def lookup(self, identifier):

        db = self.registry.load()

        return db.get(identifier)

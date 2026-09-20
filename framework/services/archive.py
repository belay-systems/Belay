from framework.services.base import Service


class ArchiveManager(Service):

    name = "Archive"

    def run(self, belay):

        print("Archiving historical artifacts...")

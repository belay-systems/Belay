from framework.services.librarian import LibrarianService

from framework.services.archive import ArchiveManager


class KnowledgeDepartment(Department):

    name = "Knowledge"

    def run(self, belay):

        LibrarianService().run(belay)

        ArchiveManager().run(belay)

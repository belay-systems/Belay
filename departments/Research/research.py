from framework.departments.base import Department

from framework.services.universe import UniverseDiscovery

from framework.services.regime import RegimeDetection

from framework.services.scientist import ChiefScientist


class ResearchDepartment(Department):

    name = "Research"

    def run(self, belay):

        UniverseDiscovery().run(belay)

        RegimeDetection().run(belay)

        ChiefScientist().run(belay)

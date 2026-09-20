from framework.services.base import Service


class PortfolioManager(Service):

    name = "Portfolio"

    def run(self, belay):

        print("Updating paper portfolio...")

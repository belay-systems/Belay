from framework.services.portfolio import PortfolioManager

from framework.services.performance import PerformanceReview


class OperationsDepartment(Department):

    name = "Operations"

    def run(self, belay):

        PortfolioManager().run(belay)

        PerformanceReview().run(belay)

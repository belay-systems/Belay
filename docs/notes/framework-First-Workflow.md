market_open.py
from framework.workflows.base import Workflow

from framework.workflows.registry import register


class MarketOpen(Workflow):

    name = "market-open"

    trigger = "schedule"

    departments = [

        "Knowledge",

        "Research",

        "Operations",

        "Validation"

    ]

    def execute(self, belay):

        belay.load_memory()

        belay.run_department("Knowledge")

        belay.run_department("Research")

        belay.run_department("Operations")

        belay.run_department("Validation")

        belay.save()


register(MarketOpen())

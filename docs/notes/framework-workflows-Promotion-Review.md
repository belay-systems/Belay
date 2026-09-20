class PromotionReview(Workflow):

    name = "promotion-review"

    trigger = "event"

    departments = [

        "Validation",

        "Operations",

        "Knowledge"

    ]

    def execute(self, belay):

        belay.run_department("Validation")

        belay.run_department("Operations")

        belay.run_department("Knowledge")

        belay.save()

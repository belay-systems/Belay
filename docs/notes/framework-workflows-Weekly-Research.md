class WeeklyResearch(Workflow):

    name = "weekly-research"

    trigger = "schedule"

    departments = [

        "Knowledge",

        "Research"

    ]

    def execute(self, belay):

        belay.run_department(

            "Knowledge"

        )

        belay.run_department(

            "Research"

        )

        belay.save()

from framework.logging import info


class BelayEngine:

    def __init__(self):

        info("Belay initialized.")

    def run(self, workflow):

        info(f"Running {workflow.name}")

        workflow.execute()

        info("Workflow complete.")

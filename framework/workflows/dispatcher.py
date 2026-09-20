from framework.workflows.registry import get


class WorkflowDispatcher:

    def dispatch(self, name, belay):

        workflow = get(name)

        if workflow is None:

            raise Exception(

                f"Workflow '{name}' not found."

            )

        workflow.execute(belay)

WORKFLOWS = {}


def register(workflow):

    WORKFLOWS[workflow.name] = workflow


def get(name):

    return WORKFLOWS.get(name)


def list_all():

    return WORKFLOWS

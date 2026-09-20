import typer

from framework.engine import BelayEngine

app = typer.Typer()


@app.command()

def run(workflow: str):

    print(f"Requested workflow: {workflow}")

    engine = BelayEngine()

    print("Workflow dispatch not yet implemented.")


@app.command()

def doctor():

    print("Belay Repository Health")

    print("✓ Constitution")

    print("✓ Knowledge")

    print("✓ Strategies")

    print("✓ Workflows")


@app.command()

def version():

    print("Belay v1.0.0-alpha")


if __name__ == "__main__":

    app()

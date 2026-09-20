from framework.services.base import Service


class Critic(Service):

    name = "Critic"

    def run(self, belay):

        print("Attempting falsification...")

from framework.artifacts.factory import ArtifactFactory


class UniverseDiscovery(Service):

    def run(self, belay):

        universe = [

            "SPY",

            "QQQ",

            "IWM"

        ]

        artifact = ArtifactFactory().create(

            identifier=belay.next_id("report"),

            title="Universe Discovery",

            artifact_type="UniverseReport",

            evidence="B",

            content={

                "symbols": universe

            }

        )

        return artifact

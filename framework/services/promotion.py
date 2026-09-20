from framework.services.base import Service


class PromotionReview(Service):

    name = "Promotion Review"

    def run(self, belay):

        print("Evaluating maturity progression...")

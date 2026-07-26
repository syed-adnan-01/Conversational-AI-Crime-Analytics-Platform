class DecisionValidator:
    def validate(self, response):
        for recommendation in response.recommendations:
            if not recommendation.explanation or not recommendation.reasoning_chain: raise ValueError('Every recommendation requires an explanation and reasoning chain.')
        return response

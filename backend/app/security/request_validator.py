class RequestValidator:
    def validate(self, request):
        if not request.user_id or not request.endpoint: raise ValueError('user_id and endpoint are required')
        return request

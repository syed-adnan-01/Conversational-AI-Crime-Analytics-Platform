from .models import DataClassification
class PermissionEvaluator:
    minimum_roles = {DataClassification.PUBLIC: set(), DataClassification.INTERNAL: set(), DataClassification.CONFIDENTIAL: {'officer','supervisor','admin'}, DataClassification.RESTRICTED: {'supervisor','admin'}, DataClassification.HIGHLY_SENSITIVE: {'admin'}}
    def evaluate(self, request): return request.role.casefold() in self.minimum_roles[request.classification] or not self.minimum_roles[request.classification]

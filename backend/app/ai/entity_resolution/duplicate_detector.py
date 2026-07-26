from .similarity import name_similarity

IDENTIFIERS = ("phone", "mobile_no", "vehicle", "aadhaar", "passport", "email", "address")
def matching_fields(left, right):
    exact = [field for field in IDENTIFIERS if left.metadata.get(field) and str(left.metadata.get(field)).casefold() == str(right.metadata.get(field)).casefold()]
    return exact, name_similarity(left.label, right.label)

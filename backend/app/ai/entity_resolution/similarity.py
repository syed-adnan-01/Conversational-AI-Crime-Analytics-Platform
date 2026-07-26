from difflib import SequenceMatcher

def name_similarity(left: str, right: str) -> float: return SequenceMatcher(None, left.casefold(), right.casefold()).ratio()

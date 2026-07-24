"""
============================================================
Query Expander
============================================================

Module  : AI Query Processing Subsystem
Purpose : Performs domain-specific synonym expansion to increase vector recall.
"""

from typing import Optional


class QueryExpander:
    """
    Expands user query strings using police & investigative synonym mappings.
    """

    SYNONYM_MAP: dict[str, list[str]] = {
        "knife": ["weapon", "blade", "sharp object"],
        "weapon": ["firearm", "knife", "revolver", "pistol"],
        "phone": ["mobile", "device", "call log", "smartphone"],
        "money": ["cash", "bribe", "currency", "funds", "financial"],
        "car": ["vehicle", "automobile", "four-wheeler"],
        "gun": ["firearm", "pistol", "revolver", "weapon"],
        "stolen": ["theft", "robbery", "looted", "burglary"],
        "murder": ["homicide", "killing", "assassination"],
        "bribe": ["corruption", "gratification", "illegal payment"],
    }

    @classmethod
    def expand(cls, query: str) -> str:
        if not query:
            return ""

        words = query.lower().split()
        expanded_terms: set[str] = set(words)

        for word in words:
            clean_word = word.strip(".,!?\"'()")
            if clean_word in cls.SYNONYM_MAP:
                expanded_terms.update(cls.SYNONYM_MAP[clean_word])

        return " ".join(expanded_terms)

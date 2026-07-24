"""
============================================================
Query Normalizer
============================================================

Module  : AI Query Processing Subsystem
Purpose : Cleans and normalizes user query strings prior to search processing.
"""

import re


class QueryNormalizer:
    """
    Normalizes input query strings by lowercasing, stripping excessive punctuation,
    and removing duplicated whitespaces.
    """

    @classmethod
    def normalize(cls, query: str) -> str:
        if not query:
            return ""
        # Strip outer whitespace & lowercase
        cleaned = query.strip().lower()
        # Collapse multiple spaces
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned

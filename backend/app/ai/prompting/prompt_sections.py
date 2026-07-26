"""
Dynamic Prompt Section Enums for selective context inclusion.
"""

from enum import Enum


class PromptSection(str, Enum):
    """
    Selectable domain context sections for reducing token consumption.
    """
    CASE = "case"
    SUMMARY = "summary"
    TIMELINE = "timeline"
    EVIDENCE = "evidence"
    LEGAL = "legal"
    OFFICERS = "officers"
    ARREST = "arrest"
    CHARGESHEET = "chargesheet"
    VICTIMS = "victims"
    ACCUSED = "accused"

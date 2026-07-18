"""
============================================================
Legal Seed Data
============================================================

Module  : Act & Section Management
Purpose : Initial legal master/reference data seed values.
"""

from typing import Any

# Seed Acts
SEED_ACTS: list[dict[str, Any]] = [
    {
        "act_id": "ACT-BNS2023",
        "name": "Bharatiya Nyaya Sanhita",
        "short_name": "BNS",
        "year": 2023,
        "description": "The primary criminal code of India, replacing the Indian Penal Code.",
    },
    {
        "act_id": "ACT-BNSS2023",
        "name": "Bharatiya Nagarik Suraksha Sanhita",
        "short_name": "BNSS",
        "year": 2023,
        "description": "The primary legislation on procedure for administration of criminal law in India, replacing CrPC.",
    },
    {
        "act_id": "ACT-IT2000",
        "name": "Information Technology Act",
        "short_name": "IT Act",
        "year": 2000,
        "description": "Primary law in India dealing with cybercrime and electronic commerce.",
    },
]

# Seed Sections
SEED_SECTIONS: list[dict[str, Any]] = [
    # BNS Sections
    {
        "section_id": "SEC-BNS103",
        "act_id": "ACT-BNS2023",
        "section_number": "103",
        "title": "Punishment for Murder",
        "description": "Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine.",
        "is_cognizable": True,
        "is_bailable": False,
        "maximum_punishment": "Death or Imprisonment for Life",
    },
    {
        "section_id": "SEC-BNS303",
        "act_id": "ACT-BNS2023",
        "section_number": "303",
        "title": "Theft",
        "description": "Punishment for theft, including dishonestly taking movable property without consent.",
        "is_cognizable": True,
        "is_bailable": False,
        "maximum_punishment": "Imprisonment up to 3 years, or with fine, or with both",
    },
    # BNSS Sections
    {
        "section_id": "SEC-BNSS35",
        "act_id": "ACT-BNSS2023",
        "section_number": "35",
        "title": "When police may arrest without warrant",
        "description": "Procedural guidelines outlining circumstances under which a police officer may arrest any person without an order from a Magistrate.",
        "is_cognizable": True,
        "is_bailable": True,
        "maximum_punishment": "Procedural section (no direct punishment)",
    },
    # IT Act Sections
    {
        "section_id": "SEC-IT66D",
        "act_id": "ACT-IT2000",
        "section_number": "66D",
        "title": "Punishment for cheating by personation by using computer resource",
        "description": "Whoever by means of any communication device or computer resource cheats by personation shall be punished.",
        "is_cognizable": True,
        "is_bailable": True,
        "maximum_punishment": "Imprisonment up to 3 years and fine up to 1 lakh rupees",
    },
]

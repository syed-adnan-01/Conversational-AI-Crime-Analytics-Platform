"""
============================================================
Evaluation Datasets
============================================================

Module  : AI Evaluation Subsystem
Purpose : Benchmark evaluation test dataset definitions.
"""

EVALUATION_DATASET_V1 = [
    {
        "query": "weapon used in assault",
        "relevant_ids": ["EVI-001", "EVI-002"],
        "k": 5,
    },
    {
        "query": "IPC section 420 fraud charges",
        "relevant_ids": ["SEC-420", "CS-001"],
        "k": 5,
    },
]

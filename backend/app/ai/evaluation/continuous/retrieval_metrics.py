import math
def precision_at_k(retrieved, relevant, k): return sum(item in set(relevant) for item in retrieved[:k]) / k if k else 0.0
def recall_at_k(retrieved, relevant, k): return sum(item in set(relevant) for item in retrieved[:k]) / len(relevant) if relevant else 0.0
def mrr(retrieved, relevant):
    for index, item in enumerate(retrieved, 1):
        if item in set(relevant): return 1 / index
    return 0.0
def ndcg(retrieved, relevant, k):
    dcg = sum(1 / math.log2(index + 1) for index, item in enumerate(retrieved[:k], 1) if item in set(relevant)); ideal = sum(1 / math.log2(index + 1) for index in range(1, min(k, len(relevant)) + 1)); return dcg / ideal if ideal else 0.0

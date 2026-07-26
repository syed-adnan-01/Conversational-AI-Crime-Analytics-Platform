from collections import defaultdict, deque
from time import monotonic
class RateLimiter:
    def __init__(self, limit=60, window_seconds=60): self.limit = limit; self.window_seconds = window_seconds; self._events = defaultdict(deque)
    def allow(self, key):
        now = monotonic(); events = self._events[key]
        while events and now-events[0] >= self.window_seconds: events.popleft()
        if len(events) >= self.limit: return False
        events.append(now); return True

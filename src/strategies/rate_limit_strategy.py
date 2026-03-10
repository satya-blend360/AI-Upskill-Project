"""Rate limiting strategies (Design Patterns)."""
from abc import ABC, abstractmethod
import asyncio
from typing import Any, Coroutine


class RateLimitStrategy(ABC):
    """Abstract strategy for rate limiting."""
    
    @abstractmethod
    async def __aenter__(self):
        """Acquire permission."""
        pass
    
    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Release permission."""
        pass


class SemaphoreStrategy(RateLimitStrategy):
    """
    Semaphore-based rate limiting.
    
    Limits concurrent operations.
    """
    
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def __aenter__(self):
        await self.semaphore.acquire()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.semaphore.release()


class NoRateLimitStrategy(RateLimitStrategy):
    """Strategy that does nothing (Null Object Pattern)."""
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

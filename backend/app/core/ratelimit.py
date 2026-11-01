from typing import Callable, Any

try:
    from slowapi import Limiter
    from slowapi.util import get_remote_address
    limiter = Limiter(key_func=get_remote_address)
except ImportError:
    class DummyLimiter:
        def limit(self, limit_value: str) -> Callable:
            def decorator(func: Callable) -> Callable:
                return func
            return decorator

    limiter = DummyLimiter()  # type: ignore

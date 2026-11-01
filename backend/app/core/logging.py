import logging
import sys
from typing import Any

try:
    import structlog

    def configure_logging() -> None:
        logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
        )

    logger = structlog.get_logger()
except ImportError:
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )
    _std_logger = logging.getLogger("proofpath")

    class StructuredLoggerWrapper:
        def info(self, msg: str, **kwargs: Any) -> None:
            extra = " ".join(f"{k}={v}" for k, v in kwargs.items())
            _std_logger.info(f"{msg} {extra}".strip())

        def error(self, msg: str, **kwargs: Any) -> None:
            extra = " ".join(f"{k}={v}" for k, v in kwargs.items())
            _std_logger.error(f"{msg} {extra}".strip())

        def warning(self, msg: str, **kwargs: Any) -> None:
            extra = " ".join(f"{k}={v}" for k, v in kwargs.items())
            _std_logger.warning(f"{msg} {extra}".strip())

    logger = StructuredLoggerWrapper()

    def configure_logging() -> None:
        pass

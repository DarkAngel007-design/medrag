import logging


class MedRAGFormatter(logging.Formatter):
    """
    Default formatter for MedRAG logging.
    """

    DEFAULT_FORMAT = "%(asctime)s | " "%(levelname)-8s | " "%(name)s | " "%(message)s"

    DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self) -> None:
        super().__init__(
            fmt=self.DEFAULT_FORMAT,
            datefmt=self.DEFAULT_DATE_FORMAT,
        )

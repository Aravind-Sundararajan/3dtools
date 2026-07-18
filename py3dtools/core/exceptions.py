"""Custom exceptions for py3dtools."""


class ConversionError(Exception):
    """Raised when a file conversion fails."""

    pass


class ValidationError(Exception):
    """Raised when input validation fails."""

    pass


class FileNotFoundError(Exception):
    """Raised when a required file is not found."""

    pass


class UnsupportedFormatError(Exception):
    """Raised when a file format is not supported."""

    pass

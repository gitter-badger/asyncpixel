"""All exceptions for asyncpixel."""
from typing import Optional


class RateLimitError(Exception):
    """Raised when a ratelimit is reached."""

    def __init__(self, source: Optional[str] = "unknown source") -> None:
        """Error raised when ratelimit reached.

        Args:
            source (str, optional): Source of the error. Defaults to "unknown source".
        """
        self.message = f"The {source}API ratelimit was reached!"
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return error in readable format.

        Returns:
            str: string version of error
        """
        return self.message


class ApiNoSuccess(Exception):
    """Raised when an error occurred."""

    def __init__(self) -> None:
        """Create error."""
        self.message = "The method encountered an error on the hypixel side."
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return error in readable format.

        Returns:
            str: string version of error
        """
        return self.message


class InvalidApiKey(Exception):
    """Raised when api key is incorrect."""

    def __init__(self) -> None:
        """Create error."""
        self.message = "Entered API key is not valid"
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return error in readable format.

        Returns:
            str: string version of error
        """
        return self.message

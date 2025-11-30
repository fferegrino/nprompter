"""
Output utilities for CLI commands with verbosity control.

This module provides a centralized way to handle output with different verbosity levels:
- QUIET: Only errors and critical messages
- NORMAL: Standard output (info, warnings, errors)
- VERBOSE: Detailed output including progress and debug info
- DEBUG: Very detailed output with all debug information
"""

from enum import IntEnum
from typing import Optional

import typer


class VerbosityLevel(IntEnum):
    """Verbosity levels for CLI output."""

    QUIET = 0
    NORMAL = 1
    VERBOSE = 2
    DEBUG = 3


class OutputHandler:
    """Handles output with verbosity control."""

    def __init__(self, verbosity: VerbosityLevel = VerbosityLevel.NORMAL):
        self.verbosity = verbosity

    def set_verbosity(self, verbosity: VerbosityLevel):
        """Set the verbosity level."""
        self.verbosity = verbosity

    def error(self, message: str, err: Optional[Exception] = None):
        """Print an error message (always shown, even in quiet mode)."""
        typer.echo(typer.style(f"Error: {message}", fg="red"), err=True)
        if err and self.verbosity >= VerbosityLevel.DEBUG:
            typer.echo(typer.style(f"  {type(err).__name__}: {err}", fg="red"), err=True)

    def warning(self, message: str):
        """Print a warning message (shown in normal mode and above)."""
        if self.verbosity >= VerbosityLevel.NORMAL:
            typer.echo(typer.style(f"Warning: {message}", fg="yellow"), err=True)

    def info(self, message: str):
        """Print an informational message (shown in normal mode and above)."""
        if self.verbosity >= VerbosityLevel.NORMAL:
            typer.echo(message)

    def success(self, message: str):
        """Print a success message (shown in normal mode and above)."""
        if self.verbosity >= VerbosityLevel.NORMAL:
            typer.echo(typer.style(message, fg="green"))

    def verbose(self, message: str):
        """Print a verbose message (shown in verbose mode and above)."""
        if self.verbosity >= VerbosityLevel.VERBOSE:
            typer.echo(typer.style(f"  → {message}", fg="blue"))

    def debug(self, message: str):
        """Print a debug message (shown in debug mode only)."""
        if self.verbosity >= VerbosityLevel.DEBUG:
            typer.echo(typer.style(f"  [DEBUG] {message}", fg="cyan"), err=True)

    def progress(self, message: str):
        """Print a progress message (shown in verbose mode and above)."""
        if self.verbosity >= VerbosityLevel.VERBOSE:
            typer.echo(typer.style(f"  • {message}", fg="magenta"))

    def echo(self, message: str, force: bool = False):
        """
        Print a message directly.

        Args:
            message: The message to print
            force: If True, print even in quiet mode
        """
        if force or self.verbosity >= VerbosityLevel.NORMAL:
            typer.echo(message)


# Global output handler instance
_output_handler: Optional[OutputHandler] = None


def get_output_handler() -> OutputHandler:
    """Get the global output handler instance."""
    global _output_handler
    if _output_handler is None:
        _output_handler = OutputHandler()
    return _output_handler


def set_verbosity(verbosity: VerbosityLevel):
    """Set the global verbosity level."""
    get_output_handler().set_verbosity(verbosity)


def parse_verbosity(quiet: bool, verbose: int) -> VerbosityLevel:
    """
    Parse verbosity from CLI flags.

    Args:
        quiet: If True, return QUIET level
        verbose: Number of -v flags (0, 1, or 2+)

    Returns:
        The appropriate VerbosityLevel
    """
    if quiet:
        return VerbosityLevel.QUIET
    if verbose == 0:
        return VerbosityLevel.NORMAL
    if verbose == 1:
        return VerbosityLevel.VERBOSE
    return VerbosityLevel.DEBUG


# Convenience functions that use the global handler
def error(message: str, err: Optional[Exception] = None):
    """Print an error message."""
    get_output_handler().error(message, err)


def warning(message: str):
    """Print a warning message."""
    get_output_handler().warning(message)


def info(message: str):
    """Print an informational message."""
    get_output_handler().info(message)


def success(message: str):
    """Print a success message."""
    get_output_handler().success(message)


def verbose(message: str):
    """Print a verbose message."""
    get_output_handler().verbose(message)


def debug(message: str):
    """Print a debug message."""
    get_output_handler().debug(message)


def progress(message: str):
    """Print a progress message."""
    get_output_handler().progress(message)


def echo(message: str, force: bool = False):
    """Print a message directly."""
    get_output_handler().echo(message, force)

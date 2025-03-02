from __future__ import annotations

import typing as t
from dataclasses import dataclass

import term
from term import boxed
from term._cli import type_util

if t.TYPE_CHECKING:
    from term.cli import Argument, SubCommand


@dataclass
class ProgramConfig:
    prog: str


def _get_long_short(ls: t.Sequence[str]) -> tuple[str, str | None]:
    if len(ls) == 1:
        return ls[0], None
    return ls[1], ls[0]


def _ext(ls: list[str], s: str | list[str] | None) -> list[str] | str | None:
    if s is None:
        return ls
    if isinstance(s, str):
        ls.append(s)
    else:
        ls.extend(s)


@dataclass
class TermFormatter:
    prog: list[str]
    description: str | None
    epilog: str | None
    options: list[Argument]
    positionals: list[Argument]
    subcommands: list[SubCommand]
    error: str | None

    def _format_option(self, option: Argument) -> list[str]:
        long, short = _get_long_short([option.name])
        usage = term.style(f"--{long}", fg="blue", bold=True)
        short_usage = term.style(f"-{short}", fg="green", bold=True) if short else ""
        type_str = term.style(
            type_util.type_to_str(option._type).upper(), fg="yellow", bold=True
        )
        help = option.help or ""
        return [usage, short_usage, type_str, help]

    def _format_options(self) -> list[str]:
        lines = []
        for o in self.options:
            lines.append(" ".join(self._format_option(o)))
        return list(boxed(lines, title="Options"))

    def _format_positional(self, positional: Argument) -> list[str]:
        name = term.style(positional.name, fg="blue", bold=True)
        help = positional.help or ""
        type_str = term.style(
            type_util.type_to_str(positional._type).upper(), fg="yellow", bold=True
        )
        return [name, type_str, help]

    def _format_positionals(self) -> list[str] | str | None:
        lines = []
        for p in self.positionals:
            lines.append(" ".join(self._format_positional(p)))
        return list(boxed(lines, title="Arguments"))

    def _format_header(self) -> list[str] | str | None:
        prefix = term.style("Usage:", fg="yellow")
        prog = term.style(" ".join(self.prog), bold=True)

        options = (
            " [" + term.style("OPTIONS", fg="blue", bold=True) + "]"
            if self.options
            else ""
        )
        command = (
            term.style(" COMMAND", fg="blue", bold=True) if self.subcommands else ""
        )
        positional = (
            " "
            + " ".join(
                term.style(p.name.upper(), fg="blue", bold=True)
                for p in self.positionals
            )
            if self.positionals
            else ""
        )

        return [f"{prefix} {prog}{options}{command}{positional}"]

    def _format_description(self) -> list[str] | str | None:
        if not self.description:
            return None
        return [self.description, ""]

    def _format_error(self) -> list[str] | str | None:
        if not self.error:
            return ""
        return list(boxed([self.error.capitalize()], title="Error", color="red"))

    def format_help(self) -> str:
        lines = []

        # Header
        _ext(lines, self._format_header())
        _ext(lines, "")

        # Description
        _ext(lines, self._format_description())

        # Options
        _ext(lines, self._format_options())

        # Positionals
        _ext(lines, self._format_positionals())

        # Errors
        _ext(lines, self._format_error())

        return "\n".join(lines)

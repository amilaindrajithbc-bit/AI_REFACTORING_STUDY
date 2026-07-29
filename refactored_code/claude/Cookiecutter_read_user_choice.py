from collections import OrderedDict
from itertools import starmap
from typing import Iterator, Optional, Union

from rich.prompt import Prompt


def _build_choice_map(options: list) -> "OrderedDict[str, str]":
    """Build an ordered mapping of ``"1", "2", ...`` to the given options."""
    return OrderedDict((f"{i}", value) for i, value in enumerate(options, 1))


def _resolve_question_and_choice_lines(
    var_name: str,
    choice_map: "OrderedDict[str, str]",
    prompts: Optional[dict],
) -> tuple[str, Iterator[str]]:
    """Determine the question text and formatted choice lines.

    If a human-readable prompt configuration is provided for ``var_name``,
    it is used to override the default question and/or per-choice labels.
    Otherwise, sensible defaults derived from ``choice_map`` are used.
    """
    question = f"Select {var_name}"
    choice_lines: Iterator[str] = starmap(
        "    [bold magenta]{}[/] - [bold]{}[/]".format, choice_map.items()
    )

    if not prompts or var_name not in prompts:
        return question, choice_lines

    var_prompt: Union[str, dict] = prompts[var_name]

    if isinstance(var_prompt, str):
        question = var_prompt
        return question, choice_lines

    if "__prompt__" in var_prompt:
        question = var_prompt["__prompt__"]

    choice_lines = (
        f"    [bold magenta]{i}[/] - [bold]{var_prompt[option]}[/]"
        if option in var_prompt
        else f"    [bold magenta]{i}[/] - [bold]{option}[/]"
        for i, option in choice_map.items()
    )

    return question, choice_lines


def read_user_choice(var_name: str, options: list, prompts=None, prefix: str = ""):
    """Prompt the user to choose from several options for the given variable.

    The first item will be returned if no input happens.

    :param var_name: Variable as specified in the context
    :param list options: Sequence of options that are available to select from
    :param prompts: Optional mapping providing human-readable prompt text
        and/or per-choice labels for ``var_name``
    :param prefix: Optional string prepended to the question line
    :return: Exactly one item of ``options`` that has been chosen by the user
    """
    if not options:
        raise ValueError

    choice_map = _build_choice_map(options)
    choices = choice_map.keys()

    question, choice_lines = _resolve_question_and_choice_lines(
        var_name, choice_map, prompts
    )

    prompt = "\n".join(
        (
            f"{prefix}{question}",
            "\n".join(choice_lines),
            "    Choose from",
        )
    )

    user_choice = Prompt.ask(prompt, choices=list(choices), default=next(iter(choices)))
    return choice_map[user_choice]
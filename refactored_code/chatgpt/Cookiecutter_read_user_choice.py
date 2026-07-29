from collections import OrderedDict
from itertools import starmap
from typing import Iterator

from rich.prompt import Prompt


def read_user_choice(
    var_name: str,
    options: list,
    prompts=None,
    prefix: str = "",
):
    """Prompt the user to choose from the available options.

    If the user provides no input, the first option is selected by default.

    :param var_name: Variable name used in the prompt context.
    :param options: Sequence of available options.
    :param prompts: Optional mapping containing custom prompts and display labels.
    :param prefix: Optional prefix added to the prompt.
    :return: The selected item from ``options``.
    :raises ValueError: If ``options`` is empty.
    """
    if not options:
        raise ValueError

    choice_map = OrderedDict(
        (str(index), value)
        for index, value in enumerate(options, start=1)
    )
    choices = list(choice_map.keys())

    question = f"Select {var_name}"

    choice_lines: Iterator[str] = starmap(
        "    [bold magenta]{}[/] - [bold]{}[/]".format,
        choice_map.items(),
    )

    # Handle custom prompts and display labels if provided.
    if prompts and var_name in prompts:
        prompt_config = prompts[var_name]

        if isinstance(prompt_config, str):
            question = prompt_config
        else:
            question = prompt_config.get("__prompt__", question)

            choice_lines = (
                (
                    f"    [bold magenta]{index}[/] - "
                    f"[bold]{prompt_config.get(option, option)}[/]"
                )
                for index, option in choice_map.items()
            )

    prompt = "\n".join(
        (
            f"{prefix}{question}",
            "\n".join(choice_lines),
            "    Choose from",
        )
    )

    user_choice = Prompt.ask(
        prompt,
        choices=choices,
        default=choices[0],
    )

    return choice_map[user_choice]
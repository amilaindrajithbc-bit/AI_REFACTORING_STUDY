from collections import OrderedDict
from typing import Any, Mapping, Sequence, Union
from rich.prompt import Prompt


def read_user_choice(
    var_name: str,
    options: Sequence[Any],
    prompts: Union[Mapping[str, Any], None] = None,
    prefix: str = "",
) -> Any:
    """Prompt the user to choose from several options for the given variable.

    The first item will be returned if no input happens.

    :param var_name: Variable name as specified in the context.
    :param options: Sequence of options available for selection.
    :param prompts: Optional mapping containing custom questions or label overrides.
    :param prefix: Optional string prefix added to the prompt title.
    :return: The single item selected by the user from ``options``.
    :raises ValueError: If the options sequence is empty.
    """
    if not options:
        raise ValueError("Options list cannot be empty.")

    choice_map = OrderedDict((str(i), value) for i, value in enumerate(options, 1))
    choices = list(choice_map.keys())

    question = f"Select {var_name}"
    var_prompt = prompts.get(var_name) if prompts else None

    if var_prompt is None:
        choice_lines = [
            f"    [bold magenta]{i}[/] - [bold]{val}[/]"
            for i, val in choice_map.items()
        ]
    elif isinstance(var_prompt, str):
        question = var_prompt
        choice_lines = [
            f"    [bold magenta]{i}[/] - [bold]{val}[/]"
            for i, val in choice_map.items()
        ]
    else:
        if "__prompt__" in var_prompt:
            question = var_prompt["__prompt__"]

        choice_lines = [
            f"    [bold magenta]{i}[/] - [bold]{var_prompt[val] if val in var_prompt else val}[/]"
            for i, val in choice_map.items()
        ]

    prompt_text = "\n".join(
        (
            f"{prefix}{question}",
            "\n".join(choice_lines),
            "    Choose from",
        )
    )

    user_choice = Prompt.ask(prompt_text, choices=choices, default=choices[0])
    return choice_map[user_choice]
def read_user_choice(var_name: str, options: list, prompts=None, prefix: str = ""):
    """Prompt the user to choose from several options for the given variable.

    The first item will be returned if no input happens.

    :param var_name: Variable as specified in the context
    :param list options: Sequence of options that are available to select from
    :return: Exactly one item of ``options`` that has been chosen by the user
    """
    if not options:
        raise ValueError

    choice_map = OrderedDict((f'{i}', value) for i, value in enumerate(options, 1))
    choices = choice_map.keys()

    question = f"Select {var_name}"

    choice_lines: Iterator[str] = starmap(
        "    [bold magenta]{}[/] - [bold]{}[/]".format, choice_map.items()
    )

    # Handle if human-readable prompt is provided
    if prompts and var_name in prompts:
        if isinstance(prompts[var_name], str):
            question = prompts[var_name]
        else:
            if "__prompt__" in prompts[var_name]:
                question = prompts[var_name]["__prompt__"]
            choice_lines = (
                f"    [bold magenta]{i}[/] - [bold]{prompts[var_name][p]}[/]"
                if p in prompts[var_name]
                else f"    [bold magenta]{i}[/] - [bold]{p}[/]"
                for i, p in choice_map.items()
            )

    prompt = '\n'.join(
        (
            f"{prefix}{question}",
            "\n".join(choice_lines),
            "    Choose from",
        )
    )

    user_choice = Prompt.ask(prompt, choices=list(choices), default=next(iter(choices)))
    return choice_map[user_choice]
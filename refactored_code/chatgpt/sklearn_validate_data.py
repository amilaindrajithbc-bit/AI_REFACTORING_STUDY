def validate_data(
    _estimator,
    /,
    X="no_validation",
    y="no_validation",
    reset=True,
    validate_separately=False,
    skip_check_array=False,
    **check_params,
):
    """Validate input data and set or check feature names and counts.

    This helper function should be used in an estimator that requires input
    validation. It mutates the estimator by setting the ``n_features_in_`` and
    ``feature_names_in_`` attributes when ``reset=True``.

    Parameters
    ----------
    _estimator : estimator instance
        The estimator to validate the input for.

    X : {array-like, sparse matrix, dataframe} of shape (n_samples, n_features), \
            default="no_validation"
        The input samples.

    y : array-like of shape (n_samples,), default="no_validation"
        The target values.

    reset : bool, default=True
        Whether to reset the ``n_features_in_`` attribute.

    validate_separately : False or tuple of dicts, default=False
        Whether to validate ``X`` and ``y`` separately.

    skip_check_array : bool, default=False
        If ``True``, skip array validation and only perform feature checks.

    **check_params : dict
        Additional parameters passed to validation routines.

    Returns
    -------
    ndarray, sparse matrix, or tuple
        The validated input data.
    """
    _check_feature_names(_estimator, X, reset=reset)

    tags = get_tags(_estimator)
    if y is None and tags.target_tags.required:
        raise ValueError(
            f"This {_estimator.__class__.__name__} estimator "
            "requires y to be passed, but the target y is None."
        )

    no_val_X = isinstance(X, str) and X == "no_validation"
    no_val_y = y is None or (isinstance(y, str) and y == "no_validation")

    if no_val_X and no_val_y:
        raise ValueError("Validation should be done on X, y or both.")

    default_check_params = {"estimator": _estimator}
    check_params = {**default_check_params, **check_params}

    if skip_check_array:
        if not no_val_X and no_val_y:
            out = X
        elif no_val_X and not no_val_y:
            out = y
        else:
            out = (X, y)
    elif not no_val_X and no_val_y:
        out = check_array(X, input_name="X", **check_params)
    elif no_val_X and not no_val_y:
        out = _check_y(y, **check_params)
    else:
        if validate_separately:
            # Some estimators require independent validation of X and y.
            check_X_params, check_y_params = validate_separately

            if "estimator" not in check_X_params:
                check_X_params = {**default_check_params, **check_X_params}

            X = check_array(X, input_name="X", **check_X_params)

            if "estimator" not in check_y_params:
                check_y_params = {**default_check_params, **check_y_params}

            y = check_array(y, input_name="y", **check_y_params)
        else:
            X, y = check_X_y(X, y, **check_params)

        out = (X, y)

    if not no_val_X and check_params.get("ensure_2d", True):
        _check_n_features(_estimator, X, reset=reset)

    return out
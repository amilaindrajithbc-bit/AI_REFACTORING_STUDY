def wsgi_app(
    self, environ: WSGIEnvironment, start_response: StartResponse
) -> cabc.Iterable[bytes]:
    """The actual WSGI application. This is not implemented in
    :meth:`__call__` so that middlewares can be applied without
    losing a reference to the app object. Instead of doing this::

        app = MyMiddleware(app)

    It's a better idea to do this instead::

        app.wsgi_app = MyMiddleware(app.wsgi_app)

    Then you still have the original application object around and
    can continue to call methods on it.

    .. versionchanged:: 0.7
        Teardown events for the request and app contexts are called
        even if an unhandled error occurs. Other events may not be
        called depending on when an error occurs during dispatch.

    :param environ: A WSGI environment.
    :param start_response: A callable accepting a status code,
        a list of headers, and an optional exception context to
        start the response.
    """
    ctx = self.request_context(environ)
    error: BaseException | None = None

    try:
        try:
            ctx.push()
            response = self.full_dispatch_request(ctx)
        except Exception as e:
            # Handled exceptions are converted into a response. The
            # original exception is kept so it can be reported during
            # context teardown.
            error = e
            response = self.handle_exception(ctx, e)
        except:
            # Unhandled/non-Exception errors (e.g. SystemExit,
            # KeyboardInterrupt) are recorded for teardown but must
            # continue to propagate unchanged.
            error = sys.exc_info()[1]
            raise

        return response(environ, start_response)
    finally:
        # Allow the debugger to keep the request/app contexts alive
        # for post-mortem inspection instead of tearing them down.
        preserve_context = environ.get("werkzeug.debug.preserve_context")
        if preserve_context is not None:
            preserve_context(ctx)

        # Errors the application explicitly wants to ignore should not
        # be reported to teardown handlers.
        if (
            error is not None
            and self.should_ignore_error is not None
            and self.should_ignore_error(error)
        ):
            error = None

        ctx.pop(error)
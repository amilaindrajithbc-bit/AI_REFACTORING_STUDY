def wsgi_app(
    self, environ: WSGIEnvironment, start_response: StartResponse
) -> cabc.Iterable[bytes]:
    """The actual WSGI application.

    This is implemented separately from :meth:`__call__` so that WSGI
    middlewares can be applied without losing a reference to the original
    application object. For example, prefer::

        app.wsgi_app = MyMiddleware(app.wsgi_app)

    instead of::

        app = MyMiddleware(app)

    This preserves access to the original application instance and its
    methods.

    .. versionchanged:: 0.7
        Teardown events for the request and application contexts are called
        even if an unhandled error occurs. Other events may not be called
        depending on when an error occurs during request dispatch.

    :param environ: A WSGI environment.
    :param start_response: A callable that accepts a status code,
        a list of headers, and an optional exception context to start
        the response.
    """
    ctx = self.request_context(environ)
    error: BaseException | None = None

    try:
        try:
            ctx.push()
            response = self.full_dispatch_request(ctx)
        except Exception as exc:
            error = exc
            response = self.handle_exception(ctx, exc)
        except:
            error = sys.exc_info()[1]
            raise

        return response(environ, start_response)
    finally:
        preserve_context = environ.get("werkzeug.debug.preserve_context")
        if preserve_context is not None:
            preserve_context(ctx)

        if (
            error is not None
            and self.should_ignore_error is not None
            and self.should_ignore_error(error)
        ):
            error = None

        ctx.pop(error)
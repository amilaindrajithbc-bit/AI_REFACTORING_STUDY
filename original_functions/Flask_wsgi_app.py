def wsgi_app(
    self, environ: WSGIEnvironment, start_response: StartResponse
) -> cabc.Iterable[bytes]:
    """The actual WSGI application...
    """
    ctx = self.request_context(environ)
    error: BaseException | None = None

    try:
        try:
            ctx.push()
            response = self.full_dispatch_request(ctx)
        except Exception as e:
            error = e
            response = self.handle_exception(ctx, e)
        except:
            error = sys.exc_info()[1]
            raise

        return response(environ, start_response)

    finally:
        if "werkzeug.debug.preserve_context" in environ:
            environ["werkzeug.debug.preserve_context"](ctx)

        if (
            error is not None
            and self.should_ignore_error is not None
            and self.should_ignore_error(error)
        ):
            error = None

        ctx.pop(error)
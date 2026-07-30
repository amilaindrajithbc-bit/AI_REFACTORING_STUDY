def prepare_url(
    self,
    url: _t.UriType,
    params: _t.ParamsType,
) -> None:
    """Prepare and validate the given HTTP URL."""

    # Accept objects that have string representations without introducing
    # Python 3 byte string markers (e.g. b"...").
    if isinstance(url, bytes):
        url = url.decode("utf8")
    else:
        url = str(url)

    # Remove leading whitespace.
    url = url.lstrip()

    # Skip URL preparation for non-HTTP schemes (e.g. mailto:, data:).
    if ":" in url and not url.lower().startswith("http"):
        self.url = url
        return

    try:
        scheme, auth, host, port, path, query, fragment = parse_url(url)
    except LocationParseError as exc:
        raise InvalidURL(*exc.args)

    if not scheme:
        raise MissingSchema(
            f"Invalid URL {url!r}: No scheme supplied. "
            f"Perhaps you meant https://{url}?"
        )

    if not host:
        raise InvalidURL(f"Invalid URL {url!r}: No host supplied")

    # Apply IDNA encoding for non-ASCII hostnames and validate ASCII hostnames.
    if not unicode_is_ascii(host):
        try:
            host = self._get_idna_encoded_host(host)
        except UnicodeError:
            raise InvalidURL("URL has an invalid label.")
    elif host.startswith(("*", ".")):
        raise InvalidURL("URL has an invalid label.")

    # Reconstruct the network location.
    netloc = ""
    if auth:
        netloc = f"{auth}@"

    netloc += host

    if port:
        netloc += f":{port}"

    # Bare domains require a root path.
    if not path:
        path = "/"

    if isinstance(params, (str, bytes)):
        params = to_native_string(params)

    enc_params = self._encode_params(params) if params is not None else ""

    if enc_params:
        query = f"{query}&{enc_params}" if query else enc_params

    self.url = requote_uri(
        urlunparse((scheme, netloc, path, "", query, fragment))
    )
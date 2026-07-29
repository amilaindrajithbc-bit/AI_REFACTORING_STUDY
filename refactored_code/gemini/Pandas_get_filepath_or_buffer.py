def _get_filepath_or_buffer(
    filepath_or_buffer: FilePath | BaseBuffer,
    encoding: str = "utf-8",
    compression: CompressionOptions | None = None,
    mode: str = "r",
    storage_options: StorageOptions | None = None,
) -> IOArgs:
    """
    If the filepath_or_buffer is a url, translate and return the buffer.
    Otherwise passthrough.

    Parameters
    ----------
    filepath_or_buffer : a url, filepath (str or pathlib.Path),
                         or buffer

    compression : str or dict, default 'infer'
        For on-the-fly compression of the output data. If 'infer' and
        'filepath_or_buffer' is path-like, then detect compression from the
        following extensions: '.gz',
        '.bz2', '.zip', '.xz', '.zst', '.tar', '.tar.gz', '.tar.xz' or '.tar.bz2'
        (otherwise no compression).
        Set to ``None`` for no compression.
        Can also be a dict with key ``'method'`` set
        to one of {``'zip'``, ``'gzip'``, ``'bz2'``, ``'zstd'``, ``'xz'``, ``'tar'``}
        and other key-value pairs are forwarded to
        ``zipfile.ZipFile``, ``gzip.GzipFile``,
        ``bz2.BZ2File``, ``zstandard.ZstdCompressor``, ``lzma.LZMAFile`` or
        ``tarfile.TarFile``, respectively.
        As an example, the following could be passed for faster compression and to
        create a reproducible gzip archive:
        ``compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1}``.

    encoding : the encoding to use to decode bytes, default is 'utf-8'
    mode : str, optional

    storage_options : dict, optional
        Extra options that make sense for a particular storage connection, e.g.
        host, port, username, password, etc. For HTTP(S) URLs the key-value pairs
        are forwarded to ``urllib.request.Request`` as header options. For other
        URLs (e.g. starting with "s3://", and "gcs://") the key-value pairs are
        forwarded to ``fsspec.open``.

    Returns the dataclass IOArgs.
    """
    filepath_or_buffer = stringify_path(filepath_or_buffer)

    compression_method, compression = get_compression_method(compression)
    compression_method = infer_compression(filepath_or_buffer, compression_method)

    if compression_method and hasattr(filepath_or_buffer, "write") and "b" not in mode:
        warnings.warn(
            "compression has no effect when passing a non-binary object as input.",
            RuntimeWarning,
            stacklevel=find_stack_level(),
        )
        compression_method = None

    compression = dict(compression, method=compression_method)

    if (
        "w" in mode
        and compression_method in ["bz2", "xz"]
        and encoding in ["utf-16", "utf-32"]
    ):
        warnings.warn(
            f"{compression_method} will not write the byte order mark for {encoding}",
            UnicodeWarning,
            stacklevel=find_stack_level(),
        )

    if "a" in mode and compression_method in ["zip", "tar"]:
        warnings.warn(
            "zip and tar do not support mode 'a' properly. "
            "This combination will result in multiple files with same name "
            "being added to the archive.",
            RuntimeWarning,
            stacklevel=find_stack_level(),
        )

    fsspec_mode = mode
    if "t" not in fsspec_mode and "b" not in fsspec_mode:
        fsspec_mode += "b"

    # Handle standard HTTP(S) URLs
    if isinstance(filepath_or_buffer, str) and is_url(filepath_or_buffer):
        import urllib.request

        headers = storage_options or {}
        req_info = urllib.request.Request(filepath_or_buffer, headers=headers)
        with urlopen(req_info) as req:
            content_encoding = req.headers.get("Content-Encoding", None)
            if content_encoding == "gzip":
                compression = {"method": "gzip"}
            reader = BytesIO(req.read())

        return IOArgs(
            filepath_or_buffer=reader,
            encoding=encoding,
            compression=compression,
            should_close=True,
            mode=fsspec_mode,
        )

    # Handle remote/cloud storage URLs supported by fsspec
    if is_fsspec_url(filepath_or_buffer):
        assert isinstance(filepath_or_buffer, str)

        if filepath_or_buffer.startswith("s3a://"):
            filepath_or_buffer = filepath_or_buffer.replace("s3a://", "s3://")
        elif filepath_or_buffer.startswith("s3n://"):
            filepath_or_buffer = filepath_or_buffer.replace("s3n://", "s3://")

        fsspec = import_optional_dependency("fsspec")

        err_types_to_retry_with_anon: list[Any] = []
        try:
            import_optional_dependency("botocore")
            from botocore.exceptions import ClientError, NoCredentialsError

            err_types_to_retry_with_anon = [
                ClientError,
                NoCredentialsError,
                PermissionError,
            ]
        except ImportError:
            pass

        options = dict(storage_options or {})
        try:
            open_file = fsspec.open(
                filepath_or_buffer,
                mode=fsspec_mode,
                **options,
            )
            file_obj = open_file.open()
        except tuple(err_types_to_retry_with_anon):
            options["anon"] = True
            open_file = fsspec.open(
                filepath_or_buffer,
                mode=fsspec_mode,
                **options,
            )
            file_obj = open_file.open()

        return IOArgs(
            filepath_or_buffer=file_obj,
            encoding=encoding,
            compression=compression,
            close_handles=[open_file],
            should_close=True,
            mode=fsspec_mode,
        )

    if storage_options:
        raise ValueError(
            "storage_options passed with file object or non-fsspec file path"
        )

    # Handle local path-like string/bytes or memory mapped files
    if isinstance(filepath_or_buffer, (str, bytes, mmap.mmap)):
        return IOArgs(
            filepath_or_buffer=_expand_user(filepath_or_buffer),
            encoding=encoding,
            compression=compression,
            should_close=False,
            mode=mode,
        )

    # Handle standard stream/buffer objects
    if hasattr(filepath_or_buffer, "read") or hasattr(filepath_or_buffer, "write"):
        return IOArgs(
            filepath_or_buffer=filepath_or_buffer,
            encoding=encoding,
            compression=compression,
            should_close=False,
            mode=mode,
        )

    raise ValueError(
        f"Invalid file path or buffer object type: {type(filepath_or_buffer)}"
    )
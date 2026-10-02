"""EBCDIC Code Page 037 decoder and encoder.

This package provides functions to convert between Python ``str`` and bytes in
IBM EBCDIC Code Page 037 (USA/Canada, with euro-update positions left alone).

Why a dedicated package?
-----------------------
Mainframe interchange often delivers bytes in CP037. Python's standard library
ships codec tables for ``cp037`` via the ``codecs`` module, but those tables are
not guaranteed to be present on every build (they live in the optional
``encodings`` package data files). Carrying our own table removes that
environment dependency entirely, which matters in locked-down containers.

Design decision
---------------
We implement a single code page (037) rather than a configurable registry.
Multi-code-page support invites configuration drift and ambiguous dispatch on
unknown bytes. One table, one behaviour.

The awkward edge
----------------
EBCDIC control characters (bytes 0x00-0x3F) map to C0 control codes in the
Unicode mapping CP037 uses. We map them to the corresponding ``chr`` values
(0x00 through 0x1F, plus 0x7F for the byte that CP037 defines as DEL). Round-
tripping those through Python strings is lossy in *interpretation* (they are
not printable) but lossless in *value*.
"""

from .core import decode, encode, DecodeError, EncodeError

__all__ = ["decode", "encode", "DecodeError", "EncodeError"]

__version__ = "1.0.0"

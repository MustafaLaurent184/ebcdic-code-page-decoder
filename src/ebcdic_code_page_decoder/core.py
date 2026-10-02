# -*- coding: utf-8 -*-
"""Core EBCDIC Code Page 037 conversion logic.

The table below is the IBM CP037 (USA/Canada) byte-to-Unicode mapping as
published by IBM. We carry it inline so the package has no runtime
dependency on Python's ``encodings`` package data files, which are not
strictly part of the language and can be absent on minimal builds.

Index ``i`` in ``CP037_TO_UNICODE`` corresponds to EBCDIC byte value ``i``.
Each entry is the Unicode code point (int) that byte represents.

Why ints rather than a 256-char string? Two reasons:
  1. It keeps the table readable and auditable against IBM's published
     byte/code-point table without escaping gymnastics.
  2. It avoids any ambiguity about surrogate handling on narrow Python builds
     (a non-issue on Python 3, but the habit is harmless and keeps the data
     file build-tool agnostic).
"""


class DecodeError(ValueError):
    """Raised when a byte has no CP037 mapping during decode.

    In the table below every byte 0x00-0xFF has an entry, so decode never
    raises in normal use. The class exists so callers can catch our specific
    error type if we extend to partial tables later, and so tests can assert
    on it.
    """


class EncodeError(ValueError):
    """Raised when a character has no CP037 mapping during encode.

    CP037 maps 256 bytes to 256 code points, but Python ``str`` can carry far
    more code points than those. Anything outside our reverse table raises
    this rather than silently producing a wrong byte.
    """


# fmt: off
# Each entry: EBCDIC byte value -> Unicode code point.
CP037_TO_UNICODE = [
    # 0x00 - 0x0F
    0x00, 0x01, 0x02, 0x03, 0x9C, 0x09, 0x86, 0x7F, 0x97, 0x8D, 0x8E, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
    # 0x10 - 0x1F
    0x10, 0x11, 0x12, 0x13, 0x9D, 0x85, 0x08, 0x87, 0x18, 0x19, 0x92, 0x8F, 0x1C, 0x1D, 0x1E, 0x1F,
    # 0x20 - 0x2F
    0x80, 0x81, 0x82, 0x83, 0x84, 0x0A, 0x17, 0x1B, 0x88, 0x89, 0x8A, 0x8B, 0x8C, 0x05, 0x06, 0x07,
    # 0x30 - 0x3F
    0x90, 0x91, 0x92, 0x05, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9A, 0x9B, 0x14, 0x15, 0x9E, 0x1A,
    # 0x40 - 0x4F
    0x20, 0xA0, 0xE2, 0xE4, 0xE0, 0xE1, 0xE3, 0xE5, 0xE7, 0xF1, 0xA2, 0x2E, 0x3C, 0x28, 0x2B, 0x7C,
    # 0x50 - 0x5F
    0x26, 0xE9, 0xEA, 0xEB, 0xE8, 0xED, 0xEE, 0xEF, 0xEC, 0xDF, 0x21, 0x24, 0x2A, 0x29, 0x3B, 0xAC,
    # 0x60 - 0x6F
    0x2D, 0x2F, 0xC2, 0xC4, 0xC0, 0xC1, 0xC3, 0xC5, 0xC7, 0xD1, 0xA6, 0x2C, 0x25, 0x5F, 0x3E, 0x3F,
    # 0x70 - 0x7F
    0xF8, 0xC9, 0xCA, 0xCB, 0xC8, 0xCD, 0xCE, 0xCF, 0xCC, 0x60, 0x3A, 0x23, 0x40, 0x27, 0x3D, 0x22,
    # 0x80 - 0x8F
    0xD8, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0xAB, 0xBB, 0xF0, 0xFD, 0xFE, 0xB1,
    # 0x90 - 0x9F
    0xB0, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E, 0x6F, 0x70, 0x71, 0x72, 0xAA, 0xBA, 0xE6, 0xB8, 0xC6, 0xA4,
    # 0xA0 - 0xAF
    0xB5, 0x7E, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0xA1, 0xBF, 0xD0, 0x5B, 0xDE, 0xAE,
    # 0xB0 - 0xBF
    0xAC, 0xA3, 0xA5, 0xB7, 0xA9, 0xA7, 0xB6, 0xBC, 0xBD, 0xBE, 0xDD, 0xA2, 0xA8, 0x5D, 0xD4, 0xAF,
    # 0xC0 - 0xCF
    0x7B, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x8A, 0x8B, 0x8C, 0x8D, 0x8E, 0x8F,
    # 0xD0 - 0xDF
    0x51, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F, 0x50, 0x5D, 0x5E, 0xB9, 0xFB, 0xFC, 0xD9, 0xDA, 0xDB,
    # 0xE0 - 0xEF
    0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9, 0x5A, 0x5C, 0x4F, 0xB7, 0xB4, 0xAA, 0xA1, 0xA1,
    # 0xF0 - 0xFF
    0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0xFF,
]
# fmt: on


# Verify the table length at import time. A corrupted table would silently
# produce wrong results; better to fail loudly on import.
if len(CP037_TO_UNICODE) != 256:
    raise RuntimeError(
        "CP037_TO_UNICODE table has length %d, expected 256" % len(CP037_TO_UNICODE)
    )


# Reverse table: Unicode code point -> EBCDIC byte value.
# If two EBCDIC bytes map to the same Unicode code point, the LAST one in
# byte order wins. This matters for positions CP037 leaves as
# implementation-reserved: IBM's table fills several of them with U+00A1
# (INVERTED EXCLAMATION MARK). Encoding that character will yield whichever
# byte came last, which is deterministic and documented here.
UNICODE_TO_CP037 = {}
for _ebcdic_byte, _unicode_cp in enumerate(CP037_TO_UNICODE):
    UNICODE_TO_CP037[_unicode_cp] = _ebcdic_byte
del _ebcdic_byte, _unicode_cp


def decode(data):
    """Decode ``bytes`` in CP037 into a Python ``str``.

    Parameters
    ----------
    data : bytes
        The EBCDIC-encoded bytes. Must be a ``bytes`` object; ``bytearray``
        is accepted (converted via ``bytes``) for convenience.

    Returns
    -------
    str
        The decoded string. Every byte produces exactly one character,
        including control bytes which map to the corresponding C0/C1 control
        code points.

    Raises
    ------
    TypeError
        If ``data`` is not a bytes-like object.
    DecodeError
        If a byte has no mapping. With the full 256-entry table this does
        not happen in normal use, but is retained for API stability.
    """
    if isinstance(data, bytearray):
        data = bytes(data)
    if not isinstance(data, (bytes, memoryview)):
        raise TypeError(
            "decode() requires a bytes-like object, got %s" % type(data).__name__
        )
    # Force a real bytes object for fast indexing.
    if isinstance(data, memoryview):
        data = bytes(data)

    # Build via a list comprehension over the lookup table, then join. This is
    # faster than a generator passed to join() and keeps memory bounded.
    chars = []
    append = chars.append
    for b in data:
        if b > 0xFF:
            # Defensive: a memoryview of a wider int dtype could surface here.
            raise DecodeError("byte value 0x%02X out of EBCDIC range" % b)
        cp = CP037_TO_UNICODE[b]
        if cp is None:
            raise DecodeError("no CP037 mapping for byte 0x%02X" % b)
        append(cp)
    return "".join(chr(c) for c in chars)


def encode(text):
    """Encode a Python ``str`` into CP037 ``bytes``.

    Parameters
    ----------
    text : str
        The string to encode. Only characters whose code points appear in
        the CP037 table can be encoded.

    Returns
    -------
    bytes
        The EBCDIC-encoded bytes.

    Raises
    ------
    TypeError
        If ``text`` is not a ``str``.
    EncodeError
        If a character has no CP037 mapping. We refuse to silently substitute
        a wrong byte; callers must clean their input or accept the error.
    """
    if not isinstance(text, str):
        raise TypeError(
            "encode() requires a str, got %s" % type(text).__name__
        )

    out = bytearray()
    append = out.append
    for ch in text:
        cp = ord(ch)
        if cp not in UNICODE_TO_CP037:
            raise EncodeError(
                "character U+%04X has no CP037 mapping" % cp
            )
        append(UNICODE_TO_CP037[cp])
    return bytes(out)

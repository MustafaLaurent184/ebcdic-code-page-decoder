# ebcdic_code_page_decoder

Decode and encode bytes using IBM EBCDIC Code Page 037, the USA/Canada mainframe code page.

## Usage

```python
from ebcdic_code_page_decoder import decode, encode, DecodeError, EncodeError

# EBCDIC bytes for "Hello" in CP037
hello_bytes = b"\xC8\x85\x93\x93\x96"
print(decode(hello_bytes))  # -> "Hello"

print(encode("Hello"))  # -> b'\xc8\x85\x93\x93\x96'

# Characters not in CP037 raise EncodeError rather than silently substituting a wrong byte.
try:
    encode("\U0001F600")  # emoji, not in CP037
except EncodeError as e:
    print(e)  # character U+1F600 has no CP037 mapping
```

Exported names: `decode`, `encode`, `DecodeError`, `EncodeError`.

## Why this exists

Mainframe data interchange still delivers CP037-encoded bytes. Python ships a
`cp037` codec via the `codecs` module, but that codec relies on data files in
the `encodings` package which are not part of the language proper and can be
absent from minimal/container builds. Carrying the table inline removes that
environment dependency entirely.

The trade-off: we implement exactly one code page (037) with no plugin or
registry support. Configurable code pages invite configuration drift and
ambiguous dispatch on unknown bytes; one table, one behaviour.

## The awkward edge

Several byte positions in the CP037 table (the C0-D0 range) are reserved by
IBM and mapped to U+00A1 (inverted exclamation mark). This means those bytes
decode to `¡`, and re-encoding `¡` yields whichever byte position appears
**last** in byte order. The round-trip is stable for the character value but
not for the original byte position — if you need byte-exact round-tripping of
reserved positions, normalize first.

Control bytes (0x00–0x3F) decode to C0 control code points (U+0000–U+001F plus
U+007F). They are not printable but round-trip losslessly in *value*.

`encode` raises `EncodeError` for any character not in the CP037 repertoire
rather than substituting a placeholder. Clean your input or handle the error.

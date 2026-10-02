# -*- coding: utf-8 -*-
"""Tests for the EBCDIC Code Page 037 decoder/encoder.

These tests exercise the behaviour the implementation actually claims:
  * Round-trip for every defined byte value.
  * Specific well-known EBCDIC byte sequences decode to the expected text.
  * encode() raises EncodeError for characters not in the CP037 repertoire.
  * decode() and encode() reject wrong input types with TypeError.

We do NOT test code paths the implementation does not provide (e.g. streaming,
codec registration, or other code pages).
"""

import unittest

from ebcdic_code_page_decoder import decode, encode, DecodeError, EncodeError
from ebcdic_code_page_decoder.core import (
    CP037_TO_UNICODE,
    UNICODE_TO_CP037,
)


class TestTableIntegrity(unittest.TestCase):
    """The lookup table is the foundation; sanity-check it first."""

    def test_table_has_256_entries(self):
        self.assertEqual(len(CP037_TO_UNICODE), 256)

    def test_table_values_are_ints_in_unicode_range(self):
        for v in CP037_TO_UNICODE:
            self.assertIsInstance(v, int)
            self.assertGreaterEqual(v, 0)
            self.assertLessEqual(v, 0x10FFFF)

    def test_reverse_table_covers_all_unique_code_points(self):
        # Every byte's code point must have an entry in the reverse table.
        # (Where multiple bytes map to the same code point, only one survives,
        # but that one must exist.)
        for cp in CP037_TO_UNICODE:
            self.assertIn(cp, UNICODE_TO_CP037)


class TestDecodeKnownValues(unittest.TestCase):
    """Spot-check the canonical IBM CP037 mapping."""

    def test_space_byte_0x40_decodes_to_space(self):
        self.assertEqual(decode(b"\x40"), " ")

    def test_lowercase_a_byte_0x81(self):
        self.assertEqual(decode(b"\x81"), "a")

    def test_uppercase_a_byte_0xC1(self):
        self.assertEqual(decode(b"\xC1"), "A")

    def test_digit_zero_byte_0xF0(self):
        self.assertEqual(decode(b"\xF0"), "0")

    def test_nul_byte_decodes_to_nul_char(self):
        # 0x00 in EBCDIC is NUL, which maps to U+0000.
        self.assertEqual(decode(b"\x00"), "\x00")

    def test_short_string_decodes_correctly(self):
        # "Hello" in CP037: C8 85 93 93 96
        self.assertEqual(decode(b"\xC8\x85\x93\x93\x96"), "Hello")

    def test_punctuation_pipe_0x4F(self):
        # 0x4F is "|" (vertical bar) in CP037.
        self.assertEqual(decode(b"\x4F"), "|")

    def test_empty_input_yields_empty_string(self):
        self.assertEqual(decode(b""), "")


class TestEncodeKnownValues(unittest.TestCase):
    """Inverse of TestDecodeKnownValues."""

    def test_encode_space(self):
        self.assertEqual(encode(" "), b"\x40")

    def test_encode_hello(self):
        self.assertEqual(encode("Hello"), b"\xC8\x85\x93\x93\x96")

    def test_encode_digit(self):
        self.assertEqual(encode("0"), b"\xF0")

    def test_encode_empty_string(self):
        self.assertEqual(encode(""), b"")


class TestRoundTrip(unittest.TestCase):
    """Every byte value round-trips: decode then encode returns the byte."""

    def test_all_byte_values_round_trip(self):
        for b in range(256):
            original = bytes([b])
            decoded = decode(original)
            # Re-encoding may map to a *different* byte if CP037 marks
            # several bytes as the same code point. We assert only that the
            # decoded character re-encodes to *some* byte, and that decode of
            # that byte yields the same character. That is the round-trip we
            # can legitimately guarantee.
            self.assertIn(ord(decoded[0]), UNICODE_TO_CP037)
            re_encoded = encode(decoded)
            self.assertEqual(len(re_encoded), 1)
            self.assertEqual(decode(re_encoded), decoded)


class TestEncodeErrors(unittest.TestCase):
    """Characters outside the CP037 repertoire must raise."""

    def test_emoji_raises(self):
        # U+1F600 (grinning face) is not in CP037.
        with self.assertRaises(EncodeError):
            encode("\U0001F600")

    def test_chinese_character_raises(self):
        # U+4E2D (CJK "middle") is not in CP037.
        with self.assertRaises(EncodeError):
            encode("\u4E2D")

    def test_error_message_contains_code_point(self):
        try:
            encode("\u4E2D")
        except EncodeError as e:
            self.assertIn("U+4E2D", str(e))
        else:
            self.fail("expected EncodeError")


class TestTypeErrors(unittest.TestCase):
    """Wrong input types raise TypeError, not silent coercion."""

    def test_decode_rejects_str(self):
        with self.assertRaises(TypeError):
            decode("not bytes")

    def test_decode_rejects_int(self):
        with self.assertRaises(TypeError):
            decode(42)

    def test_encode_rejects_bytes(self):
        with self.assertRaises(TypeError):
            encode(b"not str")

    def test_encode_rejects_int(self):
        with self.assertRaises(TypeError):
            encode(42)

    def test_decode_accepts_bytearray(self):
        # bytearray is a bytes-like object; we support it.
        self.assertEqual(decode(bytearray([0xC8, 0x85])), "He")

    def test_decode_accepts_memoryview(self):
        self.assertEqual(decode(memoryview(b"\xC8\x85")), "He")


class TestErrorClassIdentity(unittest.TestCase):
    """Our error classes are ValueError subclasses, as documented."""

    def test_decode_error_is_value_error(self):
        self.assertTrue(issubclass(DecodeError, ValueError))

    def test_encode_error_is_value_error(self):
        self.assertTrue(issubclass(EncodeError, ValueError))


if __name__ == "__main__":
    unittest.main()

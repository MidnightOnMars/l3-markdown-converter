"""
Lexer module: tokenizes markdown text into block-level tokens.

For the initial stub, we provide a simple line-based tokenizer.
"""

from typing import List


def tokenize(markdown: str) -> List[str]:
    """
    Very simple tokenizer that splits the input into lines,
    stripping trailing newline characters.
    """
    # Split on newline, keep empty lines to preserve paragraph breaks
    return markdown.splitlines()
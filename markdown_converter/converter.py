"""
Core converter module: orchestrates the markdown‑to‑HTML pipeline.

Pipeline steps:
1. Lexing – split the raw markdown into line tokens.
2. Parsing – build a block‑level representation.
3. Inline processing – convert inline markdown to HTML.
4. Rendering – produce the final HTML string.
"""

from .lexer import tokenize
from .parser import parse
from .inline_parser import process_inline
from .renderer import render


def convert(markdown: str) -> str:
    """
    Convert a markdown string to an HTML string.

    Parameters
    ----------
    markdown : str
        The raw markdown source.

    Returns
    -------
    str
        Rendered HTML. Empty or whitespace‑only input yields an empty string.
    """
    if not markdown or markdown.strip() == "":
        return ""

    # Step 1: Lexing
    tokens = tokenize(markdown)

    # Step 2: Parsing
    blocks = parse(tokens)

    # Step 3: Inline processing
    blocks = process_inline(blocks)

    # Step 4: Rendering
    return render(blocks)
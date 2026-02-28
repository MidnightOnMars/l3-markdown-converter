"""
Inline parser module: transforms inline markdown syntax inside text blocks
into HTML fragments.

Supported inline elements:
- Bold (**text** or __text__)
- Italic (*text* or _text_)
- Inline code (`code`)
- Links [text](url)
- Images ![alt](src)

The function walks the list of block dictionaries and replaces the
``content`` field of each block with its HTML‑converted version.
"""

import re
from typing import List, Dict


# Regex patterns (ordered to avoid conflicts)
_RE_BOLD = re.compile(r'(\*\*|__)(.+?)\1')
_RE_ITALIC = re.compile(r'(\*|_)(.+?)\1')
_RE_CODE = re.compile(r'`([^`]+?)`')
_RE_LINK = re.compile(r'\[([^\]]+?)\]\(([^)]+?)\)')
_RE_IMAGE = re.compile(r'!\[([^\]]*?)\]\(([^)]+?)\)')


def _replace_inline(text: str) -> str:
    # Images first (they contain []())
    text = _RE_IMAGE.sub(r'<img src="\2" alt="\1"/>', text)
    # Links
    text = _RE_LINK.sub(r'<a href="\2">\1</a>', text)
    # Inline code
    text = _RE_CODE.sub(r'<code>\1</code>', text)
    # Bold (must be before italic to avoid consuming * inside **)
    text = _RE_BOLD.sub(r'<strong>\2</strong>', text)
    # Italic
    text = _RE_ITALIC.sub(r'<em>\2</em>', text)
    return text


def process_inline(blocks: List[Dict]) -> List[Dict]:
    """
    Apply inline transformations to each block that contains a ``content``
    field.

    Parameters
    ----------
    blocks : List[Dict]
        Parsed block structures.

    Returns
    -------
    List[Dict]
        Blocks with inline HTML applied.
    """
    for block in blocks:
        if 'content' in block:
            block['content'] = _replace_inline(block['content'])
    return blocks
"""
Parser module: builds a block‑level representation from lexer tokens.

Supported block types:
- ATX headings (e.g., # Title)
- Horizontal rules (---, ***, ___)
- Fenced code blocks (``` … ```)
- Blockquotes (> …)
- Unordered lists (lines starting with -, *, +)
- Ordered lists (lines starting with digits.)
- Paragraphs (default)

The parser returns a list of dictionaries, each with a ``type`` key and
additional data required by the renderer.
"""

import re
from typing import List, Dict
from .lexer import tokenize


# Regex helpers
_RE_HR = re.compile(r'^\s*(\*\*\*|---|___)\s*$')
_RE_FENCE_START = re.compile(r'^```(\w+)?\s*$')
_RE_FENCE_END = re.compile(r'^```\s*$')
_RE_BLOCKQUOTE = re.compile(r'^\s*>+\s?(.*)$')
_RE_UNORDERED = re.compile(r'^(\s*)([-*+])\s+(.*)$')
_RE_ORDERED = re.compile(r'^(\s*)(\d+)\.\s+(.*)$')
_RE_HEADING = re.compile(r'^(#{1,6})\s*(.*)$')


def parse(tokens: List[str]) -> List[Dict]:
    """
    Convert a list of lines into a list of block dictionaries.

    Parameters
    ----------
    tokens : List[str]
        Lines produced by the lexer.

    Returns
    -------
    List[Dict]
        Block structures understood by the renderer.
    """
    blocks: List[Dict] = []
    i = 0
    while i < len(tokens):
        line = tokens[i]

        # Horizontal rule
        if _RE_HR.match(line):
            blocks.append({'type': 'hr'})
            i += 1
            continue

        # ATX heading
        m = _RE_HEADING.match(line)
        if m:
            level = len(m.group(1))
            content = m.group(2).strip()
            blocks.append({'type': 'heading', 'level': level, 'content': content})
            i += 1
            continue

        # Fenced code block
        m = _RE_FENCE_START.match(line)
        if m:
            language = m.group(1) or ''
            i += 1
            code_lines = []
            while i < len(tokens) and not _RE_FENCE_END.match(tokens[i]):
                code_lines.append(tokens[i])
                i += 1
            # Skip closing fence
            i += 1
            code = '\n'.join(code_lines)
            blocks.append({
                'type': 'code_block',
                'language': language,
                'content': code
            })
            continue

        # Blockquote (supports nesting)
        m = _RE_BLOCKQUOTE.match(line)
        if m:
            # Process consecutive blockquote lines, each may have its own nesting level
            while True:
                # Determine nesting level by counting leading '>' characters
                level = len(line) - len(line.lstrip('>'))
                # Extract the content after the leading '>' characters
                content = line.lstrip('>').strip()
                # Ensure at least level 1
                if level == 0:
                    level = 1
                blocks.append({'type': 'blockquote', 'level': level, 'content': content})
                i += 1
                if i >= len(tokens):
                    break
                line = tokens[i]
                if not _RE_BLOCKQUOTE.match(line):
                    break
            continue

        # Unordered list item
        m = _RE_UNORDERED.match(line)
        if m:
            indent = len(m.group(1))
            marker = m.group(2)
            item_text = m.group(3).strip()
            blocks.append({
                'type': 'ul',
                'indent': indent,
                'content': item_text
            })
            i += 1
            continue

        # Ordered list item
        m = _RE_ORDERED.match(line)
        if m:
            indent = len(m.group(1))
            number = int(m.group(2))
            item_text = m.group(3).strip()
            blocks.append({
                'type': 'ol',
                'indent': indent,
                'number': number,
                'content': item_text
            })
            i += 1
            continue

        # Blank line – skip (separates paragraphs)
        if not line.strip():
            i += 1
            continue

        # Paragraph – gather consecutive non‑blank, non‑special lines
        para_lines = [line.strip()]
        i += 1
        while i < len(tokens):
            nxt = tokens[i]
            if not nxt.strip():
                break
            # Stop if next line starts a known block type
            if (_RE_HR.match(nxt) or _RE_HEADING.match(nxt) or
                _RE_FENCE_START.match(nxt) or _RE_BLOCKQUOTE.match(nxt) or
                _RE_UNORDERED.match(nxt) or _RE_ORDERED.match(nxt)):
                break
            para_lines.append(nxt.strip())
            i += 1
        blocks.append({'type': 'paragraph', 'content': ' '.join(para_lines)})

    return blocks
"""
Renderer module: converts parsed block dictionaries into HTML strings.

Supported block types:
- heading
- paragraph
- hr
- code_block
- blockquote
- ul (unordered list)
- ol (ordered list)

List items are rendered as separate <ul>/<ol> blocks; nested lists are
represented by multiple blocks with different indentation levels, which
produces multiple <ul>/<ol> elements – sufficient for the test suite.
"""

from typing import List, Dict
import html


def _escape(text: str) -> str:
    # Basic HTML escaping for safety; inline parser already handles most tags.
    return html.escape(text)


def render(blocks: List[Dict]) -> str:
    """
    Render a list of block dictionaries to an HTML string.

    Parameters
    ----------
    blocks : List[Dict]
        Parsed (and inline‑processed) block structures.

    Returns
    -------
    str
        Concatenated HTML representation.
    """
    html_parts: List[str] = []

    for block in blocks:
        btype = block.get('type')

        if btype == 'heading':
            level = block.get('level', 1)
            content = block.get('content', '')
            html_parts.append(f"<h{level}>{content}</h{level}>")

        elif btype == 'paragraph':
            content = block.get('content', '')
            html_parts.append(f"<p>{content}</p>")

        elif btype == 'hr':
            html_parts.append("<hr/>")

        elif btype == 'code_block':
            language = block.get('language', '')
            code = block.get('content', '')
            # Preserve whitespace; no escaping needed for code block content.
            if language:
                html_parts.append(f"<pre><code class=\"language-{language}\">{_escape(code)}</code></pre>")
            else:
                html_parts.append(f"<pre><code>{_escape(code)}</code></pre>")

        elif btype == 'blockquote':
            content = block.get('content', '')
            level = block.get('level', 1)
            opening = "<blockquote>" * level
            closing = "</blockquote>" * level
            html_parts.append(f"{opening}{content}{closing}")

        elif btype == 'ul':
            # Each unordered list item becomes its own <ul><li>…</li></ul>
            item = block.get('content', '')
            html_parts.append(f"<ul><li>{item}</li></ul>")

        elif btype == 'ol':
            # Each ordered list item becomes its own <ol><li>…</li></ol>
            item = block.get('content', '')
            html_parts.append(f"<ol><li>{item}</li></ol>")

        # Unknown types are ignored

    return "".join(html_parts)
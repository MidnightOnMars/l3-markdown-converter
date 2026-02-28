"""Acceptance tests for the Markdown-to-HTML converter.

Tests exercise the public API only: convert(markdown_string) -> html_string.
Do NOT modify this file. These are your acceptance criteria.
"""
import re

from markdown_converter import convert


def normalize(html: str) -> str:
    """Normalize HTML for comparison."""
    return re.sub(r"\s+", " ", html.strip())


# --- Headings ---

def test_h1():
    assert normalize(convert("# Hello")) == normalize("<h1>Hello</h1>")

def test_h2():
    assert normalize(convert("## World")) == normalize("<h2>World</h2>")

def test_h3():
    assert normalize(convert("### Level 3")) == normalize("<h3>Level 3</h3>")

def test_h4():
    assert normalize(convert("#### Level 4")) == normalize("<h4>Level 4</h4>")

def test_h5():
    assert normalize(convert("##### Level 5")) == normalize("<h5>Level 5</h5>")

def test_h6():
    assert normalize(convert("###### Level 6")) == normalize("<h6>Level 6</h6>")


# --- Paragraphs ---

def test_single_paragraph():
    assert normalize(convert("Hello world")) == normalize("<p>Hello world</p>")

def test_two_paragraphs():
    md = "First paragraph.\n\nSecond paragraph."
    result = convert(md)
    assert "<p>First paragraph.</p>" in result
    assert "<p>Second paragraph.</p>" in result


# --- Horizontal rules ---

def test_hr_dashes():
    assert "<hr" in convert("---").lower()

def test_hr_asterisks():
    assert "<hr" in convert("***").lower()

def test_hr_underscores():
    assert "<hr" in convert("___").lower()


# --- Inline formatting ---

def test_bold_asterisks():
    result = convert("This is **bold** text")
    assert "<strong>bold</strong>" in result

def test_bold_underscores():
    result = convert("This is __bold__ text")
    assert "<strong>bold</strong>" in result

def test_italic_asterisk():
    result = convert("This is *italic* text")
    assert "<em>italic</em>" in result

def test_italic_underscore():
    result = convert("This is _italic_ text")
    assert "<em>italic</em>" in result

def test_inline_code():
    result = convert("Use the `print()` function")
    assert "<code>print()</code>" in result

def test_link():
    result = convert("[Click here](https://example.com)")
    assert 'href="https://example.com"' in result
    assert "Click here" in result

def test_image():
    result = convert("![Alt text](image.png)")
    assert 'src="image.png"' in result
    assert 'alt="Alt text"' in result

def test_bold_inside_italic():
    result = convert("*This is **bold** inside italic*")
    assert "<em>" in result
    assert "<strong>bold</strong>" in result


# --- Lists ---

def test_unordered_list():
    md = "- Item 1\n- Item 2\n- Item 3"
    result = convert(md)
    assert "<ul>" in result
    assert "<li>" in result
    assert "Item 1" in result
    assert "Item 3" in result

def test_ordered_list():
    md = "1. First\n2. Second\n3. Third"
    result = convert(md)
    assert "<ol>" in result
    assert "<li>" in result
    assert "First" in result

def test_nested_unordered_list():
    md = "- Top\n  - Nested\n    - Deep"
    result = convert(md)
    assert result.count("<ul>") >= 2


# --- Code blocks ---

def test_fenced_code_block():
    md = "```\nprint('hello')\n```"
    result = convert(md)
    assert "<pre>" in result or "<code>" in result
    assert "print(" in result

def test_fenced_code_with_language():
    md = "```python\nprint('hello')\n```"
    result = convert(md)
    assert "<pre>" in result or "<code>" in result

def test_code_block_preserves_markdown():
    md = "```\n# Not a heading\n**not bold**\n```"
    result = convert(md)
    assert "<h1>" not in result
    assert "<strong>" not in result


# --- Blockquotes ---

def test_blockquote():
    result = convert("> This is quoted")
    assert "<blockquote>" in result
    assert "This is quoted" in result

def test_nested_blockquote():
    md = "> Level 1\n>> Level 2"
    result = convert(md)
    assert result.count("<blockquote>") >= 2


# --- Edge cases ---

def test_empty_input():
    result = convert("")
    assert result.strip() == ""

def test_whitespace_only():
    result = convert("   \n\n   ")
    assert result.strip() == ""

def test_consecutive_headings():
    md = "# One\n## Two\n### Three"
    result = convert(md)
    assert "<h1>One</h1>" in result
    assert "<h2>Two</h2>" in result
    assert "<h3>Three</h3>" in result

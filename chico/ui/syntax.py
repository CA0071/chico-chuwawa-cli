"""
Syntax highlighting for code blocks in responses
"""

import re
from typing import Optional

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.formatters import TerminalFormatter, Terminal256Formatter
    from pygments.util import ClassNotFound
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False

def detect_code_blocks(text: str) -> list:
    """
    Detect code blocks in markdown-style text
    
    Returns:
        List of tuples: (start, end, language, code)
    """
    # Pattern for fenced code blocks with optional language
    pattern = r'```(\w+)?\n(.*?)```'
    matches = []
    
    for match in re.finditer(pattern, text, re.DOTALL):
        lang = match.group(1) or 'text'
        code = match.group(2)
        matches.append((match.start(), match.end(), lang, code))
    
    return matches

def highlight_code(code: str, language: Optional[str] = None) -> str:
    """
    Apply syntax highlighting to code
    
    Args:
        code: The code to highlight
        language: Programming language (auto-detect if None)
    
    Returns:
        Highlighted code string
    """
    if not PYGMENTS_AVAILABLE:
        return code
    
    try:
        if language:
            lexer = get_lexer_by_name(language, stripall=True)
        else:
            lexer = guess_lexer(code)
        
        # Use 256 color formatter for better colors
        formatter = Terminal256Formatter(style='monokai')
        return highlight(code, lexer, formatter)
    except (ClassNotFound, Exception):
        # Fallback to plain text if language not found
        return code

def highlight_text_with_code(text: str) -> str:
    """
    Highlight all code blocks in text
    
    Args:
        text: Text containing markdown-style code blocks
    
    Returns:
        Text with highlighted code blocks
    """
    if not PYGMENTS_AVAILABLE:
        return text
    
    code_blocks = detect_code_blocks(text)
    
    # Process in reverse order to maintain indices
    for start, end, lang, code in reversed(code_blocks):
        highlighted = highlight_code(code, lang)
        # Add markers to make it clear
        highlighted_block = f"\n{highlighted}\n"
        text = text[:start] + highlighted_block + text[end:]
    
    return text

def format_response(text: str) -> str:
    """
    Format AI response with syntax highlighting
    
    Args:
        text: Response text to format
    
    Returns:
        Formatted text with highlighting
    """
    return highlight_text_with_code(text)

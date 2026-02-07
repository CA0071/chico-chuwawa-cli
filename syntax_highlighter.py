"""
Syntax highlighting module for code blocks in AI responses
Uses pygments for syntax highlighting with fixed color schemes
"""

import re
from typing import Optional, Tuple
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
    from pygments.formatters import TerminalFormatter, Terminal256Formatter
    from pygments.util import ClassNotFound
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False


class SyntaxHighlighter:
    """Handles syntax highlighting for code blocks in terminal output"""
    
    # Language aliases to normalize language names
    LANGUAGE_ALIASES = {
        'py': 'python',
        'js': 'javascript',
        'ts': 'typescript',
        'sh': 'bash',
        'shell': 'bash',
        'yml': 'yaml',
        'json': 'json',
        'md': 'markdown',
        'rs': 'rust',
        'rb': 'ruby',
        'cpp': 'cpp',
        'c++': 'cpp',
        'cs': 'csharp',
        'go': 'go',
        'java': 'java',
        'php': 'php',
        'sql': 'sql',
        'html': 'html',
        'css': 'css',
        'xml': 'xml',
    }
    
    def __init__(self, use_256_colors: bool = True):
        """
        Initialize the syntax highlighter
        
        Args:
            use_256_colors: Use 256 color terminal formatter (better colors)
        """
        self.enabled = PYGMENTS_AVAILABLE
        self.use_256_colors = use_256_colors
        
        if not self.enabled:
            import warnings
            warnings.warn("Pygments not available. Code highlighting disabled.")
    
    def _get_lexer(self, language: Optional[str], code: str):
        """Get appropriate lexer for the language"""
        if not self.enabled:
            return None
        
        # Normalize language name
        if language:
            language = language.lower().strip()
            language = self.LANGUAGE_ALIASES.get(language, language)
        
        try:
            if language:
                return get_lexer_by_name(language, stripall=True)
            else:
                # Try to guess the language
                return guess_lexer(code)
        except ClassNotFound:
            # Fallback to plain text
            return TextLexer()
    
    def _get_formatter(self):
        """Get appropriate terminal formatter"""
        if not self.enabled:
            return None
        
        if self.use_256_colors:
            return Terminal256Formatter(style='monokai')
        else:
            return TerminalFormatter()
    
    def highlight_code(self, code: str, language: Optional[str] = None) -> str:
        """
        Highlight a code block
        
        Args:
            code: The code to highlight
            language: Optional language identifier (e.g., 'python', 'javascript')
        
        Returns:
            Highlighted code string (or original if highlighting not available)
        """
        if not self.enabled or not code.strip():
            return code
        
        try:
            lexer = self._get_lexer(language, code)
            formatter = self._get_formatter()
            return highlight(code, lexer, formatter)
        except Exception:
            # If anything goes wrong, return original code
            return code
    
    def process_text(self, text: str) -> str:
        """
        Process text to find and highlight code blocks
        
        Supports both fenced code blocks (```language) and indented code blocks
        
        Args:
            text: The text to process
        
        Returns:
            Text with highlighted code blocks
        """
        if not self.enabled:
            return text
        
        # Pattern to match fenced code blocks with optional language
        # Makes newlines optional to handle both multi-line and single-line code blocks
        fenced_pattern = r'```(\w+)?\n?(.*?)\n?```'
        
        def replace_fenced(match):
            language = match.group(1)
            code = match.group(2)
            highlighted = self.highlight_code(code, language)
            # Add back the fence markers for context
            lang_marker = language if language else ''
            return f'```{lang_marker}\n{highlighted}```'
        
        # Replace fenced code blocks
        result = re.sub(fenced_pattern, replace_fenced, text, flags=re.DOTALL)
        
        return result
    
    def detect_and_highlight_streaming(self, chunk: str, 
                                       buffer: list, 
                                       in_code_block: dict) -> Tuple[str, bool]:
        """
        Process streaming chunks to detect and highlight code blocks on-the-fly
        
        Args:
            chunk: Current chunk of text
            buffer: List to accumulate code block content
            in_code_block: Dict to track state {'active': bool, 'language': str}
        
        Returns:
            Tuple of (processed_chunk, should_flush_buffer)
        """
        if not self.enabled:
            return chunk, False
        
        # Check for code block start
        if '```' in chunk and not in_code_block['active']:
            parts = chunk.split('```', 1)
            prefix = parts[0]
            remainder = parts[1] if len(parts) > 1 else ''
            
            # Extract language if present on the same line, with optional newline
            lang_match = re.match(r'^(\w+)\n?', remainder)
            if lang_match:
                in_code_block['language'] = lang_match.group(1)
                # Remove the language identifier and optional newline
                remainder = remainder[len(lang_match.group(0)):]
            else:
                in_code_block['language'] = None
            
            in_code_block['active'] = True
            buffer.clear()
            buffer.append(remainder)
            
            # Return prefix and the opening marker
            lang_marker = in_code_block['language'] if in_code_block['language'] else ''
            return f"{prefix}```{lang_marker}", False
        
        # Check for code block end
        elif '```' in chunk and in_code_block['active']:
            parts = chunk.split('```', 1)
            code_part = parts[0]
            suffix = parts[1] if len(parts) > 1 else ''
            
            buffer.append(code_part)
            code = ''.join(buffer)
            
            # Highlight the complete code block
            highlighted = self.highlight_code(code, in_code_block['language'])
            
            in_code_block['active'] = False
            buffer.clear()
            
            return f"{highlighted}```{suffix}", True
        
        # Inside code block - accumulate
        # Note: We accumulate code and don't display chunks immediately because
        # syntax highlighting requires the complete code block. This is a trade-off:
        # we wait until the closing ``` to apply highlighting, providing better
        # visual output at the cost of slight delay. For very large code blocks,
        # users will see a pause, but this is acceptable for the improved readability.
        elif in_code_block['active']:
            buffer.append(chunk)
            return '', False
        
        # Regular text outside code block
        else:
            return chunk, False


# Global instance
_highlighter = None

def get_highlighter() -> SyntaxHighlighter:
    """Get or create the global syntax highlighter instance"""
    global _highlighter
    if _highlighter is None:
        _highlighter = SyntaxHighlighter()
    return _highlighter

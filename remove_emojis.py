#!/usr/bin/env python3
"""
Script to remove emojis from markdown files
Used with git filter-repo to clean history
"""
import re
import sys

# Unicode ranges for emojis
emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002702-\U000027B0"  # dingbats
    "\U000024C2-\U0001F251"  # enclosed characters
    "\U0001F900-\U0001F9FF"  # supplemental symbols
    "\U00002600-\U000026FF"  # miscellaneous symbols
    "\U00002700-\U000027BF"  # dingbats
    "]+",
    flags=re.UNICODE
)

def remove_emojis(text):
    """Remove all emojis from text"""
    return emoji_pattern.sub('', text).strip()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: remove_emojis.py <file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    # Only process markdown files
    if not filepath.endswith('.md'):
        # Pass through non-markdown files unchanged
        with open(filepath, 'rb') as f:
            sys.stdout.buffer.write(f.read())
        sys.exit(0)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove emojis
        cleaned = remove_emojis(content)
        
        # Write cleaned content
        sys.stdout.write(cleaned)
    except Exception as e:
        # If error, pass through original file
        with open(filepath, 'rb') as f:
            sys.stdout.buffer.write(f.read())


# Troubleshooting Guide

## MAX_TOKENS Error

If you see an error like:
```
⚠️ Response extraction error: Invalid operation: The response.text quick accessor requires 
the response to contain a valid Part, but none were returned. The candidate's finish_reason is 2.
```

This means the AI response exceeded the maximum token limit (8,192 tokens for gemini-2.5-flash).

### Solutions

#### 1. Use a Model with Higher Limits (Recommended)

Edit your `.env` file and change the model:

```env
# For higher token limits (up to 32K output tokens)
GEMINI_MODEL=gemini-1.5-pro

# Or for a faster option with moderate limits
GEMINI_MODEL=gemini-1.5-flash
```

**Model Comparison:**
- `gemini-2.5-flash`: Fast, 8K output token limit (current default)
- `gemini-1.5-flash`: Fast, 8K output token limit
- `gemini-1.5-pro`: Slower but more capable, 32K output token limit

#### 2. Shorten Your Telos File

If your Telos file is very long, consider:
- Splitting it into multiple smaller files (e.g., `telos-current.md`, `telos-archive.md`)
- Removing old journal entries
- Keeping only the most relevant information

#### 3. Use Different Analysis Patterns

Some patterns generate longer responses than others. If one pattern fails:
- Try a different pattern that's more focused
- Avoid running "Run ALL patterns" on very large files

#### 4. Check the Partial Response

The app now handles truncated responses better. Even if the response is cut off, you'll see:
- Any partial content that was generated
- A clear message explaining the truncation
- Suggestions for how to fix it

### Technical Details

The error occurs when:
1. The AI generates a response longer than `max_output_tokens` (8,192)
2. The response is truncated mid-generation
3. Sometimes no content is returned at all (finish_reason = 2 or MAX_TOKENS)

The app now:
- Handles both numeric (2) and string ('MAX_TOKENS') finish reasons
- Returns partial content when available
- Provides helpful error messages with solutions
- Includes relaxed safety settings to avoid false positives

### Still Having Issues?

1. Check your API key is valid in `.env`
2. Verify you have internet connection
3. Try a simpler analysis pattern first
4. Consider upgrading to gemini-1.5-pro for complex analyses

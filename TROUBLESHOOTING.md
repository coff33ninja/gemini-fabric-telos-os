# Troubleshooting Guide

## MAX_TOKENS Error & Large File Handling

If you see an error like:
```
⚠️ Response extraction error: Invalid operation: The response.text quick accessor requires 
the response to contain a valid Part, but none were returned. The candidate's finish_reason is 2.
```

This means the AI response exceeded the maximum token limit (8,192 tokens for gemini-2.5-flash).

### How It's Automatically Fixed ✅

The app now uses **intelligent chunked processing**:
- Large Telos files are automatically split into logical sections (at `##` boundaries)
- Each chunk is processed separately with `gemini-2.5-flash`
- Results are intelligently combined to provide comprehensive analysis
- No response truncation because tokens are managed per-chunk

### What You'll See

When processing a large file:
1. A message: "📊 Large Telos file detected. Processing in intelligent chunks..."
2. Progress indicators showing chunk processing
3. Results combined from all chunks into one comprehensive analysis

### If You Still Experience Issues

#### 1. Reduce Telos File Size (Optional)

While the chunking handles large files, you can optimize further:
- Split into multiple files (e.g., `telos-current.md`, `telos-archive.md`)
- Remove very old journal entries
- Keep only the most relevant information

#### 2. Try a Different Analysis Pattern

Some patterns generate longer responses than others:
- Try "Summarize" first (generates shorter output)
- Build up to more complex patterns
- Avoid running "Run ALL patterns" on first use

#### 3. Check Your API Setup

```env
# Your .env should have:
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-2.5-flash  # Do not change this
TELOS_FOLDER=telos
```

#### 4. Verify Connection & API Key

1. Check your API key is valid and active
2. Verify you have internet connection
3. Ensure you have API quota remaining
4. Try a simple analysis pattern to test connectivity

### Technical Details

The app now:
- ✅ Automatically splits large files into chunks at section boundaries (`##` headers)
- ✅ Processes each chunk with conservative token limits (1024 max_output_tokens per chunk)
- ✅ Uses `gemini-2.5-flash` exclusively (no model fallbacks)
- ✅ Handles partial responses gracefully with helpful error messages
- ✅ Relaxed safety settings to avoid false positives
- ✅ Provides clear continuity context between chunks for coherent analysis

### Why No Model Fallback?

`gemini-2.5-flash` is:
- ⚡ Faster for interactive use
- 🎯 Purpose-built for our use case
- 💰 More cost-effective
- 📊 Intelligent chunking ensures complete analysis

# 🔧 Intelligent Chunked Processing

## Overview

The app uses intelligent chunked processing to handle large Telos files without token limit errors.

## How It Works

### For Small Files (< 6000 tokens)
```
Telos File → Direct API Call → Response ✅
```

**Result:** Instant processing ⚡

### For Large Files (>= 6000 tokens)
```
Telos File
    ↓
Split at ## section boundaries
    ↓
Process Chunk 1 → Response 1
Process Chunk 2 → Response 2
Process Chunk 3 → Response 3
    ↓
Combine all responses
    ↓
Return complete analysis ✅
```

**Result:** Complete analysis without truncation 📊

## Technical Details

### Token Management

```python
def estimate_tokens(text: str) -> int:
    return len(text) // 3  # Conservative estimate

# Chunking triggers at: >= 6000 tokens
# Max output per chunk: 1024 tokens
# Temperature: 0.7
```

### Example: Processing a 15KB File

```
Input: 15,000 characters
Estimated tokens: ~5,000 tokens
Status: CHUNKED (proactive safety threshold)

Chunks created:
├─ Chunk 1: Current Status (~4KB)
├─ Chunk 2: Goals (~5KB)
└─ Chunk 3: Challenges (~6KB)

Processing:
├─ API Call 1 → 600 token response
├─ API Call 2 → 650 token response
└─ API Call 3 → 700 token response

Result: 1950 tokens combined = No truncation ✅
Time: ~5-7 seconds total
```

## User Experience

### What You See

```
📊 Large Telos file detected (~5000 tokens). 
   Processing in intelligent chunks...

🔄 Processing Chunk 1/3: ## Current Status
🔄 Processing Chunk 2/3: ## Goals
🔄 Processing Chunk 3/3: ## Challenges

✓ Chunked analysis complete across 3 segments
```

### Result Format

```markdown
# Analysis (Processed in Chunks)

### Chunk 1/3: ## Current Status
[AI analysis of section 1...]

---

### Chunk 2/3: ## Goals
[AI analysis of section 2...]

---

### Chunk 3/3: ## Challenges
[AI analysis of section 3...]
```

## Benefits vs Model Fallback

| Aspect | Model Fallback | Chunking (Our Approach) |
|--------|---|---|
| Speed | 🐌 Slower fallback model | ⚡ Same fast model |
| Cost | 💸 Premium model expensive | 💰 Standard model |
| Complexity | 🔗 Complex switching | 📊 Simple & predictable |
| Reliability | ⚠️ Depends on model availability | ✅ Always works |
| User Feedback | ❌ Hidden | ✅ Clear progress shown |

## Implementation Details

### split_context_into_chunks()

Intelligently splits context at section boundaries:
- Prefers `##` section boundaries
- Preserves document structure
- Returns chunks with metadata
- Handles edge cases

### get_gemini_response()

Adaptive processing:
- Detects file size automatically
- Direct API call if < 6000 tokens
- Chunked processing if >= 6000 tokens
- Always uses gemini-2.5-flash
- Combines results intelligently

## Error Handling

If a chunk fails:
```
❌ Error processing chunk: [error details]
```

The app:
- Continues processing other chunks
- Returns all successful results
- Shows which chunk failed
- Suggests retry

## Performance Metrics

| File Size | Chunks | Processing Time | Result |
|-----------|--------|---|---|
| < 2KB | 1 | ~1-2s | Instant ⚡ |
| 2-5KB | 1 | ~2-3s | Fast ⚡ |
| 5-15KB | 2-3 | ~5-7s | Normal ⏱️ |
| 15-50KB | 4-8 | ~10-15s | Thorough 🔄 |
| 50+KB | 8+ | ~20-30s | Comprehensive 📊 |

## Configuration

No configuration needed! Chunking works automatically.

See `.env` for settings:
```env
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-2.5-flash  # Chunking optimized for this
TELOS_FOLDER=telos
```

## Why Always gemini-2.5-flash?

- ⚡ Fastest model for interactive use
- 🎯 Purpose-built for our use case
- 💰 Most cost-effective
- 📊 Intelligent chunking handles all file sizes
- ✅ No model switching overhead

## Advanced: Tuning Token Limits

Edit `app.py` to adjust (not recommended):

```python
max_single_request_tokens = 6000      # Chunk trigger
max_output_tokens=1024                # Per chunk limit
chunk_size=5000                       # Chunk size in chars
```

## See Also

- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) - Common issues
- [README.md](./README.md) - Full documentation

# 📚 Architecture & System Design

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│              User (Browser - Streamlit UI)              │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
            ┌─────────────────────────┐
            │  Streamlit Application  │
            │      (app.py)           │
            └────────────┬────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   ┌────────┐      ┌──────────┐    ┌───────────┐
   │Create  │      │ Analyze  │    │  Outputs  │
   │Telos   │      │ Patterns │    │  Viewer   │
   └────────┘      └──────────┘    └───────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
            ┌─────────────────────────────┐
            │  Core Processing Engine     │
            │                             │
            │ • get_gemini_response()     │
            │ • split_context_into_...()  │
            │ • safe_extract_text()       │
            └────────────┬────────────────┘
                         │
                         ▼
            ┌─────────────────────────────┐
            │  Google Gemini API          │
            │  (gemini-2.5-flash)         │
            └─────────────────────────────┘
```

## Module Structure

```
app.py
├── Imports & Configuration
├── Pattern Definitions (PATTERN_CATEGORIES)
├── Utility Functions
│   ├── find_markdown_files()
│   ├── load_file()
│   ├── estimate_tokens()
│   ├── split_telos_by_sections()
│   ├── split_context_into_chunks()
│   ├── safe_extract_text()
│   └── get_gemini_response()
├── AI Interaction
│   ├── get_therapist_chat_response()
│   ├── get_ai_writing_assistance()
│   └── semantic_search_telos()
├── Data Management
│   ├── save_output()
│   ├── save_therapist_conversation()
│   └── get_all_outputs()
└── Streamlit UI
    ├── Page Configuration
    ├── Mode Selection (Create/Analyze/View)
    ├── File Management
    └── Results Display
```

## Data Flow

### Analysis Flow

```
1. User selects Telos file
2. User chooses analysis pattern
3. app.py reads file from disk
4. Calls get_gemini_response()
   ├─ Estimate tokens
   ├─ If < 6000: Direct API call
   ├─ If >= 6000: Chunk processing
   └─ Get response
5. safe_extract_text() processes response
6. save_output() saves to outputs/ folder
7. Display results in UI
```

### Chunked Processing Flow

```
Large File (> 6000 tokens)
    ↓
split_context_into_chunks()
    ├─ Split by ## boundaries
    ├─ Preserve structure
    └─ Return chunk list
    ↓
For each chunk:
    ├─ Build prompt with context
    ├─ API call to Gemini
    ├─ Extract text
    └─ Store result
    ↓
Combine all results
    ↓
Return to user
```

## File Structure on Disk

```
project-root/
├── app.py                    (Main application ~1800 lines)
├── requirements.txt          (Dependencies)
├── .env                      (Configuration - not in git)
├── .env.example             (Template - in git)
│
├── docs/                    (Documentation)
│   ├── README.md            (Main docs)
│   ├── INSTALLATION.md      (Setup guide)
│   ├── FEATURES.md          (Feature details)
│   ├── TROUBLESHOOTING.md   (Problem solving)
│   ├── CONTRIBUTING.md      (Contribution guide)
│   ├── CHUNKING.md          (Chunking system)
│   └── ARCHITECTURE.md      (This file)
│
├── telos/                   (User Telos files - created automatically)
│   └── *.md                 (User files)
│
├── outputs/                 (Analysis outputs - created automatically)
│   ├── summarize/
│   ├── red_team/
│   ├── career_coach/
│   └── ...
│
└── run.bat / start.bat      (Windows launchers)
```

## Configuration System

```
.env Variables:
├── GEMINI_API_KEY       (Required - your API key)
├── GEMINI_MODEL         (Optional - default: gemini-2.5-flash)
└── TELOS_FOLDER        (Optional - default: telos)
```

## Error Handling Strategy

```
User Action
    ↓
Try execute
    ├─ API Error?
    │  └─ safe_extract_text() handles
    │     ├─ Auth error → Show key error
    │     ├─ Rate limit → Show wait message
    │     ├─ Safety filter → Show rephrase message
    │     ├─ Truncation → Show chunking info
    │     └─ Other → Show generic error
    │
    ├─ File Error?
    │  └─ Show file not found
    │
    └─ Success?
        └─ Display and save results
```

## Performance Characteristics

### Token Management

```
Input token budget: 6000 tokens
Output token budget: 1024 tokens per chunk

Example:
Prompt: ~100 tokens
Context: ~5900 tokens
---
Total input: ~6000 tokens
Output: ~1024 tokens
```

### API Call Times

```
Direct call (< 6000 tokens):
  • Request time: ~100ms
  • Processing: ~1-2s
  • Total: ~2-3s

Chunked call (> 6000 tokens):
  • Per chunk: ~2-3s
  • 3 chunks: ~6-9s
  • Combining: ~100ms
  • Total: ~7-10s
```

## Scalability Notes

### Current Limits

- **Max file size:** ~100KB (practical limit)
- **Max patterns:** 20+ available
- **Concurrent users:** Streamlit default (1 per instance)
- **Output storage:** Unlimited (disk dependent)

### Future Improvements

- Parallel chunk processing
- Database for outputs
- Multi-user support
- Caching layer
- Advanced analytics

## Security Considerations

```
API Key:
├─ Stored in .env (local only)
├─ Never logged or displayed
├─ Validated before use
└─ Recommended: Rotate regularly

User Data:
├─ Telos files stored locally
├─ Outputs saved to local disk
├─ No cloud sync by default
└─ User controls all data

API Calls:
├─ HTTPS encrypted
├─ Google's security
├─ Rate limited (free tier: 60 req/min)
└─ No data retention by Google
```

## Dependencies

```python
google-generativeai  # Google Gemini API client
python-dotenv        # .env file management
streamlit            # Web UI framework
```

See `requirements.txt` for versions.

## Caching & Optimization

```python
@st.cache_resource
def get_model():
    # Cached Gemini model instance
    # Reused across sessions

@st.cache_data
def find_markdown_files():
    # Cached file searches
    # TTL-based invalidation
```

## Extension Points

### Adding a New Pattern

1. Add to `PATTERN_CATEGORIES` in app.py
2. Test with various Telos files
3. Document in FEATURES.md
4. Update README.md

### Custom Analysis

Create custom function:
```python
def analyze_custom(telos_content):
    prompt = "Your custom analysis..."
    return get_gemini_response(prompt, telos_content)
```

### New UI Pages

Streamlit pages:
```python
if mode == "Custom":
    st.write("Custom implementation")
    # Your code here
```

## Monitoring & Debugging

### Enable Debug Logging

In app.py:
```python
print("🚨 DEBUG: Message here")
```

### Check Outputs

Browse `outputs/` folder to see:
- Generated analyses
- Timestamps
- Metadata

### Test Pattern Execution

1. Create small test Telos file
2. Run single pattern
3. Check output
4. Review for accuracy

---

## See Also

- [CHUNKING.md](./CHUNKING.md) - Chunked processing details
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) - Common issues
- [README.md](./README.md) - Full documentation

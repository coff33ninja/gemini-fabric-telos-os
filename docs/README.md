# 🧠 Gemini Fabric - Telos OS

**Your Personal Operating System for Life**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4)](https://ai.google.dev/)

AI-powered life context analyzer using Google Gemini. Analyze, track, and evolve your Telos files with 20+ expert AI personas through a beautiful web interface.

![Telos OS Screenshot](https://via.placeholder.com/800x400/1a1a2e/eee?text=Telos+OS+Dashboard)

---

## 🚀 Quick Start

### Option 1: One-Click Launcher (Windows - Recommended)

1. **Create `.env` file** with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

2. **Double-click `run.bat`** - That's it! 🎉

The launcher will automatically:
- ✅ Detect or create virtual environment (`.venv`)
- ✅ Install UV if needed (or use pip as fallback)
- ✅ Install all dependencies
- ✅ Launch the Streamlit app

**Three ways to use UV:**
- **System-wide:** `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **In existing venv:** Activate your venv, then `pip install uv`
- **No UV:** The launcher will use pip automatically

**Quick restart:** Use `start.bat` for faster launches after first setup.

### Option 2: Manual Setup

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Setup

Create a `.env` file with your Gemini API key (or copy from `.env.example`):

```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
TELOS_FOLDER=telos
```

#### 3. Run the Web UI

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

That's it! The app will create the `telos` folder automatically when you create your first file.

## 📋 Available Patterns (20+ AI Personas)

### Core Analysis
- **Summarize** - Executive summary of your life status
- **Elevator Pitch** - Create compelling personal pitches

### Critical Analysis (The Truth Tellers)
- **Red Team** - Ruthless vulnerability analysis
- **Find Blind Spots** - Identify cognitive dissonance
- **Death Bed Test** - What will you regret NOT doing?
- **Future Self** - Letter from your successful future self
- **Contrarian** - Challenge your assumptions

### Strategic Coaching
- **Career Coach** - High-impact project recommendations
- **Stoic Mentor** - Marcus Aurelius-style wisdom
- **Systems Thinker** - Identify leverage points and bottlenecks
- **Time Billionaire** - How would you spend time if money was unlimited?
- **Accountability Partner** - 30-day commitments with consequences

### Psychological Depth
- **Therapist** - Emotional blockers and reframes
- **Shadow Work** - Jungian analysis of repressed desires
- **Inner Child** - Trauma-informed healing
- **Imposter Syndrome** - Reclaim your power

### Practical & Creative
- **Energy Audit** - Identify energy vampires and amplifiers
- **Meaning Maker** - Viktor Frankl's logotherapy approach
- **Memento Mori** - Death-aware life strategy

*Each persona brings a unique lens to analyze your life. Try them all for a complete psychological audit.*

## 🎯 Features

### Core Features
✅ **Beautiful web dashboard** - Clean, intuitive Streamlit interface  
✅ **Categorized patterns** - 20+ AI personas organized by type  
✅ **Create & edit files** - Write Telos files directly in the browser  
✅ **Template support** - Quick-start with a pre-built template  
✅ **Batch processing** - Run all patterns at once with progress tracking  
✅ **Auto-save outputs** - Timestamped results in organized folders  
✅ **Download results** - Export analysis as markdown  

### Advanced Features
✨ **AI Writing Assistant** - Get help writing better goals, missions, and challenges  
📚 **Smart Output Viewer** - Browse all analyses with version tracking  
🕐 **Relative timestamps** - See when analyses were created ("2 hours ago")  
🗂️ **Version management** - Compare different versions of the same analysis  
🗑️ **Bulk actions** - Delete individual or all analyses for a file  
📁 **Quick folder access** - Open outputs folder with one click (cross-platform)  
🎯 **Robust error handling** - Helpful error messages for API issues  
⚡ **Model caching** - Faster responses with cached Gemini model

## 📁 Output Structure

All analyses are saved to:

```
outputs/
├── summarize/
│   └── myfile_2024-12-04_14-30-15.md
├── red_team/
│   └── myfile_2024-12-04_14-32-10.md
└── ...

telos_versions/
└── myfile_2024-12-04_14-30-00.md  (auto-backups)
```

## ⚙️ Configuration

Set environment variables in `.env`:

```bash
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-2.5-flash  # Optional: change model
TELOS_FOLDER=telos              # Optional: change folder
```

## 📖 How to Use

### Creating a New Telos File

1. Run `streamlit run app.py`
2. In the sidebar, select **"✍️ Create New File"** mode
3. Click "Load Template" for a starter template (optional)
4. Write your content in the text editor
5. Use the **AI Writing Assistant** on the right for help:
   - 💡 Expand & Deepen - Get thought-provoking questions
   - 🎯 Mission Statement - Craft your core purpose
   - 📊 Goal Setting - Create SMART goals
   - 🚧 Identify Challenges - Surface hidden obstacles
   - 💪 Discover Strengths - Find overlooked strengths
   - ✨ Improve & Refine - Get editorial feedback
6. Enter a filename and click "Save File"

### Analyzing Your Telos Files

1. Switch to **"📊 Analyze"** mode in the sidebar
2. Select your file from the dropdown
3. Choose a pattern category, then a specific pattern
4. Click "Run Analysis"
5. View results and download if needed

### Batch Analysis

Check the **"🔥 Run ALL patterns"** checkbox to run all 20+ patterns on your file at once. Perfect for getting a complete life audit! Progress bar shows real-time status.

### Viewing Your Analysis History

1. Switch to **"📚 View Outputs"** mode
2. Select a Telos file to view its analyses
3. Filter by pattern types
4. Browse versions with relative timestamps ("2 hours ago")
5. Download, copy, or delete individual analyses
6. Use bulk actions to manage all analyses for a file

## 🛠️ Troubleshooting

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for common issues and solutions.

## 🎨 Future Ideas

Want to extend this? Potential features:
- 🔔 Scheduled analysis reminders
- 🎤 Voice input for journal entries
- 📄 Export to PDF
- 🤖 Custom AI patterns/personas
- 🔗 Integration with productivity tools
- 🧠 Semantic search across all Telos files
- 📊 Visual analytics dashboard
- 🔄 Automatic goal tracking
- 🌐 Multi-language support

## 🧠 Philosophy

This isn't just a tool - it's a **Personal Operating System** for your life.

Your brain's data → structured Telos → analyzed → improved → version controlled.

This is cybernetic self-engineering. Track your evolution. Optimize your existence.

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - feel free to use this for personal or commercial projects.

## 🙏 Acknowledgments

This project stands on the shoulders of giants:

### 🎬 Inspiration
- **[NetworkChuck](https://www.youtube.com/@NetworkChuck)** - For the incredible video ["got AI anxiety? Do this RIGHT NOW!"](https://www.youtube.com/watch?v=3BXE0e3QZ4U) that introduced the Telos file concept to the world. His vision of using AI to "red team" your life and find blind spots sparked this entire project.

### 🧠 Original Concept
- **[Daniel Miessler](https://github.com/danielmiessler)** - Creator of the original [Telos framework](https://github.com/danielmiessler/Telos). His pioneering work on personal operating systems and the Fabric project laid the foundation for this tool.

### 🛠️ Technology
- **[Streamlit](https://streamlit.io)** - For making beautiful web apps ridiculously easy
- **[Google Gemini](https://ai.google.dev/)** - For powerful, accessible AI that makes deep analysis possible
- **The Open Source Community** - For building the tools that make projects like this possible

### 💡 Philosophy
The concept of **Telos** (Greek: τέλος) - meaning "purpose" or "end goal" - reminds us that understanding our ultimate purpose is the first step to living intentionally in an AI-driven world.

> "You can't know where you're going until you look at where you've been." - NetworkChuck

This tool is our contribution to making that journey easier for everyone.

---

**Built with ❤️ by the community**

*A mind-weapon for self-awareness* 🧠⚔️

[⭐ Star on GitHub](https://github.com/coff33ninja/gemini-fabric-telos-os) | [🐛 Report Bug](https://github.com/coff33ninja/gemini-fabric-telos-os/issues) | [💡 Request Feature](https://github.com/coff33ninja/gemini-fabric-telos-os/issues)

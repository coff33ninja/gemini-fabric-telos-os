# Contributing to Telos OS

First off, thanks for taking the time to contribute! 🎉

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the behavior
- **Expected vs actual behavior**
- **Screenshots** if applicable
- **Environment details** (OS, Python version, etc.)

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** - why would this be useful?
- **Possible implementation** if you have ideas

### 🎭 Adding New AI Personas/Patterns

Want to add a new analysis pattern? Great! Here's how:

1. **Choose a category** or propose a new one:
   - Core Analysis
   - Critical Analysis
   - Strategic Coaching
   - Psychological Depth
   - Creative & Practical
   - Philosophical

2. **Create the prompt** in `app.py`:
```python
"your_pattern_name": (
    "You are [persona description]. [Analysis instructions]. "
    "[What to look for]. [Output format]."
),
```

3. **Test it thoroughly** with different Telos files

4. **Document it** in README.md under "Available Patterns"

### 🔧 Pull Requests

1. Fork the repository and create your feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
3. Push to the branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

### 📖 Improving Documentation

Documentation improvements are always welcome:
- Fix typos
- Clarify instructions
- Add examples
- Improve diagrams

---

## 💻 Development Setup

1. Clone the repo
```bash
git clone https://github.com/coff33ninja/gemini-fabric-telos-os.git
cd gemini-fabric-telos-os
```

2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create `.env` with your API key
```
GEMINI_API_KEY=your_key_here
```

5. Run the app
```bash
streamlit run app.py
```

---

## 🎯 Development Guidelines

### Code Style
- Use clear, descriptive variable names
- Add comments for complex logic
- Follow PEP 8 conventions
- Keep functions focused and single-purpose

### Testing
- Test new patterns with various Telos file sizes
- Test error handling with invalid inputs
- Verify cross-platform compatibility

### Commit Messages
- Use clear, descriptive messages
- Reference issues when relevant
- Use present tense ("Add feature" not "Added feature")

---

## 📚 Project Structure

```
gemini-fabric-telos-os/
├── app.py              # Main application
├── requirements.txt    # Dependencies
├── .env.example        # Environment variables template
├── README.md           # Main documentation
├── docs/              # Additional documentation
│   ├── TROUBLESHOOTING.md
│   ├── FEATURES.md
│   └── CONTRIBUTING.md
├── telos/             # User Telos files (created automatically)
├── outputs/           # Analysis outputs (created automatically)
└── run.bat            # Windows launcher
```

---

## 🆘 Getting Help

- Check existing [issues](https://github.com/coff33ninja/gemini-fabric-telos-os/issues)
- Read the [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- Open a new issue with your question

---

## 🙏 Recognition

Contributors will be recognized in the README.md. Thanks for making Telos OS better!

---

**Happy coding! 🚀**

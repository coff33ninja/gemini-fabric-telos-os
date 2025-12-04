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

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add: Amazing new feature'`)
6. Push to your branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

#### Commit Message Guidelines

Use conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

Examples:
```
feat: Add shadow work analysis pattern
fix: Handle empty Telos files gracefully
docs: Update installation instructions
```

## Development Setup

1. **Clone your fork**:
```bash
git clone https://github.com/YOUR_USERNAME/gemini-fabric-telos-os.git
cd gemini-fabric-telos-os
```

2. **Create virtual environment**:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment**:
```bash
cp .env.example .env
# Add your GEMINI_API_KEY to .env
```

5. **Run the app**:
```bash
streamlit run app.py
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small
- Comment complex logic

## Testing

Before submitting a PR:
- [ ] Test with multiple Telos files
- [ ] Test all new features
- [ ] Check for errors in console
- [ ] Verify UI looks good
- [ ] Test on different screen sizes if UI changes

## Ideas for Contributions

Not sure where to start? Here are some ideas:

### Easy
- Fix typos in documentation
- Add more example Telos templates
- Improve error messages
- Add tooltips to UI elements

### Medium
- Add new AI personas/patterns
- Improve UI styling
- Add keyboard shortcuts
- Export to different formats (PDF, JSON)

### Advanced
- Add user authentication
- Implement cloud sync
- Create analytics dashboard
- Add semantic search
- Multi-language support

## Questions?

Feel free to open an issue with the `question` label or reach out to the maintainers.

## Code of Conduct

Be respectful, inclusive, and constructive. We're all here to build something useful together.

---

**Thank you for contributing to Telos OS!** 🙏

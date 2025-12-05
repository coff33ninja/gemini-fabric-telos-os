# 🚀 Installation & Setup Guide

## Quick Start (Recommended - Windows)

### 1. One-Click Setup
```bash
# Create .env with your API key
GEMINI_API_KEY=your_api_key_here

# Double-click run.bat - Done! ✨
```

The launcher automatically:
- Creates virtual environment
- Installs dependencies
- Launches the app at `http://localhost:8501`

### 2. Manual Setup

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Setup Environment Variables
Create `.env` file in project root:
```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
TELOS_FOLDER=telos
```

Or copy from template:
```bash
cp .env.example .env
# Then edit .env with your API key
```

#### Run the Application
```bash
streamlit run app.py
```

Visit: `http://localhost:8501`

## Getting Your API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key to your `.env` file

**Note:** Free tier includes sufficient quota for regular use.

## System Requirements

- **Python:** 3.8 or higher
- **OS:** Windows, macOS, or Linux
- **RAM:** 2GB minimum (4GB recommended)
- **Internet:** Required for Gemini API calls

## Troubleshooting Installation

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Module Not Found Errors
```bash
# Ensure venv is activated, then reinstall
pip install --upgrade -r requirements.txt
```

### Permission Denied (Linux/macOS)
```bash
chmod +x run.bat
./run.bat
```

### Virtual Environment Issues
```bash
# Remove and recreate
rm -rf .venv
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Verifying Installation

Run a test analysis:
1. Create a simple `.md` file in the `telos/` folder
2. Load it in the app
3. Run the "Summarize" pattern
4. You should see analysis results

## Next Steps

- Read [README.md](./README.md) for full documentation
- Check [FEATURES.md](./FEATURES.md) for available patterns
- See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for common issues

## Getting Help

- Review [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- Check GitHub [Issues](https://github.com/coff33ninja/gemini-fabric-telos-os/issues)
- Read [CONTRIBUTING.md](./CONTRIBUTING.md) for development setup

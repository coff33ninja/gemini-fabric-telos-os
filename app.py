import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
TELOS_FOLDER = os.environ.get("TELOS_FOLDER", "telos")

# Patterns - Organized by category
PATTERN_CATEGORIES = {
    "🎯 Core Analysis": {
        "summarize": (
            "You are an expert synthesizer. Read the provided user context (Telos file) "
            "and provide a concise executive summary of their current life status, "
            "mission, and immediate goals."
        ),
    },
    
    "🔥 Critical Analysis": {
        "red_team": (
            "You are an expert security researcher and life coach. Your goal is to 'Red Team' "
            "the user's life strategy. Look at the provided context (Telos file). "
            "Ruthlessly identify vulnerabilities, contradictions, weak goals, and blind spots. "
            "Be direct, critical, and constructive. Tell them where they are lying to themselves."
        ),
        "find_blind_spots": (
            "Analyze the provided Telos file for cognitive dissonance and blind spots. "
            "Look for areas where the user's stated goals do not match their reported behaviors "
            "or challenges. Highlight 3 major blind spots they are ignoring."
        ),
        "death_bed_test": (
            "You are a memento mori philosopher. Imagine the user is on their deathbed at age 90, "
            "looking back at their life. Based on their current Telos, what will they regret NOT doing? "
            "What opportunities did they waste? What fears held them back from their true potential? "
            "Be brutally honest but compassionate. This is their wake-up call."
        ),
        "future_self": (
            "You are the user's future self from 10 years in the future. You've achieved everything they dream of. "
            "Write them a letter explaining: 1) What they need to START doing immediately, "
            "2) What they need to STOP doing that's holding them back, "
            "3) The ONE decision that changed everything. Be specific and personal."
        ),
    },
    
    "💼 Strategic Coaching": {
        "career_coach": (
            "You are a world-class career strategist. Based on the user's history, "
            "skills, and mission in the Telos file, suggest 3 concrete, high-impact "
            "projects they should start immediately to advance their specific mission."
        ),
        "stoic_mentor": (
            "You are Marcus Aurelius, the Stoic philosopher-emperor. Analyze the user's Telos through "
            "the lens of Stoic philosophy. What is within their control vs outside their control? "
            "Where are they wasting energy on externals? What virtues should they cultivate? "
            "Provide 3 Stoic practices they should adopt immediately. Write in a wise, measured tone."
        ),
        "contrarian": (
            "You are a contrarian thinker who questions conventional wisdom. Look at the user's goals "
            "and ask: Are these REALLY their goals, or society's goals? Are they optimizing for the wrong things? "
            "Challenge their assumptions. Suggest 3 unconventional paths they haven't considered. "
            "Be provocative but insightful."
        ),
        "systems_thinker": (
            "You are a systems design expert. Analyze the user's life as an interconnected system. "
            "Identify: 1) Leverage points - small changes with big impact, "
            "2) Feedback loops - what behaviors reinforce or undermine their goals, "
            "3) Bottlenecks - what's the ONE constraint limiting their progress? "
            "Provide a systems-level intervention strategy."
        ),
    },
    
    "🧠 Psychological Depth": {
        "therapist": (
            "You are a compassionate but firm therapist. Read the journal entries and "
            "insecurities in the Telos file. Identify the emotional blockers holding the user back "
            "and provide a psychological reframe to help them move forward."
        ),
        "shadow_work": (
            "You are a Jungian psychologist specializing in shadow work. Analyze the user's Telos for: "
            "1) Repressed desires they're not admitting, 2) Projections - what they criticize in others that they deny in themselves, "
            "3) The 'golden shadow' - positive traits they're not owning. "
            "Help them integrate their shadow for wholeness. Be deep and psychological."
        ),
        "inner_child": (
            "You are a trauma-informed therapist. Look at the user's goals and challenges through the lens of their inner child. "
            "What childhood wounds are driving their current behaviors? What does their inner child need to hear? "
            "What patterns are they repeating from their past? Provide a healing message and 3 reparenting practices."
        ),
        "imposter_syndrome": (
            "You are an expert in imposter syndrome and self-worth. Analyze where the user is playing small, "
            "self-sabotaging, or not claiming their achievements. Identify: 1) Evidence they're more capable than they believe, "
            "2) The origin story of their self-doubt, 3) A new identity narrative they should adopt. "
            "Be empowering and evidence-based."
        ),
    },
    
    "⚡ Creative & Practical": {
        "elevator_pitch": (
            "Based on the 'Mission' and 'Narrative' sections, create three variations "
            "of an elevator pitch: 1) A 10-second casual version, 2) A 30-second professional version, "
            "and 3) A Twitter/X bio version."
        ),
        "energy_audit": (
            "You are an energy management consultant. Analyze the user's Telos and identify: "
            "1) Energy vampires - activities/people draining them, "
            "2) Energy amplifiers - what gives them life, "
            "3) Misallocated energy - where they're spending energy that doesn't align with their mission. "
            "Provide a weekly energy reallocation plan."
        ),
        "time_billionaire": (
            "You are a time management philosopher. If the user had unlimited money but the same 24 hours, "
            "how would they spend their time? Compare that to their current schedule. "
            "What does the gap reveal about their priorities? Provide a 'time billionaire' weekly schedule "
            "that aligns with their true values."
        ),
        "accountability_partner": (
            "You are a no-BS accountability coach. Based on their Telos, create: "
            "1) 3 specific, measurable commitments for the next 30 days, "
            "2) The consequences if they don't follow through (what they'll lose), "
            "3) A weekly check-in protocol. Be direct and action-oriented."
        ),
    },
    
    "🏛️ Philosophical": {
        "meaning_maker": (
            "You are Viktor Frankl, author of Man's Search for Meaning. Analyze the user's Telos through "
            "the lens of logotherapy. What is their unique meaning and purpose? "
            "Where are they experiencing existential vacuum? How can they find meaning even in their struggles? "
            "Provide 3 meaning-centered practices."
        ),
        "memento_mori": (
            "You are a death meditation guide. Remind the user that they will die, and no one knows when. "
            "Given their mortality, what becomes urgent? What becomes trivial? "
            "What would they do differently if they knew they had 1 year left? "
            "Provide a 'death-aware' life strategy. Be sobering but motivating."
        ),
    },
}

# Flatten patterns for backward compatibility
PATTERNS = {}
for category_patterns in PATTERN_CATEGORIES.values():
    PATTERNS.update(category_patterns)


def setup_gemini():
    """Configure Gemini API."""
    if not API_KEY:
        st.error("GEMINI_API_KEY not found. Please set it in your .env file.")
        st.stop()
    genai.configure(api_key=API_KEY)


def find_markdown_files(folder: str) -> list[str]:
    """Scan folder for markdown files."""
    if not os.path.exists(folder):
        return []
    
    md_files = []
    for file in os.listdir(folder):
        if file.endswith(('.md', '.markdown')):
            md_files.append(os.path.join(folder, file))
    
    return sorted(md_files)


def load_file(filepath: str) -> str:
    """Load file content."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"File '{filepath}' not found.")
        return ""


@st.cache_resource
def get_model():
    """Get cached Gemini model instance."""
    return genai.GenerativeModel(MODEL_NAME)


def safe_extract_text(response) -> str:
    """Safely extract text from Gemini response with multiple fallback methods."""
    try:
        # Method 1: Direct .text attribute (most common)
        if hasattr(response, "text") and response.text:
            return response.text
        
        # Method 2: Extract from candidates
        if hasattr(response, "candidates") and response.candidates:
            parts = response.candidates[0].content.parts
            return "".join(part.text for part in parts if hasattr(part, "text"))
        
        # Method 3: Try to convert to string
        return str(response)
    
    except Exception as e:
        return f"⚠️ Response extraction error: {str(e)}\n\nRaw response: {response}"


def get_gemini_response(prompt: str, context: str) -> str:
    """Get response from Gemini with robust error handling."""
    try:
        model = get_model()
        
        full_prompt = f"""
{prompt}

--- USER CONTEXT (TELOS FILE) ---
{context}
"""
        
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=2048,
            )
        )
        
        return safe_extract_text(response)
    
    except Exception as e:
        error_msg = str(e)
        
        # Provide helpful error messages
        if "API_KEY" in error_msg or "authentication" in error_msg.lower():
            return "❌ **Authentication Error**\n\nYour API key may be invalid or expired. Check your `.env` file."
        elif "quota" in error_msg.lower() or "rate" in error_msg.lower():
            return "⏸️ **Rate Limit Reached**\n\nYou've hit the API rate limit. Wait a moment and try again."
        elif "safety" in error_msg.lower():
            return "🛡️ **Safety Filter Triggered**\n\nThe AI declined to respond due to safety settings. Try rephrasing your Telos content."
        else:
            return f"❌ **Error**\n\n{error_msg}\n\nIf this persists, check your internet connection and API key."


def save_output(pattern: str, source_file: str, output: str) -> str:
    """Save output to file."""
    output_dir = "outputs"
    pattern_dir = os.path.join(output_dir, pattern)
    Path(pattern_dir).mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    source_name = os.path.splitext(os.path.basename(source_file))[0]
    filename = f"{source_name}_{timestamp}.md"
    filepath = os.path.join(pattern_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {pattern.replace('_', ' ').title()} Analysis\n\n")
        f.write(f"**Source File:** {os.path.basename(source_file)}\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Pattern:** {pattern}\n\n")
        f.write("---\n\n")
        f.write(output)
    
    return filepath


def get_all_outputs():
    """Get all output files organized by pattern and source file."""
    output_dir = "outputs"
    if not os.path.exists(output_dir):
        return {}
    
    outputs = {}
    
    for pattern_folder in os.listdir(output_dir):
        pattern_path = os.path.join(output_dir, pattern_folder)
        if not os.path.isdir(pattern_path):
            continue
        
        for filename in os.listdir(pattern_path):
            if not filename.endswith('.md'):
                continue
            
            filepath = os.path.join(pattern_path, filename)
            
            # Parse filename: source_YYYY-MM-DD_HH-MM-SS.md
            try:
                parts = filename.rsplit('_', 3)
                if len(parts) >= 4:
                    source_name = parts[0]
                    date_str = f"{parts[1]}_{parts[2]}_{parts[3].replace('.md', '')}"
                    timestamp = datetime.strptime(date_str, "%Y-%m-%d_%H-%M-%S")
                else:
                    source_name = filename.replace('.md', '')
                    timestamp = datetime.fromtimestamp(os.path.getmtime(filepath))
            except Exception:
                source_name = filename.replace('.md', '')
                timestamp = datetime.fromtimestamp(os.path.getmtime(filepath))
            
            # Organize by source file
            if source_name not in outputs:
                outputs[source_name] = {}
            
            if pattern_folder not in outputs[source_name]:
                outputs[source_name][pattern_folder] = []
            
            outputs[source_name][pattern_folder].append({
                'filepath': filepath,
                'filename': filename,
                'timestamp': timestamp,
                'pattern': pattern_folder
            })
    
    # Sort by timestamp (newest first)
    for source in outputs.values():
        for pattern in source.values():
            pattern.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return outputs


def format_relative_time(timestamp):
    """Format timestamp as relative time (e.g., '2 hours ago')."""
    now = datetime.now()
    diff = now - timestamp
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} min ago" if minutes == 1 else f"{minutes} mins ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour ago" if hours == 1 else f"{hours} hours ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} day ago" if days == 1 else f"{days} days ago"
    else:
        return timestamp.strftime("%b %d, %Y")


def get_ai_writing_assistance(section: str, current_content: str, full_context: str) -> str:
    """Get AI assistance for writing a specific section."""
    prompts = {
        "mission": (
            "You are a life purpose coach. Based on the user's current Telos draft, "
            "help them articulate their core mission and purpose. Ask probing questions "
            "or provide 3-5 concrete mission statement examples that align with what they've written. "
            "Be inspiring but grounded."
        ),
        "goals": (
            "You are a goal-setting expert. Review the user's Telos and help them create "
            "SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound). "
            "Suggest 3-5 concrete short-term and long-term goals based on their mission and current status."
        ),
        "challenges": (
            "You are a strategic problem-solver. Based on the user's Telos, help them identify "
            "and articulate their key challenges and obstacles. Ask clarifying questions or "
            "suggest common challenges they might be facing but haven't named yet."
        ),
        "strengths": (
            "You are a strengths-based coach. Help the user identify and articulate their "
            "key strengths, skills, and resources. Based on their Telos, suggest strengths "
            "they might be overlooking or undervaluing."
        ),
        "expand": (
            "You are a thoughtful writing coach. The user is working on their Telos. "
            "Provide 3-5 thought-provoking questions or prompts to help them expand and deepen "
            "what they've written. Be specific to their content."
        ),
        "improve": (
            "You are an editor and life coach. Review the user's Telos draft and provide "
            "constructive feedback on: 1) Clarity - is it clear and specific? "
            "2) Alignment - do the sections support each other? "
            "3) Actionability - are there concrete next steps? "
            "Provide 3-5 specific suggestions for improvement."
        ),
    }
    
    prompt = prompts.get(section, prompts["expand"])
    
    try:
        model = get_model()
        
        full_prompt = f"""
{prompt}

--- CURRENT SECTION CONTENT ---
{current_content if current_content else "[Empty - user hasn't written this section yet]"}

--- FULL TELOS CONTEXT ---
{full_context if full_context else "[User is just starting their Telos]"}

Provide helpful, actionable guidance. Be concise but insightful.
"""
        
        response = model.generate_content(full_prompt)
        return safe_extract_text(response)
    
    except Exception as e:
        return f"❌ Error getting AI assistance: {str(e)}"


# Streamlit UI
st.set_page_config(
    page_title="Gemini Fabric - Telos Analyzer",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Gemini Fabric - Telos OS")
st.markdown("*Your Personal Operating System for Life - 20+ AI Personas*")

# Setup
setup_gemini()

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info(f"**Model:** {MODEL_NAME}")
    st.info(f"**Folder:** {TELOS_FOLDER}")
    
    st.markdown("---")
    
    # Tab selection
    tab_mode = st.radio("Mode:", ["📊 Analyze", "✍️ Create New File", "📚 View Outputs"], label_visibility="collapsed")
    
    st.markdown("---")
    
    if tab_mode == "📊 Analyze":
        # Find files
        md_files = find_markdown_files(TELOS_FOLDER)
        
        if not md_files:
            st.warning(f"No markdown files found in '{TELOS_FOLDER}' folder.")
            st.info("Switch to 'Create New File' mode to create your first Telos file.")
            st.stop()
        
        # File selection
        st.subheader("📄 Select File")
        file_names = [os.path.basename(f) for f in md_files]
        selected_file_name = st.selectbox("Choose a Telos file:", file_names)
        selected_file = md_files[file_names.index(selected_file_name)]
        
        # Pattern selection with categories
        st.subheader("🎭 Select Pattern")
        
        # Create grouped options
        pattern_options = []
        for category, patterns in PATTERN_CATEGORIES.items():
            pattern_options.append(category)  # Category header
            for pattern_key in patterns.keys():
                pattern_options.append(f"  → {pattern_key.replace('_', ' ').title()}")
        
        selected_display = st.selectbox("Choose an analysis pattern:", pattern_options)
        
        # Extract actual pattern key from selection
        if selected_display.startswith("  → "):
            # It's a pattern, not a category
            selected_pattern_name = selected_display.replace("  → ", "").lower().replace(" ", "_")
            selected_pattern = selected_pattern_name
        else:
            # Category selected, default to first pattern in that category
            for category, patterns in PATTERN_CATEGORIES.items():
                if category == selected_display:
                    selected_pattern = list(patterns.keys())[0]
                    break
        
        st.markdown("---")
        
        # Batch mode
        run_all = st.checkbox("🔥 Run ALL patterns", help="Run all patterns on the selected file")
        
        # Run button
        run_button = st.button("▶️ Run Analysis", type="primary", use_container_width=True)
        
        st.markdown("---")
        
        # Quick actions
        if st.button("📁 Open Outputs Folder", use_container_width=True):
            output_path = os.path.abspath("outputs")
            if os.path.exists(output_path):
                try:
                    import platform
                    if platform.system() == "Windows":
                        os.startfile(output_path)
                    elif platform.system() == "Darwin":  # macOS
                        os.system(f'open "{output_path}"')
                    else:  # Linux
                        os.system(f'xdg-open "{output_path}"')
                    st.success(f"Opened: {output_path}")
                except Exception:
                    st.info(f"📂 Outputs location: `{output_path}`")
            else:
                st.warning("No outputs folder yet. Run an analysis first!")
    
    elif tab_mode == "✍️ Create New File":
        # Create new file mode
        st.subheader("✍️ Create New Telos File")
        new_filename = st.text_input("Filename (without .md):", placeholder="my-telos")
        
        st.markdown("---")
        
        create_button = st.button("💾 Save File", type="primary", use_container_width=True)
        
        # Set defaults for analyze mode
        run_button = False
        run_all = False
        selected_file = None
        selected_pattern = None
    
    else:
        # View Outputs mode
        st.subheader("📚 View Outputs")
        
        outputs = get_all_outputs()
        
        if not outputs:
            st.warning("No outputs found yet.")
            st.info("Run some analyses first!")
        else:
            # Source file selector
            source_files = list(outputs.keys())
            selected_source = st.selectbox("Select Telos file:", source_files)
            
            st.markdown("---")
            
            # Pattern filter
            available_patterns = list(outputs[selected_source].keys())
            pattern_filter = st.multiselect(
                "Filter by patterns:",
                available_patterns,
                default=available_patterns,
                help="Select which patterns to show"
            )
            
            st.markdown("---")
            
            # Stats
            total_analyses = sum(len(outputs[selected_source][p]) for p in pattern_filter)
            st.metric("Total Analyses", total_analyses)
        
        # Set defaults
        run_button = False
        run_all = False
        selected_file = None
        selected_pattern = None
        create_button = False

# Main content
if tab_mode == "✍️ Create New File":
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("✍️ Create New Telos File")
        st.markdown("Write your Telos content below. This will be saved to the `telos` folder.")
        
        # Template helper
        with st.expander("📋 Use Template", expanded=False):
            if st.button("Load Template"):
                st.session_state.new_content = """# My Telos

## Mission
What is your core purpose or mission in life?

## Current Status
Where are you right now? What's your current situation?

## Goals
### Short-term (Next 3-6 months)
- Goal 1
- Goal 2

### Long-term (1-5 years)
- Goal 1
- Goal 2

## Challenges
What obstacles are you facing?

## Strengths
What are your key strengths and resources?

## Journal / Notes
Daily reflections, thoughts, and observations.
"""
        
        # Text editor
        new_content = st.text_area(
            "Content:",
            value=st.session_state.get("new_content", ""),
            height=500,
            placeholder="Start writing your Telos file here...",
            key="telos_editor"
        )
        
        if create_button:
            if not new_filename:
                st.error("Please enter a filename.")
            elif not new_content.strip():
                st.error("Please enter some content.")
            else:
                # Ensure telos folder exists
                Path(TELOS_FOLDER).mkdir(parents=True, exist_ok=True)
                
                # Create filename
                safe_filename = new_filename.strip().replace(" ", "-")
                if not safe_filename.endswith(".md"):
                    safe_filename += ".md"
                
                filepath = os.path.join(TELOS_FOLDER, safe_filename)
                
                # Check if file exists
                if os.path.exists(filepath):
                    st.error(f"File '{safe_filename}' already exists. Choose a different name.")
                else:
                    # Save file
                    try:
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        st.success(f"✓ File saved: `{filepath}`")
                        st.balloons()
                        st.info("Switch to 'Analyze' mode to analyze your new file!")
                    except Exception as e:
                        st.error(f"Error saving file: {str(e)}")
    
    with col2:
        st.subheader("🤖 AI Writing Assistant")
        st.markdown("Get AI help to write better Telos content.")
        
        # AI assistance options
        assist_type = st.selectbox(
            "What do you need help with?",
            [
                "💡 Expand & Deepen",
                "🎯 Mission Statement",
                "📊 Goal Setting",
                "🚧 Identify Challenges",
                "💪 Discover Strengths",
                "✨ Improve & Refine"
            ]
        )
        
        # Map display to internal keys
        assist_map = {
            "💡 Expand & Deepen": "expand",
            "🎯 Mission Statement": "mission",
            "📊 Goal Setting": "goals",
            "🚧 Identify Challenges": "challenges",
            "💪 Discover Strengths": "strengths",
            "✨ Improve & Refine": "improve"
        }
        
        selected_section = st.text_area(
            "Paste the section you want help with (optional):",
            height=100,
            placeholder="Leave empty to get help based on your full Telos...",
            key="section_input"
        )
        
        if st.button("✨ Get AI Suggestions", type="primary", use_container_width=True):
            with st.spinner("Thinking..."):
                section_key = assist_map[assist_type]
                current_content = new_content if new_content else ""
                section_content = selected_section if selected_section else ""
                
                suggestions = get_ai_writing_assistance(
                    section_key,
                    section_content,
                    current_content
                )
                
                st.markdown("### 💭 AI Suggestions")
                st.markdown(suggestions)
                
                # Store in session state for reference
                if "ai_suggestions" not in st.session_state:
                    st.session_state.ai_suggestions = []
                st.session_state.ai_suggestions.append({
                    "type": assist_type,
                    "content": suggestions,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
        
        # Show suggestion history
        if "ai_suggestions" in st.session_state and st.session_state.ai_suggestions:
            with st.expander("📜 Suggestion History", expanded=False):
                for i, suggestion in enumerate(reversed(st.session_state.ai_suggestions[-5:])):
                    st.caption(f"**{suggestion['type']}** - {suggestion['timestamp']}")
                    st.markdown(suggestion['content'])
                    st.markdown("---")

elif tab_mode == "📊 Analyze":
    # Analyze mode
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📝 Source Content")
        context_content = load_file(selected_file)
        
        if context_content:
            with st.expander("View file content", expanded=False):
                st.text_area("File content", context_content, height=400, disabled=True, label_visibility="collapsed")
            st.caption(f"File: {selected_file_name} ({len(context_content)} characters)")

    with col2:
        st.subheader("🤖 AI Analysis")
    
        if run_button:
            if run_all:
                # Run all patterns with progress tracking
                total_patterns = sum(len(patterns) for patterns in PATTERN_CATEGORIES.values())
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                st.info(f"Running {total_patterns} patterns... Grab a coffee ☕")
                
                completed = 0
                
                for category, patterns in PATTERN_CATEGORIES.items():
                    st.markdown(f"### {category}")
                    for pattern in patterns.keys():
                        status_text.text(f"Processing: {pattern.replace('_', ' ').title()} ({completed + 1}/{total_patterns})")
                        
                        with st.expander(f"📊 {pattern.replace('_', ' ').title()}", expanded=False):
                            output = get_gemini_response(PATTERNS[pattern], context_content)
                            st.markdown(output)
                            
                            # Save output
                            filepath = save_output(pattern, selected_file, output)
                            st.caption(f"✓ Saved to: `{os.path.basename(filepath)}`")
                        
                        completed += 1
                        progress_bar.progress(completed / total_patterns)
                
                progress_bar.empty()
                status_text.empty()
                st.balloons()
                st.success(f"🎉 All {total_patterns} patterns completed! Check the `outputs/` folder.")
            
            else:
                # Run single pattern
                pattern_title = selected_pattern.replace('_', ' ').title()
                with st.spinner(f"Analyzing with {pattern_title}..."):
                    output = get_gemini_response(PATTERNS[selected_pattern], context_content)
                    st.markdown(output)
                    
                    # Save output
                    filepath = save_output(selected_pattern, selected_file, output)
                    st.success(f"✓ Saved to: `{filepath}`")
                    
                    # Download button with full saved content
                    with open(filepath, "r", encoding="utf-8") as f:
                        saved_output = f.read()
                    
                    st.download_button(
                        label="📥 Download Result",
                        data=saved_output,
                        file_name=os.path.basename(filepath),
                        mime="text/markdown"
                    )
        else:
            st.info("👈 Select a file and pattern, then click 'Run Analysis'")

else:  # tab_mode == "📚 View Outputs"
    # View Outputs mode
    outputs = get_all_outputs()
    
    if not outputs:
        st.info("📭 No outputs yet. Run some analyses to see them here!")
    else:
        st.subheader("📚 Your Analysis History")
        
        # Get selected source from sidebar
        source_files = list(outputs.keys())
        if 'selected_source' not in locals():
            selected_source = source_files[0]
        
        # Get pattern filter from sidebar
        if 'pattern_filter' not in locals():
            pattern_filter = list(outputs[selected_source].keys())
        
        # Display analyses grouped by pattern
        for pattern in pattern_filter:
            if pattern not in outputs[selected_source]:
                continue
            
            analyses = outputs[selected_source][pattern]
            
            with st.expander(f"🎭 {pattern.replace('_', ' ').title()} ({len(analyses)} versions)", expanded=True):
                # Show version selector
                if len(analyses) > 1:
                    version_options = [
                        f"Version {i+1} - {format_relative_time(a['timestamp'])} ({a['timestamp'].strftime('%b %d, %I:%M %p')})"
                        for i, a in enumerate(analyses)
                    ]
                    selected_version_idx = st.selectbox(
                        "Select version:",
                        range(len(version_options)),
                        format_func=lambda i: version_options[i],
                        key=f"version_{pattern}"
                    )
                else:
                    selected_version_idx = 0
                
                selected_analysis = analyses[selected_version_idx]
                
                # Display metadata
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.caption(f"📅 {selected_analysis['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                with col2:
                    st.caption(f"⏱️ {format_relative_time(selected_analysis['timestamp'])}")
                with col3:
                    if len(analyses) > 1:
                        st.caption(f"📊 v{selected_version_idx + 1}/{len(analyses)}")
                
                # Load and display content
                try:
                    content = load_file(selected_analysis['filepath'])
                    
                    # Show content
                    st.markdown(content)
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.download_button(
                            label="📥 Download",
                            data=content,
                            file_name=selected_analysis['filename'],
                            mime="text/markdown",
                            key=f"download_{pattern}_{selected_version_idx}"
                        )
                    with col2:
                        if st.button("📋 Copy to Clipboard", key=f"copy_{pattern}_{selected_version_idx}"):
                            st.code(content, language="markdown")
                            st.success("Content displayed above - copy from the code block")
                    with col3:
                        if st.button("🗑️ Delete", key=f"delete_{pattern}_{selected_version_idx}"):
                            try:
                                os.remove(selected_analysis['filepath'])
                                st.success("Deleted! Refresh to update.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error deleting: {e}")
                
                except Exception as e:
                    st.error(f"Error loading file: {e}")
        
        # Bulk actions
        st.markdown("---")
        st.subheader("🔧 Bulk Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📁 Open Outputs Folder", use_container_width=True):
                output_path = os.path.abspath("outputs")
                try:
                    import platform
                    if platform.system() == "Windows":
                        os.startfile(output_path)
                    elif platform.system() == "Darwin":
                        os.system(f'open "{output_path}"')
                    else:
                        os.system(f'xdg-open "{output_path}"')
                    st.success(f"Opened: {output_path}")
                except Exception:
                    st.info(f"📂 Location: `{output_path}`")
        
        with col2:
            if st.button("🗑️ Delete All for This File", use_container_width=True, type="secondary"):
                if st.session_state.get('confirm_delete_all'):
                    # Actually delete
                    try:
                        deleted_count = 0
                        for pattern in outputs[selected_source]:
                            for analysis in outputs[selected_source][pattern]:
                                os.remove(analysis['filepath'])
                                deleted_count += 1
                        st.success(f"Deleted {deleted_count} files!")
                        st.session_state.confirm_delete_all = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    # Ask for confirmation
                    st.session_state.confirm_delete_all = True
                    st.warning("⚠️ Click again to confirm deletion of ALL analyses for this file!")

# Footer
st.markdown("---")
st.caption("Built with Streamlit & Google Gemini | Save outputs to `outputs/` folder")

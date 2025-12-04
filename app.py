import os
import re
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict

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
        return response.text
    except Exception as e:
        # If .text fails, inspect the candidates.
        if hasattr(response, "candidates") and response.candidates:
            candidate = response.candidates[0]
            
            # If there's content in parts, return it, even if truncated.
            if candidate.content and candidate.content.parts:
                text = "".join(part.text for part in candidate.content.parts if hasattr(part, "text"))
                if text:  # If we got some text
                    if candidate.finish_reason == 2 or candidate.finish_reason == 'MAX_TOKENS':
                        return text + "\n\n✂️ **Response truncated due to maximum token limit.**\n\n💡 *Tip: Try using a shorter Telos file or run a more focused analysis pattern.*"
                    return text

            # If no content, explain why based on finish_reason
            finish_reason = candidate.finish_reason
            if finish_reason == 2 or finish_reason == 'MAX_TOKENS':
                return "⚠️ **Response Truncated**\n\nThe response was cut off because it reached the maximum token limit and returned no content.\n\n**Possible solutions:**\n- Your Telos file might be too long. Try splitting it into smaller sections.\n- The analysis pattern generated too much output. Try a different pattern.\n- Consider using a model with higher token limits (e.g., gemini-1.5-pro)."
            if finish_reason == 3 or finish_reason == 'SAFETY':
                return "� ️ **Safety Filter Triggered**\n\nThe AI declined to respond due to safety settings. Try rephrasing your content."
            if finish_reason == 4 or finish_reason == 'RECITATION':
                return "📋 **Recitation Blocked**\n\nThe response was blocked for potential recitation of copyrighted material."
            if finish_reason == 5 or finish_reason == 'OTHER':
                return f"⚠️ **Unknown Error**\n\nFinish reason: {finish_reason}\n\nTry running the analysis again or use a different pattern."

        # If we still can't figure it out, show a generic error
        return f"⚠️ **Could not extract text from response**\n\nError: {str(e)}\n\nFinish reason: {getattr(response.candidates[0], 'finish_reason', 'unknown') if hasattr(response, 'candidates') and response.candidates else 'no candidates'}\n\nTry using a shorter Telos file or a different model."


def split_telos_by_sections(content: str) -> list:
    """Split Telos content by ## sections for processing large files."""
    sections = []
    current_section = ""
    current_header = ""
    
    for line in content.split('\n'):
        if line.startswith('## '):
            # Save previous section
            if current_section:
                sections.append({
                    'header': current_header,
                    'content': current_section.strip()
                })
            # Start new section
            current_header = line
            current_section = line + '\n'
        else:
            current_section += line + '\n'
    
    # Add last section
    if current_section:
        sections.append({
            'header': current_header,
            'content': current_section.strip()
        })
    
    return sections


def estimate_tokens(text: str) -> int:
    """Rough estimate of tokens (1 token ≈ 4 characters)."""
    return len(text) // 4


def get_gemini_response(prompt: str, context: str) -> str:
    """Get response from Gemini with robust error handling and automatic splitting for large files."""
    print("🚨 DEBUG: get_gemini_response() called - AI API call happening!")
    
    # Check if context is too large (rough estimate: 30K tokens = 120K chars for input)
    estimated_tokens = estimate_tokens(context)
    max_input_tokens = 30000  # Conservative limit for gemini-1.5-pro
    
    if estimated_tokens > max_input_tokens:
        # Split by sections and analyze separately
        st.info(f"📊 Large file detected (~{estimated_tokens:,} tokens). Splitting into sections for analysis...")
        sections = split_telos_by_sections(context)
        
        results = []
        for i, section in enumerate(sections, 1):
            st.caption(f"Analyzing section {i}/{len(sections)}: {section['header']}")
            
            section_prompt = f"""
{prompt}

**Note:** This is section {i} of {len(sections)} from a larger Telos document.

--- SECTION CONTENT ---
{section['content']}
"""
            try:
                model = get_model()
                response = model.generate_content(
                    section_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=4096,
                        candidate_count=1,
                    ),
                    safety_settings=[
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                    ]
                )
                results.append(f"### {section['header']}\n\n{safe_extract_text(response)}")
            except Exception as e:
                results.append(f"### {section['header']}\n\n❌ Error: {str(e)}")
        
        # Combine results
        combined = "# Analysis Results (Processed in Sections)\n\n" + "\n\n---\n\n".join(results)
        return combined
    
    # Normal processing for smaller files
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
                max_output_tokens=8192,
                candidate_count=1,
            ),
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
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


def semantic_search_telos(query: str, telos_files: list) -> list:
    """Perform semantic search across all Telos files using AI."""
    try:
        model = get_model()
        
        # Combine all Telos content
        all_content = []
        for filepath in telos_files:
            content = load_file(filepath)
            if content:
                all_content.append({
                    'file': os.path.basename(filepath),
                    'content': content
                })
        
        if not all_content:
            return []
        
        # Create search prompt
        files_text = "\n\n---\n\n".join([
            f"FILE: {item['file']}\n{item['content']}" 
            for item in all_content
        ])
        
        prompt = f"""You are a semantic search engine for personal Telos files.

USER QUERY: "{query}"

TELOS FILES:
{files_text}

Find and return the most relevant sections from these files that answer the query.
Format your response as JSON with this structure:
{{
    "results": [
        {{
            "file": "filename.md",
            "relevance": "high/medium/low",
            "excerpt": "relevant text excerpt",
            "context": "why this is relevant"
        }}
    ]
}}

Return only the JSON, no other text."""
        
        response = model.generate_content(prompt)
        result_text = safe_extract_text(response)
        
        # Try to parse JSON
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                results = json.loads(json_match.group())
                return results.get('results', [])
        except Exception:
            pass
        
        # Fallback: return formatted text
        return [{'file': 'All Files', 'relevance': 'medium', 'excerpt': result_text, 'context': 'Search results'}]
    
    except Exception as e:
        return [{'file': 'Error', 'relevance': 'low', 'excerpt': str(e), 'context': 'Search failed'}]


def extract_goals_from_telos(content: str) -> list:
    """Extract goals from Telos content using pattern matching and AI."""
    goals = []
    
    # Pattern 1: Look for Goals section
    goals_section = re.search(r'##\s*Goals\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if goals_section:
        goal_text = goals_section.group(1)
        # Extract bullet points
        bullet_goals = re.findall(r'[-*]\s+(.+)', goal_text)
        goals.extend(bullet_goals)
    
    # Pattern 2: Look for numbered goals
    numbered_goals = re.findall(r'\d+\.\s+(.+)', content)
    goals.extend(numbered_goals)
    
    return list(set(goals))  # Remove duplicates


def analyze_goal_progress(telos_file: str, outputs: dict) -> dict:
    """Analyze goal progress by comparing Telos file with analysis outputs."""
    content = load_file(telos_file)
    goals = extract_goals_from_telos(content)
    
    # Get all analyses for this file
    source_name = os.path.splitext(os.path.basename(telos_file))[0]
    file_outputs = outputs.get(source_name, {})
    
    # Count analyses
    total_analyses = sum(len(analyses) for analyses in file_outputs.values())
    
    # Get latest analysis dates
    latest_dates = []
    for pattern_analyses in file_outputs.values():
        if pattern_analyses:
            latest_dates.append(pattern_analyses[0]['timestamp'])
    
    last_analysis = max(latest_dates) if latest_dates else None
    
    return {
        'goals_count': len(goals),
        'goals': goals[:10],  # First 10 goals
        'total_analyses': total_analyses,
        'last_analysis': last_analysis,
        'patterns_used': list(file_outputs.keys())
    }


def get_analytics_data():
    """Generate analytics data from all Telos files and outputs."""
    outputs = get_all_outputs()
    telos_files = find_markdown_files(TELOS_FOLDER)
    
    # Overall stats
    total_files = len(telos_files)
    total_analyses = sum(
        len(analyses) 
        for source in outputs.values() 
        for analyses in source.values()
    )
    
    # Pattern usage
    pattern_usage = Counter()
    for source in outputs.values():
        for pattern, analyses in source.items():
            pattern_usage[pattern] += len(analyses)
    
    # Timeline data
    timeline = defaultdict(int)
    for source in outputs.values():
        for analyses in source.values():
            for analysis in analyses:
                date_key = analysis['timestamp'].strftime('%Y-%m-%d')
                timeline[date_key] += 1
    
    # Recent activity
    recent_analyses = []
    for source_name, source in outputs.items():
        for pattern, analyses in source.items():
            for analysis in analyses[:3]:  # Last 3 per pattern
                recent_analyses.append({
                    'source': source_name,
                    'pattern': pattern,
                    'timestamp': analysis['timestamp']
                })
    
    recent_analyses.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return {
        'total_files': total_files,
        'total_analyses': total_analyses,
        'pattern_usage': dict(pattern_usage.most_common(10)),
        'timeline': dict(sorted(timeline.items())),
        'recent_activity': recent_analyses[:10]
    }


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
        "analyze_expand": (
            "You are a Telos expert. Analyze the user's current Telos document and provide: "
            "1) What's working well (2-3 strengths), "
            "2) What's missing or underdeveloped (2-3 gaps), "
            "3) Specific suggestions to expand and deepen each section, "
            "4) How to better connect Problems → Mission → Goals → Challenges. "
            "Be specific and actionable. Reference their actual content."
        ),
        "connect": (
            "You are a systems thinker. Analyze how the user's Problems, Mission, Goals, and Challenges "
            "connect to each other. Show the logical flow: which goals address which problems? "
            "Which challenges block which goals? Are there gaps in the chain? "
            "Provide a clear map of connections and suggest missing links."
        ),
    }
    
    prompt = prompts.get(section, prompts["expand"])
    
    try:
        model = get_model()
        
        full_prompt = f"""
{prompt}

--- USER'S TELOS DOCUMENT ---
{full_context if full_context else "[User is just starting their Telos]"}

Provide helpful, actionable guidance. Be concise but insightful. Use markdown formatting.
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
    tab_mode = st.radio(
        "Mode:", 
        ["📊 Analyze", "✍️ Create New File", "📚 View Outputs", "🔍 Search", "📈 Analytics", "🎯 Goal Tracker"],
        label_visibility="collapsed"
    )
    
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
    
    elif tab_mode == "📚 View Outputs":
        # View Outputs mode
        st.subheader("📚 View Outputs")
        
        outputs = get_all_outputs()
        
        if not outputs:
            st.warning("No outputs found yet.")
            st.info("Run some analyses first!")
        else:
            # Source file selector with cleaner display
            source_files = list(outputs.keys())
            
            # Create display names (remove timestamps if present)
            display_names = []
            for source in source_files:
                # If it has timestamp pattern, extract just the base name
                if '_2025-' in source or '_2024-' in source or '_2026-' in source:
                    # Extract base name before timestamp
                    base_name = source.split('_202')[0]
                    display_names.append(f"{base_name}.md")
                else:
                    display_names.append(f"{source}.md")
            
            selected_display = st.selectbox("📄 Select Telos file:", display_names)
            selected_source = source_files[display_names.index(selected_display)]
            
            st.markdown("---")
            
            # Category-based filter instead of individual patterns
            st.subheader("🎯 Filter by Category")
            
            # Get available categories for this source
            available_patterns = list(outputs[selected_source].keys())
            available_categories = []
            for category, category_patterns in PATTERN_CATEGORIES.items():
                if any(p in available_patterns for p in category_patterns.keys()):
                    available_categories.append(category)
            
            selected_categories = st.multiselect(
                "Show categories:",
                available_categories,
                default=available_categories,
                help="Filter which analysis categories to display"
            )
            
            st.markdown("---")
            
            # Build pattern filter from selected categories
            pattern_filter = []
            for category in selected_categories:
                if category in PATTERN_CATEGORIES:
                    for pattern_key in PATTERN_CATEGORIES[category].keys():
                        if pattern_key in available_patterns:
                            pattern_filter.append(pattern_key)
            
            # Stats
            if pattern_filter:
                total_analyses = sum(len(outputs[selected_source][p]) for p in pattern_filter)
                st.metric("📊 Total Analyses", total_analyses)
                st.caption(f"Across {len(pattern_filter)} patterns")
        
        # Set defaults
        run_button = False
        run_all = False
        selected_file = None
        selected_pattern = None
        create_button = False
    
    else:
        # Search, Analytics, or Goal Tracker modes
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
                st.session_state.telos_editor = """# My Telos

## PROBLEMS
What current pains, inefficiencies, or negative states do I observe in my life or environment that I feel driven to change or solve?

- P1: 
- P2: 

## MISSION
What is your core purpose or mission in life? (This should address the problems above)

- M1: 

## NARRATIVES
How do you describe yourself and your mission to others?

- N1: 

## GOALS
What specific, measurable outcomes will move you toward your mission?

### Short-term (Next 3-6 months)
- G1: 
- G2: 

### Long-term (1-5 years)
- G3: 
- G4: 

## CHALLENGES
What obstacles currently stand between you and your goals?

- C1: 
- C2: 

## STRENGTHS
What are your key strengths, skills, and resources?

- S1: 
- S2: 

## CURRENT STATUS
Where are you right now across key life domains?

- Career: 
- Health: 
- Relationships: 
- Finances: 

## LOG (Journal)
Daily reflections, thoughts, and observations. Use DD/MM/YYYY format.

- """ + datetime.now().strftime("%d/%m/%Y") + """: 
"""
                st.rerun()
        
        # Text editor
        new_content = st.text_area(
            "Content:",
            value="",
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
        st.markdown("AI analyzes your Telos and suggests improvements.")
        
        # Quick actions
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔍 Analyze & Expand", use_container_width=True, type="primary"):
                if new_content.strip():
                    with st.spinner("Analyzing your Telos..."):
                        suggestions = get_ai_writing_assistance("analyze_expand", "", new_content)
                        st.markdown("### 💭 AI Analysis")
                        st.markdown(suggestions)
                else:
                    st.warning("Write some content first!")
        
        with col_b:
            if st.button("📝 Add Journal Entry", use_container_width=True):
                # Add timestamped journal entry template
                today = datetime.now().strftime("%d/%m/%Y")
                journal_template = f"\n- {today}: "
                st.session_state.telos_editor = new_content + journal_template
                st.rerun()
        
        st.markdown("---")
        
        # Specific assistance
        assist_type = st.selectbox(
            "Or get specific help:",
            [
                "💡 Expand & Deepen Current Content",
                "🎯 Refine Mission Statement",
                "📊 Set SMART Goals",
                "🚧 Identify Hidden Challenges",
                "💪 Discover Your Strengths",
                "✨ Overall Improvement Suggestions",
                "🔗 Connect Sections (Problems → Goals)"
            ]
        )
        
        # Map display to internal keys
        assist_map = {
            "💡 Expand & Deepen Current Content": "expand",
            "🎯 Refine Mission Statement": "mission",
            "📊 Set SMART Goals": "goals",
            "🚧 Identify Hidden Challenges": "challenges",
            "💪 Discover Your Strengths": "strengths",
            "✨ Overall Improvement Suggestions": "improve",
            "🔗 Connect Sections (Problems → Goals)": "connect"
        }
        
        if st.button("✨ Get Suggestions", use_container_width=True):
            if new_content.strip():
                with st.spinner("Thinking..."):
                    section_key = assist_map[assist_type]
                    suggestions = get_ai_writing_assistance(section_key, "", new_content)
                    
                    st.markdown("### 💭 AI Suggestions")
                    st.markdown(suggestions)
                    
                    # Store in session state
                    if "ai_suggestions" not in st.session_state:
                        st.session_state.ai_suggestions = []
                    st.session_state.ai_suggestions.append({
                        "type": assist_type,
                        "content": suggestions,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
            else:
                st.warning("Write some content first!")
        
        # Show suggestion history
        if "ai_suggestions" in st.session_state and st.session_state.ai_suggestions:
            with st.expander("📜 Recent Suggestions", expanded=False):
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

elif tab_mode == "📚 View Outputs":
    # View Outputs mode
    outputs = get_all_outputs()
    
    if not outputs:
        st.info("📭 No outputs yet. Run some analyses to see them here!")
    else:
        # Get selected source from sidebar
        source_files = list(outputs.keys())
        if 'selected_source' not in locals():
            selected_source = source_files[0]
        
        # Get pattern filter from sidebar
        if 'pattern_filter' not in locals():
            pattern_filter = list(outputs[selected_source].keys())
        
        # Create clean display name
        if '_2025-' in selected_source or '_2024-' in selected_source or '_2026-' in selected_source:
            display_name = selected_source.split('_202')[0] + '.md'
        else:
            display_name = selected_source + '.md'
        
        # Header with context
        st.subheader(f"📚 Analysis History for: {display_name}")
        
        if len(pattern_filter) > 0:
            st.caption(f"📁 Viewing {len(pattern_filter)} pattern(s) | 💾 Reading saved files only - no AI calls")
        else:
            st.warning("⚠️ No categories selected. Please select at least one category from the sidebar.")
        
        st.markdown("---")
        
        # Group patterns by category for organized display
        patterns_by_category = {}
        for category, category_patterns in PATTERN_CATEGORIES.items():
            patterns_in_this_category = []
            for pattern_key in category_patterns.keys():
                if pattern_key in pattern_filter and pattern_key in outputs[selected_source]:
                    patterns_in_this_category.append(pattern_key)
            if patterns_in_this_category:
                patterns_by_category[category] = patterns_in_this_category
        
        # Display analyses grouped by category, then by pattern
        if not patterns_by_category:
            st.info("📭 No analyses found for the selected categories. Try selecting different categories or run some analyses first!")
        
        for category_idx, (category, patterns_in_category) in enumerate(patterns_by_category.items()):
            if category_idx > 0:
                st.markdown("---")
            
            st.markdown(f"## {category}")
            st.caption(f"{len(patterns_in_category)} analysis pattern{'s' if len(patterns_in_category) > 1 else ''} in this category")
            
            for pattern in patterns_in_category:
                if pattern not in outputs[selected_source]:
                    continue
                
                analyses = outputs[selected_source][pattern]
                
                with st.expander(f"🎭 {pattern.replace('_', ' ').title()} ({len(analyses)} version{'s' if len(analyses) > 1 else ''})", expanded=False):
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
                    
                    # Display metadata with better context
                    st.markdown(f"**📄 Source Telos File:** `{selected_source}.md`")
                    st.markdown(f"**🎭 Analysis Pattern:** `{pattern.replace('_', ' ').title()}`")
                    st.markdown(f"**📅 Generated:** {selected_analysis['timestamp'].strftime('%Y-%m-%d at %I:%M %p')} ({format_relative_time(selected_analysis['timestamp'])})")
                    st.markdown(f"**💾 File:** `{selected_analysis['filename']}`")
                    
                    if len(analyses) > 1:
                        st.caption(f"📊 Showing version {selected_version_idx + 1} of {len(analyses)}")
                    
                    st.markdown("---")
                    
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

elif tab_mode == "🔍 Search":
    # Semantic Search mode
    st.subheader("🔍 Semantic Search Across All Telos Files")
    st.markdown("Search for concepts, themes, or specific information across all your Telos files using AI-powered semantic search.")
    
    telos_files = find_markdown_files(TELOS_FOLDER)
    
    if not telos_files:
        st.warning("No Telos files found. Create some files first!")
    else:
        st.info(f"Searching across {len(telos_files)} Telos file(s)")
        
        # Search input
        search_query = st.text_input(
            "What are you looking for?",
            placeholder="e.g., 'career goals', 'challenges with time management', 'strengths in leadership'"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            search_button = st.button("🔍 Search", type="primary", use_container_width=True)
        with col2:
            st.caption("💡 Tip: Use natural language - the AI understands context!")
        
        if search_button and search_query:
            with st.spinner("Searching with AI..."):
                results = semantic_search_telos(search_query, telos_files)
                
                if results:
                    st.success(f"Found {len(results)} relevant result(s)")
                    
                    for i, result in enumerate(results):
                        relevance_emoji = {
                            'high': '🔥',
                            'medium': '⭐',
                            'low': '💡'
                        }.get(result.get('relevance', 'medium'), '📄')
                        
                        with st.expander(f"{relevance_emoji} {result.get('file', 'Unknown')} - {result.get('relevance', 'medium').title()} Relevance", expanded=i==0):
                            st.markdown(f"**Context:** {result.get('context', 'N/A')}")
                            st.markdown("---")
                            st.markdown(result.get('excerpt', 'No excerpt available'))
                else:
                    st.info("No results found. Try a different query!")

elif tab_mode == "📈 Analytics":
    # Analytics Dashboard mode
    st.subheader("📈 Analytics Dashboard")
    st.markdown("Visualize your Telos journey with insights and statistics.")
    
    analytics = get_analytics_data()
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📁 Telos Files", analytics['total_files'])
    with col2:
        st.metric("🔍 Total Analyses", analytics['total_analyses'])
    with col3:
        avg_per_file = analytics['total_analyses'] / analytics['total_files'] if analytics['total_files'] > 0 else 0
        st.metric("📊 Avg per File", f"{avg_per_file:.1f}")
    with col4:
        st.metric("🎭 Patterns Used", len(analytics['pattern_usage']))
    
    st.markdown("---")
    
    # Pattern usage chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎭 Most Used Patterns")
        if analytics['pattern_usage']:
            # Create bar chart data
            patterns = list(analytics['pattern_usage'].keys())
            counts = list(analytics['pattern_usage'].values())
            
            # Display as horizontal bars using markdown
            for pattern, count in sorted(analytics['pattern_usage'].items(), key=lambda x: x[1], reverse=True):
                bar_length = int((count / max(counts)) * 30)
                bar = "█" * bar_length
                st.markdown(f"**{pattern.replace('_', ' ').title()}** `{bar}` {count}")
        else:
            st.info("No analyses yet. Run some patterns to see statistics!")
    
    with col2:
        st.subheader("📅 Recent Activity")
        if analytics['recent_activity']:
            for activity in analytics['recent_activity'][:5]:
                st.caption(f"**{activity['pattern'].replace('_', ' ').title()}**")
                st.caption(f"📄 {activity['source']}")
                st.caption(f"⏱️ {format_relative_time(activity['timestamp'])}")
                st.markdown("---")
        else:
            st.info("No recent activity")
    
    # Timeline
    st.markdown("---")
    st.subheader("📅 Analysis Timeline")
    if analytics['timeline']:
        dates = list(analytics['timeline'].keys())
        counts = list(analytics['timeline'].values())
        
        # Simple timeline visualization
        for date, count in list(analytics['timeline'].items())[-14:]:  # Last 14 days
            bar_length = int((count / max(counts)) * 40)
            bar = "▓" * bar_length
            st.markdown(f"`{date}` {bar} **{count}** analyses")
    else:
        st.info("No timeline data yet")

elif tab_mode == "🎯 Goal Tracker":
    # Goal Tracking mode
    st.subheader("🎯 Automatic Goal Tracker")
    st.markdown("Track goals extracted from your Telos files and monitor progress through analyses.")
    
    telos_files = find_markdown_files(TELOS_FOLDER)
    outputs = get_all_outputs()
    
    if not telos_files:
        st.warning("No Telos files found. Create some files first!")
    else:
        # File selector
        file_names = [os.path.basename(f) for f in telos_files]
        selected_file_name = st.selectbox("Select Telos file:", file_names)
        selected_file = telos_files[file_names.index(selected_file_name)]
        
        st.markdown("---")
        
        # Analyze goals
        with st.spinner("Extracting goals..."):
            progress_data = analyze_goal_progress(selected_file, outputs)
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎯 Goals Found", progress_data['goals_count'])
        with col2:
            st.metric("🔍 Total Analyses", progress_data['total_analyses'])
        with col3:
            if progress_data['last_analysis']:
                st.metric("📅 Last Analysis", format_relative_time(progress_data['last_analysis']))
            else:
                st.metric("📅 Last Analysis", "Never")
        
        st.markdown("---")
        
        # Display goals
        if progress_data['goals']:
            st.subheader("📋 Extracted Goals")
            for i, goal in enumerate(progress_data['goals'], 1):
                with st.expander(f"Goal {i}: {goal[:60]}...", expanded=i<=3):
                    st.markdown(goal)
                    
                    # Check if this goal appears in analyses
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if st.button("🔍 Search in Analyses", key=f"search_goal_{i}"):
                            st.info("Searching for this goal in your analyses...")
                            # This would trigger a search
                    with col2:
                        st.caption("Status: 📝 Active")
        else:
            st.info("No goals found. Add goals to your Telos file in a '## Goals' section with bullet points.")
            
            with st.expander("💡 How to add goals"):
                st.markdown("""
Add a Goals section to your Telos file like this:

```markdown
## Goals

### Short-term (Next 3-6 months)
- Complete Python certification
- Build 3 portfolio projects
- Network with 10 industry professionals

### Long-term (1-5 years)
- Land senior developer role
- Contribute to open source
- Start tech blog
```
                """)
        
        # Patterns used
        if progress_data['patterns_used']:
            st.markdown("---")
            st.subheader("🎭 Analysis Patterns Used")
            cols = st.columns(4)
            for i, pattern in enumerate(progress_data['patterns_used']):
                with cols[i % 4]:
                    st.caption(f"✓ {pattern.replace('_', ' ').title()}")

# Footer
st.markdown("---")
st.caption("Built with Streamlit & Google Gemini | Save outputs to `outputs/` folder")

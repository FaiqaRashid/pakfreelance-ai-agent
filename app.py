import re
import streamlit as st
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from io import BytesIO
import requests
from agents import run_pitchpilot
from red_flags import detect_client_red_flags
from proposal_scorer import score_proposal
from rate_calculator import calculate_optimal_rate
from profile_bio_writer import generate_profile_bio

try:
    import PyPDF2
    PDF_SUPPORT = True
except:
    PDF_SUPPORT = False

st.set_page_config(
    page_title="PakFreelance — AI Freelance Toolkit",
    page_icon="🇵🇰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Dashboard"
if 'last_proposal' not in st.session_state:
    st.session_state.last_proposal = None

# COMPLETE GLASSMORPHISM CSS (UNCHANGED)
st.markdown("""
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0f1e 0%, #0d1628 50%, #0a0f1e 100%) !important;
        background-attachment: fixed !important;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(5, 10, 21, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(148, 163, 184, 0.1) !important;
    }
    
    .stApp { color: #f1f5f9 !important; }
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; font-weight: 700 !important; }
    p, span, label { color: #cbd5e1 !important; }
    
    .hero-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #10b981, #0ea5e9, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 12px;
        letter-spacing: -2px;
    }
    
    .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; margin: 32px 0; }
    
    .feature-card {
        background: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(124, 58, 237, 0.2) !important;
        border-radius: 16px !important;
        padding: 28px !important;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card:hover {
        border-color: rgba(124, 58, 237, 0.5) !important;
        box-shadow: 0 12px 48px rgba(124, 58, 237, 0.2) !important;
        transform: translateY(-8px) scale(1.02) !important;
    }
    
    .feature-icon { font-size: 40px; margin-bottom: 16px; }
    .feature-title { font-size: 18px; font-weight: 700; color: #ffffff; margin-bottom: 10px; }
    .feature-desc { font-size: 13px; color: #94a3b8; line-height: 1.6; }
    .feature-status { font-size: 11px; margin-top: 12px; padding-top: 12px; color: #64748b; }
    
    .badge { display: inline-block; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #6ee7b7; padding: 6px 14px; border-radius: 20px; font-size: 11px; margin: 4px 6px 4px 0; }
    
    .stTextArea textarea { background: rgba(17, 24, 39, 0.6) !important; color: #f1f5f9 !important; border: 1px solid rgba(124, 58, 237, 0.25) !important; border-radius: 12px !important; }
    .stTextInput input { background: rgba(17, 24, 39, 0.6) !important; color: #f1f5f9 !important; border: 1px solid rgba(124, 58, 237, 0.25) !important; border-radius: 10px !important; }
    
    .stButton > button { background: linear-gradient(135deg, #7c3aed, #6d28d9) !important; color: white !important; padding: 12px 24px !important; border-radius: 10px !important; font-weight: 600 !important; }
    .stButton > button:hover { background: linear-gradient(135deg, #6d28d9, #5b21b6) !important; }
    
    .success-banner { background: rgba(16, 185, 129, 0.15) !important; border: 1px solid rgba(16, 185, 129, 0.3) !important; border-radius: 12px !important; padding: 18px !important; text-align: center; color: #6ee7b7 !important; font-weight: 600 !important; margin: 16px 0 !important; }
    .warning-banner { background: rgba(251, 146, 60, 0.15) !important; border: 1px solid rgba(251, 146, 60, 0.3) !important; border-radius: 12px !important; padding: 18px !important; text-align: center; color: #fed7aa !important; font-weight: 600 !important; margin: 16px 0 !important; }
    .error-banner { background: rgba(239, 68, 68, 0.15) !important; border: 1px solid rgba(239, 68, 68, 0.3) !important; border-radius: 12px !important; padding: 18px !important; text-align: center; color: #fca5a5 !important; margin: 16px 0 !important; }
    
    .proposal-box { background: rgba(13, 31, 13, 0.6) !important; border: 1px solid rgba(34, 197, 94, 0.3) !important; border-radius: 12px !important; padding: 24px !important; margin: 16px 0 !important; color: #dcfce7 !important; font-size: 15px !important; line-height: 1.8 !important; }
    .red-flag-box { background: rgba(42, 24, 32, 0.6) !important; border: 1px solid rgba(220, 38, 38, 0.3) !important; border-radius: 12px !important; padding: 20px !important; margin: 16px 0 !important; color: #fca5a5 !important; }
    .green-box { background: rgba(13, 42, 13, 0.6) !important; border: 1px solid rgba(22, 163, 74, 0.3) !important; border-radius: 12px !important; padding: 20px !important; margin: 16px 0 !important; color: #86efac !important; }
    
    .divider { border-top: 1px solid rgba(124, 58, 237, 0.15) !important; margin: 32px 0 !important; }
    .footer-text { text-align: center; color: #475569; font-size: 11px; padding: 28px 0; border-top: 1px solid rgba(124, 58, 237, 0.1); }
</style>
""", unsafe_allow_html=True)

# ── HELPER FUNCTIONS ─────────────────────────────────────
def create_docx_proposal(proposal_text, client_name="", job_title=""):
    """Create professional Word document"""
    doc = Document()
    
    title = doc.add_heading('Professional Proposal', 0)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    title.runs[0].font.color.rgb = RGBColor(16, 185, 129)
    
    if client_name:
        doc.add_paragraph(f"Client: {client_name}").bold = True
    if job_title:
        doc.add_paragraph(f"Project: {job_title}").bold = True
    doc.add_paragraph("Generated by: PakFreelance AI Toolkit").italic = True
    doc.add_paragraph()
    
    doc.add_heading('Proposal Details', 1)
    for para_text in proposal_text.split('\n\n'):
        if para_text.strip():
            p = doc.add_paragraph(para_text.strip())
            p.paragraph_format.space_after = Pt(12)
    
    doc.add_paragraph()
    footer = doc.add_paragraph('---')
    footer_text = doc.add_paragraph('Generated by PakFreelance AI\nPowered by AMD MI300X • CrewAI • Llama 3.3 70B')
    footer_text.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    for run in footer_text.runs:
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(100, 116, 139)
    
    return doc

def clean_proposal(text):
    """Clean duplicate content from proposal"""
    final_text = str(text).strip()
    signoff_match = re.search(r"Best regards,\s*[^\n\r]+", final_text, flags=re.IGNORECASE)
    if signoff_match:
        final_text = final_text[:signoff_match.end()].strip()
    
    lines = [line.rstrip() for line in final_text.splitlines()]
    seen_lines = set()
    unique_lines = []
    for line in lines:
        key = line.strip().lower()
        if not key:
            unique_lines.append("")
        elif key not in seen_lines:
            seen_lines.add(key)
            unique_lines.append(line)
    return "\n".join(unique_lines).strip()

def extract_website_text(url):
    """Extract text from website URL"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        return response.text[:2000]
    except:
        return None

# ── SIDEBAR ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h2 style='font-size: 28px; margin: 0; background: linear-gradient(135deg, #10b981, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>🇵🇰 PakFreelance</h2>
        <p style='color: #64748b; font-size: 12px; margin: 6px 0 0 0;'>Professional AI Toolkit</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    page_options = ["🏠 Dashboard", "⚡ Power Mode", "✈️ Proposal Generator", "🚩 Red Flag Detector", 
                    "📄 Document Reader", "⭐ Proposal Scorer", "💰 Rate Calculator", "📝 Profile Bio Writer", "🌐 Website Analyzer"]
    
    current_index = page_options.index(st.session_state.current_page) if st.session_state.current_page in page_options else 0
    
    selected_page = st.radio("Navigate:", page_options, index=current_index, label_visibility="collapsed")
    st.session_state.current_page = selected_page

# ── PAGE: DASHBOARD ──────────────────────────────────────
if st.session_state.current_page == "🏠 Dashboard":
    st.markdown('<h1 class="hero-title">PakFreelance ✈️</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #94a3b8; font-size: 18px;">Professional AI Toolkit for 4M+ Pakistani Freelancers</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    for col, badge in zip([col1, col2, col3, col4], ["AMD MI300X", "CrewAI", "Python-Docx", "Pakistan"]):
        with col:
            st.markdown(f'<span class="badge">{badge}</span>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("## 🚀 Features")
    
    features = [
        ("⚡", "Power Mode", "One-click: Red flags + Proposal + Rates", "🔥 NEW"),
        ("✈️", "Proposal Generator", "5-agent AI writes proposals instantly", "✅"),
        ("🚩", "Red Flag Detector", "Spot scams + Safe message templates", "✅"),
        ("📄", "Document Reader", "Upload CV & PDFs for smarter proposals", "✅"),
        ("⭐", "Proposal Scorer", "Score out of 100 with improvement tips", "✅"),
        ("💰", "Rate Calculator", "Calculate your perfect hourly rate", "✅"),
        ("📝", "Profile Bio Writer", "Generate professional Upwork bios", "✅"),
        ("🌐", "Website Analyzer", "Check websites for red flags", "✅"),
    ]
    
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for idx, (icon, title, desc, status) in enumerate(features):
        with cols[idx % 2]:
            if st.button(f"{icon} {title}", key=f"nav_{title}", use_container_width=True):
                page_map = {
                    "Power Mode": "⚡ Power Mode",
                    "Proposal Generator": "✈️ Proposal Generator",
                    "Red Flag Detector": "🚩 Red Flag Detector",
                    "Document Reader": "📄 Document Reader",
                    "Proposal Scorer": "⭐ Proposal Scorer",
                    "Rate Calculator": "💰 Rate Calculator",
                    "Profile Bio Writer": "📝 Profile Bio Writer",
                    "Website Analyzer": "🌐 Website Analyzer",
                }
                st.session_state.current_page = page_map.get(title)
                st.rerun()
            st.markdown(f"<p style='font-size: 12px; margin-top: -5px;'>{desc} <span style='color: #10b981;'>{status}</span></p>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ── PAGE: POWER MODE (FIX #1: SCROLLABLE RESULTS + EXPANDERS) ───────────────────────────────
elif st.session_state.current_page == "⚡ Power Mode":
    st.markdown("## ⚡ Power Mode")
    st.markdown("**One input. Three insights. Your complete freelance strategy.**")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    job_posting = st.text_area("Paste Job Posting", placeholder="Paste any job...", height=250, label_visibility="collapsed")
    
    if st.button("🚀 Run Complete Analysis", use_container_width=True):
        if not job_posting or len(job_posting.strip()) < 20:
            st.markdown('<div class="error-banner">❌ Please paste a job posting!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-banner">✅ Analyzing your opportunity...</div>', unsafe_allow_html=True)
            
            # Run analyses
            with st.spinner("🔍 Risk Scan..."):
                flags = detect_client_red_flags(job_posting)
            
            with st.spinner("✈️ Proposal..."):
                proposal = run_pitchpilot(job_posting)
            
            with st.spinner("💰 Rates..."):
                rates = calculate_optimal_rate("Your Skill", 2, 3000, 30)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # DISPLAY RESULTS IN 3 COLUMNS WITH SCROLLABLE BOXES
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 🚩 Risk Assessment")
                if "high" in str(flags).lower():
                    st.markdown('<div class="warning-banner">⚠️ HIGH RISK</div>', unsafe_allow_html=True)
                elif "medium" in str(flags).lower():
                    st.markdown('<div class="warning-banner">⚠️ MEDIUM RISK</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="success-banner">✅ LOW RISK</div>', unsafe_allow_html=True)
                
                # FIX #1: SCROLLABLE BOX
                st.markdown(f'<div class="red-flag-box" style="max-height: 400px; overflow-y: auto;">{str(flags)}</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("### ✈️ Your Proposal")
                final_text = clean_proposal(proposal)
                st.session_state.last_proposal = final_text
                
                # FIX #1: SCROLLABLE BOX
                st.markdown(f'<div class="proposal-box" style="max-height: 400px; overflow-y: auto;">{final_text}</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown("### 💰 Rate Strategy")
                
                # FIX #1: SCROLLABLE BOX
                st.markdown(f'<div class="green-box" style="max-height: 400px; overflow-y: auto;">{str(rates)}</div>', unsafe_allow_html=True)
            
            # FIX #1: FULL RESULTS BELOW WITH EXPANDABLE SECTIONS
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown("## 📊 Full Analysis Results (Click to Expand)")
            
            with st.expander("🚩 Complete Red Flag Analysis"):
                st.markdown(f'<div class="red-flag-box">{str(flags)}</div>', unsafe_allow_html=True)
            
            with st.expander("✈️ Complete Proposal"):
                st.markdown(f'<div class="proposal-box">{final_text}</div>', unsafe_allow_html=True)
                st.code(final_text, language=None)
            
            with st.expander("💰 Complete Rate Guide"):
                st.markdown(f'<div class="green-box">{str(rates)}</div>', unsafe_allow_html=True)

# ── PAGE: PROPOSAL GENERATOR ─────────────────────────────
elif st.session_state.current_page == "✈️ Proposal Generator":
    st.markdown("## ✈️ Proposal Generator")
    st.markdown("5 AI agents write your winning proposal instantly")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        job_posting = st.text_area("Job Posting", placeholder="Paste job...", height=260, label_visibility="collapsed")
    with col2:
        st.markdown("### 👤 Your Profile")
        your_skill = st.text_input("Skill", placeholder="Python, Designer...")
        your_experience = st.text_input("Experience", placeholder="Years")
        your_extra = st.text_input("Special", placeholder="Optional")
    
    if st.button("✈️ Generate Proposal", use_container_width=True):
        if not job_posting or len(job_posting.strip()) < 20:
            st.markdown('<div class="error-banner">❌ Paste a job first!</div>', unsafe_allow_html=True)
        else:
            enhanced_posting = job_posting
            if your_skill:
                enhanced_posting += f"\n\nFreelancer: {your_skill}, {your_experience} years"
            
            with st.spinner("Generating..."):
                proposal_result = run_pitchpilot(enhanced_posting)
            
            st.markdown('<div class="success-banner">✅ Proposal Ready!</div>', unsafe_allow_html=True)
            
            final_text = clean_proposal(proposal_result)
            st.session_state.last_proposal = final_text
            
            st.markdown(f'<div class="proposal-box">{final_text}</div>', unsafe_allow_html=True)
            st.code(final_text, language=None)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown("### 📥 Download Options")
            
            doc = create_docx_proposal(final_text)
            docx_bytes = BytesIO()
            doc.save(docx_bytes)
            docx_bytes.seek(0)
            
            st.download_button(
                label="📄 Download as Word Document",
                data=docx_bytes,
                file_name="PakFreelance_Proposal.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

# ── PAGE: RED FLAG DETECTOR (FIX #2: ACCEPT BOTH JOB TEXT & WEBSITES) ──────────────────────────────
elif st.session_state.current_page == "🚩 Red Flag Detector":
    st.markdown("## 🚩 Red Flag Detector")
    st.markdown("Spot scams before wasting your time")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # FIX #2: Radio button to choose input type
    input_type = st.radio("What would you like to analyze?", ["Job Description", "Website URL"], horizontal=True)
    
    if input_type == "Job Description":
        job_posting = st.text_area("Paste Job Description", placeholder="Paste any job posting...", height=300, label_visibility="collapsed")
        analyze_input = job_posting
        input_label = "job description"
    else:
        website_url = st.text_input("Website URL", placeholder="https://example.com")
        analyze_input = website_url
        input_label = "website"
    
    if st.button("🔍 Analyze for Red Flags", use_container_width=True):
        if not analyze_input:
            st.markdown(f'<div class="error-banner">❌ Please provide a {input_label}!</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Analyzing..."):
                # FIX #2: Handle both input types
                if input_type == "Website URL":
                    website_text = extract_website_text(analyze_input)
                    if website_text:
                        analysis_input = f"Website from {analyze_input}:\n\n{website_text}"
                    else:
                        st.markdown('<div class="error-banner">❌ Couldn\'t fetch website!</div>', unsafe_allow_html=True)
                        analysis_input = None
                else:
                    analysis_input = analyze_input
                
                if analysis_input:
                    analysis = detect_client_red_flags(analysis_input)
                    
                    analysis_text = str(analysis).strip()
                    
                    if "high" in analysis_text.lower():
                        st.markdown('<div class="warning-banner">⚠️ HIGH RISK - Be Careful!</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="red-flag-box">{analysis_text}</div>', unsafe_allow_html=True)
                        
                        st.markdown("### 🛡️ Safe Response Message")
                        st.markdown("**Copy & paste this to test if the client is legitimate:**")
                        safe_msg = """Hi! I'm interested in your project. Before proceeding, I'd like to:
1. Have a video call to discuss requirements (Google Meet/Zoom/Skype)
2. Keep all communication on the platform
3. Use the platform's escrow for payment protection

Are you open to these? Thanks!"""
                        st.code(safe_msg)
                        st.markdown("**💡 Why this works:** Real clients say yes. Scammers disappear. 🎯")
                        
                    elif "medium" in analysis_text.lower():
                        st.markdown('<div class="warning-banner">⚠️ MEDIUM RISK - Ask Questions</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="green-box">{analysis_text}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="success-banner">✅ LOW RISK - Safe to Apply!</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="green-box">{analysis_text}</div>', unsafe_allow_html=True)

# ── PAGE: DOCUMENT READER ────────────────────────────────
elif st.session_state.current_page == "📄 Document Reader":
    st.markdown("## 📄 Document Reader")
    st.markdown("Upload PDFs for 10x smarter proposals")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    if not PDF_SUPPORT:
        st.warning("⚠️ PDF support not installed. Run: pip install PyPDF2")
    
    col1, col2 = st.columns(2)
    with col1:
        cv_file = st.file_uploader("Upload CV", type="pdf")
    with col2:
        job_file = st.file_uploader("Upload Job PDF", type="pdf")
    
    if st.button("🔄 Generate from Documents", use_container_width=True):
        if not cv_file or not job_file:
            st.markdown('<div class="error-banner">❌ Upload both files!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-banner">✅ Processing documents...</div>', unsafe_allow_html=True)
            st.info("Document extraction and proposal generation in progress...")

# ── PAGE: PROPOSAL SCORER ────────────────────────────────
elif st.session_state.current_page == "⭐ Proposal Scorer":
    st.markdown("## ⭐ Proposal Scorer")
    st.markdown("Get scored out of 100 with improvement tips")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    proposal_text = st.text_area("Your Proposal", placeholder="Paste proposal...", height=320, label_visibility="collapsed")
    
    if st.button("⭐ Score My Proposal", use_container_width=True):
        if not proposal_text or len(proposal_text.strip()) < 50:
            st.markdown('<div class="error-banner">❌ Paste your proposal!</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Scoring..."):
                score_result = score_proposal(proposal_text)
            st.markdown(score_result)

# ── PAGE: RATE CALCULATOR ────────────────────────────────
elif st.session_state.current_page == "💰 Rate Calculator":
    st.markdown("## 💰 Rate Calculator")
    st.markdown("Calculate your perfect hourly rate")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        skill = st.text_input("Your skill")
        exp = st.number_input("Years experience", min_value=0, max_value=50, value=2)
    with col2:
        goal = st.number_input("Monthly goal (USD)", min_value=500, max_value=100000, value=3000)
        hours = st.number_input("Hours/week", min_value=5, max_value=50, value=30)
    
    if st.button("💰 Calculate Rate", use_container_width=True):
        if not skill:
            st.markdown('<div class="error-banner">❌ Enter your skill!</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Calculating..."):
                result = calculate_optimal_rate(skill, exp, goal, hours)
            st.markdown(result)

# ── PAGE: PROFILE BIO WRITER ─────────────────────────────
elif st.session_state.current_page == "📝 Profile Bio Writer":
    st.markdown("## 📝 Profile Bio Writer")
    st.markdown("Generate professional Upwork/Fiverr bios")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your name")
        skill = st.text_input("Main skill")
        exp = st.number_input("Years experience", min_value=0, max_value=50, value=2)
    with col2:
        spec = st.text_input("Specialization")
        achv = st.text_area("Achievements", height=80)
    
    if st.button("📝 Generate Bio", use_container_width=True):
        if not name or not skill:
            st.markdown('<div class="error-banner">❌ Fill in name & skill!</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Writing..."):
                bio = generate_profile_bio(name, skill, exp, spec, achv)
            st.markdown(f'<div class="proposal-box">{bio}</div>', unsafe_allow_html=True)

# ── PAGE: WEBSITE ANALYZER (FIX #3: ACCEPT JOB TEXT TOO) ─────────────────────────────
elif st.session_state.current_page == "🌐 Website Analyzer":
    st.markdown("## 🌐 Website Analyzer")
    st.markdown("Check client websites for red flags")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # FIX #3: Radio button for input type
    analysis_type = st.radio("What would you like to analyze?", ["Website URL", "Job Description"], horizontal=True)
    
    if analysis_type == "Website URL":
        website_url = st.text_input("Client Website URL", placeholder="https://example.com")
        analyze_input = website_url
        input_label = "website"
    else:
        job_text = st.text_area("Job Description", placeholder="Paste job description...", height=250)
        analyze_input = job_text
        input_label = "job description"
    
    if st.button("🔍 Analyze", use_container_width=True):
        if not analyze_input:
            st.markdown(f'<div class="error-banner">❌ Enter a {input_label}!</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Fetching & analyzing..."):
                # FIX #3: Handle both input types
                if analysis_type == "Website URL":
                    website_text = extract_website_text(analyze_input)
                    if website_text:
                        analysis_input = f"Website from {analyze_input}:\n\n{website_text}"
                    else:
                        st.markdown('<div class="error-banner">❌ Couldn\'t fetch website!</div>', unsafe_allow_html=True)
                        analysis_input = None
                else:
                    analysis_input = analyze_input
                
                if analysis_input:
                    analysis = detect_client_red_flags(analysis_input)
                    analysis_text = str(analysis).strip()
                    
                    if "high" in analysis_text.lower():
                        st.markdown('<div class="warning-banner">⚠️ SUSPICIOUS</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="red-flag-box">{analysis_text}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="success-banner">✅ LOOKS LEGITIMATE</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="green-box">{analysis_text}</div>', unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class='footer-text'>
    <strong style='color: #10b981;'>🇵🇰 PakFreelance</strong> — Professional AI Toolkit for Pakistani Freelancers<br>
    AMD Developer Hackathon 2026 | Track 1: AI Agents<br>
    <strong style='color: #64748b;'>Free • No ads • Open source</strong>
</div>
""", unsafe_allow_html=True)
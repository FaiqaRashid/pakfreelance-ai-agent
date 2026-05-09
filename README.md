# 🇵🇰 PakFreelance — AI Freelance Toolkit

> **Professional AI Agent Toolkit for Pakistani Freelancers**  
> *AMD Developer Hackathon 2026 | Track 1: AI Agents & Agentic Workflows*

**Powered by AMD MI300X through Groq's optimized API, running Llama 3.3 70B for fast inference. Deployed on HuggingFace Spaces.**

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![AMD](https://img.shields.io/badge/Powered%20By-AMD%20MI300X-ED1C24?logo=amd&logoColor=white)

---

## 🎯 Overview

**PakFreelance** is an AI-powered toolkit built with **CrewAI agents** that helps freelancers across Pakistan and South Asia:

✅ **Generate winning proposals** in seconds (5-agent AI orchestration)  
✅ **Detect client scams** before wasting time (red flag analysis)  
✅ **Calculate optimal rates** based on skills and goals  
✅ **Score proposals** with detailed improvement feedback  
✅ **Write professional bios** for Upwork/Fiverr  
✅ **Analyze client websites** for legitimacy  
✅ **One-click Power Mode** for complete job analysis  

Built for the **4M+ freelancers in Pakistan and South Asia** using **AMD MI300X infrastructure**, **Llama 3.3 70B**, and **CrewAI**.

---

## 🚀 Key Features

### ⚡ Power Mode (One-Click Analysis)
Paste a job posting → Get **risk assessment + proposal + pricing strategy** in 3 columns

### ✈️ Proposal Generator
5 specialized AI agents working together:
1. **Scout** - Extract job requirements
2. **Researcher** - Analyze client context  
3. **Writer** - Generate personalized proposal (150-200 words)
4. **Pricer** - Recommend optimal pricing
5. **Reviewer** - Polish & finalize

### 🚩 Red Flag Detector
- Identifies scam patterns
- Detects unrealistic budgets
- Spots exposure-only offers
- Provides safe response templates

### ⭐ Proposal Scorer
- Scores out of 100
- Breakdown by 7 criteria (Hook, Credibility, Understanding, Solution, etc.)
- Top 3 specific improvement suggestions

### 💰 Rate Calculator
- Pakistan-specific pricing (30-50% lower than US rates)
- Experience multiplier
- Monthly goal calculation
- Tax & platform fee buffer
- Three-tier pricing strategy (Start/Target/Premium)

### 📝 Profile Bio Writer
- Upwork/Fiverr optimized
- Compelling headlines
- Professional 150-200 word bios
- Personality-driven tone

### 🌐 Website Analyzer
- Extract website content
- Analyze for red flags
- Assess client legitimacy

### 📄 Document Reader
- Upload CV & Job PDFs
- Extract relevant info
- Provide smarter analysis

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **AI Framework** | CrewAI | Multi-agent orchestration |
| **LLM** | Llama 3.3 70B (via Groq) | Fast inference on AMD MI300X |
| **Infrastructure** | AMD MI300X (via Groq API) | GPU acceleration |
| **Web Framework** | Streamlit | Beautiful UI |
| **Document Export** | python-docx | Word document generation |
| **PDF Support** | PyPDF2 | PDF reading |
| **Web Scraping** | requests | Website text extraction |

---

## 📋 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  PAKFREELANCE APP                       │
│              (Streamlit Web Interface)                  │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
    ┌────────────┐      ┌──────────────┐
    │  Job Input │      │ User Profile │
    └──────┬─────┘      └──────┬───────┘
           │                   │
           └───────┬───────────┘
                   ▼
        ┌──────────────────────┐
        │   CrewAI Agents:     │
        ├──────────────────────┤
        │ • Scout Agent        │
        │ • Researcher Agent   │
        │ • Writer Agent       │
        │ • Pricer Agent       │
        │ • Reviewer Agent     │
        └───────┬──────────────┘
                │
                ▼
        ┌──────────────────────┐
        │  Groq API Call       │
        │ (Llama 3.3 70B)      │
        │                      │
        │ AMD MI300X Powered   │
        └───────┬──────────────┘
                │
                ▼
        ┌──────────────────────┐
        │  Output Results:     │
        ├──────────────────────┤
        │ • Proposals          │
        │ • Red Flags          │
        │ • Rates              │
        │ • Scores             │
        │ • Bios               │
        └──────────────────────┘
```

---

## 📦 Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/pakfreelance.git
cd pakfreelance
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt --break-system-packages
```

### 4. Set Up Environment Variables
Create `.env` file in project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

**Get API Keys:**
- **Groq:** https://console.groq.com (Free tier: 12,000 TPM)

### 5. Run Application
```bash
streamlit run app.py
```

Visit: `http://localhost:8501`

---

## 🎮 Usage Guide

### Power Mode (Quickest)
1. Click **⚡ Power Mode** in sidebar
2. Paste job posting
3. Click **🚀 Run Complete Analysis**
4. Get risk assessment + proposal + rates in 3 columns
5. Click expanders for full results

### Proposal Generator
1. Paste job posting
2. (Optional) Enter your skill & experience
3. Click **✈️ Generate Proposal**
4. Review proposal
5. Download as Word document (.docx)

### Red Flag Detector
1. Choose: **Job Description** or **Website URL**
2. Paste job or enter website
3. Click **🔍 Analyze for Red Flags**
4. Get risk level + specific red flags
5. Copy safe response template if HIGH RISK

### Rate Calculator
1. Enter skill (e.g., "Python Developer")
2. Enter years of experience
3. Enter monthly income goal (USD)
4. Enter available hours/week
5. Click **💰 Calculate Rate**
6. Get optimal hourly rate + pricing strategy

### Proposal Scorer
1. Paste your proposal
2. Click **⭐ Score My Proposal**
3. Get score out of 100 + breakdown + improvements

### Profile Bio Writer
1. Enter name, skill, experience
2. (Optional) Specialization & achievements
3. Click **📝 Generate Bio**
4. Get headline + professional bio

---

## 📊 Example Output

### Proposal Generated
```
Professional Proposal
Generated by: PakFreelance AI Toolkit

Building a complete e-commerce platform with a MERN stack is exactly 
the kind of challenge I enjoy solving. I have 5+ years of experience 
building scalable applications for e-commerce clients, including 10+ 
projects with React, Node.js, and MongoDB.

I'll design a responsive UI using React, implement a robust backend 
with Node.js and MongoDB, integrate Stripe for payments, and set up 
JWT authentication. You'll get a GitHub repo and full documentation.

I'm available immediately and can deliver within your 20-day timeline...

Best regards,
[Your Name]

---
Generated by PakFreelance AI
Powered by AMD MI300X • CrewAI • Llama 3.3 70B
```

### Rate Calculation
```
OPTIMAL HOURLY RATE: $15 - $30/hour

CALCULATION BREAKDOWN:
- Monthly goal: $3000
- Weeks per month: 4.3
- Hours per week: 30
- Base rate needed: $22.08/hour
- Market rate for Prompt Engineering: $25 - $50/hour
- Experience multiplier (2 years): 1.2
- Adjusted rate: $20 - $40/hour
- Considering Pakistani context: $15 - $30/hour

PRICING STRATEGY:
- Start at: $15/hour (to build reviews)
- Target rate: $25/hour (once established)
- Premium rate: $35/hour (for repeat clients)
```

---

## 🏗️ Project Structure

```
pakfreelance/
├── app.py                    # Main Streamlit app (650+ lines)
├── agents.py                 # CrewAI agents + tasks (150+ lines)
├── red_flags.py              # Red flag detection agent
├── proposal_scorer.py        # Proposal scoring agent
├── rate_calculator.py        # Rate calculation agent
├── profile_bio_writer.py     # Bio generation agent
├── requirements.txt          # Python dependencies
├── .env.example              # Example environment variables
├── README.md                 # This file
└── .gitignore               # Git ignore patterns
```

---

## 📋 Dependencies

```
crewai==0.25.0              # Multi-agent orchestration
streamlit==1.28.0           # Web UI framework
groq==0.4.1                 # Groq API client
litellm==1.0.0              # LLM wrapper
python-dotenv==1.0.0        # Environment variables
python-docx==0.8.11         # Word document creation
PyPDF2==3.0.1               # PDF reading
requests==2.31.0            # HTTP requests
duckduckgo-search==3.8.4    # Web search (optional)
```

Full list: See `requirements.txt`

---

## 🎯 AMD Technology Integration

### Infrastructure Overview

This project leverages **AMD MI300X GPUs through Groq's optimized API**:

- **LLM:** Llama 3.3 70B (AMD-optimized model)
- **Inference:** Groq API (runs on AMD MI300X)
- **Performance:** Fast token generation (100+ tokens/sec)
- **Hosting:** HuggingFace Spaces (production-ready)

### How AMD Powers This Application

1. **AMD MI300X GPU Compute**
   - All AI inference runs on AMD Instinct MI300X architecture
   - Powered via Groq's AMD-optimized endpoints
   - Fast token generation (100+ tokens/sec)
   - Cost-effective for production workloads

2. **ROCm Support**
   - Llama 3.3 70B is ROCm-compatible
   - Optimized for AMD Instinct MI300X
   - Can scale to local AMD GPU clusters with ROCm

3. **CrewAI Multi-Agent Orchestration on AMD**
   - 5 specialized agents working in sequence
   - All processing runs on AMD MI300X hardware
   - Demonstrates scalable agent architecture

4. **Why AMD for This Project**
   - ✅ Cost-effective inference (free API tier)
   - ✅ Production-ready infrastructure
   - ✅ Supports open-source models (Llama 3.3)
   - ✅ Scalable to enterprise deployments
   - ✅ No vendor lock-in (ROCm is open source)

---

## 🚀 Deployment

### Hugging Face Spaces (Recommended)

1. Create Hugging Face Space at https://huggingface.co/spaces
2. Select Streamlit SDK
3. Connect GitHub repository
4. Add environment variable: `GROQ_API_KEY`
5. Deploy automatically (3-5 minutes)
6. Get live URL for submission

### Local Testing
```bash
streamlit run app.py
```

---

## 🐛 Troubleshooting

### "RateLimitError from Groq"
Wait 8 seconds between requests. Free tier: 12,000 TPM (tokens per minute)

### "Invalid API Key"
Check `.env` file - make sure key starts with `gsk_` and has no extra spaces

### "ModuleNotFoundError"
```bash
pip install module-name --break-system-packages
```
## ⚡ Token Optimization

PakFreelance uses optimized token usage for Groq's free tier:
- All agents use `verbose=False` (reduces logging tokens)
- Job posting input limited to 500 characters (reduces context)
- 4 agents instead of 5 (faster processing)
- Each proposal generation: ~1,500-2,000 tokens

**Groq Free Tier:** 12,000 tokens/minute
- You can run 6-8 proposals per minute
- Wait 2 minutes between heavy usage

**Upgrade to Dev Tier (FREE):**
- 120,000 tokens/minute
- Unlimited proposals
- Go: https://console.groq.com/settings/billing

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- **AMD Developer Program** - Infrastructure & credits
- **lablab.ai** - Hackathon platform  
- **CrewAI** - Multi-agent orchestration framework
- **Groq** - Fast LLM inference on AMD MI300X
- **Llama 3.3 70B** - Powerful open-source language model
- **Streamlit** - Beautiful web framework

---

## 📞 Support

- **Documentation:** See this README
- **Issues:** Open a GitHub issue
- **Setup Help:** Check `.env.example` for environment variables

---

## 🚀 Future Roadmap

### Current (v1.0)
- ✅ Multi-agent proposal generation
- ✅ Red flag detection
- ✅ Rate calculation
- ✅ Proposal scoring
- ✅ Bio generation
- ✅ Website analysis
- ✅ Power Mode

### Planned (v2.0)
- Document upload & analysis
- Browser extension
- Mobile app
- Multi-language support

### Stretch Goals (v3.0)
- Fine-tuned models
- Real-time job scraping
- Auto-apply features
- Client management dashboard

---

**Built with ❤️ for Pakistani Freelancers**  
**Powered by AMD MI300X through Groq**  
**AMD Developer Hackathon 2026 - Track 1: AI Agents**

*Last Updated: May 8, 2026*

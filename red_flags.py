from crewai import Agent, Task, Crew, Process
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

MODEL = "groq/llama-3.3-70b-versatile"


red_flag_analyst = Agent(
    role="Client Red Flag Analyst",
    goal="Detect risky freelance job postings and protect freelancers from bad clients",
    backstory="""You are an expert at evaluating freelance job posts for risk.
You can quickly identify scam patterns, vague requirements, exposure-only offers,
scope-budget mismatch, manipulative tone, and warning signs that waste freelancer time.""",
    verbose=False,
    allow_delegation=False,
    llm=MODEL
)


def detect_client_red_flags(job_posting):
    task = Task(
        description=f"""Analyze this freelance job posting and detect client red flags.

JOB POSTING:
{job_posting}

Evaluate specifically for:
1. Exposure-only or unpaid work language
2. Unrealistic budget vs scope mismatch
3. Vague requirements or missing deliverables
4. Unrealistic timeline pressure
5. Scam-like patterns (external contact push, payment outside platform, urgency pressure)
6. Communication or tone red flags

Output format (strict):
RISK LEVEL: Low/Medium/High
RISK SCORE: X/10

RED FLAGS:
- [Short bullet]
- [Short bullet]

WHY THIS MATTERS:
[2-4 concise lines]

RECOMMENDED ACTION:
[1-3 practical steps for freelancer]

Rules:
- Keep total output under 180 words
- Be specific to this job post
- If no strong red flags exist, say so clearly and explain why
- Output only the final analysis text""",
        expected_output="A concise risk report with risk level, score, red flags, and actions",
        agent=red_flag_analyst
    )

    crew = Crew(
        agents=[red_flag_analyst],
        tasks=[task],
        process=Process.sequential,
        verbose=False
    )

    result = crew.kickoff()
    return str(result).strip()

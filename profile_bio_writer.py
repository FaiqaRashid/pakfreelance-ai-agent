from crewai import Agent, Task, Crew, Process
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

MODEL = "groq/llama-3.3-70b-versatile"

bio_writer = Agent(
    role="Professional Bio Writer",
    goal="Create compelling Upwork/Fiverr profile bios that win clients",
    backstory="""You are an expert at writing profile bios for freelancers.
You know exactly what clients look for and how to present freelancers
in the most professional, compelling way possible.""",
    verbose=False,
    allow_delegation=False,
    llm=MODEL
)

def generate_profile_bio(name, skill, years_exp, specialization, achievements):
    task = Task(
        description=f"""Write a professional Upwork/Fiverr profile bio.

FREELANCER INFO:
- Name: {name}
- Main Skill: {skill}
- Experience: {years_exp} years
- Specialization: {specialization}
- Achievements: {achievements}

Write BOTH:

1. PROFILE HEADLINE (max 60 characters):
A catchy, specific headline that includes their main skill

2. PROFILE OVERVIEW (150-200 words):
- Start with a strong opening statement
- Mention key achievements from their list
- Highlight specializations
- Show personality while staying professional
- Include call to action ("Let's discuss your project")
- Never use clichés like "hardworking" or "passionate"
- Make it conversational, not robotic

TONE: Professional, friendly, confident
LENGTH: Exactly 150-200 words for overview
LANGUAGE: Clear, engaging English

Output format:

HEADLINE:
[Write the headline here]

OVERVIEW:
[Write the full overview bio here]

Rules:
- Be specific, not generic
- Show personality
- Focus on client benefits, not your background
- Make the first sentence strong""",
        expected_output="Professional headline and profile overview bio",
        agent=bio_writer
    )

    crew = Crew(
        agents=[bio_writer],
        tasks=[task],
        process=Process.sequential,
        verbose=False
    )

    result = crew.kickoff()
    return str(result).strip()

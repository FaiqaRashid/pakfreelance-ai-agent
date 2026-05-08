from crewai import Agent, Task, Crew, Process
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

MODEL = "groq/llama-3.3-70b-versatile"

rate_expert = Agent(
    role="Freelance Pricing Expert",
    goal="Calculate optimal hourly rates for freelancers",
    backstory="""You are an expert in freelance pricing with deep knowledge of
market rates across different skills, experience levels, and regions.
You help freelancers earn what they deserve.""",
    verbose=False,
    allow_delegation=False,
    llm=MODEL
)

def calculate_optimal_rate(skill, experience_years, monthly_goal, hours_per_week):
    task = Task(
        description=f"""Calculate the optimal hourly rate for this freelancer.

FREELANCER PROFILE:
- Skill: {skill}
- Experience: {experience_years} years
- Monthly Income Goal: ${monthly_goal}
- Available Hours Per Week: {hours_per_week}

Consider:
1. Market rates for this skill on Upwork/Fiverr globally
2. Pakistani freelancer context (rates are typically 30-50% lower than US)
3. Experience level multiplier
4. Monthly goal calculation: (monthly_goal / 4.3 weeks / hours_per_week) = hourly_rate
5. Buffer for taxes, platform fees (take 20% off for Upwork/Fiverr fees)

Output format:
OPTIMAL HOURLY RATE: $XX - $YY/hour

CALCULATION BREAKDOWN:
- Monthly goal: ${monthly_goal}
- Weeks per month: 4.3
- Hours per week: {hours_per_week}
- Base rate needed: $XX/hour
- Market rate for {skill}: $XX - $YY/hour
- Experience multiplier ({experience_years} years): X.X
- Adjusted rate: $XX - $YY/hour

PRICING STRATEGY:
- Start at: $XX/hour (to build reviews)
- Target rate: $YY/hour (once established)
- Premium rate: $ZZ/hour (for repeat clients)

TIPS FOR {skill} IN YOUR REGION:
1. [Specific tip]
2. [Specific tip]
3. [Specific tip]

Keep output under 200 words.""",
        expected_output="Detailed rate calculation with pricing strategy",
        agent=rate_expert
    )

    crew = Crew(
        agents=[rate_expert],
        tasks=[task],
        process=Process.sequential,
        verbose=False
    )

    result = crew.kickoff()
    return str(result).strip()

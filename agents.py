from crewai import Agent, Task, Crew, Process
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

MODEL = "groq/llama-3.3-70b-versatile"

# ── AGENT 1: SCOUT ──────────────────────────────────────────
scout = Agent(
    role="Job Scout",
    goal="Extract all important details from a freelance job posting clearly and completely",
    backstory="""You are an expert at reading freelance job postings on platforms 
    like Upwork and Fiverr. You extract key requirements, skills needed, budget, 
    timeline, and client tone with perfect accuracy.""",
    verbose=True,
    allow_delegation=False,
    llm=MODEL
)

# ── AGENT 2: RESEARCHER ─────────────────────────────────────
researcher = Agent(
    role="Client Researcher",
    goal="Research the client and job context to find useful background information",
    backstory="""You are a skilled researcher who finds information about clients, 
    their companies, and their project needs. You help freelancers understand 
    exactly who they are pitching to so they can personalize their proposals.""",
    verbose=True,
    allow_delegation=False,
    llm=MODEL
)

# ── AGENT 3: WRITER ─────────────────────────────────────────
writer = Agent(
    role="Proposal Writer",
    goal="Write a compelling, personalized freelance proposal that wins the job",
    backstory="""You are an expert freelance proposal writer with years of 
    experience winning jobs on Upwork and Fiverr. You write proposals that 
    feel personal, professional, and directly address the client's needs. 
    You never use generic templates.""",
    verbose=True,
    allow_delegation=False,
    llm=MODEL
)

# ── AGENT 4: PRICER ─────────────────────────────────────────
pricer = Agent(
    role="Pricing Strategist",
    goal="Recommend the perfect price for the freelance job based on market rates",
    backstory="""You are a freelance pricing expert who understands market rates 
    for different skills and project types. You suggest competitive prices that 
    are neither too low nor too high, helping freelancers win jobs while earning 
    what they deserve.""",
    verbose=True,
    allow_delegation=False,
    llm=MODEL
)

# ── AGENT 5: REVIEWER ────────────────────────────────────────
reviewer = Agent(
    role="Quality Reviewer",
    goal="Review and improve the proposal to make it perfect before sending",
    backstory="""You are a senior editor who reviews freelance proposals for 
    quality, tone, relevance, and professionalism. You catch any issues and 
    improve the proposal to maximize the chance of winning the job.""",
    verbose=True,
    allow_delegation=False,
    llm=MODEL
)


# ── TASKS ────────────────────────────────────────────────────
def create_tasks(job_posting):

    task1 = Task(
        description=f"""Carefully read this job posting and extract all key information:

        JOB POSTING:
        {job_posting}

        Extract and clearly list:
        1. What exactly the client needs
        2. Required skills and technologies
        3. Budget (if mentioned)
        4. Timeline/deadline (if mentioned)
        5. Client tone (formal/casual/technical)
        6. Any special requirements or preferences
        """,
        expected_output="A clear, structured list of all job requirements and details",
        agent=scout
    )

    task2 = Task(
        description=f"""Based on this job posting, research and identify:

        JOB POSTING:
        {job_posting}

        Find out:
        1. What type of client/company is this likely to be
        2. What do clients like this usually value most
        3. What common mistakes freelancers make with this type of job
        4. What would make a proposal stand out for this specific job
        5. Any industry context that would help personalize the proposal
        """,
        expected_output="Detailed client research and insights to personalize the proposal",
        agent=researcher
    )

    task3 = Task(
       description=f"""Using the job analysis and client research, 
write a complete freelance proposal following this EXACT structure:

JOB POSTING:
{job_posting}

Follow this structure STRICTLY:

LINE 1 - HOOK (1 sentence):
Start with something specific from the job that caught your attention.
NOT "I am excited" or "I am thrilled" — be specific and different.
Example: "Optimizing MongoDB indexing for high-traffic apps is exactly 
the kind of challenge I enjoy solving."

LINE 2-3 - CREDIBILITY (2-3 sentences):
Mention your relevant experience briefly.
Use numbers if possible: "I have done this for 5+ clients"
Reference the freelancer profile if provided.

LINE 4-5 - YOUR PLAN (3-4 sentences):
Tell them SPECIFICALLY what you will do for their project.
Reference their exact requirements by name.
Show you read and understood their job posting.

LINE 6 - AVAILABILITY AND TIMELINE (1 sentence):
Confirm you can meet their timeline and are available immediately.

LINE 7 - CALL TO ACTION (1 sentence):
Invite them to chat — keep it simple and confident.

SIGN OFF:
Best regards,
[Your Name]

STRICT RULES:
- Total length: 150-200 words MAXIMUM
- Never start with "I am excited", "I am thrilled", "I am happy"
- Never repeat any sentence
- Never write the proposal twice
- Replace [Your Name] literally as [Your Name] — do not change it
- Do NOT sign off with any agent name or role name
- Sound like a real human freelancer, not a robot""",
        expected_output="A complete, personalized 150-200 word freelance proposal ready to send",
        agent=writer
    )

    task4 = Task(
        description=f"""Based on this job posting, suggest the ideal pricing:

        JOB POSTING:
        {job_posting}

        Provide:
        1. Recommended price range (minimum and maximum)
        2. What to include in the price
        3. Whether to charge hourly or fixed price
        4. Reasoning for this price recommendation
        5. One negotiation tip for this specific job
        """,
        expected_output="Clear pricing recommendation with reasoning and strategy",
        agent=pricer
    )

    task5 = Task(
       description="""Review the proposal from the Writer agent.

YOUR ONLY JOB:
1. Make sure it follows the hook, credibility, plan, availability, CTA structure
2. Make sure it does NOT start with "I am excited" or "I am thrilled"
3. Make sure the sign off is exactly: Best regards, [Your Name]
4. Make sure it is NOT longer than 200 words
5. Remove ANY repetition
6. Make sure it sounds human and genuine

OUTPUT RULES — CRITICAL:
- Output the final proposal text ONLY
- Do NOT add any explanation before or after
- Do NOT write "Here is the proposal" or any introduction
- Do NOT sign with your agent role name
- The ONLY sign off allowed is: Best regards, [Your Name]
- Write it ONCE and STOP""",
        expected_output="The final polished proposal ready to copy and send to the client",
        agent=reviewer
    )

    return [task1, task2, task3, task4, task5]


# ── MAIN CREW FUNCTION ───────────────────────────────────────
def run_pitchpilot(job_posting):
    tasks = create_tasks(job_posting)

    crew = Crew(
        agents=[scout, researcher, writer, pricer, reviewer],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()

    # Return only reviewer (task5) output to avoid mixed/duplicated text
    try:
        task_outputs = getattr(result, "tasks_output", None)
        if task_outputs and len(task_outputs) >= 5:
            reviewer_output = task_outputs[4]
            reviewer_text = getattr(reviewer_output, "raw", None) or str(reviewer_output)
            return reviewer_text.strip()
    except Exception:
        pass

    return str(result).strip()
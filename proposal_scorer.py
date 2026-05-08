from crewai import Agent, Task, Crew, Process
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

MODEL = "groq/llama-3.3-70b-versatile"

scorer = Agent(
    role="Proposal Quality Scorer",
    goal="Rate freelance proposals and provide improvement suggestions",
    backstory="""You are an expert at evaluating freelance proposals.
You know what makes proposals win or lose jobs. You score them fairly and give
actionable tips to improve them.""",
    verbose=False,
    allow_delegation=False,
    llm=MODEL
)

def score_proposal(proposal_text):
    task = Task(
        description=f"""Score this freelance proposal on a scale of 0-100.

PROPOSAL:
{proposal_text}

Evaluate on these criteria:
1. Opening Hook (10pts) - Does it grab attention immediately?
2. Credibility (15pts) - Does it show relevant experience?
3. Understanding (15pts) - Does it show the freelancer read the job?
4. Solution (20pts) - Is the plan clear and specific?
5. Professionalism (15pts) - Is it polished and grammatically correct?
6. Call to Action (10pts) - Does it end confidently?
7. Length (5pts) - Is it the right length (not too long/short)?

Output format:
OVERALL SCORE: XX/100

BREAKDOWN:
- Opening Hook: X/10 (feedback)
- Credibility: X/15 (feedback)
- Understanding: X/15 (feedback)
- Solution: X/20 (feedback)
- Professionalism: X/15 (feedback)
- Call to Action: X/10 (feedback)
- Length: X/5 (feedback)

TOP 3 IMPROVEMENTS:
1. [Specific suggestion]
2. [Specific suggestion]
3. [Specific suggestion]

Keep total output under 250 words.""",
        expected_output="A fair score with detailed feedback and improvement tips",
        agent=scorer
    )

    crew = Crew(
        agents=[scorer],
        tasks=[task],
        process=Process.sequential,
        verbose=False
    )

    result = crew.kickoff()
    return str(result).strip()

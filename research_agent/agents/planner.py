from langchain_google_genai import ChatGoogleGenerativeAI

from research_agent.contracts.research_contracts import (
    ResearchRequest,
    ResearchPlan
)
import os
from dotenv import load_dotenv
load_dotenv()

class ResearchPlanner:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
            google_api_key=os.environ["GEMINI_API_KEY"],
        )

        self.planner = self.llm.with_structured_output(
            ResearchPlan
        )

    def plan(self, request: ResearchRequest) -> ResearchPlan:

        prompt = f"""
You are an expert research planning agent.

Your job is to create a rigorous research plan
for the user's research request.

Do NOT answer the research question.

Instead:
1. Break the question into independent research tasks.
2. Define the objective of each task.
3. Generate useful search queries.
4. Assign a priority.
5. Identify useful source types.

Research request:

Question:
{request.question}

Domain:
{request.domain or "Not specified"}

Depth:
{request.depth}

Maximum sources:
{request.max_sources}

Create a focused research plan.
Avoid redundant tasks.
Make each task independently actionable.

Allocate the max_sources budget across tasks. The sum of all task source budgets must not exceed max_sources f'{request.max_sources}'. Phrase research questions neutrally and do not assume a conclusion.

"""
        print("Planning.... \n")
        plan = self.planner.invoke(prompt)
        return self.validate_plan(request, plan)


    def validate_plan(
        self,
        request: ResearchRequest,
        plan: ResearchPlan,
    ) -> ResearchPlan:

        print("Validating Plan...... \n")
        total_source_budget = sum(
            task.source_budget
            for task in plan.tasks
        )

        if total_source_budget > request.max_sources:
            raise ValueError(
                f"Research plan requests {total_source_budget} sources, "
                f"but the request allows only {request.max_sources}."
            )
        return plan

from research_agent.contracts.research_contracts import ResearchRequest
from research_agent.agents.planner import ResearchPlanner

from dotenv import load_dotenv

load_dotenv()


def main():

    request = ResearchRequest(
        question=(
            "What are the most effective approaches "
            "for reducing hallucinations in RAG systems?"
        ),
        domain="AI / LLMs",
        depth="standard",
        max_sources=10,
    )

    planner = ResearchPlanner()

    plan = planner.plan(request)

    print(plan.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
import pytest

from research_agent.contracts.research_contracts import (
    ResearchRequest,
    ResearchPlan,
    ResearchTask,
)

from research_agent.agents.planner import validate_plan


def test_plan_respects_source_budget():

    request = ResearchRequest(
        question="Test question",
        max_sources=10,
    )

    plan = ResearchPlan(
        research_question="Test question",
        tasks=[
            ResearchTask(
                question="Task 1",
                objective="Objective 1",
                search_queries=["query 1"],
                priority="high",
                source_budget=4,
            ),
            ResearchTask(
                question="Task 2",
                objective="Objective 2",
                search_queries=["query 2"],
                priority="medium",
                source_budget=3,
            ),
            ResearchTask(
                question="Task 3",
                objective="Objective 3",
                search_queries=["query 3"],
                priority="low",
                source_budget=3,
            ),
        ],
        expected_source_types=["academic research papers"],
    )

    validated_plan = validate_plan(request, plan)

    assert validated_plan == plan
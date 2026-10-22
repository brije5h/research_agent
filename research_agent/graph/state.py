from typing import Annotated

from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

from typing_extensions import TypedDict

from research_agent.contracts.research_contracts import (
    Finding,
    ResearchPlan,
    ResearchReport,
    ResearchRequest,
    ResearchTask,
    Source,
)

class ResearchState(TypedDict, total=False):

    request: ResearchRequest

    plan: ResearchPlan

    current_task: ResearchTask | None

    sources: list[Source]

    findings: list[Finding]

    report: ResearchReport

    messages: Annotated[
        list[AnyMessage],
        add_messages,
    ]
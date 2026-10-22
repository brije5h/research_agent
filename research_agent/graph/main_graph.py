from langgraph.graph import StateGraph, START, END

from research_agent.graph.state import ResearchState

from research_agent.agents.planner import ResearchPlanner
from research_agent.agents.researcher import Researcher
from research_agent.agents.evidence_extractor import EvidenceExtractor
from research_agent.agents.synthesizer import Synthesizer
from research_agent.graph.researcher_graph import build_researcher_graph

from research_agent.contracts.research_contracts import (Source)


planner = ResearchPlanner()
researcher = Researcher()
extractor = EvidenceExtractor()
synthesizer = Synthesizer()

def planner_node(state: ResearchState):

    request = state["request"]

    plan = planner.plan(request)
    # research_state = ResearchState()

    # research_state[plan] = plan
    return {
        "plan": plan
    }

def researcher_node(state: ResearchState):

    plan = state["plan"]

    all_sources = []

    for task in plan.tasks:

        result = researcher.research(task)

        # We will extract Source objects from the
        # researcher's tool
        #  messages here.
        #
        # For now this will be implemented using
        # a helper function.

        sources = extract_sources_from_messages(
            result["messages"]
        )

        all_sources.extend(sources)

    return {
        "sources": all_sources
    }


def researcher_graph_node(state: ResearchState):

    researcher_graph = build_researcher_graph()

    all_source = []

    plan = state["plan"]
    for task in plan:
        result = researcher_graph.invoke(task)

        for message in result["messages"]:
            if message.type =="Tool":
                source = Source(
                    
                )
                

        

    result = researcher_graph.invoke(

    )
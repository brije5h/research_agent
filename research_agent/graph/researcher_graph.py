from research_agent.tools.source_reader import read_source
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from research_agent.graph.state import ResearchState
from research_agent.tools.web_search import search_web
from research_agent.agents.researcher import Researcher

researcher = Researcher()

tools = [search_web, read_source]

tool_node = ToolNode(tools)

def researcher_node(state: ResearchState):

    response = researcher.llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }

def should_continue(state: ResearchState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END

def build_researcher_graph():

    graph = StateGraph(ResearchState)

    graph.add_node(
        "researcher",
        researcher_node,
    )

    graph.add_node(
        "tools",
        tool_node,
    )

    graph.add_edge(
        START,
        "researcher",
    )

    graph.add_conditional_edges(
        "researcher",
        should_continue,
        {
            "tools": "tools",
            END: END,
        },
    )

    graph.add_edge(
        "tools",
        "researcher",
    )

    return graph.compile()


if __name__ == "__main__":

    graph = build_researcher_graph()

    result = graph.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": """
                    Research the following:

                    Benefits of agents made with langGraph and deep agents.
                    """
                }
            ]
        }
    )

    for message in result["messages"]:
        if message.type == "tool":

            print("\n==============================")
            print("TOOL MESSAGE")
            print("==============================")
    
            print("content:", message.content)
            print("artifact:", getattr(message, "artifact", None))
            print("additional_kwargs:", message.additional_kwargs)
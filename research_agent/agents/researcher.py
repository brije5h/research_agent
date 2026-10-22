from _pytest._code.source import Source
from langchain_google_genai import ChatGoogleGenerativeAI
import json

from research_agent.contracts.research_contracts import (
    Source,
    ResearchTask,
    ResearchTaskResult,
)
from research_agent.tools.web_search import search_web
from research_agent.tools.source_reader import read_source

import os
from dotenv import load_dotenv
load_dotenv()

class Researcher:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model = "gemini-3.5-flash-lite",
            google_api_key = os.environ["GEMINI_API_KEY"]
        )
        self.tools = [
            search_web,
            read_source,
        ]
        self.llm_with_tools = self.llm.bind_tools(
            self.tools
        )
    
    def collect_sources(
        messages,
    ) -> list[Source]:

        sources = []

        for message in messages:

            if not hasattr(message, "artifact"):
                continue


    def extract_sources(messages) -> list[Source]:
    
        sources = []
    
        for message in messages:
        
            if message.type != "tool":
                continue
            
            if message.name != "read_source":
                continue
            
            try:
                data = json.loads(message.content)
    
                source = Source(
                    title=data["title"],
                    url=data["url"],
                    source_type=data["source_type"],
                    content=data["content"],
                )
    
                sources.append(source)
    
            except (json.JSONDecodeError, KeyError, TypeError):
                continue
            
        return sources

    def research(self, task: ResearchTask) -> ResearchTaskResult:
        
        prompt = f"""You are an advanced research agent. Your goal is to investigate the research task thoroughly by fetching live web pages and reading their full content.

            ### Research Task
            - **Question:** {task.question}
            - **Objective:** {task.objective}
            - **Suggested Search Queries:** {task.search_queries}
            - **Source Budget:** Up to {task.source_budget} sources

            ### Instructions & Workflow:
            1. **Search:** Use the `search_web` tool to find relevant URLs based on the research queries.
            2. **Select & Read:** From the search results, select the most authoritative sources and use the `read_source` tool to fetch their full content. Do not rely solely on search snippets.
            3. **Synthesize:** Base your final claims strictly on the text retrieved from `read_source`. 
            4. **Cite:** Keep track of which URL supports each claim. If evidence is insufficient, state so clearly. Do not invent facts.
            """
        response = self.llm_with_tools.invoke(prompt)

        return response

#         prompt = f"""
# You are a research agent.

# Your job is to investigate the following research task.

# Research question:
# {task.question}

# Objective:
# {task.objective}

# Search queries you may consider:
# {task.search_queries}

# Source budget:
# {task.source_budget}

# Use the search_web tool to find relevant information.

# Do not invent facts.
# Do not answer based only on your internal knowledge.
# Prefer authoritative and primary sources where possible.

# Research the task and report what you found.

# 1. Search for relevant sources.
# 2. Identify the strongest sources.
# 3. Read the sources using {self.tools.read_source} tool.
# 4. Do not treat search snippets as verified evidence.
# 5. Base claims on source content.
# 6. Keep track of which source supports each claim.
# 7. If evidence is insufficient, say so.

# """

        # response = self.llm_with_tools.invoke(prompt)

        # return response


if __name__ == "__main__":

    from research_agent.contracts.research_contracts import ResearchTask

    task = ResearchTask(
        question="What techniques reduce hallucinations in RAG?",
        objective="Find evidence about retrieval-based mitigation techniques.",
        search_queries=[
            "RAG hallucination retrieval mitigation"
        ],
        priority="high",
        source_budget=3,
    )

    researcher = Researcher()
    response = researcher.research(task)
    print(response)

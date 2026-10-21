from langchain_google_genai import ChatGoogleGenerativeAI

from research_agent.contracts.research_contracts import (
    ResearchTask,
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
    
    def research(self, task: ResearchTask):
        prompt = f"""
You are a research agent.

Your job is to investigate the following research task.

Research question:
{task.question}

Objective:
{task.objective}

Search queries you may consider:
{task.search_queries}

Source budget:
{task.source_budget}

Use the search_web tool to find relevant information.

Do not invent facts.
Do not answer based only on your internal knowledge.
Prefer authoritative and primary sources where possible.

Research the task and report what you found.

1. Search for relevant sources.
2. Identify the strongest sources.
3. Read the sources using {self.tools.read_source} tool.
4. Do not treat search snippets as verified evidence.
5. Base claims on source content.
6. Keep track of which source supports each claim.
7. If evidence is insufficient, say so.

"""

        response = self.llm_with_tools.invoke(prompt)

        return response


# if __name__ == "__main__":

#     from research_agent.contracts.research_contracts import ResearchTask

#     task = ResearchTask(
#         question="What techniques reduce hallucinations in RAG?",
#         objective="Find evidence about retrieval-based mitigation techniques.",
#         search_queries=[
#             "RAG hallucination retrieval mitigation"
#         ],
#         priority="high",
#         source_budget=3,
#     )

#     researcher = Researcher()
#     response = researcher.research(task)
#     print(response)

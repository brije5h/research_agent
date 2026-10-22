from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
import os

load_dotenv()

from research_agent.contracts.research_contracts import Findings
from research_agent.contracts.research_contracts import Source

class EvidenceExtractor:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
        )

        self.structured_llm = self.llm.with_structured_output(
            Findings
        )
    
    def extract(
        self,
        research_question: str,
        sources: list[dict],
    ) -> Findings:

        prompt = f"""
You are an evidence extraction agent.

Research question:
{research_question}

Your task is to extract factual findings from the
provided sources.

IMPORTANT RULES:

1. Every claim must be supported by evidence from
   the provided sources.

2. Do not use your own knowledge to introduce facts.

3. Do not treat a search-result snippet as evidence
   when source content is available.

4. Every finding must contain the URL of the source
   supporting it.

5. If the evidence is weak or ambiguous, assign a
   lower confidence score.

6. Do not invent URLs.

7. Prefer specific factual claims over vague summaries.

Sources:

{sources}
"""

        return self.structured_llm.invoke(prompt)
    

# if __name__ == "__main__":

#     evidence_extractor = EvidenceExtractor()
    
#     result = evidence_extractor.extract(
#         research_question="deep agents vs AI vs LangChain vs LangGraph",
#         sources = [Source(
#             url="https://www.langchain.com/blog/deep-agents-vs-langchain-vs-langgraph",
#             title="Deep Agents vs LangChain vs LangGraph",
#             source_type="blog",
#             content="Each layer plays a different role and offers a different amount of control. LangGraph is an agent runtime, LangChain is an agent framework, and Deep Agents is an agent harness. The runtime offers the most control and the least abstraction; the harness offers the inverse. All three are fully composable, so you can move between layers instead of picking one.\\n\\n## What each layer offers [...] The three layers sit at different points on that spectrum. LangGraph offers maximal determinism: it lets you encode domain knowledge directly into the graph's topology instead of leaving that judgment to a model. LangChain sits in the middle: the core agent loop is inherently non-deterministic, the model decides what happens next at every step. Deep Agents offers maximal agency: an agent loop that can run for longer and fan out at scale because of builtin features like summarization and [...] `\\u200d`LangChain is the agent framework: the abstraction and integrations layer. It ships with a super minimal agent harness. Whereas Deep Agents ships with best practices around context management, the LangChain agent abstraction is incredibly minimal and un-opinionated.\\n\\nThe core agent abstraction is pretty simple: an LLM, running in a loop, calling tools."
#         ),Source(
#             url="https://github.com/langchain-ai/deepagents",
#             title="GitHub - langchain-ai/deepagents: The batteries-included agent harness",
#             source_type="documentation",
#             content="Tip\\n\\nFor developing, debugging, and deploying AI agents and LLM applications, see LangSmith.\\n\\n## FAQ\\n\\n### How is this different from LangGraph or LangChain?\\n\\nLangGraph is the graph runtime. LangChain's `create_agent` is a minimal agent harness on top of it. Deep Agents is a more opinionated harness on top of `create_agent` — same building blocks, but with filesystem, sub-agents, context management, and skills bundled in. For how the three relate, see the LangChain ecosystem overview. [...] All three are layers in the same stack — see the LangChain ecosystem overview for how they relate. Use Deep Agents when you want the full harness — planning, context management, delegation — out of the box. Use LangChain's `create_agent` when you want a lighter harness without the bundled middleware. Drop to LangGraph when the agent loop itself isn't the right shape and you need a custom graph. [...] Yes! Deep Agents is built on LangGraph, designed for production agent deployments. Pair it with LangSmith for tracing, evaluation, and monitoring. See Going to production for the full guide.\\n\\n### When should I use Deep Agents vs. LangChain or LangGraph directly?"
#         ),Source(
#             url="https://www.langchain.com/deep-agents",
#             title="Deep Agents: Open Source Agent Harness | LangChain",
#             source_type="blog",
#             content="When should I use Deep Agents vs other LangChain frameworks?\\n\\nUse Deep Agents when you want to build an autonomous agent to handle complex, non-deterministic, and long running tasks.\\n\\nChoose LangGraph when you want low-level control for building stateful, long-running workflows and agents.\\n\\nChoose LangChain when you want a quick way to get started and to standardize how teams build agent patterns.\\n\\nLearn more about when to choose each LangChain framework."
#         )
#         ],
#     )

#     print(result.model_dump_json(indent=2))
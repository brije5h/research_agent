from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

load_dotenv()

from research_agent.contracts.research_contracts import (
    Finding,
    ResearchReport,
    Source,
)


class Synthesizer:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
        )

        self.structured_llm = self.llm.with_structured_output(
            ResearchReport
        )

    def synthesize(
        self,
        research_question: str,
        findings: list[Finding],
        sources: list[Source],
    ) -> ResearchReport:

        prompt = f"""
You are the final research synthesis agent.

Research question:
{research_question}

Your job is to produce a research report using ONLY
the provided findings and sources.

IMPORTANT RULES:

1. Do not introduce facts that are not present in
   the findings or sources.

2. Every important conclusion must be supported by
   one or more findings.

3. Preserve source URLs from the provided sources.

4. Do not invent sources or URLs.

5. Clearly distinguish established evidence from
   uncertain conclusions.

6. If the evidence is insufficient to make a strong
   recommendation, say so.

7. The final report should directly answer the
   research question.

Findings:
{findings}

Sources:
{sources}
"""

        return self.structured_llm.invoke(prompt)



if __name__ == "__main__":

    synthesizer = Synthesizer()

    findings = [
        Finding(
            claim="Hybrid retrieval combines dense and sparse retrieval.",
            evidence=(
                "The source describes combining semantic"
                "vector retrieval with lexical retrieval."),
            source_urls=[
                "https://example.com/source"
            ],
            confidence_score=0.85,
        )
    ]

    sources = [
        Source(
            title="Example RAG Research",
            url="https://example.com/source",
            source_type="research_paper",
            content="Retrieval-Augmented Generation (RAG) is an AI framework that improves Large Language Model (LLM) outputs by connecting them to external knowledge sources. Instead of relying only on static training data, RAG fetches verified information from databases or documents at query time to ground the response."
        )
    ]

    report = synthesizer.synthesize(
        research_question=(
            "What techniques can reduce hallucinations "
            "in RAG systems?"
        ),
        findings=findings,
        sources=sources,
    )

    print(report.model_dump_json(indent=2))
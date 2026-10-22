from pydantic import BaseModel, Field
from typing import Literal

class ResearchRequest(BaseModel):
    question: str
    domain: str | None
    depth: Literal["quick","standard", "deep"]
    max_sources: int=10

class Source(BaseModel):
    title: str
    url: str
    content: str
    source_type: Literal[
        "research_paper",
        "documentation",
        "blog",
        "forum",
        "other"
    ]


class SourceReadResponse(BaseModel):
    url: str
    title: str
    content: str
    source_type: str = Field(default="other")

class SourceReadError(BaseModel):
    url: str
    error: str = Field(default="failed to read source")
    
class Finding(BaseModel):
    claim: str
    evidence: str
    source_urls: list[str]
    confidence_score: float=Field(ge=0.0,le=1.0)

class Findings(BaseModel):
    findings: list[Finding]

class ResearchReport(BaseModel):
    title: str
    executive_summary: str
    findings: list[Finding]
    sources: list[Source]
    recommendation: str | None
    confidence: float

class ResearchTask(BaseModel):
    question: str
    objective: str
    search_queries: list[str]
    priority: Literal["high", "medium", "low"]
    source_budget: int = Field(ge=1)

class ResearchTaskResult(BaseModel):
    task: ResearchTask
    sources_found: list[Source]
    findings: list[Finding]
    completed: bool

class ResearchPlan(BaseModel):
    research_question: str
    tasks: list[ResearchTask]
    expected_source_types: list[str]

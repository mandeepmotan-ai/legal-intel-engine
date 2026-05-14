from pydantic import BaseModel, Field 
from typing import Optional, List

class ContractMetadata(BaseModel):
    """Metadata about the contract file"""
    filename: str
    page_count: int
    file_type: str = "pdf"

class ProcessedContract(BaseModel):
    """The structured output after parsing a contract"""
    content: str #the actual text/ markdown
    metadata: ContractMetadata 
    hash: str #to check if we have processed this exact file before 

class ContractRisk(BaseModel):
    clause_text: str = Field(description="The original text of the risky clause")
    risk_level: str = Field(description="High, Medium or Low")
    explanation: str = Field(description="Why this is a risk and how to fix it")

class ImportantDate(BaseModel):
    event: str = Field(description="The event (e.g., Expiry, Payment)")
    date: str = Field(description="The date found in the contract")

class ContractAuditReport(BaseModel):
    summary: str = Field(description="Plain English summary for a non-lawyer")
    pros: List[str] = Field(description="Advantages for the user")
    cons: List[str] = Field(description="Disadvantages or risks")
    red_flags: List[str] = Field(description="One-sided or predatory clauses")
    important_dates: List[ImportantDate]
    missing_clauses: List[str] = Field(description="Standard protections that are absent")
    unfair_terms: List[str] = Field(description="Terms that might be legally invalid/unfair")
    indian_law_check: str = Field(description="POV on how this fits Indian Legal System (e.g., Stamp Act, Arbitration)")
    negotiation_points: List[str] = Field(description="Ready-to-use points for negotiation")
    risk_score: int = Field(description="Overall risk from 1-10")
    
class ValidationFeedback(BaseModel):
    """Feedback from Agent B to Agent A."""
    is_valid: bool = Field(description="True if the report is accurate and legally sound")
    errors: List[str] = Field(description="List of specific hallucinations or legal inaccuracies")
    improvement_suggestions: Optional[str] = Field(description="Instructions on how to fix the report")


    
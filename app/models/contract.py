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

class ContractAuditReport(BaseModel):
    summary: str = Field(description="A brief summary of the contract")
    risks: List[ContractRisk]
    pros: List[str] = Field(description="List of clauses that benefit the user")
    suggested_negotiations: List[str]
    overall_risk_score: int = Field(description="A score from 1 to 10")
    


    
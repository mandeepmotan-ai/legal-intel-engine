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

    
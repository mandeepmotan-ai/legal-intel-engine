import os 
from groq import Groq
from dotenv import load_dotenv 
import json
from app.models.contract import ContractAuditReport


load_dotenv(override=True)

class ContractBrain():
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
        #we use llama4 Scout for it's high speed reasoning 
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"

    def analyze_contract_structured(self, contract_content: str) -> ContractAuditReport:
        # We define a simpler version of the schema for the prompt
        # but keep the actual Pydantic model for validation.
        
        system_prompt = """
        You are a Senior Legal AI Auditor. Analyze the contract and return a JSON object.
        
        The JSON must have these exact keys:
        - "summary": (string) A brief overview of the contract.
        - "risks": (list of objects) Each object must have "clause_text", "risk_level" (High/Medium/Low), and "explanation".
        - "pros": (list of strings) Beneficial clauses.
        - "suggested_negotiations": (list of strings) How to improve the contract.
        - "overall_risk_score": (integer) 1 to 10.

        IMPORTANT: Do not return the schema. Return the actual analysis populated with data from the contract.
        ONLY return the JSON object. No conversational text.
        """

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this contract:\n\n{contract_content}"}
            ],
            model=self.model,
            response_format={"type": "json_object"},
            temperature=0.1
        )

        # 1. Get the raw string content
        content_string = response.choices[0].message.content
        
        # 2. Parse the string into a Python Dictionary
        analysis_dict = json.loads(content_string)
        
        # 3. Validation: This is where Pydantic checks if the AI followed instructions
        # If the AI missed a field, this line will catch it!
        return ContractAuditReport(**analysis_dict)
    

    def answer_question(self, question: str, context_chunks: list):
        #join the relevant chunks we found in the Vector DB
        context_text = "\n---\n".join([res.document for res in context_chunks]])

        system_prompt = """
        You are a legal Assistant. Use the following excerpts from a contract to answer user's question.
        Simply if there answer is not in the given context, just simply say you dont know.

        CONTEXT : {context_text}
        """

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            model=self.model,
            temperature=0.1
        )
        return response.choices[0].message.content


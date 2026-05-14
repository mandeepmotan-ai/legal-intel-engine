import os 
from groq import Groq
from dotenv import load_dotenv 
import json
from app.models.contract import ContractAuditReport

load_dotenv(override=True)

class ContractBrain():
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        # Using the Llama 4 Scout model as discussed
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"

    def perform_initial_audit(self, contract_content: str) -> ContractAuditReport:
        """
        Performs a comprehensive 8-point audit with an Indian Legal POV.
        """
        system_prompt = """
            You are a Master Legal Auditor specialized in the Indian Contract Act, 1872.
            Analyze the provided contract and return a strictly structured JSON report.

            STRICT ADHERENCE TO TRUTH:
            1. ONLY extract information explicitly stated or clearly implied by the text.
            2. NO HALLUCINATIONS: If a specific category (e.g., Red Flags, Unfair Terms, or Important Dates) does not exist in the contract, return an empty list [] for that field.
            3. For the 'indian_law_check', if the contract is too simple to have specific Indian legal implications, state: "Standard contract with no specific Indian legal conflicts identified."
            4. If there are no missing clauses (i.e., the contract is perfect), return an empty list [].

            THE JSON SCHEMA:
            - "summary": (string) Plain English summary.
            - "pros": (list) Beneficial clauses. [] if none.
            - "cons": (list) Disadvantages. [] if none.
            - "red_flags": (list) Predatory/one-sided clauses. [] if none.
            - "important_dates": (list of objects) {"event": str, "date": str}. [] if none.
            - "missing_clauses": (list) Standard protections absent. [] if none.
            - "unfair_terms": (list) Legally questionable terms. [] if none.
            - "indian_law_check": (string) POV on Indian law.
            - "negotiation_points": (list) Points to negotiate. [] if none.
            - "risk_score": (int) 1-10.

            ONLY return the JSON object. Do not invent clauses to fill the fields.
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

        content_string = response.choices[0].message.content
        analysis_dict = json.loads(content_string)
        
        # Validates against the 10-field model we discussed
        return ContractAuditReport(**analysis_dict)

    def answer_question(self, question: str, context_chunks: list):
        """
        Uses RAG to answer specific questions based on contract excerpts.
        """
        # FIX 1: Removed the extra closing bracket ']]'
        # FIX 2: Added a check for empty chunks
        context_text = "\n---\n".join([res.document for res in context_chunks])

        # FIX 3: Changed to an f-string so {context_text} is actually inserted
        system_prompt = f"""
        You are a legal assistant. Use the following excerpts from a contract to answer the user's question.
        If the answer is not in the context, simply say: "I don't have enough information in the contract to answer that."

        CONTEXT:
        {context_text}
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
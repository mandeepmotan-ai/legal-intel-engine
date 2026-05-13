import os 
from groq import Groq
from dotenv import load_dotenv 


load_dotenv(override=True)

class ContractBrain():
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
        #we use llama4 Scout for it's high speed reasoning 
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"

    def analyze_contract(self, contract_content: str):
        system_prompt = """
            You are a Senior Legal AI Auditor with 20 years of experience in contract law.
            Your goal is to analyze the provided contract (in Markdown) and identify:
            1. TOP 3 RISKS: Specific clauses that are predatory or dangerous for the user.
            2. TOP 3 ADVANTAGES: Clauses that benefit the user.
            3. MISSING CLAUSES: Standard legal protections that are absent.
        
            RULES:
            - Use a professional, objective tone.
            - Be extremely specific (mention section numbers if available).
            - IMPORTANT: Add a disclaimer at the end stating you are an AI, not a lawyer.
            """
        
        user_prompt = f"Please analyze this contract content: \n\n{contract_content}"

        #agentic call , we expect structured reasoning 
        chat_completion = self.client.chat.completions.create(
            messages=[
                {'role':'system', 'content': system_prompt},
                {'role':'user', 'content': user_prompt}
            ],
            model=self.model,
            temperature=0.1  #so that it stay more consistent and factual output
        )

        return chat_completion.choices[0].message.content
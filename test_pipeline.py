import os 
from app.services.parser import DocumentParser
from app.services.protector import PrivacyShield
from app.services.brain import ContractBrain

def run_test():
    parser = DocumentParser()       #initialize our parser

    shield_masker = PrivacyShield()    #initialize our PII masker using presidio

    ai_brain = ContractBrain()      #initialize brain to access integrated LLM using groq

    # point to a pdf file
    test_pdf_path = "data/raw/sample.pdf"

    if not os.path.exists(test_pdf_path):
        print(f"Error: Please place a pdf file at {test_pdf_path}")
        return

    print(f'Starting to parse: {test_pdf_path}...')

    try: 
        # use the parser 
        processed_doc = parser.parse(test_pdf_path)

        # inspect the results
        print("\n--- METADATA ---")
        print(f'Filename: {processed_doc.metadata.filename}')
        print(f'Page count: {processed_doc.metadata.page_count}')

        print(f'\n--- CONTENT PREVIEW (first 500 chars only) ---')
        print(processed_doc.content[:500])
        print(f'\n--- END OF PREVIEW ---')

        print(f'\n Sucess! The document was converted to markdown.')

        print(f'---------------------------------------- Parsing Ended -------------------------------\n\n\n\n')

        print(f"Starting to mask PII...")

        masked_data = shield_masker.mask_sensitive_data(processed_doc.content)

        print(masked_data)
        print(f'---------------------------------------- Masked Data End -------------------------------\n\n\n\n')

        contract_reasoning = ai_brain.analyze_contract(masked_data)
        print(f'AI Lawyer :    \n\n{contract_reasoning}')



    
    except Exception as e:
        print(f'An error occured during parsing {e}')
    
if __name__ == "__main__":
    run_test()


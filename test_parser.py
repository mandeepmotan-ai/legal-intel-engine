import os 
from app.services.parser import DocumentParser
from app.services.protector import PrivacyShield

def run_test():
    #1. initialize our parser
    parser = DocumentParser()

    shield_masker = PrivacyShield()

    #2. point to a pdf file
    test_pdf_path = "data/raw/sample.pdf"

    if not os.path.exists(test_pdf_path):
        print(f"Error: Please place a pdf file at {test_pdf_path}")
        return

    print(f'Starting to parse: {test_pdf_path}...')

    try: 
        #3. time to use the parser we wrote in older file
        processed_doc = parser.parse(test_pdf_path)

        #4. inspect the results
        print("\n--- METADATA ---")
        print(f'Filename: {processed_doc.metadata.filename}')
        print(f'Page count: {processed_doc.metadata.page_count}')

        print(f'\n--- CONTENT PREVIEW (first 500 chars only) ---')
        print(processed_doc.content[:500])
        print(f'\n--- END OF PREVIEW ---')

        print(f'\n Sucess! The document was converted to markdown.')

        print(f"Starting to mask PII...")

        masked_data = shield_masker.mask_sensitive_data(processed_doc.content)

        print(masked_data)



    
    except Exception as e:
        print(f'An error occured during parsing {e}')
    
if __name__ == "__main__":
    run_test()


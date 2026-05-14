import os 
from app.services.orchestrator import ContractAuditor


def test_collaborative_audit():
    auditor = ContractAuditor()
    test_file = "data/raw/sample.pdf"

    if not os.path.exists(test_file):
        print('Sample pdf not found!')
        return
    
    print("🚀 PHASE 1: Agent A is auditing...")        #Initial auditing by Agent A 
    raw_doc = auditor.parser.parse(test_file)
    safe_content = auditor.shield.mask_sensitive_data(raw_doc.content)
    report = auditor.brain.perform_initial_audit(safe_content)

    print("🕵️ PHASE 2: Agent B (Validator) is checking for hallucinations...")        #Secondary auditing by Agent B
    validation = auditor.brain.validate_audit(safe_content, report.model_dump_json())

    #presenting the results to user
    print("\n +"*50)
    print("Agent A's Summary: ")
    print(report.summary)
    print(f'Risk Score: {report.risk_score}/10')

    if not validation.is_valid:
        print("\n ⚠️  AGENT B FOUND CONCERNS:")
        for error in validation.errors:
            print(f'- {error}')
        
        print("\nPROMPT: Should we rerun Agent A with this feedback? (y/n)")
        choice = input("> ").lower()

        if choice == 'y':
            print("🔄 Rerunning with feedback... (We will implement this loop next)")
        else: 
            print("⏩ Proceeding with the original report.")

    else:
        print("\n✅ Verification of this report by Agent B is successfull!")

    print("\n💬 You can now ask questions about the contract. (Type 'exit' to stop)")
    while True:
        query = input("Ask a question: ")
        if query.lower() == 'exit': break
        print(f"AI: Let me look into that for you...")
        # (This is where our search_contract logic will go)

if __name__ == "__main__":
    test_collaborative_audit()

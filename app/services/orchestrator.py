from app.services.parser import DocumentParser
from app.services.protector import PrivacyShield
from app.services.brain import ContractBrain
from app.models.contract import ContractAuditReport


class ContractAuditor():
    def __init__(self):
        self.parser = DocumentParser()
        self.shield = PrivacyShield()
        self.brain = ContractBrain()

    def audit_contract(self, file_path: str) -> ContractAuditReport:
        #Parse and protect contract
        raw_doc = self.parser.parse(file_path)
        safe_content = self.shield.mask_sensitive_data(raw_doc.content)

        #Agent A: Initial Audit
        report = self.brain.perform_initial_audit(safe_content)

        #Agent B: The Validation
        #converting the report to string , so that agent B could read it 
        report_json = report.model_dump_json()
        validation = self.brain.validate_audit(safe_content, report_json)

        if not validation.is_valid:
            print(f'Validation Failed: {validation.errors}')
            #here Agent A is to be triggered again with the feedback
            #for now, we log it and return the corrected mindset
            # and well in a full langGraph setup, this would have been an automated loop
        
        return report 

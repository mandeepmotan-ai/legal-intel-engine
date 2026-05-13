from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig


class PrivacyShield():
    def __init__(self):
        #the analyzer find the PII (name, phones, etc)
        self.analyzer = AnalyzerEngine()
        #the anonymizer replaces them with placeholders
        self.anonymizer = AnonymizerEngine()

    def mask_sensitive_data(self, text: str) -> str:
        #1. analyze the text to find PII 
        results = self.analyzer.analyze(text=text, entities=["PERSON","PHONE_NUMBER","EMAIL_ADDRESS","LOCATION"], language='en')

        #2. define how to mask it (we wanna replace with the entity name)
        operators = {
            "PERSON" : OperatorConfig("replace", {"new_value":"<PERSON>"}),
            "LOCATION" : OperatorConfig("replace", {"new_value":"<LOCATION>"}),
            "EMAIL_ADDRESS" : OperatorConfig("replace", {"new_value":"<EMAIL_ADDRESS>"}),
            "PHONE_NUMBER" : OperatorConfig("replace", {"new_value":"<PHONE_NUMBER>"}),
        }

        #3. anonymize
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results,
            operators=operators
        )

        return anonymized_result.text
    
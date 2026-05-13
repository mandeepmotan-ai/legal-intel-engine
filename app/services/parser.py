from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter
from app.models.contract import ProcessedContract, ContractMetadata



class DocumentParser:
    def __init__(self):
        #DocumentConverter is the engine that handles different formats
        self.converter = DocumentConverter()

    def parse(self, file_path: str) -> ProcessedContract:
        #1. convert the doc
        result = self.converter.convert(file_path)

        #2. export to md as LLM's love Markdown
        markdown_content = result.document.export_to_markdown()

        #3. create our structured model 
        return ProcessedContract(
            content=markdown_content,
            metadata=ContractMetadata(
                filename=file_path.split("/")[-1],
                page_count=len(result.document.pages)
            ),
            hash='placeholder-hash' #will implement real hashing later 
        )
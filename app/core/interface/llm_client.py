from abc import ABC, abstractmethod
## 타입 명시를 위해 import
from typing import List
from langchain_core.documents import Document
from langchain_postgres import PGVector

class LlmClient(ABC):
    
    @abstractmethod
    def chat_llm(self, collection_name: str, documents: List[Document]) -> PGVector:
        pass
    
    @abstractmethod
    def llm_request(self, prompt) -> str:
        pass

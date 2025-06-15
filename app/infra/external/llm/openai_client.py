import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from app.core.interface.llm_client import LlmClient
# from app.config import vector_db_config


load_dotenv(find_dotenv()) #환경 변수 로드하기.

class OpenAIChatClient(LlmClient):
    
    _llm = None
    
    #open AI 키 로드
    def __init__(self):
        
        #싱글톤으로 매번 커넥션을 맽지 않도록 함.
        if OpenAIChatClient._llm is None:
            self._initialize_embeddings()
    
    
    def _initialize_embeddings(self):
        
        openai_api_key = os.getenv('OPENAI_API_KEY')
    
        
        if not openai_api_key:
            raise ValueError("OPENAI API KEY가 없습니다.")
    
        #OpenAI chat도 한 번만 초기화
        OpenAIChatClient._llm = ChatOpenAI(
            openai_api_key = openai_api_key,
            model = "gpt-4o",
            temperature = 0
        )
        
    @property
    def chat_llm(self):
        return OpenAIChatClient._llm
    
    
    def llm_request(self, prompt) -> str:
        return self._llm.invoke(prompt).content
    
    

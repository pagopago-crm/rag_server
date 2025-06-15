from typing import List, Dict, Any
from langchain_core.documents import Document
import os
import base64
from pathlib import Path
from typing import List, Dict

class ImageExtractor:
    def __init__(self):
        pass
    
    ## 
    def image_to_base64(self, directory_path) -> List[Dict[str,str]]:
        """이미지를 base64로 변환"""
        
        image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        
        result = []
        
        directory = Path(directory_path)
        
        for file_path in directory.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                with open(file_path, "rb") as image_file:
                    base64_string = base64.b64encode(image_file.read()).decode("utf-8")
                    result.append(
                        {
                            "filename": file_path.name,
                            "base64" : base64_string
                        }
                    )        
        return result
            
    def create_column_document(self, analysis_results: list) -> List[Document]:
        
        
        documents = []
        
        for result in analysis_results:
            
            meta_data = {
                "service_name": result["input_metadata"]["service_name"],
                "screen_name": result["input_metadata"]["screen_name"], 
                "version": result["input_metadata"]["version"],
                "access_level": result["input_metadata"]["access_level"],
                "screen_type": result["screen_analysis"]["screen_type"],
                "visible_title": result["screen_analysis"]["visible_title"],
                "primary_purpose": result["screen_analysis"]["primary_purpose"]
            }
            # 2. page_content 구성 (검색 대상 텍스트)
            page_content = f"""
                서비스명: {result["input_metadata"]["service_name"]}
                화면명: {result["input_metadata"]["screen_name"]}
                화면 제목: {result["screen_analysis"]["visible_title"]}
                화면 유형: {result["screen_analysis"]["screen_type"]}
                주요 목적: {result["screen_analysis"]["primary_purpose"]}
                레이아웃 설명: {result["screen_analysis"]["layout_description"]}

                화면의 모든 텍스트:
                {', '.join(result["extracted_elements"]["all_visible_text"])}

                버튼 텍스트:
                {', '.join(result["extracted_elements"]["button_texts"])}

                입력 필드:
                {', '.join(result["extracted_elements"]["field_labels"])}

                메뉴 항목:
                {', '.join(result["extracted_elements"]["menu_items"])}

                UI 구성요소:
                - 폼 존재: {result["ui_components"]["has_form"]}
                - 테이블 존재: {result["ui_components"]["has_table"]}  
                - 검색 기능: {result["ui_components"]["has_search"]}
                - 차트 존재: {result["ui_components"]["has_charts"]}

                사용자 액션:
                {', '.join(result["functional_indicators"]["user_actions"])}

                CRUD 작업:
                - 생성: {result["functional_indicators"]["crud_operations"]["create"]}
                - 조회: {result["functional_indicators"]["crud_operations"]["read"]}
                - 수정: {result["functional_indicators"]["crud_operations"]["update"]}
                - 삭제: {result["functional_indicators"]["crud_operations"]["delete"]}

                검색 키워드:
                {', '.join(result["search_keywords"])}
            """.strip()
            
            # 3. Document 생성 - 임베딩 할 내용
            document = Document(
                page_content=page_content,
                metadata=meta_data
            )
            
            documents.append(document)
            
        return documents
            
    

    def _get_column_business_meaning(self, table_name: str, column_name: str, description: str) -> str:
        
        # 공통 컬럼 패턴
        if column_name in ['reg_dt', 'mod_dt']:
            return "데이터 등록 및 변경 시간 저장을 위한 시스템 컬럼"
        elif 'seq' in column_name:
            return "고유 식별자로 사용되는 시퀀스 값이자 순번"
        elif 'yn' in column_name:
            return "Y/N 플래그로 상태를 관리"
        elif 'type' in column_name:
            return "분류/구분을 위한 코드 값"
        elif 'dt' in column_name:
            return "날짜/시간 정보"
        elif 'no' in column_name:
            return "번호 형태의 식별 정보"
        elif 'id' in column_name:
            return "식별자 또는 연결키"
        elif 'cnt' in column_name:
            return "수량/개수 정보"
        elif 'url' in column_name:
            return "웹 링크/경로 정보"
        
        # 테이블별 특화 의미
        if 'gift' in table_name:
            return f"상품 관련 {description}"
        elif 'user' in table_name:
            return f"사용자 관련 {description}"
        elif 'event' in table_name:
            return f"이벤트 관련 {description}"
        
        return description

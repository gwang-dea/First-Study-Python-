import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import pandas as pd

def extract_urls_from_webpage(url):
    """웹페이지에서 모든 URL 추출"""
    try:
        # 웹페이지 내용 가져오기
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 모든 a 태그에서 href 속성 추출
        urls = set()
        for a_tag in soup.find_all('a'):
            href = a_tag.get('href')
            if href and href != '#':
                # 상대 URL을 절대 URL로 변환
                full_url = urljoin(url, href)
                # URL 정규화 (파라미터, 프래그먼트 제거)
                parsed = urlparse(full_url)
                normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                urls.add(normalized_url)
        
        return list(urls)
    except Exception as e:
        print(f"URL 추출 중 오류 발생: {e}")
        return []
def compare_with_blocklist(extracted_urls, blocklist_file, output_file):
    """추출된 URL을 금지 리스트와 비교하고 신규 URL만 추가"""
    try:
        # 금지 리스트 불러오기
        try:
            blocklist_df = pd.read_excel(blocklist_file)
            # URL 컬럼 이름 확인 (실제 컬럼명으로 변경 필요)
            url_column = 'URL'  # 엑셀 파일의 URL 컬럼명
            blocklist = set(blocklist_df[url_column].str.lower())
        except Exception as e:
            print(f"금지 리스트 파일 읽기 오류: {e}")
            blocklist = set()
        
        # 신규 URL 필터링
        new_urls = []
        for url in extracted_urls:
            if url.lower() not in blocklist:
                new_urls.append(url)
        
        # 결과 출력
        print(f"추출된 URL 수: {len(extracted_urls)}")
        print(f"금지 리스트에 없는 신규 URL 수: {len(new_urls)}")
        
        # 신규 URL을 엑셀 파일에 저장
        new_urls_df = pd.DataFrame({url_column: new_urls})
        
        # 기존 파일이 있으면 합치기, 없으면 새로 생성
        try:
            existing_df = pd.read_excel(output_file)
            combined_df = pd.concat([existing_df, new_urls_df], ignore_index=True)
            # 중복 제거
            combined_df = combined_df.drop_duplicates(subset=[url_column])
            combined_df.to_excel(output_file, index=False)
        except FileNotFoundError:
            new_urls_df.to_excel(output_file, index=False)
        
        return new_urls
    except Exception as e:
        print(f"URL 비교 중 오류 발생: {e}")
        return []


def main():
    # 사용자 입력
    target_url = input("URL을 추출할 웹페이지 주소를 입력하세요: ")
    blocklist_file = input("금지 리스트가 있는 엑셀 파일 경로를 입력하세요: ")
    output_file = input("결과를 저장할 엑셀 파일 경로를 입력하세요: ")
    
    # URL 추출
    print("웹페이지에서 URL 추출 중...")
    extracted_urls = extract_urls_from_webpage(target_url)
    
    # 금지 리스트와 비교 및 저장
    print("금지 리스트와 비교 중...")
    new_urls = compare_with_blocklist(extracted_urls, blocklist_file, output_file)
    
    print(f"작업 완료! 신규 URL이 {output_file}에 저장되었습니다.")

if __name__ == "__main__":
    main()

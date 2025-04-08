import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from urllib.parse import quote
import pandas as pd
import re
import os
import idna

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

def extract_urls_from_text(text):
    """텍스트에서 URL 패턴 추출"""
    # URL 정규식 패턴
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*(?:\?[\w=&]*)?'
    
    # 정규식으로 URL 추출
    urls = re.findall(url_pattern, text)
    return list(set(urls))  # 중복 제거


def clean_file_path(path):
    """파일 경로에서 불필요한 따옴표 제거"""
    # 앞뒤 따옴표 제거
    path = path.strip('"\'')
    
    # 확장자 확인
    if not path.lower().endswith('.xlsx'):
        path += '.xlsx'
    
    return path
## 한글로 인코딩 할 수 있게 해줌. 
def encode_korean_domain(url):
    parts = url.split('://', 1)
    if len(parts) > 1:
        protocol, rest = parts
        domain, *path = rest.split('/', 1)
        encoded_domain = idna.encode(domain).decode('ascii')
        return f"{protocol}://{encoded_domain}/{'/'.join(path) if path else ''}"
    return url

def encode_korean_path(url):
    parts = url.split('://', 1)
    if len(parts) > 1:
        protocol, rest = parts
        domain, *path = rest.split('/', 1)
        encoded_path = quote('/'.join(path) if path else '', safe='/')
        return f"{protocol}://{domain}/{encoded_path}"
    return url

def encode_korean_url(url):
    return encode_korean_path(encode_korean_domain(url))

def extract_urls_from_text(text):
    url_pattern = r'(?:https?:\/\/)?(?:www\.)?[-a-zA-Z0-9@:%._\+~#=가-힣]{1,256}\.[a-zA-Z0-9()가-힣]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=가-힣]*)'
    urls = re.findall(url_pattern, text)
    return [encode_korean_url(url) for url in urls]

def extract_from_clipboard():
    try:
        import pyperclip
        text = pyperclip.paste()
        urls = extract_urls_from_text(text)
        if urls:
            print("추출된 URL:")
            for url in urls:
                print(url)
        else:
            print("URL을 찾을 수 없습니다.")
        return urls
    except ImportError:
        print("pyperclip 모듈이 설치되어 있지 않습니다. 'pip install pyperclip'으로 설치하세요.")
        return []

def compare_with_blocklist(extracted_urls, blocklist_file, output_file, url_column='URL'):
    """추출된 URL을 금지 리스트와 비교하고 신규 URL만 추가"""
    try:
        # 금지 리스트 불러오기
        try:
            blocklist_df = pd.read_excel(blocklist_file, header=3, usecols=[3])  # D열(인덱스 3)의 4번째 줄부터 읽기
            blocklist_df.columns = [url_column]  # 컬럼 이름 지정
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
            # 기존 파일의 컬럼명 확인
            if url_column not in existing_df.columns:
                print(f"경고: 기존 파일에 '{url_column}' 컬럼이 없습니다. 첫 번째 컬럼을 사용합니다.")
                url_column = existing_df.columns[0]  # 첫 번째 컬럼 사용
                new_urls_df = pd.DataFrame({url_column: new_urls})
            
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
    print("URL 추출 및 비교 도구")
    print("1. 웹페이지에서 URL 추출")
    print("2. 클립보드에서 URL 추출 (텍스트 드래그 후 Ctrl+C)")
    choice = input("선택하세요 (1 또는 2): ")
    
    extracted_urls = []
    
    if choice == '1':
        target_url = input("URL을 추출할 웹페이지 주소를 입력하세요: ")
        print("웹페이지에서 URL 추출 중...")
        extracted_urls = extract_urls_from_webpage(target_url)
    elif choice == '2':
        print("클립보드에서 URL 추출 중...")
        extracted_urls = extract_from_clipboard()
    else:
        print("잘못된 선택입니다.")
        return
    
    if not extracted_urls:
        print("URL이 추출되지 않았습니다.")
        return
    
    blocklist_file = input("금지 리스트가 있는 엑셀 파일 경로를 입력하세요: ")
    blocklist_file = clean_file_path(blocklist_file)
    if not os.path.exists(blocklist_file):
        print(f"경고: 파일 '{blocklist_file}'이 존재하지 않습니다.")
        # 계속 진행할지 물어볼 수 있음
        if input("계속 진행하시겠습니까? (y/n): ").lower() != 'y':
            return
    
    output_file = input("결과를 저장할 엑셀 파일 경로를 입력하세요: ")
    output_file = clean_file_path(output_file)
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        print(f"경고: 디렉토리 '{output_dir}'가 존재하지 않습니다.")
        try:
            os.makedirs(output_dir, exist_ok=True)
            print(f"디렉토리 '{output_dir}'를 생성했습니다.")
        except Exception as e:
            print(f"디렉토리 생성 실패: {e}")
            return
    
    url_column = input("URL이 저장된 컬럼명을 입력하세요 (기본값: URL): ") or "URL"
    
    # 금지 리스트와 비교 및 저장
    print("금지 리스트와 비교 중...")
    new_urls = compare_with_blocklist(extracted_urls, blocklist_file, output_file, url_column)
    
    print(f"작업 완료! 신규 URL이 {output_file}에 저장되었습니다.")

if __name__ == "__main__":
    main()

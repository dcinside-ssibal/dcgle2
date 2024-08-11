# DCGLE2 README

## 프로젝트 개요

**DCGLE2**는 디시인사이드 갤러리의 글을 1분 주기로 크롤링하는 웹 애플리케이션입니다. 이 프로젝트는 Python의 Flask 프레임워크를 사용하여 개발되었습니다.

## 주요 기능

- 디시인사이드 특정 갤러리의 글을 1분 간격으로 자동 크롤링
- 크롤링한 데이터를 데이터베이스에 저장
- 저장된 데이터를 웹 인터페이스를 통해 조회 가능

## 설치 및 실행 방법

### 요구 사항

- Python 3.8 이상
- Flask
- Requests
- BeautifulSoup4
- SQLAlchemy
- APScheduler

### 설치

1. 저장소를 클론합니다.

   ```bash
   git clone https://github.com/yourusername/dcgle2.git
   cd dcgle2
   ```

2. 가상 환경을 설정하고 활성화합니다.

   ```bash
   python -m venv venv
   source venv/bin/activate  # 윈도우의 경우 `venv\Scripts\activate`
   ```

3. 필요한 패키지를 설치합니다.

   ```bash
   pip install -r requirements.txt
   ```

### 실행

1. 애플리케이션을 실행합니다.

   ```bash
   flask run
   ```

2. 웹 브라우저에서 `http://127.0.0.1:5000`에 접속합니다.

## 개선할 점

현재 DCGLE2는 특정 갤러리의 첫 번째 페이지 크롤링만 지원하며, 2페이지 이상 탐색이 불가능합니다. 이를 개선하기 위해 다음과 같은 방법을 고려할 수 있습니다:

1. **페이지 네비게이션 기능 추가**:
   - 다음 페이지 링크를 파싱하여 순차적으로 크롤링
   - 각 페이지에서 필요한 데이터를 추출 후 저장

2. **비동기 처리**:
   - 비동기 요청을 통해 여러 페이지를 동시에 크롤링하여 효율성 향상

## 문의

프로젝트와 관련된 문의는 온라인 프로필을 참고해주세요.

## 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.

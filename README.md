# 🌱 AI 습관 트래커

OpenAI GPT를 활용한 AI 코칭 기능이 포함된 Streamlit 습관 트래커 앱입니다.

## 기능
- 습관 추가 / 삭제
- 매일 체크 (클릭 토글)
- 연속 달성 스트릭 표시
- 최근 7일 달성률 차트
- 최근 21일 달성 히스토리
- 🤖 OpenAI GPT 기반 AI 코칭 메시지

## 실행 방법

### 1. 가상환경 생성 및 활성화
```bash
# MacOS
virtualenv MYAI
source MYAI/bin/activate

# Windows
python -m venv MYAI
MYAI\Scripts\activate
```

### 2. git 초기화
```bash
git init
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. API 키 설정
`.env` 파일을 열어 OpenAI API 키를 입력하세요:
```
OPENAI_API_KEY=sk-...your-key-here...
```

### 5. 앱 실행
```bash
streamlit run app.py
```

## 파일 구조
```
habit-tracker/
├── .env              # API 키 (git에 올리지 마세요!)
├── .cursorrules      # Cursor AI 코딩 원칙
├── requirements.txt  # 필요한 패키지
├── app.py            # 메인 앱
└── habits.json       # 습관 데이터 (자동 생성)
```

## 주의사항
- `.env` 파일은 절대 git에 커밋하지 마세요.
- `.gitignore`에 `.env`와 `habits.json`을 추가하는 것을 권장합니다.

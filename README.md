# ◎ 마음 연구소 (Mind Laboratory)

임상심리학 검증 척도 기반의 AI 심리 탐구 플랫폼입니다. OpenAI GPT와 Streamlit으로 구축된 개인 심리 프로파일링 및 AI 상담 앱입니다.

## 주요 기능

### ◎ 내 심리 프로필
- 이름·연령대 등 기본 프로필 설정
- 심리검사 완료 현황 추적
- 애착 유형 및 핵심 가치관 요약 카드

### 🔬 성격 심층 진단 (임상 검증 척도)
- **BFI-44** (Big Five Inventory) — 개방성·성실성·외향성·친화성·신경증 20문항 측정, 레이더 차트 시각화
- **ECR-R** (Experience in Close Relationships) — 애착 불안·회피 점수 기반 4가지 애착 유형 분류 (안정·불안·회피·혼돈)
- **Schwartz 기본 가치 이론** — 10가지 가치 영역 중 핵심 가치 선택
- GPT 기반 통합 성격 요약 리포트 자동 생성

### 🧩 심리 탐색 테스트
- **기질 나침반** (Keirsey Temperament Sorter, 12문항) — SJ·SP·NF·NT 4가지 기질 유형 진단
- **에니어그램** (9문항) — 9가지 성격 유형 중 최적합 유형 탐색
- **스트레스 반응 패턴** (10문항) — 문제해결형·전환회복형·회피마비형·감정반응형 분류 및 맞춤 치료 제안

### 💬 AI 심리 상담
- AI 상담사 **'소이'** — Rogers 인간중심치료, Beck CBT, Bowlby 애착이론, Schwartz 가치이론 기반
- 개인 프로필(Big Five·애착 유형·가치관)을 컨텍스트로 반영한 개인화 상담
- 빠른 질문 주제 6종 제공
- 상담 기록 저장 및 초기화

### 📓 감정 일지
- 날짜·무드 점수(1–10)·일기 작성
- GPT 기반 AI 피드백 자동 생성
- 과거 일지 열람

## 기술 스택

| 항목 | 내용 |
|------|------|
| 프레임워크 | Streamlit |
| AI | OpenAI GPT-4o-mini |
| 시각화 | Plotly (레이더 차트) |
| 데이터 관리 | JSON 파일 로컬 저장 |
| 환경 변수 | python-dotenv |

## 실행 방법

### 1. 가상환경 생성 및 활성화
```bash
# macOS / Linux
python -m venv MYAI
source MYAI/bin/activate

# Windows
python -m venv MYAI
MYAI\Scripts\activate
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. API 키 설정
`.env` 파일을 생성하고 OpenAI API 키를 입력하세요:
```
OPENAI_API_KEY=sk-...your-key-here...
```

### 4. 앱 실행
```bash
streamlit run app.py
```

## 파일 구조
```
mindlab/
├── .env                # API 키 (git에 올리지 마세요!)
├── app.py              # 메인 앱
├── requirements.txt    # 필요한 패키지
└── mindlab_data.json   # 사용자 데이터 (자동 생성)
```

## 주의사항
- `.env` 파일은 절대 git에 커밋하지 마세요.
- `.gitignore`에 `.env`와 `mindlab_data.json`을 추가하는 것을 권장합니다.
- 이 앱은 심리 교육 및 자기 이해 목적으로 제작되었으며, 임상 진단을 대체하지 않습니다.

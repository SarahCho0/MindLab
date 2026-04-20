<div align="center">

<br/>

<img src="https://img.shields.io/badge/◎-마음_연구소-5B4FCF?style=for-the-badge&labelColor=1C1917&color=5B4FCF" height="36"/>

<br/><br/>

# 마음 연구소
### Mind Laboratory

**임상심리학 × AI 대화**로 나를 깊이 이해하는 심리 탐구 플랫폼

<br/>

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45.0-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com)
[![Plotly](https://img.shields.io/badge/Plotly-6.0.1-3F4F75?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com)

<br/>

---

</div>

<br/>

## ✦ 소개

> *"자기 자신을 아는 것이 모든 지혜의 시작이다."* — Aristotle

**마음 연구소**는 전문 심리 상담의 접근 장벽(비용·시간·사회적 낙인)을 낮추고,  
누구나 부담 없이 자신의 내면을 탐구할 수 있도록 설계된 AI 심리 플랫폼입니다.

BFI-44, ECR-R, Schwartz 가치 이론, Keirsey 기질 이론, 에니어그램 등  
**임상심리학에서 검증된 척도 5종**과 **OpenAI GPT-4o-mini**를 결합하여  
성격·애착·가치관·스트레스 패턴을 다각도로 분석하고, AI 상담사 **소이**와 대화합니다.

<br/>

---

## ◎ 주요 기능

<br/>

### `탭 1` &nbsp; ◎ &nbsp; 내 심리 프로필

| | |
|---|---|
| **오늘의 심리 명언** | 날짜별 자동 교체되는 Rogers, Frankl, Beck 등 30인의 명언 |
| **Big Five 레이더 차트** | 개방성·성실성·외향성·친화성·신경증 5요인 시각화 |
| **애착 유형 요약** | 안정·불안·회피·두려움 유형별 핵심 패턴 카드 |
| **핵심 가치관** | Schwartz 10가치 중 나의 우선 가치 시각화 |
| **AI 심층 성격 분석** | 전체 데이터 기반 GPT 통합 리포트 생성 |
| **🎯 오늘의 성장 미션** | 내 프로필 맞춤형 AI 일일 미션 자동 생성 |

<br/>

### `탭 2` &nbsp; 💬 &nbsp; AI 심리 상담 — 소이

```
Rogers 인간중심치료  ·  Beck CBT  ·  Bowlby 애착이론  ·  Schwartz 가치이론
```

- 내 성격·애착·가치관 데이터를 컨텍스트로 반영한 **개인화 상담**
- "요즘 무기력해요", "관계가 힘들어요" 등 **빠른 주제 6종** 제공
- 모든 대화 기록 **로컬 영구 저장**

<br/>

### `탭 3` &nbsp; 🔬 &nbsp; 성격 심층 진단

| 척도 | 측정 내용 | 문항 |
|------|-----------|------|
| **BFI-44** · Big Five Inventory | 성격 5요인 + 레이더 차트 시각화 | 20문항 |
| **ECR-R** · Experiences in Close Relationships | 애착 불안·회피 → 4유형 분류 | 8문항 |
| **Schwartz** · Value Survey | 자기주도·성취·쾌락 등 10가지 핵심 가치관 | 선택형 |

<br/>

### `탭 4` &nbsp; 🧩 &nbsp; 심리 탐색 테스트

| 검사 | 분류 | 특징 |
|------|------|------|
| **기질 나침반** | SJ · SP · NF · NT | 유형별 상세 설명·궁합·다른 유형 보기 |
| **에니어그램** | 1번 ~ 9번 유형 | 핵심 동기·두려움·성장 방향 분석 |
| **스트레스 패턴** | PS · RC · AV · ER | 반응 유형별 성장 팁·권장 치료 접근 |

> 모든 검사 결과는 **로컬에 영구 저장**되어 재방문 시 이어서 확인 가능합니다.

<br/>

### `탭 5` &nbsp; 📓 &nbsp; 감정 일지

- 📊 **감정 온도계** — 1~10 무드 슬라이더 + 감정 태그 복수 선택
- ✍️ **자유 일기** 작성 → **AI 감정 분석** (CBT·인간중심치료 관점)
- 📈 **14일 감정 흐름** 라인 차트
- 🔥 **연속 기록 streak** + 평균 감정 강도 통계
- 🏷️ **자주 느끼는 감정 Top 8** 빈도 바 차트

<br/>

---

## ⚙️ 기술 스택

<div align="center">

| Layer | Stack |
|-------|-------|
| **Frontend** | Streamlit 1.45.0 · Custom CSS (Design Token System) |
| **AI** | OpenAI GPT-4o-mini |
| **Visualization** | Plotly 6.0.1 |
| **Data** | JSON Local Storage · python-dotenv |
| **Language** | Python 3.x · Conda |
| **Version Control** | Git · GitHub |

</div>

<br/>

---

## 🚀 시작하기

### 1. 저장소 클론

```bash
git clone https://github.com/SarahCho0/MindLab.git
cd MindLab
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. API 키 설정

```bash
# .env 파일 생성
echo "OPENAI_API_KEY=sk-...your-key..." > .env
```

### 4. 앱 실행

```bash
streamlit run app.py
```

<br/>

---

## 📁 파일 구조

```
MindLab/
│
├── app.py                 # 메인 앱 (Streamlit)
├── requirements.txt       # 패키지 목록
├── PROJECT.md             # 프로젝트 소개 · 개선 방향
│
├── .env                   # 🔒 API 키 (git 제외)
├── .gitignore
│
└── mindlab_data.json      # 사용자 데이터 (자동 생성, git 제외)
```

<br/>

---

## ⚕️ 윤리 및 한계

```
본 앱은 심리 교육 및 자기 탐구 도구이며, 임상 진단을 대체하지 않습니다.
```

- 모든 데이터는 **로컬에만 저장**되며 외부 서버로 전송되지 않습니다
- AI 응답은 참고용이며 전문 임상의의 판단을 대체할 수 없습니다
- 정신건강 위기 시 전문가 도움을 안내합니다

| 기관 | 연락처 |
|------|--------|
| 정신건강 위기상담 | ☎ 1577-0199 |
| 자살예방상담전화 | ☎ 1393 |
| 청소년 상담 | ☎ 1388 |

<br/>

---

<div align="center">

Made with 🤍 &nbsp;·&nbsp; Powered by [Streamlit](https://streamlit.io) & [OpenAI](https://openai.com)

</div>

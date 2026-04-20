# ============================================================
#  마음 연구소 — AI 심리 탐구 플랫폼
#  Clinical-grade psychological assessment & AI counseling
# ============================================================
import streamlit as st
import json
import os
from datetime import date, timedelta
import plotly.graph_objects as go
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="마음 연구소",
    page_icon="◎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design System ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

/* ── TOKENS ── */
:root {
  --bg:          #F7F5F0;
  --bg2:         #EFECE6;
  --surface:     #FFFFFF;
  --surface2:    #FDFCFA;
  --border:      #E4DFD7;
  --border2:     #D4CFC7;
  --t1:          #1C1917;
  --t2:          #44403C;
  --t3:          #78716C;
  --t4:          #A8A29E;

  --indigo:      #5B4FCF;
  --indigo-lt:   #EEE9FF;
  --indigo-mid:  #7C6FE8;
  --indigo-dark: #3730A3;

  --sage:        #3D7A5F;
  --sage-lt:     #ECFDF5;
  --sage-mid:    #6BAF8A;

  --amber:       #B45309;
  --amber-lt:    #FFFBEB;

  --rose:        #BE123C;
  --rose-lt:     #FFF1F2;

  --sky:         #0369A1;
  --sky-lt:      #F0F9FF;

  --r:           16px;
  --r-sm:        10px;
  --sh:          0 1px 3px rgba(28,25,23,.05), 0 4px 16px rgba(28,25,23,.04);
  --sh-sm:       0 1px 2px rgba(28,25,23,.05);
  --sh-lg:       0 4px 24px rgba(28,25,23,.07), 0 16px 48px rgba(28,25,23,.05);
}

/* ── BASE ── */
html, body, [class*="css"] {
  font-family: 'Noto Sans KR', -apple-system, sans-serif;
  -webkit-font-smoothing: antialiased;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.stApp { background: var(--bg); }
.main .block-container {
  padding: 2.2rem 2.8rem 5rem;
  max-width: 1240px;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: #0F0D0B;
  border-right: 1px solid rgba(255,255,255,0.04);
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0; }
[data-testid="stSidebar"] * { color: #8A847E !important; }
[data-testid="stSidebar"] hr {
  border: none !important;
  border-top: 1px solid rgba(255,255,255,0.05) !important;
  margin: .8rem 0 !important;
}
[data-testid="stSidebar"] .stButton > button {
  background: rgba(91,79,207,.12) !important;
  border: 1px solid rgba(91,79,207,.25) !important;
  color: #B0A9E0 !important;
  border-radius: 10px !important;
  font-size: .83rem !important;
  font-weight: 500 !important;
  transition: all .2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(91,79,207,.22) !important;
  color: #DDD8FF !important;
  transform: translateX(2px) !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important;
  border-radius: 14px !important;
  padding: 4px !important;
  gap: 2px !important;
  border: 1px solid var(--border) !important;
  box-shadow: var(--sh-sm) !important;
  margin-bottom: 2rem !important;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 10px !important;
  padding: .48rem 1.2rem !important;
  font-size: .84rem !important;
  font-weight: 500 !important;
  color: var(--t3) !important;
  background: transparent !important;
  border: none !important;
}
.stTabs [aria-selected="true"] {
  background: var(--t1) !important;
  color: white !important;
  font-weight: 700 !important;
  box-shadow: 0 1px 6px rgba(28,25,23,.18) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── INNER TABS (nested) ── */
div[data-testid="stHorizontalBlock"] .stTabs [data-baseweb="tab-list"] {
  margin-bottom: 1.2rem !important;
  background: var(--bg2) !important;
  border-color: var(--border2) !important;
}

/* ── CARDS ── */
.card {
  background: var(--surface);
  border-radius: var(--r);
  padding: 1.5rem 1.6rem;
  border: 1px solid var(--border);
  box-shadow: var(--sh);
  margin-bottom: .8rem;
}
.card-sm { padding: 1.1rem 1.3rem; border-radius: var(--r-sm); }
.card-inset {
  background: var(--bg);
  border-radius: var(--r-sm);
  padding: 1rem 1.2rem;
  border: 1px solid var(--border);
}
.card-indigo {
  background: linear-gradient(135deg, #F0ECFF 0%, #E8E1FF 100%);
  border-color: #C9C0F0;
}
.card-sage {
  background: linear-gradient(135deg, #EDFDF5 0%, #D9FAE9 100%);
  border-color: #A5D6B4;
}
.card-amber {
  background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
  border-color: #F0D080;
}
.left-bar-indigo { border-left: 3px solid var(--indigo); }
.left-bar-sage   { border-left: 3px solid var(--sage); }
.left-bar-amber  { border-left: 3px solid var(--amber); }

/* ── TYPOGRAPHY ── */
.page-eyebrow {
  font-size: .68rem; font-weight: 700; color: var(--indigo);
  text-transform: uppercase; letter-spacing: .12em; margin-bottom: 6px;
}
.page-title {
  font-family: 'Lora', Georgia, serif;
  font-size: 1.7rem; font-weight: 600; color: var(--t1);
  letter-spacing: -.02em; line-height: 1.2; margin-bottom: 6px;
}
.page-desc { font-size: .86rem; color: var(--t3); line-height: 1.7; }
.sec-title { font-size: .95rem; font-weight: 700; color: var(--t1); letter-spacing: -.01em; }
.sec-sub   { font-size: .78rem; color: var(--t3); margin-top: 2px; line-height: 1.55; }
.label-sm  { font-size: .68rem; font-weight: 700; color: var(--t4); text-transform: uppercase; letter-spacing: .09em; }

/* ── SCALE ITEM ── */
.q-item {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1rem 1.15rem .3rem;
  margin-bottom: .7rem;
  transition: border-color .2s;
}
.q-item:hover { border-color: var(--indigo-mid); }
.q-label { font-size: .73rem; font-weight: 700; color: var(--indigo); letter-spacing: .05em; margin-bottom: 3px; }
.q-text  { font-size: .9rem; color: var(--t1); font-weight: 500; line-height: 1.45; margin-bottom: 6px; }

/* ── TRAIT BAR ── */
.trait-wrap { margin-bottom: 13px; }
.trait-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }
.trait-name   { font-size: .86rem; font-weight: 600; color: var(--t2); }
.trait-track  { background: var(--bg2); border-radius: 999px; height: 7px; overflow: hidden; }
.trait-fill   { height: 100%; border-radius: 999px; }
.trait-note   { font-size: .72rem; color: var(--t3); margin-top: 3px; line-height: 1.5; }

/* ── CHAT ── */
.chat-outer {
  background: var(--surface);
  border-radius: var(--r);
  border: 1px solid var(--border);
  box-shadow: var(--sh);
  overflow: hidden;
}
.chat-header {
  padding: .9rem 1.3rem;
  border-bottom: 1px solid var(--border);
  background: var(--surface2);
  display: flex; align-items: center; gap: 10px;
}
.chat-av-wrap {
  width: 34px; height: 34px; border-radius: 50%;
  background: var(--t1);
  display: flex; align-items: center; justify-content: center;
  font-size: .75rem; font-weight: 800; color: white;
  flex-shrink: 0;
}
.chat-body { padding: .8rem 1.1rem; min-height: 200px; max-height: 320px; overflow-y: auto; }
.chat-msgs { display: flex; flex-direction: column; gap: 16px; }
.msg-row { display: flex; gap: 10px; max-width: 86%; }
.msg-row.me { align-self: flex-end; flex-direction: row-reverse; }
.msg-av {
  width: 30px; height: 30px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center; font-size: .8rem;
}
.msg-av.ai-av { background: var(--t1); color: white; font-size: .6rem; font-weight: 800; }
.msg-av.me-av { background: var(--indigo-lt); color: var(--indigo); font-size: .8rem; }
.msg-bubble { padding: .75rem 1rem; border-radius: 16px; font-size: .87rem; line-height: 1.75; }
.msg-bubble.ai { background: white; border: 1px solid var(--border); border-top-left-radius: 4px; box-shadow: var(--sh-sm); }
.msg-bubble.me { background: var(--t1); color: white; border-top-right-radius: 4px; }
.msg-time { font-size: .65rem; color: var(--t4); margin-top: 3px; padding: 0 2px; }

/* ── CHIP ── */
.chip {
  display: inline-flex; align-items: center; gap: 3px;
  border-radius: 999px; padding: 3px 10px;
  font-size: .71rem; font-weight: 600; margin: 2px;
}
.chip-indigo { background: var(--indigo-lt); color: var(--indigo-dark); }
.chip-sage   { background: var(--sage-lt); color: var(--sage); }
.chip-amber  { background: var(--amber-lt); color: var(--amber); }
.chip-rose   { background: var(--rose-lt); color: var(--rose); }

/* ── ATTACHMENT CARD ── */
.att-card {
  background: var(--surface);
  border-radius: 13px;
  padding: 1.1rem 1.2rem;
  border: 1px solid var(--border);
  margin-bottom: 8px;
  cursor: default;
  transition: all .2s;
}
.att-card:hover { box-shadow: var(--sh); transform: translateY(-1px); border-color: var(--border2); }

/* ── JOURNAL ── */
.j-entry {
  background: var(--surface);
  border-radius: 13px;
  padding: 1.1rem 1.3rem;
  border: 1px solid var(--border);
  margin-bottom: 7px;
  box-shadow: var(--sh-sm);
}
.j-date { font-size: .67rem; font-weight: 700; color: var(--t4); text-transform: uppercase; letter-spacing: .07em; }
.j-mood { font-size: .78rem; font-weight: 600; margin-left: 6px; }
.j-text { font-size: .86rem; color: var(--t2); line-height: 1.68; margin-top: 5px; }
.j-ai   { margin-top: 9px; padding: 8px 11px; background: var(--indigo-lt); border-left: 3px solid var(--indigo); border-radius: 8px; font-size: .8rem; color: var(--indigo-dark); line-height: 1.7; }

/* ── EMPTY ── */
.empty { background: var(--surface); border-radius: var(--r); padding: 3rem 1.5rem; text-align: center; border: 1.5px dashed var(--border); }
.empty-icon  { font-size: 2.2rem; margin-bottom: 10px; }
.empty-title { font-size: .92rem; font-weight: 700; color: var(--t2); }
.empty-body  { font-size: .8rem; color: var(--t3); margin-top: 4px; line-height: 1.6; }

/* ── KPI ── */
.kpi-card {
  background: var(--surface);
  border-radius: var(--r);
  padding: 1.2rem 1.4rem 1rem;
  border: 1px solid var(--border);
  box-shadow: var(--sh);
  overflow: hidden; position: relative;
}
.kpi-top { height: 3px; position: absolute; top: 0; left: 0; right: 0; border-radius: var(--r) var(--r) 0 0; }
.kpi-val { font-size: 1.9rem; font-weight: 800; color: var(--t1); letter-spacing: -.05em; line-height: 1; margin-top: 4px; }
.kpi-lbl { font-size: .67rem; font-weight: 700; color: var(--t4); text-transform: uppercase; letter-spacing: .1em; margin-top: 6px; }
.kpi-sub { font-size: .74rem; color: var(--t3); margin-top: 2px; }

/* ── PROGRESS (sidebar) ── */
.sb-bar-bg   { background: rgba(255,255,255,.06); border-radius: 999px; height: 4px; }
.sb-bar-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg,#5B4FCF,#9B8EF0); }
.sb-stat { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,.04); }
.sb-stat:last-child { border-bottom: none; }

/* ── INPUTS & BUTTONS ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
  border-radius: 11px !important;
  border: 1px solid var(--border) !important;
  background: white !important;
  color: var(--t1) !important;
  font-size: .88rem !important;
  transition: all .2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--indigo) !important;
  box-shadow: 0 0 0 3px rgba(91,79,207,.1) !important;
  outline: none !important;
}
.stButton > button {
  border-radius: 10px !important;
  font-weight: 600 !important;
  font-size: .85rem !important;
  border: 1px solid var(--border) !important;
  background: white !important;
  color: var(--t2) !important;
  transition: all .2s !important;
}
.stButton > button:hover {
  border-color: var(--border2) !important;
  box-shadow: var(--sh) !important;
}
.stButton > button[kind="primary"] {
  background: var(--t1) !important;
  color: white !important;
  border-color: var(--t1) !important;
  box-shadow: 0 2px 8px rgba(28,25,23,.2) !important;
}
.stButton > button[kind="primary"]:hover {
  background: #2C2924 !important;
  box-shadow: 0 4px 14px rgba(28,25,23,.28) !important;
  transform: translateY(-1px) !important;
}
[data-testid="stForm"] .stButton > button {
  background: var(--t1) !important;
  color: white !important;
  border-color: var(--t1) !important;
}
[data-testid="stSlider"] { margin: .2rem 0 .4rem; }
[data-baseweb="tag"] { background: var(--indigo-lt) !important; border-radius: 7px !important; }
[data-baseweb="tag"] span { color: var(--indigo-dark) !important; font-weight: 600 !important; }
hr { border-color: var(--border) !important; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ─── DAILY PSYCHOLOGY QUOTES ─────────────────────────────────
# ══════════════════════════════════════════════════════════════
PSYCH_QUOTES = [
    ("모든 감정은 정보다. 억압이 아니라 이해가 필요하다.", "Aaron Beck"),
    ("자기 자신에게 친절한 것은 이기적인 것이 아니다. 그것이 모든 관계의 기초다.", "Carl Rogers"),
    ("우리는 과거를 바꿀 수 없지만, 그것에 대한 반응을 바꿀 수 있다.", "Viktor Frankl"),
    ("진정한 용기는 두려움이 없는 것이 아니라, 두려움 속에서도 행동하는 것이다.", "Brené Brown"),
    ("감사함은 행복의 결과가 아니라, 행복의 원인이다.", "Robert Emmons"),
    ("자기 인식은 변화의 첫 번째 단계다.", "Tasha Eurich"),
    ("나는 내가 통제할 수 없는 것에 에너지를 낭비하지 않겠다.", "Epictetus"),
    ("비교는 기쁨을 앗아가는 도둑이다.", "Theodore Roosevelt"),
    ("마음챙김이란 판단 없이 현재 순간에 주의를 기울이는 것이다.", "Jon Kabat-Zinn"),
    ("우리가 겪는 고통의 대부분은 피할 수 없지만, 그 고통에 대한 우리의 반응은 선택할 수 있다.", "Haruki Murakami"),
    ("취약성은 약함이 아니라 용기의 탄생지다.", "Brené Brown"),
    ("당신의 가장 큰 두려움은 당신이 가장 크게 성장할 수 있는 방향이다.", "Albert Ellis"),
    ("감정을 느끼되, 감정에 의해 지배당하지 마라.", "Viktor Frankl"),
    ("자기 수용은 변화의 역설적 조건이다.", "Carl Rogers"),
    ("지금 이 순간이 유일하게 살 수 있는 순간이다.", "Thich Nhat Hanh"),
    ("우리는 자신에 대해 말하는 이야기 속에서 살아간다.", "Dan McAdams"),
    ("심리적 건강이란 불완전함을 받아들이는 능력이다.", "Donald Winnicott"),
    ("연결감은 인간이 가진 가장 근본적인 욕구다.", "John Bowlby"),
    ("행동이 감정을 따라가길 기다리지 마라. 행동하면 감정이 따라온다.", "William James"),
    ("자신을 이해하는 것이 모든 지혜의 시작이다.", "Aristotle"),
    ("우리의 자동적 사고가 현실을 왜곡할 때, 감정도 함께 왜곡된다.", "Aaron Beck"),
    ("완벽주의는 성취의 엔진이 아니라 불안의 갑옷이다.", "Brené Brown"),
    ("타인을 용서하는 것은 그들을 위해서가 아니라 자신을 위해서다.", "Fred Luskin"),
    ("강점을 사용하는 삶이 가장 충만한 삶이다.", "Martin Seligman"),
    ("작은 전진이 매일 쌓이면 결국 큰 변화가 된다.", "BJ Fogg"),
    ("경험 자체보다 경험을 어떻게 해석하느냐가 더 중요하다.", "Albert Ellis"),
    ("돌봄은 받는 것도 중요하지만 스스로에게 주는 것도 중요하다.", "Kristin Neff"),
    ("우리는 감정을 두려워할 필요가 없다. 감정은 지나간다.", "Susan David"),
    ("불안은 미래에 대한 현재의 반응이다. 지금에 집중하자.", "Daniel Levinson"),
    ("진정성 있는 삶은 자신의 내면의 소리를 따르는 것이다.", "Carl Jung"),
]

# ══════════════════════════════════════════════════════════════
# ─── CLINICAL DATA: Validated Psychological Scales ────────────
# ══════════════════════════════════════════════════════════════

# BFI-44 (Big Five Inventory) — 선별된 20문항 (trait당 4문항)
# 출처: John & Srivastava (1999). The Big Five trait taxonomy.
BFI_ITEMS = [
    # (trait, reverse_scored, text)
    ("E", False, "나는 수다스럽고 말이 많은 편이다"),
    ("A", True,  "나는 다른 사람들의 결점을 잘 찾아내는 편이다"),
    ("C", False, "나는 철저하게 일을 처리한다"),
    ("N", False, "나는 우울하거나 기분이 가라앉는 편이다"),
    ("O", False, "나는 독창적이며 새로운 아이디어를 내놓는다"),
    ("A", False, "나는 남의 의견을 존중하고 배려하는 편이다"),
    ("C", True,  "나는 종종 게으른 편이다"),
    ("N", True,  "나는 감정적으로 안정적이고 쉽게 동요하지 않는다"),
    ("O", False, "나는 예술, 음악, 문학에 관심이 많다"),
    ("N", True,  "나는 삶을 즐기는 편이다"),
    ("E", False, "나는 주장이 강하고 자기 의견을 확실히 말한다"),
    ("A", False, "나는 사람들을 친절하게 대하는 것이 자연스럽다"),
    ("C", False, "나는 믿음직스럽고 성실하게 생각되기를 원한다"),
    ("N", False, "나는 긴장과 스트레스를 자주 느끼는 편이다"),
    ("O", False, "나는 깊은 사고와 복잡한 아이디어를 즐기는 편이다"),
    ("E", True,  "나는 수줍음이 많고 내성적인 편이다"),
    ("A", True,  "나는 사람들에게 쉽게 화를 내는 편이다"),
    ("C", False, "나는 계획을 세우고 실천해 나가는 편이다"),
    ("E", False, "나는 많은 사람들과 어울리고 모임에 나가는 것을 즐긴다"),
    ("O", False, "나는 상상력이 풍부하고 공상을 즐기는 편이다"),
]

BFI_META = {
    "O": {
        "name": "개방성 (Openness)",
        "ko":   "개방성",
        "icon": "🔭",
        "high": "새로운 경험, 아이디어, 예술에 깊은 관심을 가집니다. 상상력과 창의성이 풍부하며 지적 탐구를 즐깁니다.",
        "low":  "실용적이고 현실적인 접근을 선호합니다. 익숙하고 검증된 방식을 신뢰하며 안정성을 중시합니다.",
        "color": "#5B4FCF",
    },
    "C": {
        "name": "성실성 (Conscientiousness)",
        "ko":   "성실성",
        "icon": "📐",
        "high": "체계적이고 목표 지향적입니다. 자기조절 능력이 강하며 책임감과 신뢰성이 높습니다.",
        "low":  "유연하고 즉흥적인 면이 있습니다. 규칙보다 자유를 선호하며 현재 순간에 집중합니다.",
        "color": "#0369A1",
    },
    "E": {
        "name": "외향성 (Extraversion)",
        "ko":   "외향성",
        "icon": "🌟",
        "high": "사회적 상황에서 활력을 얻습니다. 적극적이고 열정적이며 다양한 인간관계를 즐깁니다.",
        "low":  "혼자만의 시간을 통해 에너지를 충전합니다. 깊이 있는 관계와 고요한 환경을 선호합니다.",
        "color": "#D97706",
    },
    "A": {
        "name": "친화성 (Agreeableness)",
        "ko":   "친화성",
        "icon": "🤝",
        "high": "높은 공감 능력과 협력적 성향을 가집니다. 타인을 배려하고 갈등을 최소화하려 합니다.",
        "low":  "직접적이고 독립적입니다. 타인의 시선보다 자신의 판단을 신뢰하며 경쟁적 상황에 강합니다.",
        "color": "#059669",
    },
    "N": {
        "name": "신경증 (Neuroticism)",
        "ko":   "정서 안정성",
        "icon": "🌊",
        "high": "감정적 반응이 예민합니다. 스트레스와 부정적 감정을 더 강하게 경험하는 경향이 있습니다.",
        "low":  "감정적으로 안정적이고 침착합니다. 스트레스 상황에서도 평정심을 유지하는 편입니다.",
        "color": "#7C3AED",
        "reverse_label": True,  # High N = low stability
    },
}

# ECR-R (Experience in Close Relationships — Revised) 기반 애착 검사
# 출처: Fraley et al. (2000). Self-report Measurement of Adult Attachment
ECR_ITEMS = [
    # (dimension, text)
    # AX = Attachment Anxiety, AV = Attachment Avoidance
    ("AX", "나는 연인/친한 사람이 나를 정말로 사랑할까 걱정될 때가 많다"),
    ("AV", "나는 가까운 사람에게 내 생각과 감정을 솔직히 드러내기가 어렵다"),
    ("AX", "나는 파트너가 나를 떠날까봐 두려울 때가 많다"),
    ("AV", "나는 다른 사람과 정서적으로 가까워지는 것이 불편하다"),
    ("AX", "나는 관계에서 완전히 받아들여지지 못할까봐 걱정된다"),
    ("AV", "나는 친밀한 관계에서 지나치게 의존하는 것이 불편하다"),
    ("AX", "나는 혼자가 될까봐 두려워 관계를 유지하려 한다"),
    ("AV", "나는 가까운 사람과 감정을 공유하는 것이 편하지 않다"),
]

ATTACHMENT_TYPES = {
    "secure": {
        "name":  "안정 애착형",
        "icon":  "⚓",
        "color": "#059669",
        "summary": "관계에서 친밀감과 독립성 사이의 균형을 자연스럽게 유지합니다. 상대를 신뢰하며 갈등이 생겨도 관계가 회복될 것이라는 믿음이 있습니다.",
        "strength": "높은 자기 신뢰, 건강한 경계 설정, 관계에서의 회복탄력성",
        "growth": "때로 지나치게 독립적이거나 타인의 연약함을 이해하는 데 연습이 필요할 수 있습니다.",
        "therapy": "인지행동치료(CBT) 기법을 활용해 이미 강한 정서 조절 능력을 더욱 발전시킬 수 있습니다.",
    },
    "anxious": {
        "name":  "불안 애착형",
        "icon":  "🌧",
        "color": "#0369A1",
        "summary": "관계에서 깊은 친밀감을 원하지만, 버려지거나 거부당할 것에 대한 두려움이 동반됩니다. 상대의 감정 변화에 민감하게 반응하는 경향이 있습니다.",
        "strength": "공감 능력, 관계에 대한 헌신, 깊은 감정적 연결 능력",
        "growth": "상대의 행동을 위협으로 해석하는 패턴을 인식하고, 자기 안정화 기술을 개발하는 것이 중요합니다.",
        "therapy": "애착 기반 치료(ABT)와 정서중심치료(EFT)가 특히 효과적입니다. 내면 아이 작업과 자기 위안 훈련이 도움이 됩니다.",
    },
    "avoidant": {
        "name":  "회피 애착형",
        "icon":  "🏔",
        "color": "#D97706",
        "summary": "독립성을 강하게 추구하며 감정적 친밀감이 증가할수록 심리적 거리를 두는 경향이 있습니다. 자기충족적이지만 깊은 관계에서 어려움을 경험할 수 있습니다.",
        "strength": "강한 자립심, 감정에 흔들리지 않는 침착함, 명확한 경계 유지 능력",
        "growth": "취약성을 안전하게 표현하는 연습과, 친밀함이 독립성의 위협이 아님을 내면화하는 과정이 필요합니다.",
        "therapy": "스키마 치료(Schema Therapy)와 내면화된 작동 모델(Internal Working Models) 탐색이 핵심입니다.",
    },
    "fearful": {
        "name":  "혼돈(두려움) 애착형",
        "icon":  "🌪",
        "color": "#7C3AED",
        "summary": "친밀함을 강하게 원하는 동시에 두려워하는 내적 갈등이 있습니다. 관계가 가까워질수록 밀고 당기는 패턴이 나타날 수 있습니다.",
        "strength": "깊은 공감 능력, 복잡한 감정에 대한 풍부한 이해, 강한 내적 성찰 능력 잠재력",
        "growth": "안전한 치료 환경에서 초기 애착 외상을 탐색하고, 자기 조절 및 감정 명명화 훈련이 필요합니다.",
        "therapy": "EMDR, 신체 기반 치료(Somatic Therapy), 내면가족체계(IFS) 접근법이 효과적일 수 있습니다.",
    },
}

# 슈워츠 기본 가치 이론 (Schwartz Basic Values Theory, 1992) 기반
SCHWARTZ_VALUES = {
    "자기 방향": ["자율성", "창의성", "탐구"],
    "자극":      ["흥분", "도전", "모험"],
    "쾌락주의":  ["즐거움", "삶의 향유"],
    "성취":      ["능력", "성공", "영향력"],
    "권력":      ["지위", "부", "인정"],
    "안전":      ["안정", "질서", "건강"],
    "동조":      ["규칙 준수", "예의", "친절"],
    "전통":      ["전통 존중", "영성", "겸손"],
    "박애":      ["봉사", "공감", "정직"],
    "보편성":    ["공정함", "환경 존중", "사회 정의"],
}

MOOD_MAP = {
    1: ("😞", "#EF4444"), 2: ("😔", "#F87171"), 3: ("😕", "#FB923C"),
    4: ("😐", "#FBBF24"), 5: ("🙂", "#A3A3A3"), 6: ("😊", "#84CC16"),
    7: ("😄", "#4ADE80"), 8: ("😁", "#22C55E"), 9: ("🌟", "#0EA5E9"),
    10: ("✨", "#8B5CF6"),
}

COUNSELING_QUICK = [
    "나의 가장 큰 강점은 무엇인가요?",
    "대인관계에서 반복되는 패턴이 있나요?",
    "나는 스트레스를 어떻게 처리하는 편인가요?",
    "내가 가장 두려워하는 것은 무엇인가요?",
    "자기 비판이 심한 편인지 알고 싶어요",
    "지금 가장 힘든 점을 말하고 싶어요",
]

# ══════════════════════════════════════════════════════════════
# ─── PSYCHOLOGY QUIZ TESTS ───────────────────────────────────
# ══════════════════════════════════════════════════════════════

# 1) 기질 나침반 — Keirsey Temperament Sorter (12Q)
TEMP_Q = [
    {"text": "주말 오후, 아무 계획이 없다면 나는 자연스럽게…",
     "opts": ["🗂️  밀린 일을 처리하거나 집을 정리한다", "🚀  충동적으로 어딘가 떠나거나 새로운 것을 해본다",
              "💬  가까운 사람과 깊은 대화를 나눈다", "📚  책을 읽거나 새로운 지식을 탐구한다"],
     "keys": ["SJ", "SP", "NF", "NT"]},
    {"text": "친구가 고민을 털어놓을 때 나는…",
     "opts": ["🔧  현실적인 해결책을 제시하려 한다", "🎢  함께 기분 전환 거리를 찾아본다",
              "🫂  충분히 공감하고 마음으로 들어준다", "🔬  문제의 원인을 분석해 준다"],
     "keys": ["SJ", "SP", "NF", "NT"]},
    {"text": "새로운 일을 시작할 때 나는…",
     "opts": ["📋  계획표를 세우고 단계적으로 진행한다", "⚡  일단 몸으로 부딪히며 배워 나간다",
              "🌟  이 일이 어떤 의미인지 먼저 생각한다", "🏗️  전체 구조와 원리를 파악한 후 시작한다"],
     "keys": ["SJ", "SP", "NF", "NT"]},
    {"text": "의사결정 시 내가 가장 중시하는 것은…",
     "opts": ["📜  전례, 규칙, 검증된 방법", "⚡  지금 상황에 최선인 즉각적 선택",
              "💞  관계된 사람들의 감정과 화합", "🎯  효율성과 장기적 전략"],
     "keys": ["SJ", "SP", "NF", "NT"]},
    {"text": "나에게 가장 두려운 것은…",
     "opts": ["🌀  혼란스럽고 예측 불가능한 상황", "⛓️  자유가 제약되고 속박당하는 것",
              "💔  진정한 연결과 소속감을 잃는 것", "❓  무능하거나 무지하다고 여겨지는 것"],
     "keys": ["SJ", "SP", "NF", "NT"]},
    {"text": "나는 어떤 환경에서 가장 잘 집중하나요?",
     "opts": ["🏠  정해진 루틴과 예측 가능한 구조", "🌊  자유롭고 변화가 있는 유동적 환경",
              "🤝  목적의식이 있고 사람들과 함께하는 환경", "🔇  조용하고 방해받지 않는 독립적 환경"],
     "keys": ["SJ", "SP", "NF", "NT"]},
    {"text": "갈등 상황에서 나의 첫 번째 반응은…",
     "opts": ["⚖️  규칙과 원칙에 따라 공정하게 해결한다", "🍃  일단 자리를 피해 마음을 식힌다",
              "🫶  감정을 먼저 해소하고 관계를 회복한다", "🧩  문제의 핵심을 찾아 논리적으로 풀어낸다"],
     "keys": ["SJ", "SP", "NF", "NT"]},
    {"text": "다른 사람들이 나에게 자주 기대하는 것은…",
     "opts": ["🛡️  믿음직스럽고 책임감 있는 모습", "🎉  활기차고 재미를 주는 에너지",
              "🌸  따뜻한 공감과 감정적 지지", "💡  날카로운 통찰과 분석력"],
     "keys": ["SJ", "SP", "NF", "NT"]},
    {"text": "내가 에너지를 얻는 순간은…",
     "opts": ["✅  맡은 일을 완수하고 성과를 확인했을 때", "🎆  새로운 자극과 모험을 경험했을 때",
              "🫂  누군가에게 진심으로 이해받았을 때", "🔑  복잡한 문제를 깔끔하게 해결했을 때"],
     "keys": ["SJ", "SP", "NF", "NT"]},
    {"text": "처음 보는 사람을 만났을 때 나는…",
     "opts": ["🤝  예의 바르고 사회 규범에 맞게 행동한다", "🎤  재미있는 화제로 자연스럽게 어울린다",
              "👁️  진심 어린 관심을 갖고 상대를 이해하려 한다", "🔭  관심사나 지식을 나눌 화제를 찾는다"],
     "keys": ["SJ", "SP", "NF", "NT"]},
    {"text": "내가 가장 가치를 두는 것은…",
     "opts": ["⚓  안정성, 신뢰, 전통", "🧭  자유, 경험, 다양성",
              "🌱  의미, 성장, 진정한 관계", "🔭  지식, 역량, 자율성"],
     "keys": ["SJ", "SP", "NF", "NT"]},
    {"text": "나에게 이상적인 삶의 역할은…",
     "opts": ["🏛️  조직을 안정적으로 가꾸고 지키는 사람", "🏄  모험을 즐기며 현장에서 행동하는 사람",
              "🌿  타인의 성장을 돕고 변화를 이끄는 사람", "🚀  시스템을 설계하고 혁신을 만드는 사람"],
     "keys": ["SJ", "SP", "NF", "NT"]},
]
TEMP_TYPES = {
    "SJ": {
        "name": "수호자형 (Guardian)", "icon": "🛡️", "color": "#0369A1", "population": "전체의 약 40~45%",
        "core": "책임, 안정, 전통을 삶의 기반으로 삼습니다.",
        "desc": "신뢰할 수 있고 조직을 안정적으로 유지하는 사람입니다. 규칙과 전통을 소중히 여기며 '지금 여기'의 책임을 다하는 것이 삶의 중심입니다.",
        "detail": (
            "수호자형은 사회의 든든한 토대입니다. 약속을 지키는 것을 최고의 미덕으로 여기며, "
            "맡은 역할을 끝까지 완수하는 데서 깊은 보람을 느낍니다. 과거의 검증된 방식을 신뢰하고 "
            "절차와 규범을 존중하기 때문에 조직과 공동체를 안정적으로 이끄는 데 탁월합니다.\n\n"
            "감정보다는 행동으로 돌봄을 표현하는 편이며, 가족·직장·공동체에 대한 헌신이 강합니다. "
            "변화보다는 점진적 개선을 선호하고, 실용적이고 현실적인 관점에서 문제를 접근합니다. "
            "스트레스 상황에서는 더 열심히 일하거나 기존 루틴에 집중하는 경향이 있습니다."
        ),
        "strength": "높은 신뢰성·책임감, 체계적 실행력, 전통과 구조 유지 능력",
        "growth": "변화와 새로운 가능성을 두려워하지 않는 유연성 기르기",
        "similar": "ISTJ / ESTJ / ISFJ / ESFJ",
        "compatible": {"best": ["SP", "NF"], "challenging": ["NT"]},
        "compatible_desc": {
            "best": "탐험가형(SP)의 현실 감각과 이상주의형(NF)의 온기는 수호자형의 구조와 잘 어우러집니다.",
            "challenging": "전략가형(NT)의 끊임없는 시스템 개혁 욕구는 수호자형의 안정 추구와 충돌하기 쉽습니다.",
        },
    },
    "SP": {
        "name": "탐험가형 (Artisan)", "icon": "🧭", "color": "#D97706", "population": "전체의 약 30~35%",
        "core": "현재 순간, 자유, 경험을 가장 중시합니다.",
        "desc": "지금 이 순간에 온전히 집중하는 사람입니다. 자유롭고 유연하며 직접 경험과 행동을 통해 배웁니다. 즉흥성과 적응력이 뛰어납니다.",
        "detail": (
            "탐험가형은 삶 자체가 모험입니다. 규칙이나 계획보다는 '지금 이 순간'의 흐름에 맞게 움직이는 것을 "
            "편안하게 느끼며, 손재주·예술·스포츠·위기 대응 등 즉각적인 결과가 보이는 분야에서 빛을 발합니다.\n\n"
            "이론보다 실전, 설명보다 시연을 선호합니다. 고정된 루틴이나 긴 회의는 에너지를 빠르게 소진시키며, "
            "자유가 제약될 때 답답함을 강하게 느낍니다. 즉흥적인 결정이 때로는 장기 계획과 충돌할 수 있어 "
            "자신만의 루틴을 조금씩 만들어 가는 연습이 성장의 핵심입니다."
        ),
        "strength": "높은 적응력·유연성, 현실 문제 해결력, 행동력과 용기",
        "growth": "장기적 목표 설정과 꾸준한 실천력 기르기",
        "similar": "ISTP / ESTP / ISFP / ESFP",
        "compatible": {"best": ["SJ", "NT"], "challenging": ["NF"]},
        "compatible_desc": {
            "best": "수호자형(SJ)의 안정적인 구조와 전략가형(NT)의 날카로운 통찰은 탐험가형의 행동력을 더욱 빛나게 합니다.",
            "challenging": "이상주의형(NF)의 깊은 의미 탐구는 현재 지향적인 탐험가형과 방향이 어긋날 수 있습니다.",
        },
    },
    "NF": {
        "name": "이상주의형 (Idealist)", "icon": "🌱", "color": "#059669", "population": "전체의 약 15~20%",
        "core": "의미, 정체성, 진정한 연결을 추구합니다.",
        "desc": "삶의 의미와 가능성을 탐구하는 사람입니다. 깊은 공감 능력과 타인에 대한 진정한 관심이 있으며 세상이 더 나아질 수 있다는 믿음으로 움직입니다.",
        "detail": (
            "이상주의형은 잠재력을 보는 눈이 탁월합니다. 사람들이 스스로 성장하도록 돕고, "
            "진정한 관계와 깊은 대화에서 가장 큰 에너지를 얻습니다. 언어·예술·교육·상담·사회 변화 등 "
            "'사람과 의미'가 중심인 분야에서 강점을 발휘합니다.\n\n"
            "겉과 속이 일치하는 진정성을 매우 중요하게 여기며, 위선이나 형식적인 관계에 쉽게 지칩니다. "
            "이상이 높은 만큼 현실과의 간극에서 소진되기 쉬우므로, 자기 돌봄(self-care)과 경계 설정이 "
            "특히 중요합니다. 타인의 감정을 너무 깊이 흡수하는 경향을 인식하는 것도 성장의 출발점입니다."
        ),
        "strength": "깊은 공감 능력, 의미 추구, 강한 직관, 촉매적 영향력",
        "growth": "이상과 현실의 균형, 자기 돌봄의 경계 설정",
        "similar": "INFJ / ENFJ / INFP / ENFP",
        "compatible": {"best": ["NT", "SJ"], "challenging": ["SP"]},
        "compatible_desc": {
            "best": "전략가형(NT)의 지적 깊이와 수호자형(SJ)의 믿음직한 안정감은 이상주의형이 꿈을 현실로 만드는 데 큰 힘이 됩니다.",
            "challenging": "탐험가형(SP)의 즉흥적·현실 중심적 태도는 의미를 중시하는 이상주의형과 가치관이 충돌하기 쉽습니다.",
        },
    },
    "NT": {
        "name": "전략가형 (Rational)", "icon": "⚡", "color": "#5B4FCF", "population": "전체의 약 5~10%",
        "core": "역량, 지식, 독립성을 핵심 가치로 삼습니다.",
        "desc": "세상을 논리와 원리로 이해하려는 사람입니다. 복잡한 시스템을 설계하고 혁신적인 해결책을 찾는 데 강점이 있습니다.",
        "detail": (
            "전략가형은 끊임없이 '왜?'를 묻습니다. 기존의 것을 당연하게 받아들이지 않고 "
            "더 나은 방법을 탐구하며, 지식과 역량을 축적하는 과정 자체에서 큰 만족을 느낍니다. "
            "과학·공학·철학·법·전략 등 복잡한 시스템을 다루는 분야에서 특히 두각을 나타냅니다.\n\n"
            "감정보다 논리를 우선시하는 경향이 있어 타인에게 차갑거나 오만하게 보일 수 있습니다. "
            "완벽주의가 강해 자신과 타인에게 높은 기준을 적용하며, 이것이 스트레스의 주요 원인이 되기도 합니다. "
            "감정적 연결과 취약성을 허용하는 연습이 관계의 깊이를 더해 줍니다."
        ),
        "strength": "전략적 사고, 시스템 설계 능력, 독립성, 날카로운 분석력",
        "growth": "감정적 연결과 관계의 가치 인식, 완벽주의 완화",
        "similar": "INTJ / ENTJ / INTP / ENTP",
        "compatible": {"best": ["NF", "SP"], "challenging": ["SJ"]},
        "compatible_desc": {
            "best": "이상주의형(NF)의 공감과 가치 지향은 전략가형이 놓치기 쉬운 인간적 측면을 채워 주고, 탐험가형(SP)의 실행력은 전략의 현실화를 돕습니다.",
            "challenging": "수호자형(SJ)의 '해왔던 방식' 고수는 변화와 혁신을 추구하는 전략가형과 자주 마찰을 빚습니다.",
        },
    },
}

# 2) 에니어그램 핵심 유형 (9Q)
ENNEA_ITEMS = [
    {"type": "1", "name": "개혁가형", "icon": "⚖️", "color": "#6B7280",
     "text": "올바름과 원칙을 중시하며, 잘못된 것을 보면 고치고 싶다. 스스로와 타인 모두에게 높은 기준을 적용한다.",
     "core_fear": "불완전하고 결함 있는 존재가 되는 것", "core_desire": "착하고 올바른 사람이 되는 것",
     "desc": "세상을 개선하고자 하는 강한 내적 동기. 이상적 기준에 도달하려 끊임없이 노력합니다.",
     "detail": "1번 개혁가형은 내면에 '비판하는 목소리'를 지닙니다. 이 목소리는 더 나은 세상을 만들려는 원동력이 되기도 하지만, 자기 자신과 타인에 대한 끊임없는 판단으로 이어지기도 합니다. 높은 기준과 철저함이 강점이지만, 자신의 분노를 인식하고 불완전함을 허용하는 연습이 성장의 열쇠입니다.",
     "compatible": {"best": ["7", "9"], "challenging": ["4"]},
     "compatible_desc": {"best": "7번의 자유로운 에너지는 1번의 긴장을 풀어 주고, 9번의 수용적 태도는 1번에게 쉼을 줍니다.", "challenging": "4번과는 '완벽 대 독특함'이라는 기준 충돌이 생기기 쉽습니다."}},
    {"type": "2", "name": "조력가형", "icon": "🤲", "color": "#EC4899",
     "text": "다른 사람을 돕는 것에서 만족을 느끼며, 사랑받고 필요한 존재가 되고 싶다. 타인의 감정에 매우 민감하다.",
     "core_fear": "사랑받지 못하고 필요하지 않은 존재가 되는 것", "core_desire": "진심으로 사랑받는 것",
     "desc": "따뜻한 마음으로 타인의 필요에 응답합니다. 관계 속에서 자신의 가치를 발견합니다.",
     "detail": "2번 조력가형은 사랑의 언어가 '봉사'입니다. 진심으로 타인을 돕지만, 그 이면에는 인정받고 싶은 욕구가 숨어 있을 수 있습니다. 자신의 필요를 억누르고 타인 중심으로 살다 보면 내면에 원망이 쌓이기 쉽습니다. 자기 자신에게도 같은 친절을 베푸는 것이 성장 방향입니다.",
     "compatible": {"best": ["4", "8"], "challenging": ["5"]},
     "compatible_desc": {"best": "4번의 깊은 감정 세계는 2번의 공감 능력과 잘 맞고, 8번의 직접성은 2번이 솔직해지도록 돕습니다.", "challenging": "5번의 독립·거리 선호는 연결을 원하는 2번에게 거절처럼 느껴질 수 있습니다."}},
    {"type": "3", "name": "성취자형", "icon": "🏆", "color": "#F59E0B",
     "text": "성공하고 인정받고 싶은 욕구가 강하며, 목표를 향해 효율적으로 움직인다. 이미지와 성과를 매우 중시한다.",
     "core_fear": "실패하고 가치 없는 존재가 되는 것", "core_desire": "가치 있고 성공한 사람이 되는 것",
     "desc": "목표 지향적이며 적응력이 뛰어납니다. 성과로 자신의 가치를 증명하려 합니다.",
     "detail": "3번 성취자형은 어떤 환경에서도 빠르게 성과를 내는 능력이 있습니다. 하지만 '하는 것(doing)'에 집중하다 보면 '있는 것(being)'을 잊기 쉽습니다. 이미지와 역할 뒤에 숨지 않고 진짜 자신과 만나는 것, 성과 없이도 사랑받을 수 있다는 것을 내면화하는 것이 핵심 성장 과제입니다.",
     "compatible": {"best": ["6", "9"], "challenging": ["8"]},
     "compatible_desc": {"best": "6번의 충성심은 3번에게 안전한 관계 기반을 제공하고, 9번은 3번이 쉬어갈 수 있는 공간을 만들어 줍니다.", "challenging": "8번과는 주도권 경쟁이 생기기 쉬워 갈등이 잦을 수 있습니다."}},
    {"type": "4", "name": "개인주의형", "icon": "🎭", "color": "#8B5CF6",
     "text": "자신만의 독특한 정체성과 감정 세계를 중시하며, 평범함을 거부한다. 깊은 감정과 창의적 표현에 이끌린다.",
     "core_fear": "정체성 없이 평범한 존재가 되는 것", "core_desire": "자신만의 정체성과 의미를 발견하는 것",
     "desc": "깊은 감정과 독창성을 추구합니다. 아름다움과 진정성에 민감하며 예술적 감수성이 풍부합니다.",
     "detail": "4번 개인주의형은 감정의 깊이와 아름다움을 탐구하는 예술가적 영혼을 지닙니다. '나는 남들과 다르다'는 정체성이 독창적 창조의 원천이 되지만, 동시에 소외감과 결핍감으로 이어지기도 합니다. 현재의 나 자신을 있는 그대로 받아들이는 연습, 그리고 깊은 감정을 행동으로 전환하는 능력이 성장의 핵심입니다.",
     "compatible": {"best": ["1", "5"], "challenging": ["2"]},
     "compatible_desc": {"best": "1번의 원칙은 4번에게 방향성을 주고, 5번의 지적 탐구는 4번의 내면 세계를 더욱 풍요롭게 합니다.", "challenging": "2번의 적극적 도움은 사생활을 중시하는 4번에게 부담으로 느껴질 수 있습니다."}},
    {"type": "5", "name": "탐구자형", "icon": "🔭", "color": "#06B6D4",
     "text": "지식과 정보를 축적하며 세상을 이해하고 싶다. 혼자만의 공간이 필요하며, 에너지를 아끼는 경향이 있다.",
     "core_fear": "무능하고 쓸모없는 존재가 되는 것", "core_desire": "유능하고 통찰 있는 존재가 되는 것",
     "desc": "깊이 있는 탐구를 통해 세상을 이해합니다. 독립성과 내적 자원을 중시합니다.",
     "detail": "5번 탐구자형은 관찰하고 분석하는 것으로 세상을 이해합니다. 에너지를 매우 소중하게 여기며 혼자만의 시간과 공간 없이는 고갈을 느낍니다. 지식을 축적하는 것이 강점이지만, 삶에 참여하는 것을 미루거나 감정 표현을 회피하는 경향이 있습니다. 관계 속으로 실제로 나오는 연습이 중요합니다.",
     "compatible": {"best": ["4", "8"], "challenging": ["2"]},
     "compatible_desc": {"best": "4번의 감성적 깊이는 5번의 지적 탐구를 보완하고, 8번의 직접성은 5번이 현실 세계에 더 적극적으로 참여하도록 돕습니다.", "challenging": "2번의 감정적 요구와 가까움 추구는 혼자만의 공간을 필요로 하는 5번에게 부담이 됩니다."}},
    {"type": "6", "name": "충성파형", "icon": "🔐", "color": "#10B981",
     "text": "안전을 추구하고 믿을 수 있는 시스템과 사람을 찾는다. 걱정이 많고 최악의 상황을 미리 생각하는 편이다.",
     "core_fear": "보호 없이 홀로 남겨지는 것", "core_desire": "안전과 지지를 얻는 것",
     "desc": "안전과 신뢰를 삶의 토대로 삼습니다. 위험에 민감하고 책임감이 강합니다.",
     "detail": "6번 충성파형은 위험과 문제를 미리 감지하는 탁월한 능력을 가지고 있습니다. 신뢰하는 사람에게는 한없이 헌신적이며 공동체에 대한 책임감이 강합니다. 하지만 불안과 의심이 과도해지면 의사결정이 어려워지거나 타인의 의도를 부정적으로 해석하기 쉽습니다. 자신의 내면에 충분한 자원이 있음을 신뢰하는 연습이 핵심입니다.",
     "compatible": {"best": ["3", "9"], "challenging": ["7"]},
     "compatible_desc": {"best": "3번의 자신감과 행동력은 6번이 주저하는 순간에 힘이 되고, 9번의 평화로운 에너지는 6번의 불안을 진정시킵니다.", "challenging": "7번의 즉흥성과 위험 감수 성향은 안전을 중시하는 6번에게 불안감을 줄 수 있습니다."}},
    {"type": "7", "name": "열정파형", "icon": "✨", "color": "#FF6B35",
     "text": "새로운 경험과 즐거움을 추구하며, 부정적인 것을 피하려 한다. 에너지가 넘치고 낙관적이며 늘 새로운 계획이 있다.",
     "core_fear": "고통과 결핍 속에 갇히는 것", "core_desire": "행복하고 충족된 상태를 유지하는 것",
     "desc": "삶의 즐거움과 가능성을 열정적으로 추구합니다. 다재다능하고 창의적입니다.",
     "detail": "7번 열정파형은 삶에 대한 열정이 넘쳐 주변 사람들에게 활력을 줍니다. 끊임없이 새로운 아이디어와 경험을 찾으며 낙관적인 시각으로 가능성을 봅니다. 하지만 고통·지루함·결핍을 피하려는 욕구가 강해 한 가지에 오래 머무르지 못하거나 어려운 감정을 회피하는 경향이 있습니다. 깊이 있게 머무르는 연습이 삶의 충족감을 높여 줍니다.",
     "compatible": {"best": ["1", "5"], "challenging": ["6"]},
     "compatible_desc": {"best": "1번의 집중력은 7번의 분산된 에너지에 방향을 주고, 5번의 깊이 있는 탐구는 7번이 한 곳에 머물도록 도움을 줍니다.", "challenging": "6번의 조심스럽고 불안한 에너지는 자유롭게 움직이고 싶은 7번에게 제약처럼 느껴질 수 있습니다."}},
    {"type": "8", "name": "도전자형", "icon": "🦁", "color": "#DC2626",
     "text": "강하고 독립적이며 타인에게 통제받기 싫어한다. 직접적이고 단호하며 불의에 강하게 반응한다.",
     "core_fear": "타인에게 통제되거나 상처받는 것", "core_desire": "스스로를 지키고 삶을 통제하는 것",
     "desc": "강인함과 결단력으로 세상을 직면합니다. 부당함에 맞서 싸우는 용기가 있습니다.",
     "detail": "8번 도전자형은 강렬한 존재감과 에너지로 주변에 강한 인상을 남깁니다. 약자를 보호하고 불의에 맞서는 것을 사명으로 여기며, 직접적이고 솔직한 소통을 선호합니다. 하지만 자신의 취약함을 드러내는 것을 극도로 불편해하며, 강함을 유지하려는 방어가 친밀한 관계 형성을 어렵게 할 수 있습니다. 연약함도 힘의 일부임을 받아들이는 것이 핵심 성장 과제입니다.",
     "compatible": {"best": ["2", "5"], "challenging": ["3"]},
     "compatible_desc": {"best": "2번의 따뜻함은 8번의 딱딱한 외면을 녹여 주고, 5번은 8번의 강한 에너지를 지적으로 수용할 수 있습니다.", "challenging": "3번과는 주도권 경쟁이 생기기 쉬우며 서로의 강한 자아가 충돌할 수 있습니다."}},
    {"type": "9", "name": "화해자형", "icon": "☮️", "color": "#84CC16",
     "text": "평화와 조화를 사랑하며 갈등을 피하려 한다. 타인의 입장을 잘 이해하지만 자신의 의견을 드러내길 어려워한다.",
     "core_fear": "단절과 갈등으로 평화를 잃는 것", "core_desire": "내면의 평온과 외부의 화합",
     "desc": "내면의 평화와 외부의 조화를 추구합니다. 포용력이 넓고 중재 능력이 탁월합니다.",
     "detail": "9번 화해자형은 모든 관점을 자연스럽게 수용하는 넓은 포용력을 지닙니다. 갈등을 중재하고 다양한 사람들을 연결하는 데 탁월하지만, 평화를 유지하려다 보면 자신의 욕구와 의견을 무시하게 되는 '자기 망각'이 일어납니다. '나는 무엇을 원하는가?'라는 질문을 스스로에게 자주 던지는 것, 그리고 갈등을 피하지 않고 적절히 표현하는 연습이 성장의 핵심입니다.",
     "compatible": {"best": ["3", "6"], "challenging": ["1"]},
     "compatible_desc": {"best": "3번의 추진력은 9번이 움직이도록 동기를 주고, 6번은 신뢰를 바탕으로 9번이 편안함을 느끼게 합니다.", "challenging": "1번의 높은 기준과 비판적 목소리는 평화를 원하는 9번을 위축시킬 수 있습니다."}},
]
ENNEA_OPTS = ["💯  꼭 나 같다", "🙂  어느 정도 나", "😶  별로 아니다"]
ENNEA_SCORES = [3, 2, 1]

# 3) 스트레스 반응 패턴 (10Q)
STRESS_Q = [
    {"text": "업무나 과제가 극도로 쌓였을 때 나는…",
     "opts": ["더 집중해서 하나씩 처리하려 한다", "잠시 기분 전환 후 다시 복귀한다",
              "어쩔 줄 몰라 미루거나 회피하게 된다", "짜증이 나거나 감정적으로 예민해진다"],
     "keys": ["PS", "RC", "AV", "ER"]},
    {"text": "가까운 사람과 크게 다퉜을 때 나는…",
     "opts": ["원인을 분석하고 해결책을 찾으려 한다", "각자 시간이 지나면 자연스레 해결될 것이라 생각한다",
              "그 상황을 피하거나 잊으려 한다", "감정이 격해져 울거나 즉각 표출하게 된다"],
     "keys": ["PS", "RC", "AV", "ER"]},
    {"text": "예상치 못한 실패나 실수를 했을 때 나는…",
     "opts": ["무엇이 잘못됐는지 분석하고 개선점을 찾는다", "자신을 다독이고 다음 기회를 생각한다",
              "될 수 있으면 그 일을 떠올리고 싶지 않다", "분함·자책감에 오랫동안 시달린다"],
     "keys": ["PS", "RC", "AV", "ER"]},
    {"text": "장기간 스트레스가 지속될 때 나의 상태는…",
     "opts": ["더 바지런히 움직이며 일로 해소한다", "수면·취미·운동으로 회복 시간을 챙긴다",
              "점점 무감각해지거나 아무것도 하기 싫어진다", "신체 증상이나 감정 기복이 나타난다"],
     "keys": ["PS", "RC", "AV", "ER"]},
    {"text": "불안감이 클 때 내가 자주 하는 대처는…",
     "opts": ["할 일 목록을 만들거나 계획을 세운다", "운동·산책·음악으로 기분을 환기한다",
              "유튜브·SNS·게임에 빠져 생각을 끊는다", "가까운 사람에게 털어놓거나 감정을 표현한다"],
     "keys": ["PS", "RC", "AV", "ER"]},
    {"text": "나에 대한 비판이나 부정적 평가를 들었을 때 나는…",
     "opts": ["피드백으로 받아들이고 개선하려 한다", "잠시 당황하지만 곧 기분을 회복한다",
              "그 상황을 피하거나 그 사람과 거리를 둔다", "상당히 오랫동안 마음이 쓰이고 속상하다"],
     "keys": ["PS", "RC", "AV", "ER"]},
    {"text": "중요한 결정을 앞두고 있을 때 나는…",
     "opts": ["모든 정보를 분석해 최선의 결론을 도출한다", "직관을 믿고 가볍게 결정한다",
              "결정을 최대한 미루거나 타인에게 위임한다", "불안으로 과도하게 걱정하거나 잠을 못 이룬다"],
     "keys": ["PS", "RC", "AV", "ER"]},
    {"text": "스트레스를 풀기 위해 내가 자주 사용하는 방법은…",
     "opts": ["운동·청소·일 등 몸을 움직이는 활동", "친구와의 대화·취미·여행 등 전환 활동",
              "유튜브·폭식 등 자신도 모르게 하는 것들", "울거나 감정을 솔직히 표현하는 것"],
     "keys": ["PS", "RC", "AV", "ER"]},
    {"text": "주변이 시끄럽고 혼란스러울 때 나는…",
     "opts": ["문제를 정리하고 구조화하려 한다", "잠시 자리를 피해 혼자만의 공간을 찾는다",
              "혼란을 무시하고 내 일에 집중하려 한다", "정서적으로 흔들리고 집중하기 어렵다"],
     "keys": ["PS", "RC", "AV", "ER"]},
    {"text": "내가 가장 잘 회복되는 방식은…",
     "opts": ["능동적으로 문제를 해결하고 성취감을 얻는 것", "충분한 휴식과 즐거운 경험으로 재충전하는 것",
              "조용히 시간이 지나면서 자연스럽게 회복", "가까운 사람과 감정을 나누며 위로를 받는 것"],
     "keys": ["PS", "RC", "AV", "ER"]},
]
STRESS_TYPES = {
    "PS": {"name": "문제 해결형", "icon": "🔧", "color": "#0369A1",
           "desc": "스트레스를 받을 때 즉각적으로 문제를 분석하고 해결하려 합니다. 통제감 회복이 핵심 동기이며 능동적 대처가 강점입니다.",
           "detail": "문제 해결형은 스트레스 상황을 '극복해야 할 과제'로 인식합니다. 할 일 목록 작성, 전략 수립, 정보 수집 등의 방식으로 상황을 통제하려 합니다. 이 능동적 태도는 실제로 많은 문제를 효과적으로 해결하지만, 통제할 수 없는 상황(관계 갈등, 감정의 영역)에서는 오히려 소진될 수 있습니다. 때로는 '문제를 해결하지 않아도 괜찮다'는 허용이 필요합니다.",
           "tip": "때로는 문제를 해결하지 않고 그냥 '느끼는' 연습이 필요합니다. 불확실성을 감내하는 능력을 함께 길러 가세요.",
           "therapy": "CBT의 행동 활성화 + 자기 효능감 강화 훈련",
           "compatible": {"best": ["RC"], "challenging": ["AV"]},
           "compatible_desc": {"best": "전환 회복형(RC)과는 문제에 접근하는 방식이 달라 서로 보완적입니다. RC의 유연한 회복이 PS의 긴장을 풀어 줍니다.", "challenging": "회피 마비형(AV)과는 문제를 마주하는 방식이 너무 달라 서로 답답함을 느끼기 쉽습니다."}},
    "RC": {"name": "전환 회복형", "icon": "🌊", "color": "#059669",
           "desc": "기분을 전환하고 재충전을 통해 자연스럽게 회복합니다. 정서적 유연성이 높고 회복탄력성이 뛰어납니다.",
           "detail": "전환 회복형은 스트레스를 '회복이 필요한 신호'로 읽습니다. 취미, 운동, 사교, 여행 등 자신에게 즐거움을 주는 활동으로 에너지를 재충전하며, 상황이 지나가면 자연스럽게 회복됩니다. 이 유연함은 큰 강점이지만, 회피가 패턴이 되어 중요한 문제를 계속 뒤로 미루게 될 위험이 있습니다. 때로는 불편한 감정에 머무르는 연습도 필요합니다.",
           "tip": "전환이 회피로 변하지 않도록 주의하세요. 중요한 문제는 외면하지 않고 적절히 직면하는 균형이 필요합니다.",
           "therapy": "마음챙김 기반 스트레스 감소(MBSR)",
           "compatible": {"best": ["PS"], "challenging": ["ER"]},
           "compatible_desc": {"best": "문제 해결형(PS)의 체계적 접근은 RC에게 방향을 제시하고, RC의 회복력은 PS의 긴장을 완화합니다.", "challenging": "감정 반응형(ER)의 강한 정서 표현은 평온을 추구하는 RC에게 버거울 수 있습니다."}},
    "AV": {"name": "회피 마비형", "icon": "🌫️", "color": "#6B7280",
           "desc": "스트레스 상황에서 무감각해지거나 회피하는 경향이 있습니다. 장기적으로 문제가 쌓이고 내면 소진으로 이어질 수 있습니다.",
           "detail": "회피 마비형은 스트레스 자극이 너무 클 때 차단(shutdown) 모드로 전환됩니다. 과부하를 막기 위한 자기 보호 반응이지만, 만성적으로 지속되면 미뤄진 문제들이 쌓여 더 큰 스트레스를 만들어 냅니다. 작은 일부터 시작하는 점진적 노출, 신뢰할 수 있는 사람에게 털어놓기, 몸을 움직이는 활동이 패턴을 변화시키는 좋은 출발점입니다.",
           "tip": "회피 패턴을 인식하는 것이 첫 번째 단계입니다. 작은 불편감을 점진적으로 직면하는 노출 훈련이 중요합니다.",
           "therapy": "수용전념치료(ACT)와 점진적 노출요법",
           "compatible": {"best": ["ER"], "challenging": ["PS"]},
           "compatible_desc": {"best": "감정 반응형(ER)의 직접적인 감정 표현은 AV가 억압한 감정을 안전하게 대리 경험하게 해 줄 수 있습니다.", "challenging": "문제 해결형(PS)의 즉각적 행동 요구는 마비 상태의 AV에게 더 큰 압박이 될 수 있습니다."}},
    "ER": {"name": "감정 반응형", "icon": "🌋", "color": "#DC2626",
           "desc": "스트레스가 감정 반응으로 즉각 표출되는 경향이 있습니다. 감정 민감도가 높고 자책이나 분노로 나타날 수 있습니다.",
           "detail": "감정 반응형은 감정의 안테나가 매우 예민합니다. 작은 자극에도 강하게 반응하며, 이 감수성은 공감 능력과 창의성의 원천이 되기도 합니다. 하지만 충동적 표현이 관계를 손상시키거나, 강렬한 자책 감정이 장기간 지속될 수 있습니다. 감정과 행동 사이에 '숨 고르기' 공간을 만드는 연습, 즉 자극-반응 사이의 간격을 넓히는 것이 핵심 과제입니다.",
           "tip": "감정 일기, 마음챙김 명상, 호흡법 등으로 감정과 행동 사이에 '공간'을 만드는 연습이 효과적입니다.",
           "therapy": "변증법적 행동치료(DBT) + 정서중심치료(EFT)",
           "compatible": {"best": ["AV"], "challenging": ["RC"]},
           "compatible_desc": {"best": "회피 마비형(AV)의 차분함은 ER의 강렬한 감정을 안정시켜 주는 역할을 합니다.", "challenging": "전환 회복형(RC)의 가벼운 태도는 ER에게 진지하게 받아들여지지 않는 느낌을 줄 수 있습니다."}},
}

# ══════════════════════════════════════════════════════════════
# ─── DATA LAYER ──────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════
DATA_FILE = "mindlab_data.json"

def load_data() -> dict:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "profile": {
            "name": "", "age_range": "",
            "bfi": {}, "attachment": None,
            "values": [], "ai_summary": ""
        },
        "messages": [],
        "journals": [],
        "quiz_results": {},
    }

def save_data(d: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

# ── Session ──────────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state.data = load_data()
if "msgs" not in st.session_state:
    st.session_state.msgs = st.session_state.data.get("messages", [])
if "chat_k" not in st.session_state:
    st.session_state.chat_k = 0
if "bfi_submitted" not in st.session_state:
    st.session_state.bfi_submitted = bool(st.session_state.data["profile"].get("bfi"))
if "ecr_submitted" not in st.session_state:
    st.session_state.ecr_submitted = bool(st.session_state.data["profile"].get("attachment"))
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_results" not in st.session_state:
    st.session_state.quiz_results = dict(st.session_state.data.get("quiz_results", {}))
# returning_user_choice는 data 파일 기반으로 관리 (session_state 불필요)

# ── Helpers ──────────────────────────────────────────────────
def get_client():
    key = os.getenv("OPENAI_API_KEY", "")
    if not key or key.startswith("your_"):
        return None
    return OpenAI(api_key=key)

def build_system_prompt() -> str:
    pr = st.session_state.data["profile"]
    sp  = (
        "당신은 임상심리학 전문 지식을 갖춘 AI 심리 상담사 '소이'입니다. "
        "Rogers의 인간중심 치료, Beck의 인지행동치료(CBT), "
        "Bowlby의 애착 이론, Schwartz의 가치 이론에 기반한 상담을 제공합니다.\n\n"
        "핵심 규칙:\n"
        "1. 진단(DSM/ICD)을 내리지 않습니다. 심리 교육과 자기 이해를 돕습니다.\n"
        "2. 무조건적 긍정적 존중(Unconditional Positive Regard)으로 응합니다.\n"
        "3. 반영적 경청(Reflective Listening)과 열린 질문을 사용합니다.\n"
        "4. 필요 시 '전문적인 임상 상담가의 도움을 권합니다'라고 명확히 말합니다.\n"
        "5. 응답은 200~350자, 따뜻하고 전문적인 어조로 작성합니다.\n"
        "6. 마지막에 내담자 스스로 성찰하도록 하는 열린 질문 1개를 추가합니다.\n\n"
    )
    if pr.get("name"):
        sp += f"내담자 호칭: {pr['name']} 님\n"
    if pr.get("age_range"):
        sp += f"연령대: {pr['age_range']}\n"
    bfi = pr.get("bfi", {})
    if bfi:
        sp += "\n[Big Five 성격 프로파일]:\n"
        for k, v in bfi.items():
            m = BFI_META[k]
            lvl = "높음" if v >= 60 else "보통" if v >= 40 else "낮음"
            if k == "N":
                lvl = "낮음(안정)" if v < 40 else "보통" if v < 60 else "높음(불안정)"
            sp += f"  • {m['name']}: {v}/100 ({lvl})\n"
    att = pr.get("attachment")
    if att and att in ATTACHMENT_TYPES:
        at = ATTACHMENT_TYPES[att]
        sp += f"\n[애착 유형]: {at['name']}\n{at['summary']}\n"
    vals = pr.get("values", [])
    if vals:
        sp += f"\n[핵심 가치관]: {', '.join(vals)}\n"
    return sp

def call_gpt(messages: list, system: str = "", tokens: int = 600) -> str:
    client = get_client()
    if not client:
        return "⚠️ .env 파일의 OPENAI_API_KEY를 확인해 주세요."
    all_msgs = [{"role": "system", "content": system}] + messages if system else messages
    try:
        r = client.chat.completions.create(
            model="gpt-4o-mini", messages=all_msgs,
            max_tokens=tokens, temperature=0.82,
        )
        return r.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ 오류가 발생했습니다: {e}"

def score_bfi(answers: dict) -> dict:
    trait_scores = {t: [] for t in "OCEAN"}
    for idx, (trait, reverse, _) in enumerate(BFI_ITEMS):
        val = answers.get(idx, 3)
        if reverse:
            val = 6 - val
        trait_scores[trait].append(val)
    return {
        t: round((sum(v)/len(v) - 1) / 4 * 100)
        for t, v in trait_scores.items()
    }

def score_ecr(answers: dict) -> str:
    ax = sum(answers.get(i, 3) for i in [0, 2, 4, 6]) / 4
    av = sum(answers.get(i, 3) for i in [1, 3, 5, 7]) / 4
    if ax <= 2.5 and av <= 2.5:
        return "secure"
    if ax > 2.5 and av <= 2.5:
        return "anxious"
    if ax <= 2.5 and av > 2.5:
        return "avoidant"
    return "fearful"

# ═══════════════════════════════════════════════════════════════
# ─── SIDEBAR ───────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    pr = st.session_state.data["profile"]
    name = pr.get("name", "")
    steps = sum([bool(pr.get("name")), bool(pr.get("bfi")),
                 bool(pr.get("attachment")), bool(pr.get("values"))])
    pct = int(steps / 4 * 100)
    j_n = len(st.session_state.data.get("journals", []))
    c_n = len(st.session_state.msgs) // 2

    st.markdown(f"""
    <div style="padding:1.8rem .4rem 1rem;">
      <div style="font-size:1.2rem;font-weight:800;color:#EDE8E0;letter-spacing:-.02em;font-family:'Lora',serif;">
        마음 연구소
      </div>
      <div style="font-size:.7rem;color:#3A3530;margin-top:3px;letter-spacing:.04em;">
        Mind Laboratory
      </div>
    </div>
    """, unsafe_allow_html=True)

    if name:
        st.markdown(f"""
        <div style="background:rgba(91,79,207,.08);border:1px solid rgba(91,79,207,.15);border-radius:10px;padding:.55rem .85rem;margin-bottom:.5rem;">
          <div style="font-size:.68rem;color:#5B4FCF;font-weight:700;letter-spacing:.06em;">CURRENT CLIENT</div>
          <div style="font-size:.9rem;color:#DDD8FF;font-weight:700;margin-top:2px;">{name}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    incomplete = [n for k, n in [("name","이름"),("bfi","Big Five"),("attachment","애착"),("values","가치관")] if not pr.get(k)]
    hint = "프로필 완성! 🎉" if not incomplete else f"{' · '.join(incomplete)} 필요"
    st.markdown(f"""
    <div style="margin-bottom:12px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
        <span style="font-size:.66rem;font-weight:700;color:#3A3530;text-transform:uppercase;letter-spacing:.09em;">프로필</span>
        <span style="font-size:.76rem;font-weight:800;color:#9B8EF0;">{pct}%</span>
      </div>
      <div class="sb-bar-bg"><div class="sb-bar-fill" style="width:{pct}%;"></div></div>
      <div style="font-size:.67rem;color:#2A2520;margin-top:4px;">{hint}</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(f"""
    <div>
      <div style="font-size:.66rem;font-weight:700;color:#3A3530;text-transform:uppercase;letter-spacing:.09em;margin-bottom:10px;">세션 요약</div>
      <div class="sb-stat">
        <span style="font-size:.8rem;color:#4A4540;">💬 상담 횟수</span>
        <span style="font-size:.84rem;font-weight:700;color:#9B8EF0;">{c_n}회</span>
      </div>
      <div class="sb-stat">
        <span style="font-size:.8rem;color:#4A4540;">📓 일기 기록</span>
        <span style="font-size:.84rem;font-weight:700;color:#9B8EF0;">{j_n}편</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    if pr.get("attachment"):
        att = ATTACHMENT_TYPES[pr["attachment"]]
        st.markdown(f"""
        <div style="background:rgba(91,79,207,.06);border-radius:10px;padding:.6rem .85rem;margin-bottom:8px;">
          <div style="font-size:.66rem;color:#3A3530;font-weight:700;letter-spacing:.06em;margin-bottom:3px;">애착 유형</div>
          <div style="font-size:.84rem;color:#C4BEF0;font-weight:600;">{att["icon"]} {att["name"]}</div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🗑  상담 기록 초기화", use_container_width=True):
        st.session_state.msgs = []
        st.session_state.data["messages"] = []
        save_data(st.session_state.data)
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# ─── RETURNING USER CHECK ──────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
def _has_saved_data() -> bool:
    d = st.session_state.data
    return (
        bool(d["profile"].get("bfi")) or
        bool(d["profile"].get("attachment")) or
        bool(d["profile"].get("name")) or
        bool(d.get("quiz_results")) or
        bool(d.get("journals")) or
        bool(d.get("messages"))
    )

# 환영 화면: 저장된 데이터가 있고, 아직 선택 안 한 경우에만 1회 표시
if not st.session_state.data.get("welcomed") and _has_saved_data():
    pr_name = st.session_state.data["profile"].get("name", "")
    greeting = f"{pr_name} 님, 다시 오셨군요!" if pr_name else "다시 오셨군요!"

    qr = st.session_state.data.get("quiz_results", {})
    bfi_done  = bool(st.session_state.data["profile"].get("bfi"))
    ecr_done  = bool(st.session_state.data["profile"].get("attachment"))
    temp_done = bool(qr.get("temperament"))
    ennn_done = bool(qr.get("enneagram"))
    strss_done = bool(qr.get("stress"))
    done_count = sum([bfi_done, ecr_done, temp_done, ennn_done, strss_done])

    st.markdown(f"""
    <div style="max-width:580px;margin:3rem auto 0;text-align:center;">
      <div style="font-size:2.8rem;margin-bottom:.8rem;">◎</div>
      <div style="font-size:1.55rem;font-weight:800;color:var(--t1);margin-bottom:.4rem;">{greeting}</div>
      <div style="font-size:.92rem;color:var(--t3);margin-bottom:1.8rem;line-height:1.7;">
        마음 연구소에 이전 기록이 남아 있어요.<br>
        이어서 탐구하거나, 처음부터 새로 시작할 수 있어요.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # progress summary
    badges = []
    if bfi_done:   badges.append("🧠 Big Five")
    if ecr_done:   badges.append("💞 애착 유형")
    if temp_done:
        tt = TEMP_TYPES.get(qr["temperament"], {})
        badges.append(f"{tt.get('icon','🧭')} {tt.get('name','기질')}")
    if ennn_done:
        ei = next((e for e in ENNEA_ITEMS if e["type"] == qr["enneagram"]), None)
        badges.append(f"{ei['icon'] if ei else '🔢'} {qr['enneagram']}번 에니어그램" if ei else "🔢 에니어그램")
    if strss_done:
        st_ = STRESS_TYPES.get(qr["stress"], {})
        badges.append(f"{st_.get('icon','⚡')} {st_.get('name','스트레스')}")

    if badges:
        badge_html = "".join(
            f'<span style="display:inline-block;background:var(--indigo-lt);color:var(--indigo);'
            f'border-radius:20px;padding:4px 12px;font-size:.76rem;font-weight:700;margin:3px 4px;">'
            f'{b}</span>'
            for b in badges
        )
        st.markdown(f"""
        <div style="max-width:580px;margin:0 auto 1.6rem;text-align:center;">
          <div style="font-size:.72rem;color:var(--t4);font-weight:700;letter-spacing:.06em;
                      text-transform:uppercase;margin-bottom:.6rem;">완료한 검사 · {done_count}/5</div>
          <div>{badge_html}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='max-width:480px;margin:0 auto;'>", unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns(2, gap="medium")
    with btn_col1:
        if st.button("📂  이전 기록 이어서 하기", use_container_width=True, type="primary"):
            st.session_state.data["welcomed"] = True
            save_data(st.session_state.data)
            st.rerun()
    with btn_col2:
        if st.button("🔄  처음부터 다시하기", use_container_width=True):
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ═══════════════════════════════════════════════════════════════
# ─── MAIN TABS ─────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
T1, T2, T3, T4, T5 = st.tabs([
    "◎  내 심리 프로필",
    "💬  AI 심리 상담",
    "🔬  성격 심층 진단",
    "🧩  심리 탐색 테스트",
    "📓  감정 일지",
])

# ═══════════════════════════════════════════════════════════════
# TAB 1 · PROFILE
# ═══════════════════════════════════════════════════════════════
with T1:
    pr = st.session_state.data["profile"]

    st.markdown("""
    <div style="margin-bottom:1.2rem;">
      <div class="page-eyebrow">심리 프로파일링</div>
      <div class="page-title">나의 심리 프로필</div>
      <div class="page-desc">임상심리학에서 검증된 척도를 기반으로 나의 성격·애착·가치관을 통합적으로 이해합니다.</div>
    </div>
    """, unsafe_allow_html=True)

    # ── 오늘의 심리 명언 ──
    _q_idx = date.today().toordinal() % len(PSYCH_QUOTES)
    _q_text, _q_author = PSYCH_QUOTES[_q_idx]
    st.markdown(f"""
    <div style="padding:.85rem 1.25rem;background:linear-gradient(135deg,var(--indigo-lt),#F5F3FF);
                border-left:3px solid var(--indigo);border-radius:12px;margin-bottom:1.4rem;">
      <div style="font-size:.68rem;font-weight:700;color:var(--indigo);letter-spacing:.07em;margin-bottom:5px;">
        ✦ 오늘의 심리 명언
      </div>
      <div style="font-size:.9rem;color:var(--t1);font-style:italic;line-height:1.7;margin-bottom:5px;">
        "{_q_text}"
      </div>
      <div style="font-size:.75rem;color:var(--t3);font-weight:600;">— {_q_author}</div>
    </div>
    """, unsafe_allow_html=True)

    col_info, col_right = st.columns([2, 3], gap="large")

    with col_info:
        # ── 기본 정보 ──
        new_name = st.text_input("이름/닉네임", value=pr.get("name",""),
                                 placeholder="어떻게 불러드릴까요?", key="p_name")
        age_options = ["선택", "10대", "20대 초반", "20대 후반", "30대", "40대", "50대 이상"]
        cur_age = pr.get("age_range", "선택")
        age_idx = age_options.index(cur_age) if cur_age in age_options else 0
        new_age = st.selectbox("연령대", age_options, index=age_idx, key="p_age")
        if st.button("저장", key="save_basic", use_container_width=True):
            st.session_state.data["profile"]["name"] = new_name
            st.session_state.data["profile"]["age_range"] = new_age if new_age != "선택" else ""
            save_data(st.session_state.data)
            st.toast("저장되었습니다.", icon="✅")

        # ── 검사 현황 ──
        _all_steps = [
            ("Big Five 성격 검사", bool(pr.get("bfi")), "🧠"),
            ("애착 유형 검사", bool(pr.get("attachment")), "💞"),
            ("핵심 가치 선택", bool(pr.get("values")), "✦"),
            ("기질 나침반", bool(st.session_state.quiz_results.get("temperament")), "🧭"),
            ("에니어그램", bool(st.session_state.quiz_results.get("enneagram")), "🔢"),
            ("스트레스 패턴", bool(st.session_state.quiz_results.get("stress")), "⚡"),
        ]
        _done = sum(1 for _, d, _ in _all_steps if d)
        _pct  = int(_done / len(_all_steps) * 100)
        _bar_items = "".join(
            f"<div style='display:flex;align-items:center;gap:8px;padding:5px 0;"
            f"border-bottom:1px solid var(--border);'>"
            f"<span style='font-size:.75rem;color:{'var(--sage)' if d else 'var(--t4)'};"
            f"width:14px;flex-shrink:0;'>{'✓' if d else '○'}</span>"
            f"<span style='font-size:.75rem;'>{ic}</span>"
            f"<span style='font-size:.79rem;color:{'var(--t1)' if d else 'var(--t3)'};"
            f"flex:1;'>{nm}</span>"
            f"{'<span class=\"chip chip-sage\" style=\"font-size:.6rem;padding:1px 7px;\">완료</span>' if d else '<span class=\"chip chip-amber\" style=\"font-size:.6rem;padding:1px 7px;\">대기</span>'}"
            f"</div>"
            for nm, d, ic in _all_steps
        )
        st.markdown(f"""
        <div class="card card-sm" style="margin-top:.5rem;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <div class="sec-title">검사 현황</div>
            <span style="font-size:.78rem;font-weight:800;color:var(--indigo);">{_done}/{len(_all_steps)}</span>
          </div>
          <div style="background:var(--bg2);border-radius:999px;height:4px;margin-bottom:10px;">
            <div style="width:{_pct}%;height:100%;background:var(--indigo);border-radius:999px;"></div>
          </div>
          {_bar_items}
        </div>
        """, unsafe_allow_html=True)

        # ── 애착 유형 ──
        if pr.get("attachment") and pr["attachment"] in ATTACHMENT_TYPES:
            at = ATTACHMENT_TYPES[pr["attachment"]]
            st.markdown(f"""
            <div class="card card-sm" style="border-top:3px solid {at['color']};margin-top:.4rem;">
              <div class="label-sm" style="margin-bottom:6px;">애착 유형 (ECR-R)</div>
              <div style="font-size:1.5rem;margin-bottom:4px;">{at['icon']}</div>
              <div style="font-size:.97rem;font-weight:700;color:var(--t1);margin-bottom:5px;">{at['name']}</div>
              <div style="font-size:.78rem;color:var(--t3);line-height:1.65;">{at['summary']}</div>
            </div>
            """, unsafe_allow_html=True)

        # ── 핵심 가치관 ──
        if pr.get("values"):
            chips = "".join(f"<span class='chip chip-indigo'>{v}</span>" for v in pr["values"])
            st.markdown(f"""
            <div class="card card-sm" style="margin-top:.4rem;">
              <div class="label-sm" style="margin-bottom:8px;">핵심 가치관 (Schwartz)</div>
              {chips}
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        bfi = pr.get("bfi", {})
        if bfi:
            traits_order = ["O", "C", "E", "A", "N"]
            labels = [BFI_META[t]["ko"] for t in traits_order]
            vals   = [bfi.get(t, 50) for t in traits_order]
            v_c = vals + [vals[0]]
            l_c = labels + [labels[0]]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=v_c, theta=l_c, fill="toself",
                fillcolor="rgba(91,79,207,0.10)",
                line=dict(color="#5B4FCF", width=2.2),
                marker=dict(size=6, color="#5B4FCF", line=dict(color="white", width=1.5)),
            ))
            fig.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0, 100],
                                   tickfont=dict(size=8, color="#C0BBB5"),
                                   gridcolor="rgba(91,79,207,0.08)", linecolor="rgba(91,79,207,0.06)"),
                    angularaxis=dict(tickfont=dict(size=11, color="#44403C", family="Noto Sans KR"),
                                    gridcolor="rgba(91,79,207,0.07)"),
                ),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=20, b=20, l=45, r=45), height=265, showlegend=False,
            )
            st.markdown("<div class='label-sm' style='margin-bottom:3px;'>Big Five 성격 레이더 (BFI-44)</div>", unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)

            for t in traits_order:
                m = BFI_META[t]
                score = bfi.get(t, 0)
                if t == "N":
                    display_score = 100 - score
                    level = "안정" if score < 40 else "보통" if score < 60 else "민감"
                else:
                    display_score = score
                    level = "높음" if score >= 60 else "보통" if score >= 40 else "낮음"
                desc = m["high"] if score >= 50 else m["low"]
                st.markdown(f"""
                <div class="trait-wrap">
                  <div class="trait-header">
                    <span class="trait-name">{m['icon']} {m['name']}</span>
                    <span style="font-size:.72rem;font-weight:700;color:{m['color']};">{display_score}/100 · {level}</span>
                  </div>
                  <div class="trait-track">
                    <div class="trait-fill" style="width:{display_score}%;background:{m['color']};"></div>
                  </div>
                  <div class="trait-note">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

            # Quiz results summary
            qr = st.session_state.quiz_results
            quiz_cards = []
            if qr.get("temperament") and qr["temperament"] in TEMP_TYPES:
                tt = TEMP_TYPES[qr["temperament"]]
                quiz_cards.append(f"<span style='font-size:.85rem;'>{tt['icon']}</span> <b>{tt['name']}</b>")
            if qr.get("enneagram"):
                ei = next((e for e in ENNEA_ITEMS if e["type"] == qr["enneagram"]), None)
                if ei:
                    quiz_cards.append(f"<span style='font-size:.85rem;'>{ei['icon']}</span> {ei['type']}번 · <b>{ei['name']}</b>")
            if qr.get("stress") and qr["stress"] in STRESS_TYPES:
                st2 = STRESS_TYPES[qr["stress"]]
                quiz_cards.append(f"<span style='font-size:.85rem;'>{st2['icon']}</span> <b>{st2['name']}</b>")
            if quiz_cards:
                rows = "".join(f"<div style='font-size:.8rem;color:var(--t2);padding:4px 0;border-bottom:1px solid var(--border);'>{c}</div>" for c in quiz_cards)
                st.markdown(f"""
                <div class="card card-sm" style="margin-top:.3rem;">
                  <div class="label-sm" style="margin-bottom:7px;">탐색 테스트 결과</div>
                  {rows}
                </div>
                """, unsafe_allow_html=True)
        else:
            # Onboarding — no empty whitespace
            _steps2 = [
                ("🔬 성격 심층 진단 탭", "Big Five 검사 (BFI-44)", bool(pr.get("bfi"))),
                ("🔬 성격 심층 진단 탭", "애착 유형 검사 (ECR-R)", bool(pr.get("attachment"))),
                ("🔬 성격 심층 진단 탭", "핵심 가치 선택 (Schwartz)", bool(pr.get("values"))),
                ("🧩 심리 탐색 테스트 탭", "기질 나침반 검사", bool(st.session_state.quiz_results.get("temperament"))),
                ("🧩 심리 탐색 테스트 탭", "에니어그램 핵심 유형", bool(st.session_state.quiz_results.get("enneagram"))),
                ("🧩 심리 탐색 테스트 탭", "나의 스트레스 패턴", bool(st.session_state.quiz_results.get("stress"))),
            ]
            _d2 = sum(1 for *_, done in _steps2 if done)
            _p2 = int(_d2 / len(_steps2) * 100)
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#F4F1FF,#EEE9FF);border:1px solid #C9C0F0;
                        border-radius:14px;padding:1.3rem 1.4rem;margin-bottom:.8rem;">
              <div class="label-sm" style="color:var(--indigo);margin-bottom:6px;">PROFILE COMPLETION</div>
              <div style="font-size:2rem;font-weight:900;color:var(--t1);letter-spacing:-.05em;line-height:1;">{_p2}<span style="font-size:.9rem;font-weight:700;">%</span></div>
              <div style="background:rgba(91,79,207,.15);border-radius:999px;height:5px;margin:8px 0;">
                <div style="width:{_p2}%;height:100%;background:var(--indigo);border-radius:999px;"></div>
              </div>
              <div style="font-size:.76rem;color:var(--indigo-dark);">{_d2}/{len(_steps2)}개 검사 완료 — 검사를 완료할수록 AI 상담이 정확해집니다</div>
            </div>
            """, unsafe_allow_html=True)
            _last_tab = ""
            for tab_label, test_name, is_done in _steps2:
                if tab_label != _last_tab:
                    st.markdown(f"<div class='label-sm' style='margin:{('1rem' if _last_tab else '.3rem')} 0 5px;'>{tab_label}</div>", unsafe_allow_html=True)
                    _last_tab = tab_label
                _chip = "<span class='chip chip-sage' style='font-size:.6rem;margin-left:auto;'>완료</span>" if is_done else "<span class='chip chip-amber' style='font-size:.6rem;margin-left:auto;'>미완료</span>"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:9px;padding:6px 10px;background:var(--surface);
                            border:1px solid var(--border);border-radius:9px;margin-bottom:5px;">
                  <span style="font-size:.8rem;">{'✅' if is_done else '⬜'}</span>
                  <span style="font-size:.82rem;color:{'var(--t1)' if is_done else 'var(--t2)'};">{test_name}</span>
                  {_chip}
                </div>
                """, unsafe_allow_html=True)

    # ── AI 심층 분석 ──
    bfi = pr.get("bfi", {})
    if bfi or pr.get("attachment"):
        st.markdown("<div style='height:.4rem;'></div>", unsafe_allow_html=True)
        ai_c1, ai_c2 = st.columns([5, 2])
        with ai_c1:
            st.markdown("<div class='sec-title' style='margin-bottom:2px;'>AI 심층 성격 분석</div>", unsafe_allow_html=True)
            st.markdown("<div class='sec-sub'>임상심리학적 관점에서 나의 성격 데이터를 종합적으로 해석합니다</div>", unsafe_allow_html=True)
        with ai_c2:
            if st.button("◎  분석 생성", type="primary", key="gen_summary", use_container_width=True):
                with st.spinner("분석 중 (약 10~15초)..."):
                    prompt = (
                        "내담자의 Big Five 성격 프로파일과 애착 유형, 가치관 데이터를 바탕으로 "
                        "임상 심리학적 관점에서 심층 분석을 해주세요.\n\n"
                        "다음을 포함해 전문적이면서도 따뜻한 어조로 400~500자 내외로 작성하세요:\n"
                        "1. 핵심 성격 패턴 및 강점\n2. 대인관계 및 감정 처리 방식\n"
                        "3. 스트레스 반응 예측 패턴\n4. 심리적 성장을 위한 구체적 방향\n"
                        "5. 내담자에게 가장 도움이 될 상담 접근법\n\n"
                        "전문적 용어를 사용하되, 이해하기 쉽게 설명해 주세요."
                    )
                    res = call_gpt([{"role":"user","content":prompt}],
                                   system=build_system_prompt(), tokens=700)
                st.session_state.data["profile"]["ai_summary"] = res
                save_data(st.session_state.data)
                st.rerun()
        if pr.get("ai_summary"):
            st.markdown(f"""
            <div style="background:var(--surface);border:1px solid var(--border);border-left:3px solid var(--indigo);
                        border-radius:12px;padding:1.1rem 1.3rem;margin-top:.6rem;line-height:1.85;
                        font-size:.88rem;color:var(--t2);box-shadow:var(--sh-sm);">
              {pr["ai_summary"]}
            </div>
            """, unsafe_allow_html=True)

    # ── AI 오늘의 성장 미션 ──
    st.markdown("<div style='height:.6rem;'></div>", unsafe_allow_html=True)
    mission_date = str(date.today())
    saved_mission = pr.get("daily_mission", {})
    mission_text  = saved_mission.get("text", "") if saved_mission.get("date") == mission_date else ""

    mis_c1, mis_c2 = st.columns([5, 2])
    with mis_c1:
        st.markdown("<div class='sec-title' style='margin-bottom:2px;'>🎯 오늘의 성장 미션</div>", unsafe_allow_html=True)
        st.markdown("<div class='sec-sub'>나의 심리 프로필에 맞춘 오늘 실천할 수 있는 작은 미션</div>", unsafe_allow_html=True)
    with mis_c2:
        if st.button("✨  미션 생성", type="primary", key="gen_mission", use_container_width=True):
            with st.spinner("소이가 미션을 만드는 중..."):
                res_m = call_gpt(
                    [{"role":"user","content":(
                        "내담자의 성격 프로파일, 애착 유형, 가치관 데이터를 바탕으로 "
                        "오늘 하루 실천할 수 있는 구체적인 심리 성장 미션 1가지를 만들어 주세요.\n\n"
                        "형식:\n"
                        "• 미션 제목 (10자 이내)\n"
                        "• 구체적 실천 방법 (2~3문장)\n"
                        "• 이 미션이 왜 도움이 되는지 한 문장\n\n"
                        "오늘 날짜 기준으로 일상에서 쉽게 할 수 있는 것으로 부탁드립니다."
                    )}],
                    system=build_system_prompt(), tokens=300,
                )
            st.session_state.data["profile"]["daily_mission"] = {"date": mission_date, "text": res_m}
            save_data(st.session_state.data)
            st.rerun()

    if mission_text:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#FFFBEB,#FEF3C7);border:1px solid #FDE68A;
                    border-left:3px solid var(--amber);border-radius:12px;
                    padding:1rem 1.2rem;margin-top:.6rem;line-height:1.8;
                    font-size:.88rem;color:var(--t2);">
          {mission_text.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
    elif not (pr.get("bfi") or pr.get("attachment")):
        st.markdown("""
        <div style="padding:.7rem 1rem;background:var(--bg2);border-radius:9px;
                    border:1px solid var(--border);margin-top:.5rem;">
          <span style="font-size:.78rem;color:var(--t4);">💡 성격 심층 진단을 먼저 완료하면 더 맞춤화된 미션이 생성됩니다.</span>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TAB 2 · AI COUNSELING CHAT
# ═══════════════════════════════════════════════════════════════
with T2:
    st.markdown("""
    <div style="margin-bottom:.6rem;">
      <div class="page-eyebrow">AI 심리 상담</div>
      <div style="font-family:'Lora',serif;font-size:1.3rem;font-weight:600;color:var(--t1);letter-spacing:-.02em;margin-bottom:2px;">소이와 대화하기</div>
      <div style="font-size:.78rem;color:var(--t3);">CBT·인간중심치료·애착 이론 기반 AI 상담사 &nbsp;·&nbsp; 진단을 제공하지 않습니다</div>
    </div>
    """, unsafe_allow_html=True)

    # Chat window
    msgs = st.session_state.msgs
    now  = date.today().strftime("%H:%M")

    st.markdown("<div class='chat-outer'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="chat-header">
      <div class="chat-av-wrap">소이</div>
      <div>
        <div style="font-size:.87rem;font-weight:700;color:var(--t1);">소이 (Soi)</div>
        <div style="font-size:.71rem;color:var(--t3);">임상심리 기반 AI 상담사 · CBT, 애착 이론, 인간중심치료</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='chat-body'>", unsafe_allow_html=True)
        st.markdown("<div class='chat-msgs'>", unsafe_allow_html=True)

        if not msgs:
            st.markdown("""
            <div style="text-align:center;padding:2rem 1rem;">
              <div style="font-size:1.8rem;margin-bottom:10px;">◎</div>
              <div style="font-size:.93rem;font-weight:600;color:var(--t2);margin-bottom:5px;">안녕하세요. 저는 소이예요.</div>
              <div style="font-size:.82rem;color:var(--t3);line-height:1.75;">
                무엇이든 편하게 이야기해 주세요.<br>
                성격, 관계, 감정, 반복되는 패턴 — 함께 탐구해 볼게요.<br>
                <span style="font-size:.72rem;background:#F7F5F0;border-radius:6px;padding:2px 8px;">
                  본 서비스는 의료 진단을 대체하지 않습니다
                </span>
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for m in msgs:
                if m["role"] == "user":
                    st.markdown(f"""
                    <div class="msg-row me">
                      <div class="msg-av me-av">😊</div>
                      <div>
                        <div class="msg-bubble me">{m["content"]}</div>
                        <div class="msg-time" style="text-align:right;">{now}</div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="msg-row">
                      <div class="msg-av ai-av">소이</div>
                      <div>
                        <div class="msg-bubble ai">{m["content"]}</div>
                        <div class="msg-time">{now}</div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:.5rem;'></div>", unsafe_allow_html=True)

    # Input row
    c_inp, c_btn = st.columns([9, 1])
    with c_inp:
        user_input = st.text_input("input", key=f"ci_{st.session_state.chat_k}",
                                   label_visibility="collapsed",
                                   placeholder="소이에게 이야기해 보세요...")
    with c_btn:
        send = st.button("전송", type="primary", use_container_width=True)

    if send and user_input.strip():
        st.session_state.msgs.append({"role":"user","content":user_input.strip()})
        with st.spinner("소이가 응답 중..."):
            reply = call_gpt(st.session_state.msgs, system=build_system_prompt(), tokens=500)
        st.session_state.msgs.append({"role":"assistant","content":reply})
        st.session_state.data["messages"] = st.session_state.msgs
        save_data(st.session_state.data)
        st.session_state.chat_k += 1
        st.rerun()

    # Quick prompts
    st.markdown("""
    <div style="margin-top:.8rem;">
      <div class="label-sm" style="margin-bottom:7px;">자주 하는 질문</div>
    </div>
    """, unsafe_allow_html=True)

    qr1, qr2, qr3 = st.columns(3)
    qr_cols = [qr1, qr2, qr3, qr1, qr2, qr3]
    for col, qp in zip(qr_cols, COUNSELING_QUICK):
        with col:
            if st.button(qp, key=f"qbtn_{qp}", use_container_width=True):
                st.session_state.msgs.append({"role":"user","content":qp})
                with st.spinner("소이가 응답 중..."):
                    reply = call_gpt(st.session_state.msgs, system=build_system_prompt(), tokens=500)
                st.session_state.msgs.append({"role":"assistant","content":reply})
                st.session_state.data["messages"] = st.session_state.msgs
                save_data(st.session_state.data)
                st.rerun()

    # Disclaimer
    st.markdown("""
    <div style="margin-top:1rem;padding:.7rem 1rem;background:var(--bg2);border-radius:9px;border:1px solid var(--border);">
      <span style="font-size:.71rem;color:var(--t4);">
        ⚕️ <b>전문적 도움이 필요하다면:</b>
        정신건강 위기상담 1577-0199 · 자살예방상담전화 1393 · 청소년 상담 1388
      </span>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TAB 3 · CLINICAL ASSESSMENTS
# ═══════════════════════════════════════════════════════════════
with T3:
    st.markdown("""
    <div style="margin-bottom:1.8rem;">
      <div class="page-eyebrow">임상 심리 진단 도구</div>
      <div class="page-title">성격 심층 진단</div>
      <div class="page-desc">
        국제 학술지에 검증된 척도를 사용합니다. 각 검사를 완료할수록 AI 상담사의 이해도가 높아집니다.<br>
        <span style="font-size:.73rem;font-weight:700;background:var(--indigo-lt);color:var(--indigo-dark);padding:2px 9px;border-radius:5px;">BFI-44</span>&nbsp;
        <span style="font-size:.73rem;font-weight:700;background:var(--indigo-lt);color:var(--indigo-dark);padding:2px 9px;border-radius:5px;">ECR-R</span>&nbsp;
        <span style="font-size:.73rem;font-weight:700;background:var(--indigo-lt);color:var(--indigo-dark);padding:2px 9px;border-radius:5px;">Schwartz Values</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    S1, S2, S3 = st.tabs([
        "🧠  Big Five (BFI-44)",
        "💞  애착 유형 (ECR-R)",
        "✦  핵심 가치 (Schwartz)",
    ])

    # ─── BFI ─────────────────────────────────────────────────
    with S1:
        bfi_done = bool(st.session_state.data["profile"].get("bfi"))
        bfi_data = st.session_state.data["profile"].get("bfi", {})

        # ── Info header ──
        st.markdown(f"""
        <div class="card card-inset" style="margin-bottom:1.3rem;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;">
            <div>
              <div class="sec-title">Big Five Inventory (BFI-44)</div>
              <div class="sec-sub" style="margin-top:4px;">
                John &amp; Srivastava (1999)의 BFI-44 기반 단축형 자기 보고식 검사입니다.<br>
                총 20문항 · 개방성(O) · 성실성(C) · 외향성(E) · 친화성(A) · 신경증(N) 측정
              </div>
            </div>
            {'<span class="chip chip-sage">✓ 완료</span>' if bfi_done else '<span class="chip chip-amber">검사 필요</span>'}
          </div>
          <div style="margin-top:12px;padding:.55rem .9rem;background:var(--bg2);border-radius:8px;border:1px solid var(--border);">
            <div style="font-size:.68rem;font-weight:700;color:var(--t4);margin-bottom:5px;">응답 척도</div>
            <div style="display:flex;justify-content:space-between;font-size:.71rem;color:var(--t2);font-weight:500;">
              <span>❶ 전혀 아니다</span><span>❷ 아닌 편이다</span><span>❸ 보통이다</span><span>❹ 그런 편이다</span><span>❺ 매우 그렇다</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("bfi_form", clear_on_submit=False):
            bfi_ans = {}
            cur_trait = None
            for idx, (trait, reverse, text) in enumerate(BFI_ITEMS):
                m = BFI_META[trait]
                if trait != cur_trait:
                    top_m = "1.6rem" if cur_trait else ".2rem"
                    cnt = sum(1 for t2, _, __ in BFI_ITEMS if t2 == trait)
                    st.markdown(f"""
                    <div style="margin:{top_m} 0 .7rem;display:flex;align-items:center;gap:9px;
                                padding:.48rem .9rem;background:var(--bg2);border-radius:9px;
                                border-left:3px solid {m['color']};">
                      <span style="font-size:.95rem;">{m['icon']}</span>
                      <span style="font-size:.82rem;font-weight:700;color:{m['color']};">{m['name']}</span>
                      <span style="font-size:.68rem;color:var(--t4);margin-left:auto;">{cnt}문항</span>
                    </div>
                    """, unsafe_allow_html=True)
                    cur_trait = trait
                rev_tag = ' <span style="font-size:.6rem;background:#FEF3C7;color:#92400E;border-radius:4px;padding:1px 5px;font-weight:700;">역채점</span>' if reverse else ''
                st.markdown(f"""
                <div class="q-item">
                  <div style="display:flex;align-items:center;gap:5px;margin-bottom:3px;">
                    <span class="q-label" style="margin-bottom:0;">Q{idx+1:02d}</span>{rev_tag}
                  </div>
                  <div class="q-text">{text}</div>
                </div>
                """, unsafe_allow_html=True)
                bfi_ans[idx] = st.slider(
                    f"q{idx}", 1, 5, 3,
                    key=f"bfi_{idx}",
                    format="%d",
                    label_visibility="collapsed",
                )

            st.markdown("<div style='height:.4rem;'></div>", unsafe_allow_html=True)
            if st.form_submit_button("검사 완료 및 결과 분석하기  →", use_container_width=True):
                result = score_bfi(bfi_ans)
                st.session_state.data["profile"]["bfi"] = result
                save_data(st.session_state.data)
                st.session_state.bfi_submitted = True
                st.rerun()

        # ── Completion result card ──
        if bfi_done:
            st.markdown("<div style='height:.8rem;'></div>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background:linear-gradient(135deg,#ECFDF5,#D1FAE5);border:1.5px solid #6EE7B7;
                        border-radius:14px;padding:1.3rem 1.5rem;margin-bottom:1.2rem;">
              <div style="font-size:1rem;font-weight:800;color:#065F46;margin-bottom:5px;">✅ Big Five 검사가 완료되었습니다</div>
              <div style="font-size:.83rem;color:#047857;line-height:1.7;">
                성격 5요인 프로파일이 저장되었습니다. <b>내 심리 프로필</b> 탭에서 레이더 차트와 심층 해석을 확인하세요.<br>
                다음 단계로 <b>애착 유형 검사 (ECR-R)</b>를 완료하면 더 정밀한 AI 상담이 가능해집니다.
              </div>
            </div>
            """, unsafe_allow_html=True)
            traits_order = ["O", "C", "E", "A", "N"]
            r_cols = st.columns(5, gap="small")
            for rc, t in zip(r_cols, traits_order):
                m = BFI_META[t]
                score  = bfi_data.get(t, 0)
                dscore = (100 - score) if t == "N" else score
                lvl    = ("안정" if score < 40 else "보통" if score < 60 else "민감") if t == "N" \
                         else ("낮음" if score < 40 else "보통" if score < 60 else "높음")
                with rc:
                    st.markdown(f"""
                    <div style="background:white;border:1px solid var(--border);border-top:3px solid {m['color']};
                                border-radius:11px;padding:.8rem .5rem;text-align:center;box-shadow:var(--sh-sm);">
                      <div style="font-size:1.05rem;">{m['icon']}</div>
                      <div style="font-size:.67rem;font-weight:700;color:{m['color']};margin-top:3px;">{m['ko']}</div>
                      <div style="font-size:1.2rem;font-weight:900;color:var(--t1);line-height:1.2;margin-top:2px;">{dscore}</div>
                      <div style="font-size:.63rem;color:var(--t3);margin-top:1px;">{lvl}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ─── ECR ─────────────────────────────────────────────────
    with S2:
        att_done = bool(st.session_state.data["profile"].get("attachment"))
        att_key  = st.session_state.data["profile"].get("attachment")

        # ── Info header ──
        st.markdown(f"""
        <div class="card card-inset" style="margin-bottom:1.2rem;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;">
            <div>
              <div class="sec-title">애착 유형 검사 (ECR-R)</div>
              <div class="sec-sub" style="margin-top:4px;">
                Fraley et al. (2000)의 ECR-R 기반 8문항 검사입니다.<br>
                불안(Anxiety) · 회피(Avoidance) 두 축으로 4가지 애착 유형을 도출합니다.<br>
                <b>현재 삶에서 가장 가까운 한 사람을 구체적으로 떠올리며</b> 솔직하게 응답해 주세요.
              </div>
            </div>
            {'<span class="chip chip-sage">✓ 완료</span>' if att_done else '<span class="chip chip-amber">검사 필요</span>'}
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Attachment type reference
        st.markdown("<div class='label-sm' style='margin-bottom:8px;'>애착 유형 분류 체계 (Bowlby–Ainsworth 모델)</div>", unsafe_allow_html=True)
        ac1, ac2, ac3, ac4 = st.columns(4, gap="small")
        for col, (k, v) in zip([ac1, ac2, ac3, ac4], ATTACHMENT_TYPES.items()):
            is_cur = att_key == k
            with col:
                cur_border = f"background:linear-gradient(135deg,{v['color']}12,{v['color']}05);border-color:{v['color']};" if is_cur else ""
                st.markdown(f"""
                <div class="att-card" style="border-top:3px solid {v['color']};{cur_border}">
                  <div style="font-size:1.35rem;margin-bottom:5px;">{v["icon"]}</div>
                  <div style="font-size:.82rem;font-weight:700;color:var(--t1);margin-bottom:4px;">{v["name"]}</div>
                  <div style="font-size:.7rem;color:var(--t3);line-height:1.5;">{v["therapy"][:50]}…</div>
                  {'<div style="margin-top:6px;"><span class="chip chip-sage" style="font-size:.6rem;">현재 나의 유형</span></div>' if is_cur else ''}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:.6rem;'></div>", unsafe_allow_html=True)

        with st.form("ecr_form", clear_on_submit=False):
            ecr_ans = {}
            st.markdown("""
            <div style="display:flex;gap:10px;margin-bottom:1rem;flex-wrap:wrap;">
              <div style="padding:.4rem .9rem;background:#EFF6FF;border-radius:8px;font-size:.74rem;font-weight:700;color:#0369A1;">
                🔵 AX · 불안 축도 &nbsp;—&nbsp; 거절·버림받음에 대한 두려움
              </div>
              <div style="padding:.4rem .9rem;background:#FFFBEB;border-radius:8px;font-size:.74rem;font-weight:700;color:#D97706;">
                🟡 AV · 회피 축도 &nbsp;—&nbsp; 친밀감·의존에 대한 불편감
              </div>
            </div>
            <div style="padding:.5rem .85rem;background:var(--bg2);border-radius:8px;margin-bottom:1rem;font-size:.7rem;color:var(--t3);">
              응답 척도: <b>1</b>&nbsp;전혀 아니다 &nbsp;·&nbsp; <b>2</b>&nbsp;아닌 편이다 &nbsp;·&nbsp; <b>3</b>&nbsp;보통이다 &nbsp;·&nbsp; <b>4</b>&nbsp;그런 편이다 &nbsp;·&nbsp; <b>5</b>&nbsp;매우 그렇다
            </div>
            """, unsafe_allow_html=True)
            for idx, (dim, text) in enumerate(ECR_ITEMS):
                dim_name  = "AX · 불안" if dim == "AX" else "AV · 회피"
                dim_color = "#0369A1"  if dim == "AX" else "#D97706"
                dim_bg    = "#EFF6FF"  if dim == "AX" else "#FFFBEB"
                st.markdown(f"""
                <div class="q-item" style="border-left:3px solid {dim_color};">
                  <div style="display:flex;align-items:center;gap:7px;margin-bottom:4px;">
                    <span class="q-label" style="color:{dim_color};margin-bottom:0;">Q{idx+1:02d}</span>
                    <span style="font-size:.65rem;background:{dim_bg};color:{dim_color};border-radius:5px;padding:1px 7px;font-weight:700;">{dim_name}</span>
                  </div>
                  <div class="q-text">{text}</div>
                </div>
                """, unsafe_allow_html=True)
                ecr_ans[idx] = st.slider(
                    f"ecr_q{idx}", 1, 5, 3, key=f"ecr_{idx}",
                    format="%d",
                    label_visibility="collapsed",
                )

            st.markdown("<div style='height:.4rem;'></div>", unsafe_allow_html=True)
            if st.form_submit_button("애착 유형 확인하기  →", use_container_width=True):
                att_result = score_ecr(ecr_ans)
                st.session_state.data["profile"]["attachment"] = att_result
                save_data(st.session_state.data)
                st.session_state.ecr_submitted = True
                st.rerun()

        # ── Completion result card ──
        if att_done and att_key in ATTACHMENT_TYPES:
            at = ATTACHMENT_TYPES[att_key]
            st.markdown("<div style='height:.8rem;'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#ECFDF5,#D1FAE5);border:1.5px solid #6EE7B7;
                        border-radius:14px;padding:1.3rem 1.5rem;margin-bottom:1rem;">
              <div style="font-size:1rem;font-weight:800;color:#065F46;margin-bottom:5px;">✅ 애착 유형 검사가 완료되었습니다</div>
              <div style="font-size:.83rem;color:#047857;">아래에서 나의 애착 유형과 성장 방향을 확인하세요.</div>
            </div>
            <div class="card card-sm" style="border-left:4px solid {at['color']};margin-bottom:1.3rem;">
              <div style="display:flex;align-items:flex-start;gap:14px;">
                <div style="font-size:2.4rem;flex-shrink:0;margin-top:3px;">{at['icon']}</div>
                <div style="flex:1;">
                  <div style="font-size:1.05rem;font-weight:800;color:var(--t1);margin-bottom:7px;">{at['name']}</div>
                  <div style="font-size:.83rem;color:var(--t2);line-height:1.72;margin-bottom:10px;">{at['summary']}</div>
                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">
                    <div style="padding:.6rem .75rem;background:var(--sage-lt);border-radius:9px;border:1px solid #A5D6B4;">
                      <div class="label-sm" style="margin-bottom:3px;color:var(--sage);">강점</div>
                      <div style="font-size:.76rem;color:var(--t2);line-height:1.55;">{at['strength']}</div>
                    </div>
                    <div style="padding:.6rem .75rem;background:var(--amber-lt);border-radius:9px;border:1px solid #F0D080;">
                      <div class="label-sm" style="margin-bottom:3px;color:var(--amber);">성장 방향</div>
                      <div style="font-size:.76rem;color:var(--t2);line-height:1.55;">{at['growth']}</div>
                    </div>
                  </div>
                  <div style="padding:.6rem .75rem;background:var(--indigo-lt);border-radius:9px;">
                    <div class="label-sm" style="margin-bottom:3px;color:var(--indigo);">권장 상담 접근법</div>
                    <div style="font-size:.76rem;color:var(--indigo-dark);line-height:1.55;">{at['therapy']}</div>
                  </div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ─── VALUES ──────────────────────────────────────────────
    with S3:
        cur_vals = st.session_state.data["profile"].get("values", [])

        st.markdown("""
        <div class="card card-inset" style="margin-bottom:1.4rem;">
          <div class="sec-title">핵심 가치 탐구 (Schwartz Basic Values Theory)</div>
          <div class="sec-sub" style="margin-top:6px;">
            Schwartz(1992)의 보편적 가치 이론은 10개 동기적 범주에 걸친 29개 보편 가치를 체계화합니다.<br>
            현재 삶에서 가장 중요하게 느껴지는 가치를 <b>최대 7개</b> 선택하세요.
            선택한 가치는 AI 상담사 '소이'의 내담자 이해를 위한 핵심 맥락 자료가 됩니다.
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Selected values summary
        if cur_vals:
            chips_html = "".join(f"<span class='chip chip-indigo'>{v}</span>" for v in cur_vals)
            at_max = len(cur_vals) >= 7
            st.markdown(f"""
            <div class="card card-sage" style="margin-bottom:1.3rem;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <div class="label-sm">현재 선택된 가치관</div>
                <span style="font-size:.83rem;font-weight:800;color:var(--sage);">{len(cur_vals)} / 7</span>
              </div>
              {chips_html}
              {'<div style="margin-top:8px;font-size:.72rem;color:var(--sage);font-weight:600;">최대 선택 수에 도달했습니다. 선택을 해제하려면 해당 항목을 다시 클릭하세요.</div>' if at_max else ''}
            </div>
            """, unsafe_allow_html=True)

        # Per-category value grid — FIXED 3-column layout for all groups
        VAL_COLORS = {
            "자기 방향": "#5B4FCF", "자극": "#0369A1", "쾌락주의": "#D97706",
            "성취": "#059669",     "권력": "#BE123C", "안전": "#7C3AED",
            "동조": "#0891B2",     "전통": "#92400E", "박애": "#047857",
            "보편성": "#065F46",
        }

        for group_name, group_vals in SCHWARTZ_VALUES.items():
            gc = VAL_COLORS.get(group_name, "#5B4FCF")
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:1.1rem 0 6px;">
              <div style="width:3px;height:14px;background:{gc};border-radius:2px;flex-shrink:0;"></div>
              <span style="font-size:.72rem;font-weight:700;color:{gc};letter-spacing:.07em;">{group_name}</span>
            </div>
            """, unsafe_allow_html=True)

            col_a, col_b, col_c = st.columns(3, gap="small")
            col_map = [col_a, col_b, col_c]

            for i, v in enumerate(group_vals):
                is_sel  = v in cur_vals
                btn_lbl = ("✓  " if is_sel else "") + v
                safe_k  = "val_" + v.replace(" ", "_")
                btn_type = "primary" if is_sel else "secondary"
                with col_map[i]:
                    if st.button(btn_lbl, key=safe_k, use_container_width=True, type=btn_type):
                        new_vals = list(cur_vals)
                        if v in new_vals:
                            new_vals.remove(v)
                            st.session_state.data["profile"]["values"] = new_vals
                            save_data(st.session_state.data)
                            st.rerun()
                        elif len(new_vals) < 7:
                            new_vals.append(v)
                            st.session_state.data["profile"]["values"] = new_vals
                            save_data(st.session_state.data)
                            st.rerun()
                        else:
                            st.toast("최대 7개까지 선택할 수 있습니다. 기존 항목을 취소 후 선택해 주세요.", icon="⚠️")


# ═══════════════════════════════════════════════════════════════
# TAB 4 · PSYCHOLOGY QUIZ TESTS
# ═══════════════════════════════════════════════════════════════
with T4:
    st.markdown("""
    <div style="margin-bottom:1.6rem;">
      <div class="page-eyebrow">심리 탐색 테스트</div>
      <div class="page-title">나를 더 깊이 탐구하기</div>
      <div class="page-desc">
        유행하는 심리 테스트부터 임상심리학 기반 기질 검사까지 — 버튼 하나로 빠르게 나를 알아가세요.<br>
        완료할수록 AI 상담사 <b>소이</b>의 이해도가 높아집니다.
      </div>
    </div>
    """, unsafe_allow_html=True)

    Q1, Q2, Q3 = st.tabs([
        "🧭  기질 나침반 (12Q)",
        "🔢  에니어그램 (9Q)",
        "⚡  스트레스 패턴 (10Q)",
    ])

    def _quiz_progress(prefix, total):
        answered = sum(1 for i in range(total) if f"{prefix}{i}" in st.session_state.quiz_answers)
        pct = answered / total if total else 0
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
                    margin:.9rem 0 .3rem;padding:.6rem .9rem;background:var(--bg2);border-radius:9px;">
          <span style="font-size:.78rem;color:var(--t3);">진행률 <b style="color:var(--t1);">{answered}</b> / {total}</span>
          <div style="width:{int(pct*160)}px;max-width:160px;height:4px;background:var(--indigo);border-radius:4px;transition:width .3s;"></div>
        </div>
        """, unsafe_allow_html=True)
        return answered == total

    # ─── TEMPERAMENT ──────────────────────────────────────────
    with Q1:
        temp_result = st.session_state.quiz_results.get("temperament")

        st.markdown("""
        <div class="card card-inset" style="margin-bottom:1.2rem;">
          <div class="sec-title">기질 나침반 (Keirsey Temperament Sorter 기반)</div>
          <div class="sec-sub" style="margin-top:5px;">
            Keirsey(1998)의 4기질 이론에 기반한 12문항 검사입니다.<br>
            각 질문에서 <b>지금 나에게 가장 자연스럽게 느껴지는 선택지 하나</b>를 눌러주세요.
          </div>
        </div>
        """, unsafe_allow_html=True)

        for q_idx, q in enumerate(TEMP_Q):
            curr = st.session_state.quiz_answers.get(f"temp_q{q_idx}")
            done_flag = curr is not None
            st.markdown(f"""
            <div style="background:var(--surface2);border:1px solid {'var(--indigo)' if done_flag else 'var(--border)'};
                        {'border-left:3px solid var(--indigo);' if done_flag else ''}
                        border-radius:12px;padding:.85rem 1.1rem .45rem;margin-bottom:.65rem;">
              <div style="display:flex;gap:8px;align-items:center;margin-bottom:.4rem;">
                <span style="font-size:.65rem;font-weight:800;color:{'var(--indigo)' if done_flag else 'var(--t4)'};">Q{q_idx+1:02d}</span>
                {"<span style='font-size:.6rem;background:var(--indigo-lt);color:var(--indigo);border-radius:4px;padding:1px 6px;font-weight:700;'>✓</span>" if done_flag else ""}
              </div>
              <div style="font-size:.9rem;font-weight:600;color:var(--t1);line-height:1.4;margin-bottom:.5rem;">{q['text']}</div>
            </div>
            """, unsafe_allow_html=True)
            btn_cols = st.columns(2, gap="small")
            for opt_idx, opt_txt in enumerate(q["opts"]):
                is_sel = curr == opt_idx
                with btn_cols[opt_idx % 2]:
                    if st.button(opt_txt, key=f"temp_q{q_idx}_o{opt_idx}",
                                 type="primary" if is_sel else "secondary",
                                 use_container_width=True):
                        st.session_state.quiz_answers[f"temp_q{q_idx}"] = opt_idx
                        st.rerun()

        all_done = _quiz_progress("temp_q", len(TEMP_Q))
        if all_done and not temp_result:
            if st.button("✨  기질 유형 결과 확인", type="primary", use_container_width=True, key="submit_temp"):
                counts = {"SJ": 0, "SP": 0, "NF": 0, "NT": 0}
                for i, q in enumerate(TEMP_Q):
                    ans = st.session_state.quiz_answers.get(f"temp_q{i}")
                    if ans is not None:
                        counts[q["keys"][ans]] += 1
                st.session_state.quiz_results["temperament"] = max(counts, key=counts.get)
                st.session_state.data.setdefault("quiz_results", {})["temperament"] = st.session_state.quiz_results["temperament"]
                save_data(st.session_state.data)
                st.rerun()
        elif not all_done:
            remaining = len(TEMP_Q) - sum(1 for i in range(len(TEMP_Q)) if f"temp_q{i}" in st.session_state.quiz_answers)
            st.markdown(f"<div style='text-align:center;font-size:.75rem;color:var(--t4);padding:.4rem;'>{remaining}문항이 남았습니다</div>", unsafe_allow_html=True)

        if temp_result and temp_result in TEMP_TYPES:
            tt = TEMP_TYPES[temp_result]
            st.markdown("<div style='height:.6rem;'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card" style="border-left:4px solid {tt['color']};margin-bottom:1.3rem;">
              <div style="display:flex;align-items:flex-start;gap:14px;">
                <div style="font-size:2.5rem;flex-shrink:0;margin-top:2px;">{tt['icon']}</div>
                <div style="flex:1;">
                  <div class="label-sm" style="color:{tt['color']};margin-bottom:4px;">나의 기질 유형 · Keirsey</div>
                  <div style="font-size:1.05rem;font-weight:800;color:var(--t1);margin-bottom:4px;">{tt['name']}</div>
                  <div style="font-size:.73rem;color:var(--t4);margin-bottom:8px;">{tt['population']} · {tt['core']}</div>
                  <div style="font-size:.86rem;color:var(--t2);line-height:1.8;margin-bottom:10px;white-space:pre-line;">{tt['detail']}</div>
                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">
                    <div style="padding:.55rem .7rem;background:var(--sage-lt);border-radius:9px;">
                      <div class="label-sm" style="color:var(--sage);margin-bottom:3px;">강점</div>
                      <div style="font-size:.74rem;color:var(--t2);line-height:1.55;">{tt['strength']}</div>
                    </div>
                    <div style="padding:.55rem .7rem;background:var(--amber-lt);border-radius:9px;">
                      <div class="label-sm" style="color:var(--amber);margin-bottom:3px;">성장 방향</div>
                      <div style="font-size:.74rem;color:var(--t2);line-height:1.55;">{tt['growth']}</div>
                    </div>
                  </div>
                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">
                    <div style="padding:.55rem .7rem;background:#ECFDF5;border-radius:9px;border:1px solid #A5D6B4;">
                      <div class="label-sm" style="color:var(--sage);margin-bottom:3px;">✅ 잘 맞는 유형</div>
                      <div style="font-size:.82rem;font-weight:700;color:var(--t1);margin-bottom:3px;">{" / ".join(TEMP_TYPES[k]["icon"] + " " + TEMP_TYPES[k]["name"] for k in tt["compatible"]["best"])}</div>
                      <div style="font-size:.72rem;color:var(--t2);line-height:1.55;">{tt["compatible_desc"]["best"]}</div>
                    </div>
                    <div style="padding:.55rem .7rem;background:#FFF1F2;border-radius:9px;border:1px solid #FECDD3;">
                      <div class="label-sm" style="color:var(--rose);margin-bottom:3px;">⚡ 주의가 필요한 유형</div>
                      <div style="font-size:.82rem;font-weight:700;color:var(--t1);margin-bottom:3px;">{" / ".join(TEMP_TYPES[k]["icon"] + " " + TEMP_TYPES[k]["name"] for k in tt["compatible"]["challenging"])}</div>
                      <div style="font-size:.72rem;color:var(--t2);line-height:1.55;">{tt["compatible_desc"]["challenging"]}</div>
                    </div>
                  </div>
                  <div style="padding:.45rem .7rem;background:var(--indigo-lt);border-radius:8px;">
                    <span class="label-sm" style="color:var(--indigo);">유사 MBTI:</span>
                    <span style="font-size:.77rem;color:var(--indigo-dark);font-weight:700;margin-left:6px;">{tt['similar']}</span>
                  </div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # 다른 유형 모두 보기
            st.markdown("<div class='label-sm' style='margin:1rem 0 8px;'>다른 기질 유형 살펴보기</div>", unsafe_allow_html=True)
            other_types = {k: v for k, v in TEMP_TYPES.items() if k != temp_result}
            other_cols = st.columns(len(other_types), gap="small")
            for col_o, (k, v) in zip(other_cols, other_types.items()):
                with col_o:
                    st.markdown(f"""
                    <div style="background:var(--surface);border:1px solid var(--border);border-top:3px solid {v['color']};
                                border-radius:11px;padding:.8rem .7rem;text-align:center;">
                      <div style="font-size:1.3rem;">{v['icon']}</div>
                      <div style="font-size:.72rem;font-weight:700;color:{v['color']};margin:.3rem 0 .2rem;">{v['name']}</div>
                      <div style="font-size:.67rem;color:var(--t4);margin-bottom:.4rem;">{v['population']}</div>
                      <div style="font-size:.7rem;color:var(--t2);line-height:1.5;text-align:left;">{v['desc']}</div>
                      <div style="margin-top:.5rem;padding:.35rem .5rem;background:var(--bg2);border-radius:7px;font-size:.67rem;color:var(--t3);">{v['similar']}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<div style='height:.5rem;'></div>", unsafe_allow_html=True)
            if st.button("🔄  기질 나침반 다시 하기", key="retry_temp", use_container_width=True):
                for k in [k for k in st.session_state.quiz_answers if k.startswith("temp_")]:
                    del st.session_state.quiz_answers[k]
                del st.session_state.quiz_results["temperament"]
                st.session_state.data.setdefault("quiz_results", {}).pop("temperament", None)
                save_data(st.session_state.data)
                st.rerun()

    # ─── ENNEAGRAM ────────────────────────────────────────────
    with Q2:
        ennea_result = st.session_state.quiz_results.get("enneagram")

        st.markdown("""
        <div class="card card-inset" style="margin-bottom:1.2rem;">
          <div class="sec-title">에니어그램 핵심 유형 (9Q)</div>
          <div class="sec-sub" style="margin-top:5px;">
            에니어그램은 9가지 핵심 동기와 두려움으로 성격을 분류하는 심리 체계입니다.<br>
            각 설명이 <b>나를 얼마나 잘 설명하는지</b> 솔직하게 선택해 주세요. (정답 없음)
          </div>
        </div>
        """, unsafe_allow_html=True)

        for e_idx, item in enumerate(ENNEA_ITEMS):
            curr_e = st.session_state.quiz_answers.get(f"ennea_{e_idx}")
            e_done = curr_e is not None
            st.markdown(f"""
            <div style="background:var(--surface2);border:1px solid {'var(--indigo)' if e_done else 'var(--border)'};
                        {'border-left:3px solid ' + item['color'] + ';' if e_done else ''}
                        border-radius:12px;padding:.8rem 1.1rem .45rem;margin-bottom:.6rem;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:.4rem;">
                <span style="font-size:1.05rem;">{item['icon']}</span>
                <span style="font-size:.72rem;font-weight:700;color:{item['color']};">{item['type']}번 · {item['name']}</span>
                {"<span style='font-size:.6rem;background:var(--indigo-lt);color:var(--indigo);border-radius:4px;padding:1px 6px;font-weight:700;'>✓</span>" if e_done else ""}
              </div>
              <div style="font-size:.87rem;color:var(--t1);line-height:1.55;font-style:italic;margin-bottom:.45rem;">"{item['text']}"</div>
            </div>
            """, unsafe_allow_html=True)
            e_cols = st.columns(3, gap="small")
            for oi, (col, opt) in enumerate(zip(e_cols, ENNEA_OPTS)):
                is_sel = curr_e == oi
                with col:
                    if st.button(opt, key=f"ennea_{e_idx}_o{oi}",
                                 type="primary" if is_sel else "secondary",
                                 use_container_width=True):
                        st.session_state.quiz_answers[f"ennea_{e_idx}"] = oi
                        st.rerun()

        all_done_e = _quiz_progress("ennea_", len(ENNEA_ITEMS))
        if all_done_e and not ennea_result:
            if st.button("✨  에니어그램 결과 확인", type="primary", use_container_width=True, key="submit_ennea"):
                type_scores = {e["type"]: 0 for e in ENNEA_ITEMS}
                for i, item in enumerate(ENNEA_ITEMS):
                    ans = st.session_state.quiz_answers.get(f"ennea_{i}")
                    if ans is not None:
                        type_scores[item["type"]] += ENNEA_SCORES[ans]
                st.session_state.quiz_results["enneagram"] = max(type_scores, key=type_scores.get)
                st.session_state.data.setdefault("quiz_results", {})["enneagram"] = st.session_state.quiz_results["enneagram"]
                save_data(st.session_state.data)
                st.rerun()
        elif not all_done_e:
            remaining_e = len(ENNEA_ITEMS) - sum(1 for i in range(len(ENNEA_ITEMS)) if f"ennea_{i}" in st.session_state.quiz_answers)
            st.markdown(f"<div style='text-align:center;font-size:.75rem;color:var(--t4);padding:.4rem;'>{remaining_e}문항이 남았습니다</div>", unsafe_allow_html=True)

        if ennea_result:
            ei = next((e for e in ENNEA_ITEMS if e["type"] == ennea_result), None)
            if ei:
                best_items = [e for e in ENNEA_ITEMS if e["type"] in ei["compatible"]["best"]]
                chal_items = [e for e in ENNEA_ITEMS if e["type"] in ei["compatible"]["challenging"]]
                best_html = "".join(
                    f'<div style="font-size:.78rem;font-weight:700;color:{e["color"]};margin-bottom:2px;">'
                    f'{e["icon"]} {e["type"]}번 {e["name"]}</div>'
                    for e in best_items
                )
                chal_html = "".join(
                    f'<div style="font-size:.78rem;font-weight:700;color:{e["color"]};margin-bottom:2px;">'
                    f'{e["icon"]} {e["type"]}번 {e["name"]}</div>'
                    for e in chal_items
                )
                st.markdown("<div style='height:.6rem;'></div>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class="card" style="border-left:4px solid {ei['color']};margin-bottom:1.3rem;">
                  <div style="display:flex;align-items:flex-start;gap:14px;">
                    <div style="font-size:2.6rem;flex-shrink:0;margin-top:2px;">{ei['icon']}</div>
                    <div style="flex:1;">
                      <div class="label-sm" style="color:{ei['color']};margin-bottom:4px;">에니어그램 {ei['type']}번 유형</div>
                      <div style="font-size:1.05rem;font-weight:800;color:var(--t1);margin-bottom:7px;">{ei['name']}</div>
                      <div style="font-size:.86rem;color:var(--t2);line-height:1.8;margin-bottom:10px;">{ei['detail']}</div>
                      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">
                        <div style="padding:.55rem .7rem;background:var(--rose-lt);border-radius:9px;">
                          <div class="label-sm" style="color:var(--rose);margin-bottom:3px;">핵심 두려움</div>
                          <div style="font-size:.74rem;color:var(--t2);line-height:1.5;">{ei['core_fear']}</div>
                        </div>
                        <div style="padding:.55rem .7rem;background:var(--sage-lt);border-radius:9px;">
                          <div class="label-sm" style="color:var(--sage);margin-bottom:3px;">핵심 욕구</div>
                          <div style="font-size:.74rem;color:var(--t2);line-height:1.5;">{ei['core_desire']}</div>
                        </div>
                      </div>
                      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                        <div style="padding:.55rem .7rem;background:#ECFDF5;border-radius:9px;border:1px solid #A5D6B4;">
                          <div class="label-sm" style="color:var(--sage);margin-bottom:4px;">✅ 잘 맞는 유형</div>
                          {best_html}
                          <div style="font-size:.71rem;color:var(--t2);line-height:1.5;margin-top:4px;">{ei["compatible_desc"]["best"]}</div>
                        </div>
                        <div style="padding:.55rem .7rem;background:#FFF1F2;border-radius:9px;border:1px solid #FECDD3;">
                          <div class="label-sm" style="color:var(--rose);margin-bottom:4px;">⚡ 주의가 필요한 유형</div>
                          {chal_html}
                          <div style="font-size:.71rem;color:var(--t2);line-height:1.5;margin-top:4px;">{ei["compatible_desc"]["challenging"]}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # 다른 유형 모두 보기
                st.markdown("<div class='label-sm' style='margin:.5rem 0 8px;'>다른 에니어그램 유형 살펴보기</div>", unsafe_allow_html=True)
                other_ennea = [e for e in ENNEA_ITEMS if e["type"] != ennea_result]
                cols_per_row = 4
                for row_start in range(0, len(other_ennea), cols_per_row):
                    row_items = other_ennea[row_start:row_start + cols_per_row]
                    row_cols = st.columns(len(row_items), gap="small")
                    for col_e, item_e in zip(row_cols, row_items):
                        with col_e:
                            st.markdown(f"""
                            <div style="background:var(--surface);border:1px solid var(--border);
                                        border-top:3px solid {item_e['color']};border-radius:10px;
                                        padding:.7rem .6rem;text-align:center;margin-bottom:.4rem;">
                              <div style="font-size:1.2rem;">{item_e['icon']}</div>
                              <div style="font-size:.7rem;font-weight:700;color:{item_e['color']};margin:.25rem 0 .15rem;">{item_e['type']}번 {item_e['name']}</div>
                              <div style="font-size:.67rem;color:var(--t3);line-height:1.45;">{item_e['core_desire']}</div>
                            </div>
                            """, unsafe_allow_html=True)

                st.markdown("<div style='height:.5rem;'></div>", unsafe_allow_html=True)
            if st.button("🔄  에니어그램 다시 하기", key="retry_ennea", use_container_width=True):
                for k in [k for k in st.session_state.quiz_answers if k.startswith("ennea_")]:
                    del st.session_state.quiz_answers[k]
                del st.session_state.quiz_results["enneagram"]
                st.session_state.data.setdefault("quiz_results", {}).pop("enneagram", None)
                save_data(st.session_state.data)
                st.rerun()

    # ─── STRESS PATTERN ───────────────────────────────────────
    with Q3:
        stress_result = st.session_state.quiz_results.get("stress")

        st.markdown("""
        <div class="card card-inset" style="margin-bottom:1.2rem;">
          <div class="sec-title">나의 스트레스 반응 패턴 (10Q)</div>
          <div class="sec-sub" style="margin-top:5px;">
            스트레스 상황에서 나타나는 반응 패턴을 파악합니다.<br>
            <b>지금 실제로 내가 그러는 것</b>을 기준으로 솔직하게 선택해 주세요.
          </div>
        </div>
        """, unsafe_allow_html=True)

        for s_idx, q in enumerate(STRESS_Q):
            curr_s = st.session_state.quiz_answers.get(f"stress_{s_idx}")
            s_done = curr_s is not None
            st.markdown(f"""
            <div style="background:var(--surface2);border:1px solid {'var(--indigo)' if s_done else 'var(--border)'};
                        {'border-left:3px solid var(--indigo);' if s_done else ''}
                        border-radius:12px;padding:.85rem 1.1rem .45rem;margin-bottom:.65rem;">
              <div style="display:flex;gap:8px;align-items:center;margin-bottom:.4rem;">
                <span style="font-size:.65rem;font-weight:800;color:{'var(--indigo)' if s_done else 'var(--t4)'};">Q{s_idx+1:02d}</span>
                {"<span style='font-size:.6rem;background:var(--indigo-lt);color:var(--indigo);border-radius:4px;padding:1px 6px;font-weight:700;'>✓</span>" if s_done else ""}
              </div>
              <div style="font-size:.9rem;font-weight:600;color:var(--t1);line-height:1.4;margin-bottom:.5rem;">{q['text']}</div>
            </div>
            """, unsafe_allow_html=True)
            s_cols = st.columns(2, gap="small")
            for opt_idx, opt_txt in enumerate(q["opts"]):
                is_sel = curr_s == opt_idx
                with s_cols[opt_idx % 2]:
                    if st.button(opt_txt, key=f"stress_{s_idx}_o{opt_idx}",
                                 type="primary" if is_sel else "secondary",
                                 use_container_width=True):
                        st.session_state.quiz_answers[f"stress_{s_idx}"] = opt_idx
                        st.rerun()

        all_done_s = _quiz_progress("stress_", len(STRESS_Q))
        if all_done_s and not stress_result:
            if st.button("✨  스트레스 유형 결과 확인", type="primary", use_container_width=True, key="submit_stress"):
                counts_s = {"PS": 0, "RC": 0, "AV": 0, "ER": 0}
                for i, q in enumerate(STRESS_Q):
                    ans = st.session_state.quiz_answers.get(f"stress_{i}")
                    if ans is not None:
                        counts_s[q["keys"][ans]] += 1
                st.session_state.quiz_results["stress"] = max(counts_s, key=counts_s.get)
                st.session_state.data.setdefault("quiz_results", {})["stress"] = st.session_state.quiz_results["stress"]
                save_data(st.session_state.data)
                st.rerun()
        elif not all_done_s:
            rem_s = len(STRESS_Q) - sum(1 for i in range(len(STRESS_Q)) if f"stress_{i}" in st.session_state.quiz_answers)
            st.markdown(f"<div style='text-align:center;font-size:.75rem;color:var(--t4);padding:.4rem;'>{rem_s}문항이 남았습니다</div>", unsafe_allow_html=True)

        if stress_result and stress_result in STRESS_TYPES:
            stype = STRESS_TYPES[stress_result]
            stress_best_html = "".join(
                f'<div style="font-size:.78rem;font-weight:700;color:{STRESS_TYPES[k]["color"]};margin-bottom:2px;">'
                f'{STRESS_TYPES[k]["icon"]} {STRESS_TYPES[k]["name"]}</div>'
                for k in stype["compatible"]["best"]
            )
            stress_chal_html = "".join(
                f'<div style="font-size:.78rem;font-weight:700;color:{STRESS_TYPES[k]["color"]};margin-bottom:2px;">'
                f'{STRESS_TYPES[k]["icon"]} {STRESS_TYPES[k]["name"]}</div>'
                for k in stype["compatible"]["challenging"]
            )
            st.markdown("<div style='height:.6rem;'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card" style="border-left:4px solid {stype['color']};margin-bottom:1.3rem;">
              <div style="display:flex;align-items:flex-start;gap:14px;">
                <div style="font-size:2.5rem;flex-shrink:0;margin-top:2px;">{stype['icon']}</div>
                <div style="flex:1;">
                  <div class="label-sm" style="color:{stype['color']};margin-bottom:4px;">나의 스트레스 반응 유형</div>
                  <div style="font-size:1.05rem;font-weight:800;color:var(--t1);margin-bottom:8px;">{stype['name']}</div>
                  <div style="font-size:.86rem;color:var(--t2);line-height:1.8;margin-bottom:10px;">{stype['detail']}</div>
                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">
                    <div style="padding:.55rem .7rem;background:var(--indigo-lt);border-radius:9px;">
                      <div class="label-sm" style="color:var(--indigo);margin-bottom:3px;">성장 팁</div>
                      <div style="font-size:.73rem;color:var(--indigo-dark);line-height:1.55;">{stype['tip']}</div>
                    </div>
                    <div style="padding:.55rem .7rem;background:var(--sage-lt);border-radius:9px;">
                      <div class="label-sm" style="color:var(--sage);margin-bottom:3px;">권장 상담 접근</div>
                      <div style="font-size:.73rem;color:var(--t2);line-height:1.55;">{stype['therapy']}</div>
                    </div>
                  </div>
                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                    <div style="padding:.55rem .7rem;background:#ECFDF5;border-radius:9px;border:1px solid #A5D6B4;">
                      <div class="label-sm" style="color:var(--sage);margin-bottom:4px;">✅ 잘 맞는 유형</div>
                      {stress_best_html}
                      <div style="font-size:.71rem;color:var(--t2);line-height:1.5;margin-top:4px;">{stype["compatible_desc"]["best"]}</div>
                    </div>
                    <div style="padding:.55rem .7rem;background:#FFF1F2;border-radius:9px;border:1px solid #FECDD3;">
                      <div class="label-sm" style="color:var(--rose);margin-bottom:4px;">⚡ 주의가 필요한 유형</div>
                      {stress_chal_html}
                      <div style="font-size:.71rem;color:var(--t2);line-height:1.5;margin-top:4px;">{stype["compatible_desc"]["challenging"]}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # 다른 스트레스 유형 모두 보기
            st.markdown("<div class='label-sm' style='margin:.5rem 0 8px;'>다른 스트레스 반응 유형 살펴보기</div>", unsafe_allow_html=True)
            other_stress = {k: v for k, v in STRESS_TYPES.items() if k != stress_result}
            stress_other_cols = st.columns(len(other_stress), gap="small")
            for col_s, (k, v) in zip(stress_other_cols, other_stress.items()):
                with col_s:
                    st.markdown(f"""
                    <div style="background:var(--surface);border:1px solid var(--border);
                                border-top:3px solid {v['color']};border-radius:10px;padding:.75rem .65rem;text-align:center;">
                      <div style="font-size:1.3rem;">{v['icon']}</div>
                      <div style="font-size:.72rem;font-weight:700;color:{v['color']};margin:.25rem 0 .3rem;">{v['name']}</div>
                      <div style="font-size:.7rem;color:var(--t2);line-height:1.5;text-align:left;">{v['desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<div style='height:.5rem;'></div>", unsafe_allow_html=True)
            if st.button("🔄  스트레스 패턴 다시 하기", key="retry_stress", use_container_width=True):
                for k in [k for k in st.session_state.quiz_answers if k.startswith("stress_")]:
                    del st.session_state.quiz_answers[k]
                del st.session_state.quiz_results["stress"]
                st.session_state.data.setdefault("quiz_results", {}).pop("stress", None)
                save_data(st.session_state.data)
                st.rerun()


# ═══════════════════════════════════════════════════════════════
# TAB 5 · EMOTIONAL JOURNAL
# ═══════════════════════════════════════════════════════════════
with T5:
    st.markdown("""
    <div style="margin-bottom:1.8rem;">
      <div class="page-eyebrow">감정 일지</div>
      <div class="page-title">오늘의 감정 기록</div>
      <div class="page-desc">
        감정을 언어로 표현하는 것은 감정 조절의 핵심 기술입니다 (Pennebaker, 1997).<br>
        꾸준한 감정 일지는 자기 인식과 심리적 회복탄력성을 높입니다.
      </div>
    </div>
    """, unsafe_allow_html=True)

    jl, jr = st.columns([5, 4], gap="large")

    with jl:
        today_str = str(date.today())
        journals  = st.session_state.data.get("journals", [])
        t_ent     = next((j for j in journals if j.get("date") == today_str), None)

        st.markdown("<div class='sec-title'>오늘 기록</div><div class='sec-sub'>솔직하고 자유롭게 — 맞춤법도 완성도도 신경 쓰지 않아도 됩니다.</div>", unsafe_allow_html=True)

        # Mood
        mood_val = st.slider("현재 감정 강도", 1, 10,
                             value=t_ent["mood"] if t_ent else 5,
                             key="mood_sl")
        em, col = MOOD_MAP[mood_val]
        mood_phrasing = (
            "매우 좋음" if mood_val >= 9 else "좋음" if mood_val >= 7
            else "보통" if mood_val >= 5 else "낮음" if mood_val >= 3 else "매우 낮음"
        )
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin:-4px 0 14px;">
          <span style="font-size:1.5rem;">{em}</span>
          <div>
            <div style="font-size:.78rem;font-weight:700;color:{col};">{mood_phrasing} ({mood_val}/10)</div>
            <div style="font-size:.7rem;color:var(--t4);">감정 온도계</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Emotion tags
        emotion_tags = ["기쁨", "슬픔", "분노", "불안", "두려움", "수치심", "죄책감", "외로움", "설렘", "무감각", "혼란", "안도"]
        cur_tags = t_ent.get("tags", []) if t_ent else []
        st.markdown("<div class='label-sm' style='margin-bottom:5px;'>감정 태그 (복수 선택)</div>", unsafe_allow_html=True)
        tag_cols = st.columns(6)
        for col_i, tag in enumerate(emotion_tags):
            with tag_cols[col_i % 6]:
                is_sel = tag in cur_tags
                if st.button(("✓ " if is_sel else "") + tag, key=f"tag_{tag}", use_container_width=True):
                    if tag in cur_tags:
                        cur_tags.remove(tag)
                    else:
                        cur_tags.append(tag)
                    if t_ent:
                        t_ent["tags"] = cur_tags
                    else:
                        t_ent = {"date": today_str, "mood": mood_val, "text": "", "tags": cur_tags, "ai_analysis": ""}
                        journals.append(t_ent)
                    save_data(st.session_state.data)
                    st.rerun()

        # Journal text
        j_text = st.text_area(
            "journal", height=200,
            value=t_ent["text"] if t_ent else "",
            key="j_txt", label_visibility="collapsed",
            placeholder=(
                "오늘 어떤 일이 일어났나요?\n"
                "어떤 생각이 머릿속을 지나갔나요?\n"
                "몸은 어떤 느낌이었나요?\n"
                "\n자유롭게 적어보세요."
            ),
        )

        b1, b2 = st.columns(2)
        with b1:
            if st.button("💾 저장하기", use_container_width=True):
                if not j_text.strip():
                    st.warning("내용을 입력해 주세요.")
                else:
                    entry = {"date": today_str, "mood": mood_val,
                             "text": j_text.strip(),
                             "tags": cur_tags,
                             "ai_analysis": t_ent["ai_analysis"] if t_ent else ""}
                    idx = next((i for i, j in enumerate(journals) if j.get("date") == today_str), None)
                    if idx is not None:
                        journals[idx] = entry
                    else:
                        journals.append(entry)
                    save_data(st.session_state.data)
                    st.success("✅ 저장 완료")
                    st.rerun()
        with b2:
            if st.button("◎ AI 감정 분석", use_container_width=True, type="primary"):
                if not j_text.strip():
                    st.warning("일기를 먼저 작성해 주세요.")
                else:
                    with st.spinner("소이가 분석 중..."):
                        tags_str = ", ".join(cur_tags) if cur_tags else "없음"
                        analysis = call_gpt(
                            [{"role":"user","content":(
                                f"감정 강도: {mood_val}/10\n"
                                f"감정 태그: {tags_str}\n\n"
                                f"일기 내용:\n{j_text.strip()}\n\n"
                                "이 감정 일기를 인지행동치료(CBT)와 인간중심치료 관점에서 분석해 주세요. "
                                "나타나는 인지 패턴, 감정 처리 방식, 내면의 욕구를 파악하고, "
                                "따뜻하고 전문적인 어조로 200자 내외로 작성해 주세요. "
                                "마지막에 자기 성찰을 돕는 질문 1개를 추가해 주세요."
                            )}],
                            system=build_system_prompt(), tokens=400,
                        )
                    entry = {"date": today_str, "mood": mood_val,
                             "text": j_text.strip(), "tags": cur_tags, "ai_analysis": analysis}
                    idx = next((i for i, j in enumerate(journals) if j.get("date") == today_str), None)
                    if idx is not None:
                        journals[idx] = entry
                    else:
                        journals.append(entry)
                    save_data(st.session_state.data)
                    st.rerun()

        if t_ent and t_ent.get("ai_analysis"):
            st.markdown(f"""
            <div style="margin-top:1rem;">
              <div class="label-sm" style="margin-bottom:5px;">◎ 소이의 분석</div>
              <div class="card left-bar-indigo" style="font-size:.86rem;color:var(--t2);line-height:1.8;padding:1rem 1.1rem;">
                {t_ent["ai_analysis"]}
              </div>
            </div>
            """, unsafe_allow_html=True)

        if cur_tags:
            shown_chips = "".join(f"<span class='chip chip-rose'>{t}</span>" for t in cur_tags)
            st.markdown(f"<div style='margin-top:.5rem;'>{shown_chips}</div>", unsafe_allow_html=True)

    with jr:
        st.markdown("<div class='sec-title'>기록 히스토리</div><div class='sec-sub' style='margin-bottom:.9rem;'>최근 14일 감정 흐름</div>", unsafe_allow_html=True)

        j_sorted = sorted(journals, key=lambda x: x.get("date",""), reverse=True)

        if len(j_sorted) >= 2:
            chart_d = sorted(j_sorted[-14:], key=lambda x: x.get("date",""))
            labels  = [j["date"][5:] for j in chart_d]  # MM-DD
            vals    = [j["mood"] for j in chart_d]

            fig_j = go.Figure()
            fig_j.add_trace(go.Scatter(
                x=labels, y=vals, mode="lines+markers",
                line=dict(color="#5B4FCF", width=2.2, shape="spline"),
                marker=dict(size=7, color="#5B4FCF",
                            line=dict(color="white", width=1.5)),
                fill="tozeroy", fillcolor="rgba(91,79,207,0.06)",
                hovertemplate="%{x}<br>감정 강도: %{y}/10<extra></extra>",
            ))
            fig_j.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                margin=dict(t=10, b=8, l=8, r=8), height=150,
                yaxis=dict(range=[0,11], gridcolor="#F5F3EF",
                           tickfont=dict(size=9), color="#C0BBB5", zeroline=False),
                xaxis=dict(tickfont=dict(size=8), color="#C0BBB5", tickangle=-30),
                showlegend=False,
            )
            st.markdown("<div class='card' style='padding:.9rem .8rem .4rem;'>", unsafe_allow_html=True)
            st.plotly_chart(fig_j, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # ── 연속 기록 streak ──
        if j_sorted:
            all_dates = sorted({j.get("date","") for j in j_sorted if j.get("date")}, reverse=True)
            streak = 0
            check = date.today()
            for d_str in all_dates:
                if d_str == str(check):
                    streak += 1
                    check -= timedelta(days=1)
                else:
                    break
            avg_mood = round(sum(j.get("mood",5) for j in j_sorted) / len(j_sorted), 1)
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:.8rem 0;">
              <div style="padding:.7rem .9rem;background:linear-gradient(135deg,var(--indigo-lt),#F5F3FF);
                          border-radius:10px;text-align:center;">
                <div style="font-size:1.5rem;font-weight:800;color:var(--indigo);">{streak}일</div>
                <div style="font-size:.7rem;color:var(--t3);font-weight:600;">🔥 연속 기록</div>
              </div>
              <div style="padding:.7rem .9rem;background:linear-gradient(135deg,var(--sage-lt),#D1FAE5);
                          border-radius:10px;text-align:center;">
                <div style="font-size:1.5rem;font-weight:800;color:var(--sage);">{avg_mood}</div>
                <div style="font-size:.7rem;color:var(--t3);font-weight:600;">📊 평균 감정 강도</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # ── 감정 태그 빈도 분석 ──
        all_tags = [t for j in j_sorted for t in j.get("tags", [])]
        if all_tags:
            tag_count = {}
            for t in all_tags:
                tag_count[t] = tag_count.get(t, 0) + 1
            tag_sorted = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:8]
            t_labels = [x[0] for x in tag_sorted]
            t_vals   = [x[1] for x in tag_sorted]
            tag_colors = ["#BE123C","#5B4FCF","#B45309","#3D7A5F","#0369A1","#7C3AED","#D97706","#059669"]

            fig_t = go.Figure(go.Bar(
                x=t_vals, y=t_labels, orientation="h",
                marker_color=tag_colors[:len(t_labels)],
                text=t_vals, textposition="outside",
                textfont=dict(size=9, color="#44403C"),
            ))
            fig_t.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                margin=dict(t=5, b=5, l=5, r=30), height=max(120, len(t_labels)*28),
                xaxis=dict(visible=False),
                yaxis=dict(tickfont=dict(size=10, color="#44403C"), autorange="reversed"),
                showlegend=False,
            )
            st.markdown("<div class='label-sm' style='margin:1rem 0 4px;'>자주 느끼는 감정 Top 8</div>", unsafe_allow_html=True)
            st.markdown("<div class='card' style='padding:.7rem .6rem .3rem;'>", unsafe_allow_html=True)
            st.plotly_chart(fig_t, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if not j_sorted:
            st.markdown("""
            <div class="empty">
              <div class="empty-icon">📓</div>
              <div class="empty-title">기록이 없습니다</div>
              <div class="empty-body">오늘 첫 번째 감정 일지를 작성해 보세요</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for j in j_sorted[:12]:
                mood_icon, _ = MOOD_MAP.get(j.get("mood",5), ("😐","#999"))
                tags_html = ""
                if j.get("tags"):
                    tags_html = "".join(f"<span class='chip chip-rose' style='font-size:.65rem;padding:1px 7px;margin:1px;'>{t}</span>" for t in j["tags"][:4])
                ai_html = f"<div class='j-ai'>{j['ai_analysis'][:180]}{'...' if len(j.get('ai_analysis',''))>180 else ''}</div>" if j.get("ai_analysis") else ""
                preview = j.get("text","")[:140] + ("..." if len(j.get("text","")) > 140 else "")
                st.markdown(f"""
                <div class="j-entry">
                  <div style="display:flex;align-items:center;gap:5px;">
                    <span class="j-date">{j.get("date","")}</span>
                    <span class="j-mood">{mood_icon} {j.get("mood",5)}/10</span>
                    <span style="flex:1;"></span>
                    {tags_html}
                  </div>
                  <div class="j-text">{preview}</div>
                  {ai_html}
                </div>
                """, unsafe_allow_html=True)

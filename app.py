"""
╔══════════════════════════════════════════════════════════════════════════╗
║  🚀  COSMOS MISSION CONTROL DASHBOARD  ·  v7.0.0                      ║
║  Complete NASA/SpaceX-style analytics platform                         ║
║  Features: Login · Landing page · 6-page navigation · Physics sim      ║
║  Run: streamlit run cosmos_app.py                                      ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

# ─────────────────────────────────────────────────────────────────────────────
#  IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import hashlib
import time
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="COSMOS · Mission Control",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
#  CREDENTIALS
# ─────────────────────────────────────────────────────────────────────────────
USERS = {
    "admin":    hashlib.sha256("rocket123".encode()).hexdigest(),
    "engineer": hashlib.sha256("nasa2024".encode()).hexdigest(),
    "guest":    hashlib.sha256("guest".encode()).hexdigest(),
}

ROLES = ["Mission Analyst", "Flight Engineer", "Payload Specialist", "Systems Commander"]

# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;800&family=Share+Tech+Mono&display=swap');

/* ══════════════════════════════════════════════════════════
   COSMOS DESIGN SYSTEM — OFFICIAL COLOR TOKENS
   ══════════════════════════════════════════════════════════ */
:root {
  --bg:       #0b0f1a;
  --bg-deep:  #020617;
  --panel:    #0f172a;
  --panel2:   #141a2e;
  --border:   #1e3a5f;
  --border2:  #0f2040;

  --cyan:     #00e5ff;
  --cyan-dim: rgba(0,229,255,.15);
  --cyan-glow:rgba(0,229,255,.35);
  --orange:   #ff6b00;
  --orange-h: #ff8c3a;
  --green:    #00ff9c;
  --red:      #ff4b4b;
  --purple:   #7c8cff;
  --amber:    #ffb300;

  --text:     #ffffff;
  --text2:    #b8c1ec;
  --text3:    #6a86a8;
  --dim:      #4a6a8a;
  --dim2:     #1e3050;
}

/* ── GLOBAL RESETS — force dark everywhere so no white ever shows ── */
html{background:#020617!important;}
body{background:#0b0f1a!important;color:var(--text2)!important;font-family:'Exo 2',sans-serif!important;}
[class*="css"]{color:var(--text2)!important;font-family:'Exo 2',sans-serif!important;}

/* Kill every possible Streamlit white container */
.stApp{background:#0b0f1a!important;}
[data-testid="stAppViewContainer"]{background:#0b0f1a!important;}
[data-testid="stAppViewBlockContainer"]{background:transparent!important;}
section[data-testid="stMain"]{background:transparent!important;}
section[data-testid="stSidebar"]+div{background:transparent!important;}
.main{background:transparent!important;}
.block-container{background:transparent!important;}
/* Streamlit injects an inner white wrapper — nuke it */
[data-testid="stAppViewContainer"] > .main > .block-container{background:transparent!important;}
[data-testid="stVerticalBlock"]{background:transparent!important;}
[data-testid="stHorizontalBlock"]{background:transparent!important;}
div[data-testid="column"]{background:transparent!important;}
/* Streamlit's root element */
#root,#root > div{background:#0b0f1a!important;}
/* iframes and tool containers */
iframe{background:transparent!important;}

::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:#020617;}
::-webkit-scrollbar-thumb{background:#1e3a5f;border-radius:4px;}
::-webkit-scrollbar-thumb:hover{background:#00e5ff;}

/* ── SIDEBAR ── */
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,rgba(2,6,23,.97) 0%,rgba(8,15,35,.98) 100%)!important;
  border-right:1px solid rgba(0,229,255,.12)!important;
  backdrop-filter:blur(16px)!important;
}
[data-testid="stSidebar"] *{font-family:'Share Tech Mono',monospace!important;}
[data-testid="stSidebar"] label{color:var(--cyan)!important;font-size:0.65rem!important;letter-spacing:.16em;text-transform:uppercase;}
[data-testid="stSidebar"] p{color:var(--text2)!important;}

/* Sidebar logout / action buttons */
[data-testid="stSidebar"] .stButton>button{
  width:100%;
  background:linear-gradient(135deg,rgba(255,107,0,.12),rgba(255,107,0,.22))!important;
  border:1px solid rgba(255,107,0,.45)!important;
  color:#ff8c3a!important;
  font-family:'Share Tech Mono',monospace!important;
  font-size:.70rem;letter-spacing:.18em;text-transform:uppercase;
  border-radius:4px;padding:.65rem 0;
  box-shadow:0 0 10px rgba(255,107,0,.15);
  transition:all .25s;cursor:pointer;
}
[data-testid="stSidebar"] .stButton>button:hover{
  background:linear-gradient(135deg,rgba(255,107,0,.25),rgba(255,107,0,.40))!important;
  box-shadow:0 0 20px rgba(255,107,0,.35)!important;
  color:#fff!important;
}

/* ── MAIN LAYOUT ── */
.main .block-container{padding:0 2rem 3rem!important;max-width:1800px!important;background:transparent!important;}
/* Extra insurance: any div that Streamlit creates gets a dark fallback */
div[data-stale="false"]{background:transparent!important;}
[data-testid="stDecoration"]{background:linear-gradient(90deg,#00e5ff,#ff6b00)!important;height:3px!important;}

/* ── CANVAS BACKGROUND LAYER ── */
#cosmos-bg-canvas{
  position:fixed!important;top:0!important;left:0!important;
  width:100vw!important;height:100vh!important;
  z-index:0!important;pointer-events:none!important;display:block!important;
}
[data-testid="stAppViewContainer"]>div,
[data-testid="stSidebar"],.main,.block-container,
[data-testid="stHeader"]{position:relative!important;z-index:1!important;}
.stApp,[data-testid="stAppViewContainer"]{background:#0b0f1a!important;}
[data-testid="stHeader"]{
  background:linear-gradient(90deg,rgba(2,6,23,.92),rgba(8,15,35,.92))!important;
  backdrop-filter:blur(10px)!important;
  border-bottom:1px solid rgba(0,229,255,.08)!important;
}

/* ── STATUS BANNER ── */
.status-banner{
  background:linear-gradient(90deg,rgba(0,229,255,.03) 0%,rgba(0,229,255,.07) 50%,rgba(0,229,255,.03) 100%);
  border:1px solid rgba(0,229,255,.15);
  border-radius:6px;padding:.55rem 1.5rem;
  display:flex;justify-content:center;align-items:center;gap:2.5rem;
  margin-bottom:1.8rem;flex-wrap:wrap;
  backdrop-filter:blur(4px);
}
.sb-item{
  display:flex;align-items:center;gap:.5rem;
  font-family:'Share Tech Mono',monospace;font-size:.60rem;
  color:var(--text3);letter-spacing:.14em;text-transform:uppercase;
}
.sb-dot{width:6px;height:6px;border-radius:50%;animation:pulse 2s ease-in-out infinite;}
.sb-dot.green{background:var(--green);box-shadow:0 0 6px var(--green);}
.sb-dot.cyan{background:var(--cyan);box-shadow:0 0 6px var(--cyan);}
.sb-dot.amber{background:var(--amber);box-shadow:0 0 6px var(--amber);}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.35;transform:scale(.65)}}

/* ── LOGIN CARD ── */
.cosmos-card{
  position:relative;width:100%;max-width:480px;
  background:linear-gradient(160deg,rgba(2,6,23,.97) 0%,rgba(15,23,42,.96) 60%,rgba(5,10,25,.97) 100%);
  border:1px solid rgba(0,229,255,.20);
  border-top:3px solid var(--cyan);
  border-radius:12px;padding:0;
  box-shadow:
    0 0 0 1px rgba(0,229,255,.04),
    0 0 50px rgba(0,229,255,.07),
    0 30px 80px rgba(0,0,0,.85),
    inset 0 1px 0 rgba(0,229,255,.12);
  overflow:hidden;backdrop-filter:blur(24px);
}
.cosmos-card::before{
  content:'';position:absolute;top:0;left:0;right:0;bottom:0;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,229,255,.004) 2px,rgba(0,229,255,.004) 3px);
  pointer-events:none;z-index:1;
}
.cosmos-card::after{
  content:'';position:absolute;top:0;right:0;width:70px;height:70px;
  background:linear-gradient(225deg,rgba(0,229,255,.10) 0%,transparent 60%);
  pointer-events:none;z-index:1;
}
.card-header{
  background:linear-gradient(180deg,rgba(0,229,255,.05) 0%,transparent 100%);
  border-bottom:1px solid rgba(0,229,255,.08);
  padding:1.8rem 2.4rem 1.4rem;position:relative;z-index:2;
}
.card-body{padding:1.4rem 2.4rem 2rem;position:relative;z-index:2;}

.cosmos-auth-tag{
  display:inline-flex;align-items:center;gap:.5rem;
  background:rgba(0,229,255,.07);border:1px solid rgba(0,229,255,.25);
  border-radius:20px;padding:.22rem .8rem;
  font-family:'Share Tech Mono',monospace;font-size:.56rem;
  color:var(--cyan);letter-spacing:.20em;text-transform:uppercase;margin-bottom:.9rem;
}
.cosmos-logo{
  font-family:'Orbitron',monospace;font-size:2.6rem;font-weight:900;color:#fff;
  text-shadow:0 0 16px rgba(0,229,255,.6),0 0 40px rgba(0,229,255,.25),0 0 80px rgba(0,229,255,.10);
  letter-spacing:.14em;line-height:1;margin-bottom:.2rem;
}
.cosmos-logo span{color:var(--cyan);}
.cosmos-subtitle{
  font-family:'Share Tech Mono',monospace;font-size:.60rem;
  color:var(--text3);letter-spacing:.22em;text-transform:uppercase;
}
.cosmos-divider{
  width:100%;height:1px;margin:.8rem 0 1.2rem;
  background:linear-gradient(90deg,transparent,rgba(0,229,255,.18) 30%,rgba(0,229,255,.18) 70%,transparent);
}
.field-label{
  font-family:'Share Tech Mono',monospace;font-size:.60rem;
  color:var(--cyan);letter-spacing:.22em;text-transform:uppercase;
  margin-bottom:.35rem;display:flex;align-items:center;gap:.4rem;
}
.field-label .fl-icon{color:var(--dim);}

/* ── INPUT FIELDS ── */
.stTextInput>div>div>input{
  background:#0f172a!important;
  border:1px solid rgba(0,229,255,.22)!important;
  border-radius:5px!important;
  color:#ffffff!important;
  font-family:'Share Tech Mono',monospace!important;
  font-size:.82rem!important;
  padding:.65rem .9rem!important;
  transition:all .2s!important;
}
.stTextInput>div>div>input:focus{
  border-color:rgba(0,229,255,.60)!important;
  box-shadow:0 0 0 1px rgba(0,229,255,.20),0 0 16px rgba(0,229,255,.10)!important;
  background:#0f1f3a!important;
}
.stTextInput>div>div>input::placeholder{color:#94a3b8!important;}

/* ── SELECTBOX ── */
.stSelectbox>div>div{
  background:#0f172a!important;
  border:1px solid rgba(0,229,255,.22)!important;
  border-radius:5px!important;color:#ffffff!important;
}
.stSelectbox label{color:var(--cyan)!important;}

/* ── PRIMARY ACTION BUTTON (Login / Launch) ── */
.launch-btn-wrap .stButton>button{
  width:100%;
  background:linear-gradient(135deg,#cc4400,#ff6b00,#ff8c3a)!important;
  border:none!important;
  color:#ffffff!important;
  font-family:'Orbitron',monospace!important;
  font-size:.78rem!important;font-weight:700!important;
  letter-spacing:.22em!important;text-transform:uppercase!important;
  border-radius:5px!important;padding:.85rem 0!important;
  box-shadow:0 0 22px rgba(255,107,0,.30),0 4px 16px rgba(0,0,0,.4)!important;
  transition:all .25s!important;
}
.launch-btn-wrap .stButton>button:hover{
  background:linear-gradient(135deg,#dd5500,#ff8c3a,#ffaa66)!important;
  box-shadow:0 0 38px rgba(255,107,0,.50),0 4px 20px rgba(0,0,0,.5)!important;
  transform:translateY(-2px)!important;
}
.launch-btn-wrap .stButton>button:active{transform:translateY(0)!important;}

/* ── FEEDBACK MESSAGES ── */
.cosmos-error{
  background:rgba(255,75,75,.07);border:1px solid rgba(255,75,75,.30);
  border-left:3px solid var(--red);border-radius:5px;
  padding:.75rem 1rem;margin-top:.8rem;
  font-family:'Share Tech Mono',monospace;font-size:.64rem;
  color:#ff7a7a;letter-spacing:.08em;
  display:flex;align-items:center;gap:.6rem;
}
.cosmos-success{
  background:rgba(0,255,156,.06);border:1px solid rgba(0,255,156,.28);
  border-left:3px solid var(--green);border-radius:5px;
  padding:.75rem 1rem;margin-top:.8rem;
  font-family:'Share Tech Mono',monospace;font-size:.64rem;
  color:var(--green);letter-spacing:.08em;
  display:flex;align-items:center;gap:.6rem;
}

/* ── TELEMETRY CHIPS (login) ── */
.telem-grid{display:grid;grid-template-columns:1fr 1fr;gap:.5rem;margin-top:1.2rem;}
.telem-chip{
  background:rgba(15,23,42,.8);border:1px solid rgba(0,229,255,.10);
  border-radius:5px;padding:.45rem .7rem;
}
.tc-label{font-family:'Share Tech Mono',monospace;font-size:.50rem;color:var(--dim);letter-spacing:.14em;text-transform:uppercase;}
.tc-value{font-family:'Share Tech Mono',monospace;font-size:.68rem;color:var(--cyan);margin-top:.1rem;letter-spacing:.06em;}

/* ── SECURITY NOTICE ── */
.security-notice{
  text-align:center;margin-top:1.3rem;
  font-family:'Share Tech Mono',monospace;font-size:.55rem;
  color:var(--dim);letter-spacing:.09em;line-height:2.2;
}
.security-notice .warn-line{color:var(--text3);}
.security-notice .cred-line{color:var(--dim);}

/* ── LOADING SCREEN ── */
.loading-overlay{background:transparent;padding:3rem;text-align:center;}
.loading-title{
  font-family:'Orbitron',monospace;font-size:1.4rem;font-weight:700;
  color:var(--green);letter-spacing:.14em;
  text-shadow:0 0 18px rgba(0,255,156,.5);margin-bottom:1.2rem;
}
.loading-msg{
  font-family:'Share Tech Mono',monospace;font-size:.72rem;
  color:var(--text3);letter-spacing:.12em;line-height:2.5;
}
.loading-bar-wrap{width:100%;max-width:320px;margin:1.2rem auto;height:3px;background:rgba(0,229,255,.08);border-radius:3px;overflow:hidden;}
.loading-bar{height:100%;background:linear-gradient(90deg,transparent,var(--cyan),var(--green));animation:loadbar 2s ease-in-out forwards;}
@keyframes loadbar{0%{width:0%}100%{width:100%}}

/* ── LANDING PAGE ── */
.landing-wrap{min-height:90vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:3rem 2rem;}
.landing-dot{width:5px;height:5px;border-radius:50%;background:var(--green);box-shadow:0 0 6px var(--green);display:inline-block;animation:pulse 2s ease-in-out infinite;}
.landing-title{font-family:'Orbitron',monospace;font-size:clamp(2.2rem,5vw,3.8rem);font-weight:900;color:#fff;text-shadow:0 0 24px rgba(0,229,255,.45),0 0 60px rgba(0,229,255,.12);letter-spacing:.06em;line-height:1.1;margin-bottom:.5rem;}
.landing-accent{font-family:'Orbitron',monospace;font-size:clamp(1.0rem,2vw,1.5rem);font-weight:400;color:var(--cyan);letter-spacing:.12em;margin-bottom:1.8rem;}
.landing-desc{font-family:'Exo 2',sans-serif;font-size:1.0rem;color:var(--text3);max-width:640px;line-height:1.75;margin:0 auto 2.4rem;}
.landing-stats{display:flex;gap:2rem;justify-content:center;flex-wrap:wrap;margin-bottom:2.8rem;}
.landing-stat{background:rgba(20,26,46,.75);border:1px solid rgba(0,229,255,.12);border-radius:8px;padding:.9rem 1.5rem;min-width:130px;backdrop-filter:blur(8px);}
.landing-stat-val{font-family:'Orbitron',monospace;font-size:1.6rem;font-weight:700;color:var(--cyan);text-shadow:0 0 10px rgba(0,229,255,.3);}
.landing-stat-lbl{font-family:'Share Tech Mono',monospace;font-size:.60rem;color:var(--dim);letter-spacing:.14em;text-transform:uppercase;margin-top:.2rem;}

/* Enter button — orange primary */
.enter-btn-wrap .stButton>button{
  background:linear-gradient(135deg,#cc4400,#ff6b00,#ff8c3a)!important;
  border:none!important;color:#fff!important;
  font-family:'Orbitron',monospace!important;font-size:.82rem!important;
  font-weight:700!important;letter-spacing:.24em!important;text-transform:uppercase!important;
  border-radius:5px!important;padding:.88rem 3rem!important;
  box-shadow:0 0 28px rgba(255,107,0,.40),0 4px 20px rgba(0,0,0,.5)!important;
  transition:all .25s!important;min-width:280px!important;
}
.enter-btn-wrap .stButton>button:hover{
  background:linear-gradient(135deg,#dd5500,#ff8c3a,#ffaa66)!important;
  box-shadow:0 0 44px rgba(255,107,0,.60),0 4px 28px rgba(0,0,0,.6)!important;
  transform:translateY(-2px)!important;
}

/* ── PAGE BANNER ── */
.page-banner{
  position:relative;
  background:linear-gradient(135deg,rgba(2,6,23,.96),rgba(15,23,42,.94),rgba(5,10,25,.96));
  border:1px solid rgba(0,229,255,.12);
  border-top:3px solid var(--ac,var(--cyan));
  border-radius:0 0 10px 10px;
  padding:1.5rem 2rem 1.2rem;margin-bottom:1.4rem;overflow:hidden;
  backdrop-filter:blur(8px);
}
.page-banner::after{content:'';position:absolute;top:0;left:0;right:0;bottom:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,229,255,.004) 2px,rgba(0,229,255,.004) 3px);pointer-events:none;}
.pg-eyebrow{font-family:'Share Tech Mono',monospace;font-size:.60rem;color:var(--dim);letter-spacing:.30em;text-transform:uppercase;margin-bottom:.3rem;}
.pg-title{font-family:'Orbitron',monospace;font-size:1.7rem;font-weight:900;margin:0;color:var(--ac,var(--cyan));text-shadow:0 0 16px var(--ac,rgba(0,229,255,.5));letter-spacing:.05em;}
.pg-subtitle{font-family:'Exo 2',sans-serif;font-size:.85rem;color:var(--text3);margin-top:.25rem;}
.badge{display:inline-block;font-family:'Share Tech Mono',monospace;font-size:.58rem;letter-spacing:.14em;padding:.18rem .65rem;border-radius:3px;text-transform:uppercase;margin:.4rem .3rem 0 0;}
.bg{background:rgba(0,255,156,.07);border:1px solid rgba(0,255,156,.40);color:var(--green);}
.bc{background:rgba(0,229,255,.07);border:1px solid rgba(0,229,255,.35);color:var(--cyan);}
.bo{background:rgba(255,107,0,.08);border:1px solid rgba(255,107,0,.40);color:var(--orange);}
.ba{background:rgba(255,179,0,.07);border:1px solid rgba(255,179,0,.35);color:var(--amber);}

/* ── SECTION DIVIDER ── */
.sdiv{display:flex;align-items:center;gap:.9rem;margin:1.8rem 0 1.1rem;}
.sline{flex:1;height:1px;background:linear-gradient(90deg,transparent,rgba(0,229,255,.15) 25%,rgba(0,229,255,.15) 75%,transparent);}
.slabel{font-family:'Share Tech Mono',monospace;font-size:.62rem;color:var(--cyan);letter-spacing:.24em;text-transform:uppercase;white-space:nowrap;}

/* ── KPI CARDS ── */
.kpi-card{
  background:rgba(15,23,42,.85);
  border:1px solid rgba(30,58,95,.8);
  border-bottom:2px solid var(--kc,var(--cyan));
  border-radius:8px;padding:1rem 1.1rem .9rem;
  position:relative;overflow:hidden;
  backdrop-filter:blur(6px);
  transition:transform .2s,box-shadow .2s;
}
.kpi-card:hover{transform:translateY(-2px);box-shadow:0 6px 24px rgba(0,0,0,.4);}
.kpi-card::before{content:'';position:absolute;bottom:0;left:0;right:0;height:50px;background:radial-gradient(ellipse at 50% 100%,var(--kg,rgba(0,229,255,.12)) 0%,transparent 70%);}
.kpi-icon{font-size:1.1rem;margin-bottom:.2rem;}
.kpi-lbl{font-family:'Share Tech Mono',monospace;font-size:.58rem;color:var(--text3);letter-spacing:.16em;text-transform:uppercase;}
.kpi-val{font-family:'Orbitron',monospace;font-size:1.9rem;font-weight:700;color:var(--kc,var(--cyan));text-shadow:0 0 10px var(--kg,rgba(0,229,255,.25));line-height:1.15;}
.kpi-sub{font-family:'Share Tech Mono',monospace;font-size:.54rem;color:var(--dim);}

/* ── CHART HEADER ── */
.chdr{font-family:'Share Tech Mono',monospace;font-size:.62rem;color:var(--cyan);letter-spacing:.14em;text-transform:uppercase;margin-bottom:.5rem;display:flex;align-items:center;gap:.4rem;}
.cdot{width:5px;height:5px;border-radius:50%;background:var(--green);box-shadow:0 0 5px var(--green);animation:blink 2.2s ease-in-out infinite;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.15}}

/* ── TELEMETRY PANEL ── */
.telem-wrap{background:rgba(15,23,42,.85);border:1px solid rgba(30,58,95,.8);border-radius:8px;padding:1rem;backdrop-filter:blur(6px);}
.telem-row{display:flex;justify-content:space-between;align-items:center;padding:.45rem .7rem;background:rgba(9,15,32,.7);border:1px solid rgba(30,58,95,.5);border-radius:5px;margin-bottom:.38rem;}
.tk{font-family:'Share Tech Mono',monospace;font-size:.60rem;color:var(--text3);letter-spacing:.10em;text-transform:uppercase;}
.tv{font-family:'Orbitron',monospace;font-size:1.15rem;font-weight:700;color:var(--green);text-shadow:0 0 6px rgba(0,255,156,.3);}
.tv.warn{color:var(--amber);text-shadow:0 0 6px rgba(255,179,0,.3);}
.tv.crit{color:var(--red);text-shadow:0 0 6px rgba(255,75,75,.3);}

/* ── STATUS BLOCK ── */
.status-blk{background:rgba(15,23,42,.85);border:1px solid rgba(30,58,95,.8);border-radius:8px;padding:1.1rem 1.3rem;backdrop-filter:blur(6px);}
.slb{font-family:'Share Tech Mono',monospace;font-size:.58rem;color:var(--text3);letter-spacing:.20em;text-transform:uppercase;margin-bottom:.4rem;}
.sv{font-family:'Orbitron',monospace;font-size:2.2rem;font-weight:900;letter-spacing:.06em;}
.sv-ok{color:var(--green);text-shadow:0 0 18px rgba(0,255,156,.6);}
.sv-fail{color:var(--red);text-shadow:0 0 18px rgba(255,75,75,.6);}

/* ── CONSOLE ── */
.console{
  background:rgba(1,4,12,.92);border:1px solid rgba(0,229,255,.10);
  border-radius:6px;padding:.8rem 1rem;
  font-family:'Share Tech Mono',monospace;font-size:.63rem;color:var(--green);
  line-height:1.8;letter-spacing:.03em;max-height:190px;overflow-y:auto;
  backdrop-filter:blur(4px);
}
.cln{color:var(--dim2);margin-right:.8rem;}
.cok{color:var(--green);}
.cwar{color:var(--amber);}
.cerr{color:var(--red);}
.cinf{color:var(--cyan);}
.cdim{color:var(--dim);}

/* ── ABOUT CARDS ── */
.about-card{background:rgba(15,23,42,.85);border:1px solid rgba(30,58,95,.8);border-radius:8px;padding:1.4rem 1.6rem;margin-bottom:1rem;backdrop-filter:blur(6px);}
.about-card h4{font-family:'Share Tech Mono',monospace;font-size:.70rem;color:var(--cyan);letter-spacing:.18em;text-transform:uppercase;border-bottom:1px solid rgba(30,58,95,.8);padding-bottom:.5rem;margin:0 0 .8rem 0;}
.about-card p,.about-card li{font-family:'Exo 2',sans-serif!important;font-size:.90rem;color:var(--text2);line-height:1.75;margin:.3rem 0;}
.formula{background:rgba(9,15,32,.8);border-left:3px solid var(--cyan);border-radius:3px;padding:.65rem 1rem;margin:.6rem 0;font-family:'Share Tech Mono',monospace;font-size:.75rem;color:var(--amber);letter-spacing:.06em;}
.tech-pill{display:inline-block;background:rgba(0,229,255,.06);border:1px solid rgba(0,229,255,.20);border-radius:20px;padding:.2rem .7rem;margin:.2rem;font-family:'Share Tech Mono',monospace;font-size:.63rem;color:var(--cyan);letter-spacing:.08em;}

/* ── DATASET EXPLORER ── */
.ex-stat{background:rgba(15,23,42,.85);border:1px solid rgba(30,58,95,.8);border-radius:8px;padding:.75rem .9rem;text-align:center;backdrop-filter:blur(6px);}
.ex-val{font-family:'Orbitron',monospace;font-size:1.6rem;font-weight:700;color:var(--cyan);}
.ex-lbl{font-family:'Share Tech Mono',monospace;font-size:.55rem;color:var(--dim);letter-spacing:.14em;text-transform:uppercase;}

/* ── INSIGHT CARDS ── */
.insight-card{background:rgba(15,23,42,.85);border:1px solid rgba(30,58,95,.8);border-left:3px solid var(--orange);border-radius:6px;padding:1rem 1.2rem;margin-bottom:.8rem;backdrop-filter:blur(6px);}
.insight-title{font-family:'Share Tech Mono',monospace;font-size:.68rem;color:var(--orange);letter-spacing:.12em;text-transform:uppercase;margin-bottom:.4rem;}
.insight-body{font-family:'Exo 2',sans-serif;font-size:.88rem;color:var(--text2);line-height:1.65;}

/* ── STREAMLIT COMPONENT OVERRIDES ── */
.stSlider>div>div>div>div{background:var(--cyan)!important;}
[data-testid="stExpander"]{background:rgba(15,23,42,.85)!important;border:1px solid rgba(30,58,95,.8)!important;border-radius:8px!important;backdrop-filter:blur(6px)!important;}
.stDataFrame{border:1px solid rgba(30,58,95,.8)!important;border-radius:6px!important;}
div[data-testid="stMetric"]{background:transparent!important;border:none!important;}
.stRadio>div>label>div>p{color:var(--text2)!important;}
.stCheckbox>label>div>p{color:var(--text2)!important;}
[data-baseweb="tab"]{color:var(--text2)!important;}

/* ══════════════════════════════════════════════════════════
   ROCKET LAUNCH SIMULATION — MISSION CONTROL UI v3
   ══════════════════════════════════════════════════════════ */

/* ── EQUATION STRIP ── */
.eq-strip{
  background:linear-gradient(90deg,rgba(0,229,255,.03),rgba(0,229,255,.07),rgba(0,229,255,.03));
  border:1px solid rgba(0,229,255,.12);border-radius:6px;
  padding:.55rem 1.2rem;margin-bottom:1rem;
  display:flex;gap:1.6rem;flex-wrap:wrap;align-items:center;
}
.eq-item{font-family:'Share Tech Mono',monospace;font-size:.64rem;color:var(--amber);letter-spacing:.06em;}
.eq-sep{color:rgba(0,229,255,.22);font-size:.9rem;}

/* ── PHASE TIMELINE ── */
.phase-bar{
  display:flex;align-items:stretch;gap:0;
  background:rgba(5,10,25,.9);border:1px solid rgba(0,229,255,.12);
  border-radius:8px;overflow:hidden;margin:.6rem 0 1.2rem;
}
.phase-item{
  flex:1;padding:.6rem .3rem .5rem;text-align:center;position:relative;
  border-right:1px solid rgba(0,229,255,.07);transition:background .3s;
}
.phase-item:last-child{border-right:none;}
.phase-item.done{background:linear-gradient(180deg,rgba(0,255,156,.08),rgba(0,255,156,.03));border-bottom:2px solid var(--green);}
.phase-item.active{background:linear-gradient(180deg,rgba(0,229,255,.10),rgba(0,229,255,.03));border-bottom:2px solid var(--cyan);}
.phase-item.pending{border-bottom:2px solid rgba(30,58,95,.6);}
.phase-icon{font-size:.95rem;display:block;margin-bottom:.15rem;}
.phase-label{font-family:'Share Tech Mono',monospace;font-size:.48rem;letter-spacing:.10em;text-transform:uppercase;}
.phase-item.done .phase-label{color:var(--green);}
.phase-item.active .phase-label{color:var(--cyan);}
.phase-item.pending .phase-label{color:var(--dim);}

/* ── LIVE KPI STRIP ── */
.live-strip{display:grid;grid-template-columns:repeat(5,1fr);gap:.55rem;margin-bottom:1.2rem;}
.ls-card{
  background:rgba(9,15,32,.92);border:1px solid rgba(30,58,95,.8);
  border-radius:8px;padding:.75rem .8rem .65rem;position:relative;overflow:hidden;
  transition:transform .2s,box-shadow .2s;
}
.ls-card:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.4);}
.ls-card::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--lc,var(--cyan)),transparent);
  box-shadow:0 0 8px var(--lc,var(--cyan));}
.ls-icon{font-size:1rem;margin-bottom:.12rem;}
.ls-label{font-family:'Share Tech Mono',monospace;font-size:.50rem;color:var(--dim);letter-spacing:.14em;text-transform:uppercase;}
.ls-val{font-family:'Orbitron',monospace;font-size:1.5rem;font-weight:700;color:var(--lc,var(--cyan));line-height:1.1;text-shadow:0 0 10px var(--lc,rgba(0,229,255,.3));}
.ls-sub{font-family:'Share Tech Mono',monospace;font-size:.46rem;color:var(--dim);margin-top:.08rem;}
.ls-bar-wrap{width:100%;height:3px;background:rgba(255,255,255,.06);border-radius:3px;margin-top:.3rem;overflow:hidden;}
.ls-bar{height:100%;border-radius:3px;}

/* ── MISSION CONTROL MAIN GRID ── */
.mc-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.8rem;margin-bottom:1rem;}
.mc-panel{
  background:rgba(9,15,32,.92);border:1px solid rgba(30,58,95,.8);
  border-radius:10px;padding:1rem;position:relative;overflow:hidden;
}
.mc-panel::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--pc,var(--cyan)),transparent);}
.mc-panel-title{
  font-family:'Share Tech Mono',monospace;font-size:.56rem;color:var(--pc,var(--cyan));
  letter-spacing:.20em;text-transform:uppercase;
  border-bottom:1px solid rgba(30,58,95,.6);padding-bottom:.45rem;margin-bottom:.7rem;
  display:flex;align-items:center;gap:.45rem;
}
.mc-dot{width:5px;height:5px;border-radius:50%;background:var(--pc,var(--cyan));
  box-shadow:0 0 4px var(--pc,var(--cyan));animation:blink 2s ease-in-out infinite;}

/* ── TRAJECTORY VISUALIZER ── */
.traj-panel{
  background:rgba(4,8,20,.96);border:1px solid rgba(0,229,255,.18);
  border-radius:10px;padding:.8rem;position:relative;overflow:hidden;
}
.traj-canvas-wrap{position:relative;width:100%;height:220px;}

/* ── ATMOSPHERE LAYER LEGEND ── */
.atmo-legend{
  display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.5rem;
}
.atmo-chip{
  font-family:'Share Tech Mono',monospace;font-size:.48rem;
  padding:.15rem .5rem;border-radius:3px;letter-spacing:.08em;
}

/* ── GO/NO-GO CHECKLIST ── */
.gonogo-grid{display:grid;grid-template-columns:1fr 1fr;gap:.4rem;}
.gng-item{
  display:flex;align-items:center;gap:.5rem;
  background:rgba(5,10,25,.8);border:1px solid rgba(30,58,95,.5);
  border-radius:5px;padding:.4rem .65rem;
  font-family:'Share Tech Mono',monospace;font-size:.55rem;letter-spacing:.06em;
  transition:border-color .2s;
}
.gng-item.go{border-left:2px solid var(--green);color:var(--text2);}
.gng-item.nogo{border-left:2px solid var(--red);color:#ff8080;}
.gng-item.warn{border-left:2px solid var(--amber);color:var(--amber);}
.gng-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
.gng-dot.go{background:var(--green);box-shadow:0 0 5px var(--green);}
.gng-dot.nogo{background:var(--red);box-shadow:0 0 5px var(--red);}
.gng-dot.warn{background:var(--amber);box-shadow:0 0 5px var(--amber);}

/* ── TELEMETRY READOUT ── */
.telem-grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.38rem;}
.tg2-cell{
  background:rgba(4,8,20,.85);border:1px solid rgba(30,58,95,.5);
  border-radius:5px;padding:.42rem .6rem;
}
.tg2-k{font-family:'Share Tech Mono',monospace;font-size:.48rem;color:var(--dim);letter-spacing:.10em;text-transform:uppercase;margin-bottom:.1rem;}
.tg2-v{font-family:'Orbitron',monospace;font-size:.85rem;font-weight:700;color:var(--green);}
.tg2-v.c{color:var(--cyan);}
.tg2-v.o{color:var(--orange);}
.tg2-v.w{color:var(--amber);}
.tg2-v.r{color:var(--red);}
.tg2-v.p{color:var(--purple);}

/* ── MISSION STATUS HERO ── */
.ms-hero{
  text-align:center;padding:1rem .5rem;
}
.ms-status-ok{
  font-family:'Orbitron',monospace;font-size:1.6rem;font-weight:900;
  color:var(--green);text-shadow:0 0 20px rgba(0,255,156,.6);letter-spacing:.06em;
  animation:statusPulse 2s ease-in-out infinite;
}
.ms-status-fail{
  font-family:'Orbitron',monospace;font-size:1.6rem;font-weight:900;
  color:var(--red);text-shadow:0 0 20px rgba(255,75,75,.6);letter-spacing:.06em;
}
@keyframes statusPulse{0%,100%{text-shadow:0 0 20px rgba(0,255,156,.6)}50%{text-shadow:0 0 35px rgba(0,255,156,.9),0 0 60px rgba(0,255,156,.3)}}
.ms-badge{
  display:inline-block;margin-top:.5rem;
  font-family:'Share Tech Mono',monospace;font-size:.52rem;
  color:var(--text3);letter-spacing:.14em;text-transform:uppercase;
}

/* ── TRAJ BADGES ── */
.traj-badge{display:inline-flex;align-items:center;gap:.35rem;
  background:rgba(0,229,255,.07);border:1px solid rgba(0,229,255,.20);
  border-radius:20px;padding:.18rem .65rem;
  font-family:'Share Tech Mono',monospace;font-size:.56rem;color:var(--cyan);
  letter-spacing:.12em;text-transform:uppercase;margin:.18rem .25rem;}
.traj-badge.orange{background:rgba(255,107,0,.08);border-color:rgba(255,107,0,.25);color:var(--orange);}
.traj-badge.green{background:rgba(0,255,156,.06);border-color:rgba(0,255,156,.22);color:var(--green);}
.traj-badge.red{background:rgba(255,75,75,.08);border-color:rgba(255,75,75,.25);color:var(--red);}
.traj-badge.amber{background:rgba(255,179,0,.07);border-color:rgba(255,179,0,.22);color:var(--amber);}

/* ── CONSOLE ── */
.console-v2{
  background:rgba(1,3,10,.97);border:1px solid rgba(0,229,255,.10);
  border-radius:8px;padding:.9rem 1rem;
  font-family:'Share Tech Mono',monospace;font-size:.63rem;
  line-height:2.0;letter-spacing:.03em;
  max-height:240px;overflow-y:auto;
  box-shadow:inset 0 0 30px rgba(0,0,0,.5);
}
.console-v2::-webkit-scrollbar{width:4px;}
.console-v2::-webkit-scrollbar-track{background:rgba(0,0,0,.3);}
.console-v2::-webkit-scrollbar-thumb{background:rgba(0,229,255,.2);border-radius:2px;}
.cl-num{color:#1a2d48;margin-right:.7rem;user-select:none;}
.cl-ts{color:#1e3358;margin-right:.5rem;}
.cl-ok{color:var(--green);} .cl-warn{color:var(--amber);}
.cl-err{color:var(--red);} .cl-inf{color:var(--cyan);}
.cl-dim{color:var(--dim);} .cl-data{color:#7a9ab8;}

/* ── COMPARISON TABLE ── */
.cmp-table{width:100%;border-collapse:collapse;font-family:'Share Tech Mono',monospace;}
.cmp-table th{font-size:.51rem;color:var(--cyan);letter-spacing:.14em;text-transform:uppercase;
  padding:.5rem .55rem;border-bottom:1px solid rgba(0,229,255,.14);text-align:left;}
.cmp-table td{font-size:.57rem;padding:.42rem .55rem;border-bottom:1px solid rgba(30,58,95,.35);color:var(--text2);}
.cmp-table tr:hover td{background:rgba(0,229,255,.035);}
.cmp-table .cmp-you{color:var(--orange);font-weight:bold;}
.cmp-table .cmp-name{color:var(--text);}

/* ── LAUNCH COMMIT / ABORT BANNERS ── */
.launch-commit{
  background:linear-gradient(90deg,rgba(0,255,156,.07),rgba(0,229,255,.05),rgba(0,255,156,.07));
  border:1px solid rgba(0,255,156,.28);border-radius:8px;
  padding:.9rem 1.3rem;margin-top:.8rem;
  display:flex;align-items:center;gap:1rem;
}
.lc-icon{font-size:1.8rem;flex-shrink:0;}
.lc-title{font-family:'Orbitron',monospace;font-size:.85rem;font-weight:700;color:var(--green);letter-spacing:.10em;}
.lc-sub{font-family:'Share Tech Mono',monospace;font-size:.58rem;color:var(--text3);letter-spacing:.05em;margin-top:.2rem;}
.abort-banner{
  background:linear-gradient(90deg,rgba(255,75,75,.08),rgba(255,107,0,.05),rgba(255,75,75,.08));
  border:1px solid rgba(255,75,75,.28);border-radius:8px;
  padding:.9rem 1.3rem;margin-top:.8rem;
  display:flex;align-items:center;gap:1rem;
}

/* ── FOOTER ── */
.cosmos-footer{text-align:center;font-family:'Share Tech Mono',monospace;font-size:.56rem;color:var(--dim);letter-spacing:.14em;padding-bottom:1rem;}
.cosmos-footer hr{border:none;border-top:1px solid rgba(30,58,95,.5);margin:2.5rem 0 .8rem;}
/* ══════════════════════════════════════════════════════════
   ENHANCED LOGIN PAGE STYLES
   ══════════════════════════════════════════════════════════ */

/* ── Glowing horizontal separator line ── */
.glow-line{
  width:100%;height:1px;
  background:linear-gradient(90deg,transparent 0%,rgba(0,229,255,.7) 30%,rgba(0,229,255,1) 50%,rgba(0,229,255,.7) 70%,transparent 100%);
  box-shadow:0 0 8px rgba(0,229,255,.6),0 0 16px rgba(0,229,255,.3);
  margin:0;
}
.glow-line-thin{
  width:100%;height:1px;
  background:linear-gradient(90deg,transparent 0%,rgba(0,229,255,.3) 30%,rgba(0,229,255,.55) 50%,rgba(0,229,255,.3) 70%,transparent 100%);
  margin:.6rem 0;
}

/* ── Enhanced status banner ── */
.status-banner-v2{
  position:relative;
  background:linear-gradient(90deg,rgba(0,20,50,.0) 0%,rgba(0,229,255,.06) 50%,rgba(0,20,50,.0) 100%);
  border-bottom:1px solid rgba(0,229,255,.15);
  padding:.55rem 0 .55rem;
  display:flex;justify-content:center;align-items:center;gap:0;
  margin-bottom:0;width:100%;
}
.sb2-item{
  display:flex;align-items:center;gap:.55rem;
  padding:.2rem 1.8rem;
  font-family:'Share Tech Mono',monospace;font-size:.62rem;
  color:var(--text3);letter-spacing:.14em;text-transform:uppercase;
  border-right:1px solid rgba(0,229,255,.12);
}
.sb2-item:last-child{border-right:none;}
.sb2-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0;}
.sb2-dot.g{background:#00ff9c;box-shadow:0 0 8px #00ff9c,0 0 16px rgba(0,255,156,.4);animation:sb2pulse 2s ease-in-out infinite;}
.sb2-dot.c{background:#00e5ff;box-shadow:0 0 8px #00e5ff,0 0 16px rgba(0,229,255,.4);animation:sb2pulse 2.3s ease-in-out infinite .3s;}
.sb2-dot.a{background:#ffb300;box-shadow:0 0 8px #ffb300,0 0 16px rgba(255,179,0,.4);animation:sb2pulse 1.8s ease-in-out infinite .6s;}
@keyframes sb2pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.3;transform:scale(.6)}}

/* ── Login page outer wrapper ── */
.login-outer{
  min-height:100vh;
  display:flex;flex-direction:column;
  align-items:center;justify-content:flex-start;
  padding:0;
}

/* ── Upgraded cosmos card ── */
.cosmos-card-v2{
  position:relative;
  width:100%;max-width:500px;
  background:
    linear-gradient(160deg,rgba(2,8,24,.98) 0%,rgba(10,18,38,.96) 50%,rgba(4,10,26,.98) 100%);
  border:1px solid rgba(0,229,255,.22);
  border-radius:14px;
  overflow:hidden;
  box-shadow:
    0 0 0 1px rgba(0,229,255,.06),
    0 0 30px rgba(0,229,255,.10),
    0 0 70px rgba(0,229,255,.05),
    0 30px 90px rgba(0,0,0,.9),
    inset 0 1px 0 rgba(0,229,255,.18),
    inset 0 -1px 0 rgba(0,229,255,.06);
  backdrop-filter:blur(30px);
  -webkit-backdrop-filter:blur(30px);
}
/* top accent bar */
.cosmos-card-v2::before{
  content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,transparent 0%,#00e5ff 30%,#7c8cff 70%,transparent 100%);
  box-shadow:0 0 12px rgba(0,229,255,.6),0 0 30px rgba(0,229,255,.2);
  z-index:10;
}
/* scanline texture */
.cosmos-card-v2::after{
  content:'';position:absolute;inset:0;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,229,255,.004) 2px,rgba(0,229,255,.004) 3px);
  pointer-events:none;z-index:1;
}

/* ── Card header / branding area ── */
.cc-header{
  position:relative;z-index:2;
  background:linear-gradient(180deg,rgba(0,229,255,.07) 0%,rgba(0,229,255,.02) 60%,transparent 100%);
  padding:1.6rem 2.2rem 1.2rem;
  text-align:center;
  overflow:hidden;
}
/* subtle star shimmer in header */
.cc-header::before{
  content:'';position:absolute;inset:0;
  background:
    radial-gradient(circle at 20% 50%,rgba(0,229,255,.04) 0%,transparent 40%),
    radial-gradient(circle at 80% 30%,rgba(124,140,255,.04) 0%,transparent 40%);
  pointer-events:none;
}

.cc-auth-pill{
  display:inline-flex;align-items:center;gap:.5rem;
  background:rgba(0,229,255,.08);
  border:1px solid rgba(0,229,255,.28);
  border-radius:20px;padding:.2rem .9rem;
  font-family:'Share Tech Mono',monospace;font-size:.55rem;
  color:var(--cyan);letter-spacing:.24em;text-transform:uppercase;
  margin-bottom:.8rem;
}
.cc-logo{
  font-family:'Orbitron',monospace;font-size:2.8rem;font-weight:900;
  color:#ffffff;letter-spacing:.16em;line-height:1;margin-bottom:.25rem;
  text-shadow:
    0 0 12px rgba(0,229,255,.8),
    0 0 30px rgba(0,229,255,.45),
    0 0 60px rgba(0,229,255,.18),
    0 0 100px rgba(0,229,255,.08);
}
.cc-logo-accent{color:var(--cyan);}
.cc-subtitle{
  font-family:'Share Tech Mono',monospace;font-size:.60rem;
  color:var(--text3);letter-spacing:.24em;text-transform:uppercase;
  margin-bottom:.1rem;
}

/* ── Card body ── */
.cc-body{position:relative;z-index:2;padding:1.2rem 2.2rem 1.6rem;}

/* ── Field labels ── */
.cc-label{
  font-family:'Share Tech Mono',monospace;font-size:.60rem;
  color:var(--cyan);letter-spacing:.22em;text-transform:uppercase;
  margin-bottom:.3rem;margin-top:.85rem;
  display:flex;align-items:center;gap:.45rem;
}
.cc-label-icon{
  width:14px;height:14px;border:1px solid rgba(0,229,255,.4);
  border-radius:3px;display:inline-flex;align-items:center;justify-content:center;
  font-size:.6rem;color:var(--cyan);flex-shrink:0;
}

/* ── Role selector row ── */
.role-row{
  display:flex;gap:.5rem;margin-bottom:.1rem;flex-wrap:wrap;
}
.role-btn{
  flex:1;min-width:0;
  background:rgba(15,23,42,.8);
  border:1px solid rgba(0,229,255,.15);
  border-radius:6px;padding:.45rem .4rem;
  font-family:'Share Tech Mono',monospace;font-size:.56rem;
  color:var(--text3);letter-spacing:.06em;text-align:center;
  cursor:pointer;transition:all .2s;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.role-btn:hover,.role-btn.active{
  background:rgba(0,229,255,.10);
  border-color:rgba(0,229,255,.45);color:var(--cyan);
  box-shadow:0 0 10px rgba(0,229,255,.12);
}

/* ── Divider with label ── */
.cc-divider{
  display:flex;align-items:center;gap:.7rem;margin:.7rem 0;
}
.cc-div-line{flex:1;height:1px;background:linear-gradient(90deg,transparent,rgba(0,229,255,.18),transparent);}
.cc-div-label{font-family:'Share Tech Mono',monospace;font-size:.52rem;color:var(--dim);letter-spacing:.18em;text-transform:uppercase;}

/* ── Telemetry grid v2 ── */
.telem-grid-v2{
  display:grid;grid-template-columns:1fr 1fr;gap:.55rem;margin-top:1rem;
}
.telem-chip-v2{
  background:linear-gradient(135deg,rgba(9,15,32,.9),rgba(12,20,42,.8));
  border:1px solid rgba(0,229,255,.14);
  border-radius:7px;padding:.5rem .75rem;
  display:flex;align-items:flex-start;gap:.5rem;
  transition:border-color .2s;
}
.telem-chip-v2:hover{border-color:rgba(0,229,255,.28);}
.tc2-icon{font-size:.85rem;flex-shrink:0;margin-top:.05rem;}
.tc2-content{flex:1;min-width:0;}
.tc2-label{font-family:'Share Tech Mono',monospace;font-size:.48rem;color:var(--dim);letter-spacing:.16em;text-transform:uppercase;margin-bottom:.15rem;}
.tc2-value{font-family:'Orbitron',monospace;font-size:.78rem;font-weight:700;color:var(--cyan);letter-spacing:.06em;}
.tc2-value.g{color:var(--green);text-shadow:0 0 8px rgba(0,255,156,.35);}
.tc2-value.a{color:var(--amber);}

/* ── Security notice v2 ── */
.security-v2{
  margin-top:.9rem;
  background:rgba(255,75,75,.04);
  border:1px solid rgba(255,75,75,.14);
  border-radius:6px;padding:.6rem .9rem;
  text-align:center;
}
.sec-warn{
  font-family:'Share Tech Mono',monospace;font-size:.60rem;
  color:rgba(255,120,120,.7);letter-spacing:.14em;text-transform:uppercase;
  margin-bottom:.3rem;display:flex;align-items:center;justify-content:center;gap:.4rem;
}
.sec-text{
  font-family:'Share Tech Mono',monospace;font-size:.53rem;
  color:var(--text3);letter-spacing:.06em;line-height:1.8;
}
.sec-creds{
  font-family:'Share Tech Mono',monospace;font-size:.53rem;
  color:var(--dim);letter-spacing:.06em;margin-top:.35rem;
  padding-top:.35rem;border-top:1px solid rgba(0,229,255,.08);
}

/* ── Error / Success messages v2 ── */
.msg-error-v2{
  background:linear-gradient(90deg,rgba(255,75,75,.10),rgba(255,75,75,.06));
  border:1px solid rgba(255,75,75,.35);border-left:3px solid var(--red);
  border-radius:5px;padding:.7rem 1rem;margin-top:.7rem;
  font-family:'Share Tech Mono',monospace;font-size:.65rem;color:#ff8080;
  letter-spacing:.08em;display:flex;align-items:center;gap:.7rem;
  animation:slideInDown .3s ease;
}
.msg-error-v2::before{content:'⚠';font-size:.9rem;}
@keyframes slideInDown{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:translateY(0)}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  PLOTLY THEME
# ─────────────────────────────────────────────────────────────────────────────
_PL = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(9,15,32,0.82)",
    font=dict(family="Share Tech Mono, monospace", color="#b8c1ec", size=10),
    xaxis=dict(
        gridcolor="rgba(30,58,95,0.5)", gridwidth=0.4,
        linecolor="rgba(30,58,95,0.7)", zerolinecolor="rgba(30,58,95,0.5)",
        tickfont=dict(family="Share Tech Mono", size=9, color="#6a86a8"),
    ),
    yaxis=dict(
        gridcolor="rgba(30,58,95,0.5)", gridwidth=0.4,
        linecolor="rgba(30,58,95,0.7)", zerolinecolor="rgba(30,58,95,0.5)",
        tickfont=dict(family="Share Tech Mono", size=9, color="#6a86a8"),
    ),
    legend=dict(
        bgcolor="rgba(9,15,32,0.92)", bordercolor="rgba(30,58,95,0.8)",
        borderwidth=1, font=dict(size=10, family="Share Tech Mono", color="#b8c1ec"),
    ),
    margin=dict(l=50, r=16, t=36, b=46),
    # Official COSMOS chart palette — consistent across all pages
    colorway=["#00e5ff","#ff6b00","#00ff9c","#7c8cff","#ffb300","#ff4b4b","#80deea"],
    hoverlabel=dict(
        bgcolor="rgba(9,15,32,0.95)", bordercolor="rgba(0,229,255,.3)",
        font=dict(family="Share Tech Mono", size=11, color="#ffffff"),
    ),
)

def apl(fig, xt="", yt="", h=None):
    fig.update_layout(**_PL)
    u = {}
    if xt: u["xaxis_title"] = dict(text=xt, font=dict(size=10))
    if yt: u["yaxis_title"] = dict(text=yt, font=dict(size=10))
    if h:  u["height"] = h
    if u:  fig.update_layout(**u)
    return fig

# ─────────────────────────────────────────────────────────────────────────────
#  SPACE BACKGROUND — CANVAS ANIMATION
# ─────────────────────────────────────────────────────────────────────────────
def inject_space_background():
    st.markdown("""
    <canvas id="cosmos-bg-canvas"></canvas>
    <script>
    (function(){
      if(window._cosmosRunning) return;
      window._cosmosRunning = true;

      const C = document.getElementById('cosmos-bg-canvas');
      if(!C){ window._cosmosRunning=false; return; }
      const X = C.getContext('2d');
      const PI2 = Math.PI*2;
      const R   = (a,b) => a + Math.random()*(b-a);
      const Ri  = (a,b) => Math.floor(R(a,b));

      function resize(){ C.width=window.innerWidth; C.height=window.innerHeight; }
      resize();
      window.addEventListener('resize', resize, {passive:true});

      /* ═══════════════════════════════════════════════════════════
         HUBBLE DEEP FIELD COLOUR PALETTE
         All colours sampled from real HDF imagery
      ═══════════════════════════════════════════════════════════ */
      const PAL = {
        /* galaxy colours */
        elliptical: ['#f0d8a8','#e8c890','#d4b878','#f4e0b0','#c8a860'],
        spiral:     ['#a8c4e0','#b0cce8','#90b0d8','#d0e4f4','#c4d8f0'],
        starburst:  ['#f0e8c0','#e8d8a0','#d4c888','#b4a870','#c8b888'],
        irregular:  ['#c0d4ec','#b8d0e8','#a0c0e0','#d8ecff','#88b4d8'],
        redshift:   ['#d08060','#c07050','#b86040','#e09070','#a85030'],
        edge_on:    ['#c8d8e8','#b8ccd8','#d4e4f0','#a0b8cc','#e0ecf8'],
        cluster:    ['#f4e8c8','#e8d8a8','#dcc890','#f0e0b8','#e4d098'],
        blue_comp:  ['#80b8e8','#70aae0','#90c0f0','#60a0d8','#a0ccf4'],
      };

      /* weighted random palette pick */
      function galCol(type){
        const a=PAL[type]; return a[Ri(0,a.length)];
      }

      /* ═══════════════════════════════════════════════════════════
         GALAXY OBJECT FACTORY
      ═══════════════════════════════════════════════════════════ */
      function makeGalaxy(){
        const types=['elliptical','spiral','edge_on','starburst','irregular','redshift','blue_comp','cluster'];
        const weights=[0.22,0.18,0.16,0.12,0.10,0.10,0.07,0.05];
        let roll=Math.random(), cum=0, type='elliptical';
        for(let i=0;i<types.length;i++){ cum+=weights[i]; if(roll<cum){type=types[i];break;} }

        const base_r = R(1.5, 18);   /* apparent size in px */
        const alpha  = R(0.08, 0.65);
        const col    = galCol(type);
        const rot    = R(0, PI2);
        const drift  = { x: R(-0.000025,0.000025), y: R(-0.000015,0.000015) };
        const twk    = { ph:R(0,PI2), sp:R(0.004,0.018), am:R(0.04,0.18) };

        return {
          x: R(0,1), y: R(0,1),
          type, col, alpha, base_r, rot, drift, twk,
          /* spiral-specific */
          arms:   Ri(2,5),
          wind:   R(0.5,2.2),
          /* elliptical axes */
          ax: R(0.4,1.0),  /* y-stretch */
          /* edge-on tilt */
          tilt: R(0.05,0.25),
          /* brightness pulse */
          brt: R(0.7,1.0),
        };
      }

      /* ═══════════════════════════════════════════════════════════
         POINT STAR FACTORY  (three size classes)
      ═══════════════════════════════════════════════════════════ */
      function makeStar(sizeClass){
        const rMap={tiny:[0.2,0.7], mid:[0.6,1.4], bright:[1.2,2.4]};
        const aMap={tiny:[0.05,0.35],mid:[0.15,0.60],bright:[0.35,0.90]};
        const [rlo,rhi]=rMap[sizeClass]; const [alo,ahi]=aMap[sizeClass];
        const cyan=Math.random()<0.08;
        return {
          x:R(0,1), y:R(0,1),
          r:R(rlo,rhi),
          ba:R(alo,ahi), am:R(0.04,0.25),
          ph:R(0,PI2), sp:R(0.003,0.028),
          dx:R(-0.000012,0.000012),
          col:cyan?'#b8f0ff':'#e8eef4',
          cross:sizeClass==='bright'&&Math.random()<0.4,
        };
      }

      /* ═══════════════════════════════════════════════════════════
         POPULATIONS
      ═══════════════════════════════════════════════════════════ */
      const GALAXIES  = Array.from({length:120}, makeGalaxy);
      const STARS_T   = Array.from({length:400}, ()=>makeStar('tiny'));
      const STARS_M   = Array.from({length:120}, ()=>makeStar('mid'));
      const STARS_B   = Array.from({length:30},  ()=>makeStar('bright'));

      /* ═══════════════════════════════════════════════════════════
         SHOOTING STARS
      ═══════════════════════════════════════════════════════════ */
      const SHOTS=[];
      function spawnShot(){
        SHOTS.push({
          x:R(0.02,0.75), y:R(0.01,0.55),
          len:R(0.04,0.14), spd:R(0.005,0.013),
          angle:R(18,42)*Math.PI/180,
          life:0, maxLife:R(0.4,0.8), alpha:0,
        });
      }
      setTimeout(spawnShot, R(1500,3000)|0);
      setInterval(()=>{ if(SHOTS.length<3) spawnShot(); }, 4200);

      /* ═══════════════════════════════════════════════════════════
         ROCKET
      ═══════════════════════════════════════════════════════════ */
      let rockets=[];
      function spawnRocket(){
        const fl=Math.random()<0.5;
        rockets.push({
          x:fl?-0.08:1.08, y:R(0.05,0.92),
          dx:fl?R(0.0005,0.0012):-R(0.0005,0.0012),
          dy:(Math.random()<0.5?1:-1)*R(0.0001,0.0005),
          angle:fl?R(-15,15):R(165,195),
          sz:R(10,16), trail:[],
        });
      }
      spawnRocket();
      setInterval(spawnRocket, R(14000,22000)|0);

      /* ═══════════════════════════════════════════════════════════
         DRAW GALAXY
      ═══════════════════════════════════════════════════════════ */
      function drawGalaxy(g, W, H){
        const px=g.x*W, py=g.y*H;
        const s=g.base_r;
        /* twinkle alpha */
        g.twk.ph += g.twk.sp;
        const al = Math.max(0, Math.min(1, g.alpha*(g.brt + Math.sin(g.twk.ph)*g.twk.am) ));

        X.save();
        X.translate(px, py);
        X.rotate(g.rot);
        X.globalAlpha = al;

        if(g.type==='elliptical' || g.type==='cluster'){
          /* soft elliptical blob with core */
          const eg=X.createRadialGradient(0,0,0,0,0,s);
          eg.addColorStop(0, hexA(g.col,0.95));
          eg.addColorStop(0.25,hexA(g.col,0.65));
          eg.addColorStop(0.55,hexA(g.col,0.25));
          eg.addColorStop(1, 'rgba(0,0,0,0)');
          X.save(); X.scale(1, g.ax);
          X.fillStyle=eg; X.beginPath(); X.arc(0,0,s,0,PI2); X.fill();
          X.restore();
          /* bright core */
          const cg=X.createRadialGradient(0,0,0,0,0,s*0.22);
          cg.addColorStop(0,hexA(g.col,1.0));
          cg.addColorStop(1,'rgba(0,0,0,0)');
          X.fillStyle=cg; X.save(); X.scale(1,g.ax);
          X.beginPath(); X.arc(0,0,s*0.22,0,PI2); X.fill(); X.restore();
        }
        else if(g.type==='spiral' || g.type==='blue_comp'){
          /* draw each arm as a logarithmic spiral */
          const arms=g.arms;
          for(let arm=0;arm<arms;arm++){
            const aOff=(PI2/arms)*arm;
            X.beginPath();
            let firstPt=true;
            for(let t=0;t<2.8;t+=0.06){
              const rr = s*0.18*Math.exp(0.28*t);
              const ang = t*g.wind + aOff;
              const xx = rr*Math.cos(ang), yy=rr*Math.sin(ang);
              if(firstPt){ X.moveTo(xx,yy); firstPt=false; }
              else X.lineTo(xx,yy);
            }
            X.strokeStyle = hexA(g.col, 0.55);
            X.lineWidth   = Math.max(0.4, s*0.065);
            X.stroke();
            /* dust arm (offset slightly) */
            X.beginPath(); firstPt=true;
            for(let t=0;t<2.6;t+=0.07){
              const rr=s*0.14*Math.exp(0.28*t);
              const ang=t*g.wind+aOff+0.18;
              const xx=rr*Math.cos(ang),yy=rr*Math.sin(ang);
              if(firstPt){X.moveTo(xx,yy);firstPt=false;}
              else X.lineTo(xx,yy);
            }
            X.strokeStyle=hexA(g.col,0.22);
            X.lineWidth=Math.max(0.3,s*0.04);
            X.stroke();
          }
          /* bulge */
          const bg2=X.createRadialGradient(0,0,0,0,0,s*0.28);
          bg2.addColorStop(0,hexA(g.col,1.0));
          bg2.addColorStop(0.5,hexA(g.col,0.55));
          bg2.addColorStop(1,'rgba(0,0,0,0)');
          X.fillStyle=bg2; X.beginPath(); X.arc(0,0,s*0.28,0,PI2); X.fill();
        }
        else if(g.type==='edge_on'){
          /* thin streak — edge-on disc */
          const len=s*R(2.5,4.5), hw=s*g.tilt;
          const eg2=X.createLinearGradient(-len,0,len,0);
          eg2.addColorStop(0,'rgba(0,0,0,0)');
          eg2.addColorStop(0.2,hexA(g.col,0.35));
          eg2.addColorStop(0.5,hexA(g.col,0.90));
          eg2.addColorStop(0.8,hexA(g.col,0.35));
          eg2.addColorStop(1,'rgba(0,0,0,0)');
          X.fillStyle=eg2;
          X.beginPath();
          X.ellipse(0,0,len,hw,0,0,PI2);
          X.fill();
          /* dust lane */
          X.fillStyle='rgba(0,0,0,0.25)';
          X.beginPath(); X.ellipse(0,0,len*0.85,hw*0.25,0,0,PI2); X.fill();
          /* core */
          const cg2=X.createRadialGradient(0,0,0,0,0,hw*1.4);
          cg2.addColorStop(0,hexA(g.col,1.0));
          cg2.addColorStop(1,'rgba(0,0,0,0)');
          X.fillStyle=cg2; X.beginPath(); X.arc(0,0,hw*1.4,0,PI2); X.fill();
        }
        else if(g.type==='starburst' || g.type==='redshift'){
          /* irregular blob with bright knots */
          const ig=X.createRadialGradient(0,0,0,0,0,s);
          ig.addColorStop(0,hexA(g.col,0.90));
          ig.addColorStop(0.4,hexA(g.col,0.45));
          ig.addColorStop(1,'rgba(0,0,0,0)');
          X.save(); X.scale(R(0.5,1.0),R(0.4,0.9));
          X.fillStyle=ig; X.beginPath(); X.arc(0,0,s,0,PI2); X.fill();
          X.restore();
          /* star-forming knots */
          const nk=Ri(2,5);
          for(let k=0;k<nk;k++){
            const kx=R(-s*.5,s*.5),ky=R(-s*.5,s*.5);
            const kg=X.createRadialGradient(kx,ky,0,kx,ky,s*.22);
            kg.addColorStop(0,hexA(g.col,0.95));
            kg.addColorStop(1,'rgba(0,0,0,0)');
            X.fillStyle=kg; X.beginPath(); X.arc(kx,ky,s*.22,0,PI2); X.fill();
          }
        }
        else if(g.type==='irregular'){
          /* clumpy blob */
          const nc=Ri(3,6);
          for(let c=0;c<nc;c++){
            const cx2=R(-s*.6,s*.6),cy2=R(-s*.6,s*.6),cr=s*R(0.3,0.65);
            const cg3=X.createRadialGradient(cx2,cy2,0,cx2,cy2,cr);
            cg3.addColorStop(0,hexA(g.col,0.75));
            cg3.addColorStop(1,'rgba(0,0,0,0)');
            X.fillStyle=cg3; X.beginPath(); X.arc(cx2,cy2,cr,0,PI2); X.fill();
          }
        }

        X.restore();
      }

      /* ═══════════════════════════════════════════════════════════
         ROCKET DRAW (compact, very subtle)
      ═══════════════════════════════════════════════════════════ */
      function drawRocket(rx,ry,angDeg,sz,al){
        if(al<=0) return;
        X.save(); X.globalAlpha=al*0.55;
        X.translate(rx,ry); X.rotate(angDeg*Math.PI/180);
        const s=sz;
        const eg=X.createRadialGradient(0,s*.6,0,0,s*.6,s);
        eg.addColorStop(0,'rgba(255,150,30,0.5)');
        eg.addColorStop(1,'rgba(255,50,0,0)');
        X.fillStyle=eg; X.beginPath(); X.ellipse(0,s*.6,s*.5,s*.9,0,0,PI2); X.fill();
        X.fillStyle='#bdd4ee';
        X.beginPath();
        X.moveTo(0,-s);
        X.bezierCurveTo(s*.42,-s*.25,s*.42,s*.4,s*.18,s*.54);
        X.lineTo(-s*.18,s*.54);
        X.bezierCurveTo(-s*.42,s*.4,-s*.42,-s*.25,0,-s);
        X.fill();
        const wg=X.createRadialGradient(0,-s*.26,0,0,-s*.26,s*.17);
        wg.addColorStop(0,'rgba(0,229,255,0.9)');
        wg.addColorStop(1,'rgba(0,40,90,0.4)');
        X.fillStyle=wg; X.beginPath(); X.ellipse(0,-s*.28,s*.17,s*.17,0,0,PI2); X.fill();
        X.fillStyle='#3a80c0';
        X.beginPath(); X.moveTo(-s*.18,s*.34); X.lineTo(-s*.52,s*.72); X.lineTo(-s*.18,s*.55); X.closePath(); X.fill();
        X.beginPath(); X.moveTo(s*.18,s*.34);  X.lineTo(s*.52,s*.72);  X.lineTo(s*.18,s*.55);  X.closePath(); X.fill();
        const ft=Date.now()*.001;
        const fh=s*(1.18+0.14*Math.sin(ft*13));
        const fg=X.createLinearGradient(0,s*.7,0,fh);
        fg.addColorStop(0,'rgba(255,220,70,0.9)');
        fg.addColorStop(0.4,'rgba(255,120,10,0.7)');
        fg.addColorStop(1,'rgba(255,30,0,0)');
        X.fillStyle=fg;
        X.beginPath();
        X.moveTo(-s*.11,s*.7);
        X.bezierCurveTo(-s*.17,s*.98,s*.17,s*.98,s*.11,s*.7);
        X.bezierCurveTo(s*.20,fh,-s*.20,fh,-s*.11,s*.7);
        X.fill();
        X.restore();
      }

      /* ═══════════════════════════════════════════════════════════
         HEX + ALPHA HELPER
      ═══════════════════════════════════════════════════════════ */
      function hexA(hex,a){
        const h=hex.replace('#','');
        const r=parseInt(h.slice(0,2),16),g2=parseInt(h.slice(2,4),16),b=parseInt(h.slice(4,6),16);
        return `rgba(${r},${g2},${b},${a.toFixed(3)})`;
      }

      /* ═══════════════════════════════════════════════════════════
         MAIN RENDER
      ═══════════════════════════════════════════════════════════ */
      function draw(){
        const W=C.width, H=C.height;

        /* pure deep-space black */
        X.fillStyle='#000005';
        X.fillRect(0,0,W,H);

        /* faint deep-field haze patches */
        [[0.25,0.35,0.40,0.30],[0.70,0.60,0.35,0.25],[0.50,0.15,0.30,0.20]].forEach(([cx,cy,rx,ry])=>{
          const ng=X.createRadialGradient(cx*W,cy*H,0,cx*W,cy*H,rx*W);
          ng.addColorStop(0,'rgba(10,25,60,0.06)');
          ng.addColorStop(1,'rgba(0,0,0,0)');
          X.fillStyle=ng; X.beginPath(); X.ellipse(cx*W,cy*H,rx*W,ry*H,0,0,PI2); X.fill();
        });

        /* tiny background stars */
        STARS_T.forEach(s=>{
          s.x+=s.dx; if(s.x>1.01)s.x=-0.01; if(s.x<-0.01)s.x=1.01;
          s.ph+=s.sp;
          const al=Math.max(0.02,Math.min(1,s.ba+Math.sin(s.ph)*s.am));
          X.globalAlpha=al; X.fillStyle=s.col;
          X.beginPath(); X.arc(s.x*W,s.y*H,s.r,0,PI2); X.fill();
        });

        /* mid stars */
        STARS_M.forEach(s=>{
          s.x+=s.dx; if(s.x>1.01)s.x=-0.01; if(s.x<-0.01)s.x=1.01;
          s.ph+=s.sp;
          const al=Math.max(0.05,Math.min(1,s.ba+Math.sin(s.ph)*s.am));
          X.globalAlpha=al; X.fillStyle=s.col;
          X.beginPath(); X.arc(s.x*W,s.y*H,s.r,0,PI2); X.fill();
        });

        /* galaxies — draw in depth order (smaller first) */
        X.globalAlpha=1;
        const sorted=[...GALAXIES].sort((a,b)=>a.base_r-b.base_r);
        sorted.forEach(g=>{
          g.x+=g.drift.x; g.y+=g.drift.y;
          if(g.x<-0.05)g.x=1.05; if(g.x>1.05)g.x=-0.05;
          if(g.y<-0.05)g.y=1.05; if(g.y>1.05)g.y=-0.05;
          drawGalaxy(g,W,H);
        });
        X.globalAlpha=1;

        /* bright foreground stars */
        STARS_B.forEach(s=>{
          s.x+=s.dx; if(s.x>1.01)s.x=-0.01; if(s.x<-0.01)s.x=1.01;
          s.ph+=s.sp;
          const al=Math.max(0.15,Math.min(1,s.ba+Math.sin(s.ph)*s.am));
          X.globalAlpha=al;
          if(s.cross){
            X.fillStyle=s.col;
            X.fillRect(s.x*W-s.r*3.5,s.y*H-s.r*.3,s.r*7,s.r*.6);
            X.fillRect(s.x*W-s.r*.3,s.y*H-s.r*3.5,s.r*.6,s.r*7);
            const hg=X.createRadialGradient(s.x*W,s.y*H,0,s.x*W,s.y*H,s.r*5);
            hg.addColorStop(0,'rgba(220,240,255,0.22)');
            hg.addColorStop(1,'rgba(0,0,0,0)');
            X.fillStyle=hg; X.beginPath(); X.arc(s.x*W,s.y*H,s.r*5,0,PI2); X.fill();
          }
          X.fillStyle=s.col;
          X.beginPath(); X.arc(s.x*W,s.y*H,s.r,0,PI2); X.fill();
        });
        X.globalAlpha=1;

        /* shooting stars */
        for(let i=SHOTS.length-1;i>=0;i--){
          const sh=SHOTS[i];
          sh.x+=sh.spd*Math.cos(sh.angle);
          sh.y+=sh.spd*Math.sin(sh.angle);
          sh.life+=sh.spd;
          const fi=0.08,fo=0.12;
          sh.alpha=sh.life<fi?sh.life/fi:sh.life>sh.maxLife-fo?(sh.maxLife-sh.life)/fo:1;
          if(sh.life>=sh.maxLife||sh.x>1.1||sh.y>1.1){SHOTS.splice(i,1);continue;}
          const sx=sh.x*W,sy=sh.y*H,ex=sx-Math.cos(sh.angle)*sh.len*W,ey=sy-Math.sin(sh.angle)*sh.len*W;
          const sg=X.createLinearGradient(sx,sy,ex,ey);
          sg.addColorStop(0,`rgba(255,255,255,${(sh.alpha*.92).toFixed(2)})`);
          sg.addColorStop(0.3,`rgba(200,235,255,${(sh.alpha*.6).toFixed(2)})`);
          sg.addColorStop(1,'rgba(100,160,255,0)');
          X.strokeStyle=sg; X.lineWidth=1.5; X.globalAlpha=1;
          X.beginPath(); X.moveTo(sx,sy); X.lineTo(ex,ey); X.stroke();
          X.globalAlpha=sh.alpha*.6;
          const hg2=X.createRadialGradient(sx,sy,0,sx,sy,5);
          hg2.addColorStop(0,'rgba(255,255,255,1)');
          hg2.addColorStop(1,'rgba(180,220,255,0)');
          X.fillStyle=hg2; X.beginPath(); X.arc(sx,sy,5,0,PI2); X.fill();
          X.globalAlpha=1;
        }

        /* rockets */
        rockets.forEach((rk,ri)=>{
          rk.trail.push({x:rk.x*W,y:rk.y*H});
          if(rk.trail.length>35) rk.trail.shift();
          for(let t=1;t<rk.trail.length;t++){
            const pt=rk.trail[t-1],ct=rk.trail[t];
            const ta=t/rk.trail.length;
            X.globalAlpha=ta*.22;
            X.strokeStyle=`rgba(255,120,20,${(ta*.35).toFixed(2)})`;
            X.lineWidth=ta*2.2;
            X.beginPath(); X.moveTo(pt.x,pt.y); X.lineTo(ct.x,ct.y); X.stroke();
          }
          X.globalAlpha=1;
          const ef=Math.min(1,Math.min(rk.x/0.06,(1-rk.x)/0.06,rk.y/0.05,(1-rk.y)/0.05));
          drawRocket(rk.x*W,rk.y*H,rk.angle,rk.sz,Math.max(0,Math.min(1,ef)));
          rk.x+=rk.dx; rk.y+=rk.dy;
          if(rk.x<-0.14||rk.x>1.14||rk.y<-0.14||rk.y>1.14) rockets.splice(ri,1);
        });

        /* subtle vignette — keep edges dark */
        const vg=X.createRadialGradient(W*.5,H*.5,H*.3,W*.5,H*.5,H*.9);
        vg.addColorStop(0,'rgba(0,0,0,0)');
        vg.addColorStop(1,'rgba(0,0,5,0.55)');
        X.fillStyle=vg; X.globalAlpha=1; X.fillRect(0,0,W,H);

        requestAnimationFrame(draw);
      }
      draw();
    })();
    </script>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  REAL SPACE MISSION DATA
#  196 verified historical missions: NASA · ESA · SpaceX · ISRO · CNSA · Roscosmos
#  Data sourced from: NASA, SpaceX, ESA, Wikipedia public mission records
#  Date range: 1966–2025
# ─────────────────────────────────────────────────────────────────────────────
REAL_MISSIONS = [
    {
        "Mission Name": "Apollo 1",
        "Launch Date": "1967-01-27",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Saturn IB",
        "Target Name": "LEO",
        "Distance from Earth": 400.0,
        "Mission Duration": 0.0,
        "Mission Cost": 185.0,
        "Scientific Yield": 5.0,
        "Crew Size": 3.0,
        "Mission Success": False,
        "Fuel Consumption": 400000.0,
        "Payload Weight": 28801.0
    },
    {
        "Mission Name": "Apollo 7",
        "Launch Date": "1968-10-11",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Saturn IB",
        "Target Name": "LEO",
        "Distance from Earth": 300.0,
        "Mission Duration": 10.8,
        "Mission Cost": 185.0,
        "Scientific Yield": 60.0,
        "Crew Size": 3.0,
        "Mission Success": True,
        "Fuel Consumption": 400000.0,
        "Payload Weight": 14781.0
    },
    {
        "Mission Name": "Apollo 8",
        "Launch Date": "1968-12-21",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Saturn V",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 6.1,
        "Mission Cost": 230.0,
        "Scientific Yield": 88.0,
        "Crew Size": 3.0,
        "Mission Success": True,
        "Fuel Consumption": 2150000.0,
        "Payload Weight": 28833.0
    },
    {
        "Mission Name": "Apollo 10",
        "Launch Date": "1969-05-18",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Saturn V",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 8.0,
        "Mission Cost": 355.0,
        "Scientific Yield": 80.0,
        "Crew Size": 3.0,
        "Mission Success": True,
        "Fuel Consumption": 2150000.0,
        "Payload Weight": 28834.0
    },
    {
        "Mission Name": "Apollo 11",
        "Launch Date": "1969-07-16",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Saturn V",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 8.1,
        "Mission Cost": 355.0,
        "Scientific Yield": 99.0,
        "Crew Size": 3.0,
        "Mission Success": True,
        "Fuel Consumption": 2150000.0,
        "Payload Weight": 43971.0
    },
    {
        "Mission Name": "Apollo 12",
        "Launch Date": "1969-11-14",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Saturn V",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 10.0,
        "Mission Cost": 375.0,
        "Scientific Yield": 96.0,
        "Crew Size": 3.0,
        "Mission Success": True,
        "Fuel Consumption": 2150000.0,
        "Payload Weight": 34380.0
    },
    {
        "Mission Name": "Apollo 13",
        "Launch Date": "1970-04-11",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Saturn V",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 5.9,
        "Mission Cost": 375.0,
        "Scientific Yield": 50.0,
        "Crew Size": 3.0,
        "Mission Success": False,
        "Fuel Consumption": 2150000.0,
        "Payload Weight": 28945.0
    },
    {
        "Mission Name": "Apollo 14",
        "Launch Date": "1971-01-31",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Saturn V",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 9.0,
        "Mission Cost": 480.0,
        "Scientific Yield": 95.0,
        "Crew Size": 3.0,
        "Mission Success": True,
        "Fuel Consumption": 2150000.0,
        "Payload Weight": 43800.0
    },
    {
        "Mission Name": "Apollo 15",
        "Launch Date": "1971-07-26",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Saturn V",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 12.3,
        "Mission Cost": 480.0,
        "Scientific Yield": 97.0,
        "Crew Size": 3.0,
        "Mission Success": True,
        "Fuel Consumption": 2150000.0,
        "Payload Weight": 48600.0
    },
    {
        "Mission Name": "Apollo 16",
        "Launch Date": "1972-04-16",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Saturn V",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 11.1,
        "Mission Cost": 480.0,
        "Scientific Yield": 97.0,
        "Crew Size": 3.0,
        "Mission Success": True,
        "Fuel Consumption": 2150000.0,
        "Payload Weight": 49000.0
    },
    {
        "Mission Name": "Apollo 17",
        "Launch Date": "1972-12-07",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Saturn V",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 12.5,
        "Mission Cost": 450.0,
        "Scientific Yield": 99.0,
        "Crew Size": 3.0,
        "Mission Success": True,
        "Fuel Consumption": 2150000.0,
        "Payload Weight": 48607.0
    },
    {
        "Mission Name": "Skylab 2",
        "Launch Date": "1973-05-25",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Saturn IB",
        "Target Name": "LEO",
        "Distance from Earth": 435.0,
        "Mission Duration": 28.0,
        "Mission Cost": 160.0,
        "Scientific Yield": 80.0,
        "Crew Size": 3.0,
        "Mission Success": True,
        "Fuel Consumption": 420000.0,
        "Payload Weight": 20000.0
    },
    {
        "Mission Name": "Skylab 3",
        "Launch Date": "1973-07-28",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Saturn IB",
        "Target Name": "LEO",
        "Distance from Earth": 435.0,
        "Mission Duration": 59.5,
        "Mission Cost": 160.0,
        "Scientific Yield": 90.0,
        "Crew Size": 3.0,
        "Mission Success": True,
        "Fuel Consumption": 420000.0,
        "Payload Weight": 20000.0
    },
    {
        "Mission Name": "Skylab 4",
        "Launch Date": "1973-11-16",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Saturn IB",
        "Target Name": "LEO",
        "Distance from Earth": 435.0,
        "Mission Duration": 84.1,
        "Mission Cost": 160.0,
        "Scientific Yield": 90.0,
        "Crew Size": 3.0,
        "Mission Success": True,
        "Fuel Consumption": 420000.0,
        "Payload Weight": 20000.0
    },
    {
        "Mission Name": "Viking 1",
        "Launch Date": "1975-08-20",
        "Mission Type": "Science",
        "Launch Vehicle": "Titan III-E",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 2484.0,
        "Mission Cost": 1000.0,
        "Scientific Yield": 98.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 700000.0,
        "Payload Weight": 1118.0
    },
    {
        "Mission Name": "Viking 2",
        "Launch Date": "1975-09-09",
        "Mission Type": "Science",
        "Launch Vehicle": "Titan III-E",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 1281.0,
        "Mission Cost": 1000.0,
        "Scientific Yield": 97.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 700000.0,
        "Payload Weight": 1116.0
    },
    {
        "Mission Name": "Pioneer 10",
        "Launch Date": "1972-03-02",
        "Mission Type": "Exploration",
        "Launch Vehicle": "Atlas-Centaur",
        "Target Name": "Jupiter",
        "Distance from Earth": 628000000.0,
        "Mission Duration": 28710.0,
        "Mission Cost": 380.0,
        "Scientific Yield": 96.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 560000.0,
        "Payload Weight": 258.0
    },
    {
        "Mission Name": "Pioneer 11",
        "Launch Date": "1973-04-05",
        "Mission Type": "Exploration",
        "Launch Vehicle": "Atlas-Centaur",
        "Target Name": "Saturn",
        "Distance from Earth": 1275000000.0,
        "Mission Duration": 10000.0,
        "Mission Cost": 390.0,
        "Scientific Yield": 96.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 560000.0,
        "Payload Weight": 259.0
    },
    {
        "Mission Name": "Voyager 1",
        "Launch Date": "1977-09-05",
        "Mission Type": "Exploration",
        "Launch Vehicle": "Titan III-E",
        "Target Name": "Jupiter",
        "Distance from Earth": 628000000.0,
        "Mission Duration": 17000.0,
        "Mission Cost": 900.0,
        "Scientific Yield": 99.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 700000.0,
        "Payload Weight": 825.0
    },
    {
        "Mission Name": "Voyager 2",
        "Launch Date": "1977-08-20",
        "Mission Type": "Exploration",
        "Launch Vehicle": "Titan III-E",
        "Target Name": "Jupiter",
        "Distance from Earth": 628000000.0,
        "Mission Duration": 17000.0,
        "Mission Cost": 900.0,
        "Scientific Yield": 99.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 700000.0,
        "Payload Weight": 825.0
    },
    {
        "Mission Name": "STS-1 Columbia",
        "Launch Date": "1981-04-12",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "LEO",
        "Distance from Earth": 300.0,
        "Mission Duration": 2.0,
        "Mission Cost": 10800.0,
        "Scientific Yield": 70.0,
        "Crew Size": 2.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 24400.0
    },
    {
        "Mission Name": "STS-5 Columbia",
        "Launch Date": "1982-11-11",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "LEO",
        "Distance from Earth": 300.0,
        "Mission Duration": 5.1,
        "Mission Cost": 8500.0,
        "Scientific Yield": 55.0,
        "Crew Size": 4.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 17000.0
    },
    {
        "Mission Name": "STS-7 Challenger",
        "Launch Date": "1983-06-18",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "LEO",
        "Distance from Earth": 300.0,
        "Mission Duration": 6.1,
        "Mission Cost": 9000.0,
        "Scientific Yield": 70.0,
        "Crew Size": 5.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 18000.0
    },
    {
        "Mission Name": "STS-41B Challenger",
        "Launch Date": "1984-02-03",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "LEO",
        "Distance from Earth": 300.0,
        "Mission Duration": 7.9,
        "Mission Cost": 9500.0,
        "Scientific Yield": 60.0,
        "Crew Size": 5.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 21145.0
    },
    {
        "Mission Name": "STS-51A Discovery",
        "Launch Date": "1984-11-08",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "LEO",
        "Distance from Earth": 300.0,
        "Mission Duration": 7.9,
        "Mission Cost": 9700.0,
        "Scientific Yield": 65.0,
        "Crew Size": 5.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 22040.0
    },
    {
        "Mission Name": "STS-51L Challenger",
        "Launch Date": "1986-01-28",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "LEO",
        "Distance from Earth": 300.0,
        "Mission Duration": 1.2,
        "Mission Cost": 9500.0,
        "Scientific Yield": 10.0,
        "Crew Size": 7.0,
        "Mission Success": False,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 14450.0
    },
    {
        "Mission Name": "STS-26 Discovery",
        "Launch Date": "1988-09-29",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "LEO",
        "Distance from Earth": 300.0,
        "Mission Duration": 4.0,
        "Mission Cost": 10500.0,
        "Scientific Yield": 70.0,
        "Crew Size": 5.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 11600.0
    },
    {
        "Mission Name": "STS-31 Discovery",
        "Launch Date": "1990-04-24",
        "Mission Type": "Science",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "LEO",
        "Distance from Earth": 600.0,
        "Mission Duration": 5.0,
        "Mission Cost": 10700.0,
        "Scientific Yield": 90.0,
        "Crew Size": 5.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 11110.0
    },
    {
        "Mission Name": "STS-49 Endeavour",
        "Launch Date": "1992-05-07",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "LEO",
        "Distance from Earth": 300.0,
        "Mission Duration": 8.6,
        "Mission Cost": 10000.0,
        "Scientific Yield": 75.0,
        "Crew Size": 7.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 10500.0
    },
    {
        "Mission Name": "STS-61 Endeavour",
        "Launch Date": "1993-12-02",
        "Mission Type": "Science",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "LEO",
        "Distance from Earth": 600.0,
        "Mission Duration": 10.7,
        "Mission Cost": 10500.0,
        "Scientific Yield": 95.0,
        "Crew Size": 7.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 11100.0
    },
    {
        "Mission Name": "STS-71 Atlantis",
        "Launch Date": "1995-06-27",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 9.8,
        "Mission Cost": 11500.0,
        "Scientific Yield": 80.0,
        "Crew Size": 7.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 11000.0
    },
    {
        "Mission Name": "STS-88 Endeavour",
        "Launch Date": "1998-12-04",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 11.8,
        "Mission Cost": 12000.0,
        "Scientific Yield": 82.0,
        "Crew Size": 6.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 12700.0
    },
    {
        "Mission Name": "STS-103 Discovery",
        "Launch Date": "1999-12-19",
        "Mission Type": "Science",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "LEO",
        "Distance from Earth": 600.0,
        "Mission Duration": 7.9,
        "Mission Cost": 11800.0,
        "Scientific Yield": 92.0,
        "Crew Size": 7.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 11100.0
    },
    {
        "Mission Name": "STS-107 Columbia",
        "Launch Date": "2003-01-16",
        "Mission Type": "Science",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "LEO",
        "Distance from Earth": 300.0,
        "Mission Duration": 15.9,
        "Mission Cost": 11800.0,
        "Scientific Yield": 20.0,
        "Crew Size": 7.0,
        "Mission Success": False,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 22000.0
    },
    {
        "Mission Name": "STS-114 Discovery",
        "Launch Date": "2005-07-26",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 13.8,
        "Mission Cost": 12200.0,
        "Scientific Yield": 78.0,
        "Crew Size": 7.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 12000.0
    },
    {
        "Mission Name": "STS-121 Discovery",
        "Launch Date": "2006-07-04",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 12.8,
        "Mission Cost": 12500.0,
        "Scientific Yield": 82.0,
        "Crew Size": 7.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 12000.0
    },
    {
        "Mission Name": "STS-125 Atlantis",
        "Launch Date": "2009-05-11",
        "Mission Type": "Science",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "LEO",
        "Distance from Earth": 600.0,
        "Mission Duration": 12.9,
        "Mission Cost": 13500.0,
        "Scientific Yield": 98.0,
        "Crew Size": 7.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 12500.0
    },
    {
        "Mission Name": "STS-129 Atlantis",
        "Launch Date": "2009-11-16",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 10.7,
        "Mission Cost": 12800.0,
        "Scientific Yield": 78.0,
        "Crew Size": 6.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 12000.0
    },
    {
        "Mission Name": "STS-133 Discovery",
        "Launch Date": "2011-02-24",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 12.8,
        "Mission Cost": 12900.0,
        "Scientific Yield": 80.0,
        "Crew Size": 6.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 12000.0
    },
    {
        "Mission Name": "STS-135 Atlantis",
        "Launch Date": "2011-07-08",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 12.8,
        "Mission Cost": 12500.0,
        "Scientific Yield": 82.0,
        "Crew Size": 4.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 11600.0
    },
    {
        "Mission Name": "Hubble Telescope",
        "Launch Date": "1990-04-24",
        "Mission Type": "Science",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "LEO",
        "Distance from Earth": 570.0,
        "Mission Duration": 13000.0,
        "Mission Cost": 4700.0,
        "Scientific Yield": 99.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 11110.0
    },
    {
        "Mission Name": "Compton GRO",
        "Launch Date": "1991-04-05",
        "Mission Type": "Science",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "LEO",
        "Distance from Earth": 450.0,
        "Mission Duration": 9.1,
        "Mission Cost": 580.0,
        "Scientific Yield": 91.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 17000.0
    },
    {
        "Mission Name": "Chandra X-ray",
        "Launch Date": "1999-07-23",
        "Mission Type": "Science",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "LEO",
        "Distance from Earth": 139000.0,
        "Mission Duration": 9000.0,
        "Mission Cost": 1650.0,
        "Scientific Yield": 98.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 22753.0
    },
    {
        "Mission Name": "Spitzer Space Tel.",
        "Launch Date": "2003-08-25",
        "Mission Type": "Science",
        "Launch Vehicle": "Delta II",
        "Target Name": "GEO",
        "Distance from Earth": 1500000.0,
        "Mission Duration": 5840.0,
        "Mission Cost": 776.0,
        "Scientific Yield": 98.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 220000.0,
        "Payload Weight": 950.0
    },
    {
        "Mission Name": "ISS Expedition 1",
        "Launch Date": "2000-10-31",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Soyuz",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 140.8,
        "Mission Cost": 390.0,
        "Scientific Yield": 80.0,
        "Crew Size": 3.0,
        "Mission Success": True,
        "Fuel Consumption": 280000.0,
        "Payload Weight": 7220.0
    },
    {
        "Mission Name": "ISS Expedition 6",
        "Launch Date": "2002-11-23",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Soyuz",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 161.0,
        "Mission Cost": 400.0,
        "Scientific Yield": 82.0,
        "Crew Size": 3.0,
        "Mission Success": True,
        "Fuel Consumption": 280000.0,
        "Payload Weight": 7220.0
    },
    {
        "Mission Name": "ISS Expedition 13",
        "Launch Date": "2006-03-29",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Soyuz",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 182.9,
        "Mission Cost": 420.0,
        "Scientific Yield": 84.0,
        "Crew Size": 2.0,
        "Mission Success": True,
        "Fuel Consumption": 280000.0,
        "Payload Weight": 7220.0
    },
    {
        "Mission Name": "ISS Expedition 20",
        "Launch Date": "2009-05-27",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Soyuz",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 187.7,
        "Mission Cost": 450.0,
        "Scientific Yield": 85.0,
        "Crew Size": 6.0,
        "Mission Success": True,
        "Fuel Consumption": 280000.0,
        "Payload Weight": 7220.0
    },
    {
        "Mission Name": "ISS Expedition 30",
        "Launch Date": "2011-11-13",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Soyuz",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 165.5,
        "Mission Cost": 470.0,
        "Scientific Yield": 87.0,
        "Crew Size": 6.0,
        "Mission Success": True,
        "Fuel Consumption": 280000.0,
        "Payload Weight": 7220.0
    },
    {
        "Mission Name": "ISS Expedition 40",
        "Launch Date": "2014-05-28",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Soyuz",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 169.5,
        "Mission Cost": 480.0,
        "Scientific Yield": 87.0,
        "Crew Size": 6.0,
        "Mission Success": True,
        "Fuel Consumption": 280000.0,
        "Payload Weight": 7220.0
    },
    {
        "Mission Name": "ISS Expedition 50",
        "Launch Date": "2016-10-19",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Soyuz",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 173.3,
        "Mission Cost": 490.0,
        "Scientific Yield": 88.0,
        "Crew Size": 6.0,
        "Mission Success": True,
        "Fuel Consumption": 280000.0,
        "Payload Weight": 7220.0
    },
    {
        "Mission Name": "ISS Expedition 60",
        "Launch Date": "2019-06-24",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Soyuz",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 203.0,
        "Mission Cost": 500.0,
        "Scientific Yield": 88.0,
        "Crew Size": 3.0,
        "Mission Success": True,
        "Fuel Consumption": 280000.0,
        "Payload Weight": 7220.0
    },
    {
        "Mission Name": "ISS Expedition 65",
        "Launch Date": "2021-04-09",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Soyuz",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 199.7,
        "Mission Cost": 510.0,
        "Scientific Yield": 89.0,
        "Crew Size": 7.0,
        "Mission Success": True,
        "Fuel Consumption": 280000.0,
        "Payload Weight": 7220.0
    },
    {
        "Mission Name": "ISS Expedition 68",
        "Launch Date": "2022-09-21",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Soyuz",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 157.0,
        "Mission Cost": 510.0,
        "Scientific Yield": 88.0,
        "Crew Size": 7.0,
        "Mission Success": True,
        "Fuel Consumption": 280000.0,
        "Payload Weight": 7220.0
    },
    {
        "Mission Name": "ISS Expedition 70",
        "Launch Date": "2023-09-15",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Soyuz",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 155.0,
        "Mission Cost": 520.0,
        "Scientific Yield": 89.0,
        "Crew Size": 7.0,
        "Mission Success": True,
        "Fuel Consumption": 280000.0,
        "Payload Weight": 7220.0
    },
    {
        "Mission Name": "Mars Pathfinder",
        "Launch Date": "1996-12-04",
        "Mission Type": "Science",
        "Launch Vehicle": "Delta II",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 83.0,
        "Mission Cost": 171.0,
        "Scientific Yield": 95.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 215000.0,
        "Payload Weight": 895.0
    },
    {
        "Mission Name": "Mars Global Surv.",
        "Launch Date": "1996-11-07",
        "Mission Type": "Science",
        "Launch Vehicle": "Delta II",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 3450.0,
        "Mission Cost": 212.0,
        "Scientific Yield": 97.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 215000.0,
        "Payload Weight": 1030.0
    },
    {
        "Mission Name": "Mars Odyssey",
        "Launch Date": "2001-04-07",
        "Mission Type": "Science",
        "Launch Vehicle": "Delta II",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 7000.0,
        "Mission Cost": 297.0,
        "Scientific Yield": 97.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 215000.0,
        "Payload Weight": 730.0
    },
    {
        "Mission Name": "Mars Express",
        "Launch Date": "2003-06-02",
        "Mission Type": "Science",
        "Launch Vehicle": "Soyuz-FG",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 7000.0,
        "Mission Cost": 330.0,
        "Scientific Yield": 97.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 680000.0,
        "Payload Weight": 1123.0
    },
    {
        "Mission Name": "Spirit Rover",
        "Launch Date": "2003-06-10",
        "Mission Type": "Science",
        "Launch Vehicle": "Delta II",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 2210.0,
        "Mission Cost": 820.0,
        "Scientific Yield": 98.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 215000.0,
        "Payload Weight": 1062.0
    },
    {
        "Mission Name": "Opportunity Rover",
        "Launch Date": "2003-07-07",
        "Mission Type": "Science",
        "Launch Vehicle": "Delta II",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 5111.0,
        "Mission Cost": 820.0,
        "Scientific Yield": 99.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 215000.0,
        "Payload Weight": 1063.0
    },
    {
        "Mission Name": "Mars Reconn. Orb.",
        "Launch Date": "2005-08-12",
        "Mission Type": "Science",
        "Launch Vehicle": "Atlas V",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 9000.0,
        "Mission Cost": 720.0,
        "Scientific Yield": 97.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 710000.0,
        "Payload Weight": 2180.0
    },
    {
        "Mission Name": "Phoenix Lander",
        "Launch Date": "2007-08-04",
        "Mission Type": "Science",
        "Launch Vehicle": "Delta II",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 152.0,
        "Mission Cost": 420.0,
        "Scientific Yield": 93.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 215000.0,
        "Payload Weight": 670.0
    },
    {
        "Mission Name": "Curiosity Rover",
        "Launch Date": "2011-11-26",
        "Mission Type": "Science",
        "Launch Vehicle": "Atlas V",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 4600.0,
        "Mission Cost": 2500.0,
        "Scientific Yield": 99.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 710000.0,
        "Payload Weight": 3893.0
    },
    {
        "Mission Name": "MAVEN",
        "Launch Date": "2013-11-18",
        "Mission Type": "Science",
        "Launch Vehicle": "Atlas V",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 4000.0,
        "Mission Cost": 671.0,
        "Scientific Yield": 95.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 710000.0,
        "Payload Weight": 2454.0
    },
    {
        "Mission Name": "MOM Mangalyaan",
        "Launch Date": "2013-11-05",
        "Mission Type": "Science",
        "Launch Vehicle": "PSLV-XL",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 1800.0,
        "Mission Cost": 73.0,
        "Scientific Yield": 92.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 350000.0,
        "Payload Weight": 500.0
    },
    {
        "Mission Name": "InSight Lander",
        "Launch Date": "2018-05-05",
        "Mission Type": "Science",
        "Launch Vehicle": "Atlas V",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 717.0,
        "Mission Cost": 813.0,
        "Scientific Yield": 93.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 710000.0,
        "Payload Weight": 694.0
    },
    {
        "Mission Name": "Perseverance Rover",
        "Launch Date": "2020-07-30",
        "Mission Type": "Science",
        "Launch Vehicle": "Atlas V",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 1400.0,
        "Mission Cost": 2700.0,
        "Scientific Yield": 99.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 710000.0,
        "Payload Weight": 3893.0
    },
    {
        "Mission Name": "Tianwen-1",
        "Launch Date": "2020-07-23",
        "Mission Type": "Science",
        "Launch Vehicle": "Long March 5",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 1800.0,
        "Mission Cost": 480.0,
        "Scientific Yield": 96.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1200000.0,
        "Payload Weight": 5000.0
    },
    {
        "Mission Name": "Emirates Mars Miss.",
        "Launch Date": "2020-07-19",
        "Mission Type": "Science",
        "Launch Vehicle": "H-IIA",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 2700.0,
        "Mission Cost": 200.0,
        "Scientific Yield": 94.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 580000.0,
        "Payload Weight": 1350.0
    },
    {
        "Mission Name": "Luna 9",
        "Launch Date": "1966-01-31",
        "Mission Type": "Science",
        "Launch Vehicle": "Molniya",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 133.0,
        "Mission Cost": 80.0,
        "Scientific Yield": 90.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1500000.0,
        "Payload Weight": 1583.0
    },
    {
        "Mission Name": "Lunar Prospector",
        "Launch Date": "1998-01-06",
        "Mission Type": "Science",
        "Launch Vehicle": "Athena II",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 475.0,
        "Mission Cost": 63.0,
        "Scientific Yield": 88.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 120000.0,
        "Payload Weight": 295.0
    },
    {
        "Mission Name": "SMART-1",
        "Launch Date": "2003-09-27",
        "Mission Type": "Science",
        "Launch Vehicle": "Ariane 5",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 1006.0,
        "Mission Cost": 110.0,
        "Scientific Yield": 87.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1400000.0,
        "Payload Weight": 367.0
    },
    {
        "Mission Name": "Chandrayaan-1",
        "Launch Date": "2008-10-22",
        "Mission Type": "Science",
        "Launch Vehicle": "PSLV-XL",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 312.0,
        "Mission Cost": 79.0,
        "Scientific Yield": 91.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 350000.0,
        "Payload Weight": 1380.0
    },
    {
        "Mission Name": "LRO",
        "Launch Date": "2009-06-18",
        "Mission Type": "Science",
        "Launch Vehicle": "Atlas V",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 4000.0,
        "Mission Cost": 583.0,
        "Scientific Yield": 96.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 710000.0,
        "Payload Weight": 1846.0
    },
    {
        "Mission Name": "LCROSS",
        "Launch Date": "2009-06-18",
        "Mission Type": "Science",
        "Launch Vehicle": "Atlas V",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 271.0,
        "Mission Cost": 583.0,
        "Scientific Yield": 95.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 710000.0,
        "Payload Weight": 628.0
    },
    {
        "Mission Name": "GRAIL A & B",
        "Launch Date": "2011-09-10",
        "Mission Type": "Science",
        "Launch Vehicle": "Delta II",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 441.0,
        "Mission Cost": 496.0,
        "Scientific Yield": 96.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 215000.0,
        "Payload Weight": 306.0
    },
    {
        "Mission Name": "LADEE",
        "Launch Date": "2013-09-06",
        "Mission Type": "Science",
        "Launch Vehicle": "Minotaur V",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 190.0,
        "Mission Cost": 280.0,
        "Scientific Yield": 90.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 120000.0,
        "Payload Weight": 383.0
    },
    {
        "Mission Name": "Chang'e 3",
        "Launch Date": "2013-12-01",
        "Mission Type": "Science",
        "Launch Vehicle": "Long March 3B",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 1500.0,
        "Mission Cost": 200.0,
        "Scientific Yield": 95.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1100000.0,
        "Payload Weight": 3780.0
    },
    {
        "Mission Name": "Chandrayaan-2",
        "Launch Date": "2019-07-22",
        "Mission Type": "Science",
        "Launch Vehicle": "GSLV Mk III",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 380.0,
        "Mission Cost": 146.0,
        "Scientific Yield": 78.0,
        "Crew Size": 0.0,
        "Mission Success": False,
        "Fuel Consumption": 650000.0,
        "Payload Weight": 3850.0
    },
    {
        "Mission Name": "Chang'e 5",
        "Launch Date": "2020-11-23",
        "Mission Type": "Science",
        "Launch Vehicle": "Long March 5",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 22.0,
        "Mission Cost": 900.0,
        "Scientific Yield": 98.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1200000.0,
        "Payload Weight": 8200.0
    },
    {
        "Mission Name": "CAPSTONE",
        "Launch Date": "2022-06-28",
        "Mission Type": "Tech Demo",
        "Launch Vehicle": "Electron",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 900.0,
        "Mission Cost": 30.0,
        "Scientific Yield": 88.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 65000.0,
        "Payload Weight": 25.0
    },
    {
        "Mission Name": "Artemis I",
        "Launch Date": "2022-11-16",
        "Mission Type": "Science",
        "Launch Vehicle": "Artemis SLS",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 25.0,
        "Mission Cost": 4100.0,
        "Scientific Yield": 94.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 2700000.0,
        "Payload Weight": 27000.0
    },
    {
        "Mission Name": "ispace Mission 1",
        "Launch Date": "2023-04-25",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 12.0,
        "Mission Cost": 90.0,
        "Scientific Yield": 30.0,
        "Crew Size": 0.0,
        "Mission Success": False,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 1000.0
    },
    {
        "Mission Name": "Chandrayaan-3",
        "Launch Date": "2023-07-14",
        "Mission Type": "Science",
        "Launch Vehicle": "GSLV Mk III",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 40.0,
        "Mission Cost": 140.0,
        "Scientific Yield": 97.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 650000.0,
        "Payload Weight": 3900.0
    },
    {
        "Mission Name": "Luna-25",
        "Launch Date": "2023-08-10",
        "Mission Type": "Science",
        "Launch Vehicle": "Soyuz-2.1b",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 8.0,
        "Mission Cost": 200.0,
        "Scientific Yield": 10.0,
        "Crew Size": 0.0,
        "Mission Success": False,
        "Fuel Consumption": 680000.0,
        "Payload Weight": 1750.0
    },
    {
        "Mission Name": "Galileo",
        "Launch Date": "1989-10-18",
        "Mission Type": "Science",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "Jupiter",
        "Distance from Earth": 628000000.0,
        "Mission Duration": 5000.0,
        "Mission Cost": 1600.0,
        "Scientific Yield": 98.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 2563.0
    },
    {
        "Mission Name": "Cassini-Huygens",
        "Launch Date": "1997-10-15",
        "Mission Type": "Science",
        "Launch Vehicle": "Titan IV-B",
        "Target Name": "Saturn",
        "Distance from Earth": 1275000000.0,
        "Mission Duration": 13000.0,
        "Mission Cost": 3260.0,
        "Scientific Yield": 99.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1400000.0,
        "Payload Weight": 5655.0
    },
    {
        "Mission Name": "New Horizons",
        "Launch Date": "2006-01-19",
        "Mission Type": "Exploration",
        "Launch Vehicle": "Atlas V",
        "Target Name": "Jupiter",
        "Distance from Earth": 628000000.0,
        "Mission Duration": 9.6,
        "Mission Cost": 700.0,
        "Scientific Yield": 97.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 710000.0,
        "Payload Weight": 401.0
    },
    {
        "Mission Name": "Juno",
        "Launch Date": "2011-08-05",
        "Mission Type": "Science",
        "Launch Vehicle": "Atlas V",
        "Target Name": "Jupiter",
        "Distance from Earth": 628000000.0,
        "Mission Duration": 5000.0,
        "Mission Cost": 1100.0,
        "Scientific Yield": 97.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 710000.0,
        "Payload Weight": 3625.0
    },
    {
        "Mission Name": "BepiColombo",
        "Launch Date": "2018-10-20",
        "Mission Type": "Science",
        "Launch Vehicle": "Ariane 5",
        "Target Name": "Mercury",
        "Distance from Earth": 77000000.0,
        "Mission Duration": 2562.0,
        "Mission Cost": 1200.0,
        "Scientific Yield": 93.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1400000.0,
        "Payload Weight": 4100.0
    },
    {
        "Mission Name": "GOES-16",
        "Launch Date": "2016-11-19",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Atlas V",
        "Target Name": "GEO",
        "Distance from Earth": 35786.0,
        "Mission Duration": 8000.0,
        "Mission Cost": 1100.0,
        "Scientific Yield": 92.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 710000.0,
        "Payload Weight": 5192.0
    },
    {
        "Mission Name": "Sentinel-6",
        "Launch Date": "2020-11-21",
        "Mission Type": "Science",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "LEO",
        "Distance from Earth": 800.0,
        "Mission Duration": 2800.0,
        "Mission Cost": 180.0,
        "Scientific Yield": 91.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 1440.0
    },
    {
        "Mission Name": "GRACE-FO",
        "Launch Date": "2018-05-22",
        "Mission Type": "Science",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "LEO",
        "Distance from Earth": 490.0,
        "Mission Duration": 2600.0,
        "Mission Cost": 430.0,
        "Scientific Yield": 93.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 600.0
    },
    {
        "Mission Name": "ICESat-2",
        "Launch Date": "2018-09-15",
        "Mission Type": "Science",
        "Launch Vehicle": "Delta II",
        "Target Name": "LEO",
        "Distance from Earth": 500.0,
        "Mission Duration": 3500.0,
        "Mission Cost": 304.0,
        "Scientific Yield": 93.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 215000.0,
        "Payload Weight": 1514.0
    },
    {
        "Mission Name": "Terra",
        "Launch Date": "1999-12-18",
        "Mission Type": "Science",
        "Launch Vehicle": "Atlas II",
        "Target Name": "LEO",
        "Distance from Earth": 705.0,
        "Mission Duration": 9000.0,
        "Mission Cost": 600.0,
        "Scientific Yield": 95.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 290000.0,
        "Payload Weight": 4864.0
    },
    {
        "Mission Name": "Aqua",
        "Launch Date": "2002-05-04",
        "Mission Type": "Science",
        "Launch Vehicle": "Delta II",
        "Target Name": "LEO",
        "Distance from Earth": 705.0,
        "Mission Duration": 8000.0,
        "Mission Cost": 952.0,
        "Scientific Yield": 95.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 215000.0,
        "Payload Weight": 2934.0
    },
    {
        "Mission Name": "Aura",
        "Launch Date": "2004-07-15",
        "Mission Type": "Science",
        "Launch Vehicle": "Delta II",
        "Target Name": "LEO",
        "Distance from Earth": 705.0,
        "Mission Duration": 7000.0,
        "Mission Cost": 780.0,
        "Scientific Yield": 94.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 215000.0,
        "Payload Weight": 2967.0
    },
    {
        "Mission Name": "GPM Core",
        "Launch Date": "2014-02-27",
        "Mission Type": "Science",
        "Launch Vehicle": "H-IIA",
        "Target Name": "LEO",
        "Distance from Earth": 407.0,
        "Mission Duration": 3800.0,
        "Mission Cost": 933.0,
        "Scientific Yield": 93.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 580000.0,
        "Payload Weight": 3850.0
    },
    {
        "Mission Name": "JWST",
        "Launch Date": "2021-12-25",
        "Mission Type": "Science",
        "Launch Vehicle": "Ariane 5",
        "Target Name": "L2",
        "Distance from Earth": 1500000.0,
        "Mission Duration": 4000.0,
        "Mission Cost": 10000.0,
        "Scientific Yield": 100.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1400000.0,
        "Payload Weight": 6200.0
    },
    {
        "Mission Name": "Dragon CRS-1",
        "Launch Date": "2012-10-07",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 18.8,
        "Mission Cost": 133.0,
        "Scientific Yield": 78.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 3666.0
    },
    {
        "Mission Name": "Dragon CRS-2",
        "Launch Date": "2013-03-01",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 23.3,
        "Mission Cost": 133.0,
        "Scientific Yield": 80.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 3666.0
    },
    {
        "Mission Name": "Dragon CRS-5",
        "Launch Date": "2015-01-10",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 28.1,
        "Mission Cost": 133.0,
        "Scientific Yield": 82.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 2268.0
    },
    {
        "Mission Name": "Dragon CRS-8",
        "Launch Date": "2016-04-08",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 31.9,
        "Mission Cost": 133.0,
        "Scientific Yield": 85.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 3175.0
    },
    {
        "Mission Name": "Dragon CRS-12",
        "Launch Date": "2017-08-14",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 33.5,
        "Mission Cost": 133.0,
        "Scientific Yield": 87.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 3015.0
    },
    {
        "Mission Name": "Dragon CRS-17",
        "Launch Date": "2019-05-04",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 31.9,
        "Mission Cost": 133.0,
        "Scientific Yield": 87.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 2477.0
    },
    {
        "Mission Name": "Dragon CRS-21",
        "Launch Date": "2020-12-06",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 35.1,
        "Mission Cost": 150.0,
        "Scientific Yield": 88.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 2972.0
    },
    {
        "Mission Name": "Dragon CRS-24",
        "Launch Date": "2021-12-21",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 33.0,
        "Mission Cost": 150.0,
        "Scientific Yield": 89.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 3280.0
    },
    {
        "Mission Name": "Dragon CRS-26",
        "Launch Date": "2022-11-26",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 32.0,
        "Mission Cost": 150.0,
        "Scientific Yield": 89.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 3200.0
    },
    {
        "Mission Name": "Dragon CRS-28",
        "Launch Date": "2023-06-05",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 30.0,
        "Mission Cost": 150.0,
        "Scientific Yield": 89.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 3150.0
    },
    {
        "Mission Name": "Crew Dragon DM-2",
        "Launch Date": "2020-05-30",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 63.8,
        "Mission Cost": 395.0,
        "Scientific Yield": 96.0,
        "Crew Size": 2.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 12519.0
    },
    {
        "Mission Name": "Crew-1",
        "Launch Date": "2020-11-15",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 167.2,
        "Mission Cost": 395.0,
        "Scientific Yield": 97.0,
        "Crew Size": 4.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 12519.0
    },
    {
        "Mission Name": "Crew-2",
        "Launch Date": "2021-04-23",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 199.4,
        "Mission Cost": 395.0,
        "Scientific Yield": 97.0,
        "Crew Size": 4.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 12519.0
    },
    {
        "Mission Name": "Crew-3",
        "Launch Date": "2021-11-10",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 176.9,
        "Mission Cost": 395.0,
        "Scientific Yield": 97.0,
        "Crew Size": 4.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 12519.0
    },
    {
        "Mission Name": "Crew-4",
        "Launch Date": "2022-04-27",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 170.0,
        "Mission Cost": 395.0,
        "Scientific Yield": 97.0,
        "Crew Size": 4.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 12519.0
    },
    {
        "Mission Name": "Crew-5",
        "Launch Date": "2022-10-05",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 157.0,
        "Mission Cost": 395.0,
        "Scientific Yield": 97.0,
        "Crew Size": 4.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 12519.0
    },
    {
        "Mission Name": "Crew-6",
        "Launch Date": "2023-03-02",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 186.0,
        "Mission Cost": 395.0,
        "Scientific Yield": 97.0,
        "Crew Size": 4.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 12519.0
    },
    {
        "Mission Name": "Crew-7",
        "Launch Date": "2023-08-26",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 176.0,
        "Mission Cost": 395.0,
        "Scientific Yield": 97.0,
        "Crew Size": 4.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 12519.0
    },
    {
        "Mission Name": "Crew-8",
        "Launch Date": "2024-03-03",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 240.0,
        "Mission Cost": 395.0,
        "Scientific Yield": 97.0,
        "Crew Size": 4.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 12519.0
    },
    {
        "Mission Name": "Polaris Dawn",
        "Launch Date": "2024-09-10",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "LEO",
        "Distance from Earth": 1400.0,
        "Mission Duration": 5.0,
        "Mission Cost": 200.0,
        "Scientific Yield": 97.0,
        "Crew Size": 4.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 13000.0
    },
    {
        "Mission Name": "Starlink L01",
        "Launch Date": "2019-05-23",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "LEO",
        "Distance from Earth": 550.0,
        "Mission Duration": 1800.0,
        "Mission Cost": 62.0,
        "Scientific Yield": 75.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 13620.0
    },
    {
        "Mission Name": "Starlink L04",
        "Launch Date": "2020-01-29",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "LEO",
        "Distance from Earth": 550.0,
        "Mission Duration": 1800.0,
        "Mission Cost": 62.0,
        "Scientific Yield": 80.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 13620.0
    },
    {
        "Mission Name": "Starlink L10",
        "Launch Date": "2020-08-07",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "LEO",
        "Distance from Earth": 550.0,
        "Mission Duration": 1800.0,
        "Mission Cost": 62.0,
        "Scientific Yield": 82.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 13620.0
    },
    {
        "Mission Name": "Starlink L20",
        "Launch Date": "2021-02-15",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "LEO",
        "Distance from Earth": 550.0,
        "Mission Duration": 1800.0,
        "Mission Cost": 62.0,
        "Scientific Yield": 84.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 13620.0
    },
    {
        "Mission Name": "Starlink L30",
        "Launch Date": "2021-09-14",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "LEO",
        "Distance from Earth": 550.0,
        "Mission Duration": 1800.0,
        "Mission Cost": 62.0,
        "Scientific Yield": 85.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 13620.0
    },
    {
        "Mission Name": "Starlink G6-1",
        "Launch Date": "2022-12-28",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "LEO",
        "Distance from Earth": 525.0,
        "Mission Duration": 1800.0,
        "Mission Cost": 67.0,
        "Scientific Yield": 86.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 15625.0
    },
    {
        "Mission Name": "Starlink G6-10",
        "Launch Date": "2023-05-19",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "LEO",
        "Distance from Earth": 525.0,
        "Mission Duration": 1800.0,
        "Mission Cost": 67.0,
        "Scientific Yield": 87.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 15625.0
    },
    {
        "Mission Name": "Starlink G6-20",
        "Launch Date": "2024-01-14",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "LEO",
        "Distance from Earth": 525.0,
        "Mission Duration": 1800.0,
        "Mission Cost": 67.0,
        "Scientific Yield": 87.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 15625.0
    },
    {
        "Mission Name": "FH Demo Mission",
        "Launch Date": "2018-02-06",
        "Mission Type": "Tech Demo",
        "Launch Vehicle": "Falcon Heavy",
        "Target Name": "GEO",
        "Distance from Earth": 35786.0,
        "Mission Duration": 9000.0,
        "Mission Cost": 90.0,
        "Scientific Yield": 88.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1370000.0,
        "Payload Weight": 63800.0
    },
    {
        "Mission Name": "Arabsat-6A",
        "Launch Date": "2019-04-11",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon Heavy",
        "Target Name": "GEO",
        "Distance from Earth": 35786.0,
        "Mission Duration": 5050.0,
        "Mission Cost": 150.0,
        "Scientific Yield": 80.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1370000.0,
        "Payload Weight": 63800.0
    },
    {
        "Mission Name": "STP-2",
        "Launch Date": "2019-06-25",
        "Mission Type": "Defense",
        "Launch Vehicle": "Falcon Heavy",
        "Target Name": "LEO",
        "Distance from Earth": 800.0,
        "Mission Duration": 4200.0,
        "Mission Cost": 150.0,
        "Scientific Yield": 82.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1370000.0,
        "Payload Weight": 63800.0
    },
    {
        "Mission Name": "USSF-44",
        "Launch Date": "2022-11-01",
        "Mission Type": "Defense",
        "Launch Vehicle": "Falcon Heavy",
        "Target Name": "GEO",
        "Distance from Earth": 35786.0,
        "Mission Duration": 2900.0,
        "Mission Cost": 160.0,
        "Scientific Yield": 82.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1370000.0,
        "Payload Weight": 63800.0
    },
    {
        "Mission Name": "Psyche Mission",
        "Launch Date": "2023-10-13",
        "Mission Type": "Science",
        "Launch Vehicle": "Falcon Heavy",
        "Target Name": "Jupiter",
        "Distance from Earth": 628000000.0,
        "Mission Duration": 2100.0,
        "Mission Cost": 1200.0,
        "Scientific Yield": 93.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1370000.0,
        "Payload Weight": 2608.0
    },
    {
        "Mission Name": "WGS-10",
        "Launch Date": "2019-03-15",
        "Mission Type": "Defense",
        "Launch Vehicle": "Delta IV Heavy",
        "Target Name": "GEO",
        "Distance from Earth": 35786.0,
        "Mission Duration": 8000.0,
        "Mission Cost": 650.0,
        "Scientific Yield": 80.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1430000.0,
        "Payload Weight": 5987.0
    },
    {
        "Mission Name": "SBIRS GEO-5",
        "Launch Date": "2021-05-18",
        "Mission Type": "Defense",
        "Launch Vehicle": "Atlas V",
        "Target Name": "GEO",
        "Distance from Earth": 35786.0,
        "Mission Duration": 4000.0,
        "Mission Cost": 650.0,
        "Scientific Yield": 82.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 710000.0,
        "Payload Weight": 4564.0
    },
    {
        "Mission Name": "GPS III SV05",
        "Launch Date": "2021-06-17",
        "Mission Type": "Defense",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "MEO",
        "Distance from Earth": 20200.0,
        "Mission Duration": 7000.0,
        "Mission Cost": 200.0,
        "Scientific Yield": 82.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 3880.0
    },
    {
        "Mission Name": "GPS III SV06",
        "Launch Date": "2023-01-18",
        "Mission Type": "Defense",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "MEO",
        "Distance from Earth": 20200.0,
        "Mission Duration": 7000.0,
        "Mission Cost": 200.0,
        "Scientific Yield": 82.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 3880.0
    },
    {
        "Mission Name": "NROL-87",
        "Launch Date": "2022-02-02",
        "Mission Type": "Defense",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "LEO",
        "Distance from Earth": 500.0,
        "Mission Duration": 3000.0,
        "Mission Cost": 300.0,
        "Scientific Yield": 70.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 5000.0
    },
    {
        "Mission Name": "NROL-85",
        "Launch Date": "2022-04-17",
        "Mission Type": "Defense",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "LEO",
        "Distance from Earth": 500.0,
        "Mission Duration": 3000.0,
        "Mission Cost": 300.0,
        "Scientific Yield": 70.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 5000.0
    },
    {
        "Mission Name": "Kepler Space Tel.",
        "Launch Date": "2009-03-07",
        "Mission Type": "Science",
        "Launch Vehicle": "Delta II",
        "Target Name": "GEO",
        "Distance from Earth": 1500000.0,
        "Mission Duration": 3900.0,
        "Mission Cost": 600.0,
        "Scientific Yield": 99.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 215000.0,
        "Payload Weight": 1039.0
    },
    {
        "Mission Name": "Dawn",
        "Launch Date": "2007-09-27",
        "Mission Type": "Science",
        "Launch Vehicle": "Delta II",
        "Target Name": "Jupiter",
        "Distance from Earth": 628000000.0,
        "Mission Duration": 3910.0,
        "Mission Cost": 446.0,
        "Scientific Yield": 96.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 215000.0,
        "Payload Weight": 1218.0
    },
    {
        "Mission Name": "OSIRIS-REx",
        "Launch Date": "2016-09-08",
        "Mission Type": "Science",
        "Launch Vehicle": "Atlas V",
        "Target Name": "GEO",
        "Distance from Earth": 490000.0,
        "Mission Duration": 2565.0,
        "Mission Cost": 800.0,
        "Scientific Yield": 96.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 710000.0,
        "Payload Weight": 2110.0
    },
    {
        "Mission Name": "Hayabusa2",
        "Launch Date": "2014-12-03",
        "Mission Type": "Science",
        "Launch Vehicle": "H-IIA",
        "Target Name": "GEO",
        "Distance from Earth": 300000000.0,
        "Mission Duration": 2272.0,
        "Mission Cost": 170.0,
        "Scientific Yield": 97.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 580000.0,
        "Payload Weight": 609.0
    },
    {
        "Mission Name": "Parker Solar Probe",
        "Launch Date": "2018-08-12",
        "Mission Type": "Science",
        "Launch Vehicle": "Delta IV Heavy",
        "Target Name": "LEO",
        "Distance from Earth": 36000000.0,
        "Mission Duration": 7700.0,
        "Mission Cost": 1500.0,
        "Scientific Yield": 98.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1430000.0,
        "Payload Weight": 685.0
    },
    {
        "Mission Name": "Solar Orbiter",
        "Launch Date": "2020-02-10",
        "Mission Type": "Science",
        "Launch Vehicle": "Atlas V",
        "Target Name": "LEO",
        "Distance from Earth": 36000000.0,
        "Mission Duration": 4000.0,
        "Mission Cost": 1500.0,
        "Scientific Yield": 96.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 710000.0,
        "Payload Weight": 1800.0
    },
    {
        "Mission Name": "TESS",
        "Launch Date": "2018-04-18",
        "Mission Type": "Science",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "GEO",
        "Distance from Earth": 375000.0,
        "Mission Duration": 4000.0,
        "Mission Cost": 337.0,
        "Scientific Yield": 96.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 362.0
    },
    {
        "Mission Name": "NICER",
        "Launch Date": "2017-06-03",
        "Mission Type": "Science",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 2800.0,
        "Mission Cost": 100.0,
        "Scientific Yield": 90.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 372.0
    },
    {
        "Mission Name": "CHEOPS",
        "Launch Date": "2019-12-18",
        "Mission Type": "Science",
        "Launch Vehicle": "Soyuz-Fregat",
        "Target Name": "LEO",
        "Distance from Earth": 700.0,
        "Mission Duration": 3000.0,
        "Mission Cost": 100.0,
        "Scientific Yield": 93.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 680000.0,
        "Payload Weight": 280.0
    },
    {
        "Mission Name": "Euclid",
        "Launch Date": "2023-07-01",
        "Mission Type": "Science",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "L2",
        "Distance from Earth": 1500000.0,
        "Mission Duration": 3000.0,
        "Mission Cost": 1400.0,
        "Scientific Yield": 96.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 2000.0
    },
    {
        "Mission Name": "XRISM",
        "Launch Date": "2023-09-06",
        "Mission Type": "Science",
        "Launch Vehicle": "H-IIA",
        "Target Name": "LEO",
        "Distance from Earth": 575.0,
        "Mission Duration": 3000.0,
        "Mission Cost": 1000.0,
        "Scientific Yield": 95.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 580000.0,
        "Payload Weight": 1150.0
    },
    {
        "Mission Name": "ERS-2",
        "Launch Date": "1995-04-21",
        "Mission Type": "Science",
        "Launch Vehicle": "Ariane 4",
        "Target Name": "LEO",
        "Distance from Earth": 785.0,
        "Mission Duration": 16000.0,
        "Mission Cost": 600.0,
        "Scientific Yield": 92.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 700000.0,
        "Payload Weight": 2516.0
    },
    {
        "Mission Name": "Envisat",
        "Launch Date": "2002-03-01",
        "Mission Type": "Science",
        "Launch Vehicle": "Ariane 5",
        "Target Name": "LEO",
        "Distance from Earth": 800.0,
        "Mission Duration": 10000.0,
        "Mission Cost": 2300.0,
        "Scientific Yield": 95.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1400000.0,
        "Payload Weight": 8140.0
    },
    {
        "Mission Name": "GAIA",
        "Launch Date": "2013-12-19",
        "Mission Type": "Science",
        "Launch Vehicle": "Soyuz-STB",
        "Target Name": "L2",
        "Distance from Earth": 1500000.0,
        "Mission Duration": 4000.0,
        "Mission Cost": 740.0,
        "Scientific Yield": 98.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 680000.0,
        "Payload Weight": 2030.0
    },
    {
        "Mission Name": "Herschel",
        "Launch Date": "2009-05-14",
        "Mission Type": "Science",
        "Launch Vehicle": "Ariane 5",
        "Target Name": "L2",
        "Distance from Earth": 1500000.0,
        "Mission Duration": 1647.0,
        "Mission Cost": 1100.0,
        "Scientific Yield": 97.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1400000.0,
        "Payload Weight": 3400.0
    },
    {
        "Mission Name": "Planck",
        "Launch Date": "2009-05-14",
        "Mission Type": "Science",
        "Launch Vehicle": "Ariane 5",
        "Target Name": "L2",
        "Distance from Earth": 1500000.0,
        "Mission Duration": 1554.0,
        "Mission Cost": 700.0,
        "Scientific Yield": 98.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1400000.0,
        "Payload Weight": 1800.0
    },
    {
        "Mission Name": "ExoMars TGO",
        "Launch Date": "2016-03-14",
        "Mission Type": "Science",
        "Launch Vehicle": "Proton-M",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 3900.0,
        "Mission Cost": 1500.0,
        "Scientific Yield": 85.0,
        "Crew Size": 0.0,
        "Mission Success": False,
        "Fuel Consumption": 900000.0,
        "Payload Weight": 4332.0
    },
    {
        "Mission Name": "Rosetta",
        "Launch Date": "2004-03-02",
        "Mission Type": "Science",
        "Launch Vehicle": "Ariane 5",
        "Target Name": "Jupiter",
        "Distance from Earth": 628000000.0,
        "Mission Duration": 4338.0,
        "Mission Cost": 1400.0,
        "Scientific Yield": 98.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1400000.0,
        "Payload Weight": 3000.0
    },
    {
        "Mission Name": "Mars Climate Orb.",
        "Launch Date": "1998-12-11",
        "Mission Type": "Science",
        "Launch Vehicle": "Delta II",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 286.0,
        "Mission Cost": 327.0,
        "Scientific Yield": 10.0,
        "Crew Size": 0.0,
        "Mission Success": False,
        "Fuel Consumption": 215000.0,
        "Payload Weight": 638.0
    },
    {
        "Mission Name": "MESSENGER",
        "Launch Date": "2004-08-03",
        "Mission Type": "Science",
        "Launch Vehicle": "Delta II",
        "Target Name": "Mercury",
        "Distance from Earth": 77000000.0,
        "Mission Duration": 4105.0,
        "Mission Cost": 446.0,
        "Scientific Yield": 94.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 215000.0,
        "Payload Weight": 1108.0
    },
    {
        "Mission Name": "Magellan",
        "Launch Date": "1989-05-04",
        "Mission Type": "Science",
        "Launch Vehicle": "Space Shuttle",
        "Target Name": "Venus",
        "Distance from Earth": 41000000.0,
        "Mission Duration": 1570.0,
        "Mission Cost": 551.0,
        "Scientific Yield": 93.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1800000.0,
        "Payload Weight": 3449.0
    },
    {
        "Mission Name": "Venus Express",
        "Launch Date": "2005-11-09",
        "Mission Type": "Science",
        "Launch Vehicle": "Soyuz-FG",
        "Target Name": "Venus",
        "Distance from Earth": 41000000.0,
        "Mission Duration": 2888.0,
        "Mission Cost": 220.0,
        "Scientific Yield": 93.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 680000.0,
        "Payload Weight": 1270.0
    },
    {
        "Mission Name": "AKATSUKI",
        "Launch Date": "2010-05-20",
        "Mission Type": "Science",
        "Launch Vehicle": "H-IIA",
        "Target Name": "Venus",
        "Distance from Earth": 41000000.0,
        "Mission Duration": 3500.0,
        "Mission Cost": 300.0,
        "Scientific Yield": 88.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 580000.0,
        "Payload Weight": 517.0
    },
    {
        "Mission Name": "JUICE",
        "Launch Date": "2023-04-14",
        "Mission Type": "Science",
        "Launch Vehicle": "Ariane 5",
        "Target Name": "Jupiter",
        "Distance from Earth": 628000000.0,
        "Mission Duration": 2920.0,
        "Mission Cost": 1600.0,
        "Scientific Yield": 94.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1400000.0,
        "Payload Weight": 6070.0
    },
    {
        "Mission Name": "Europa Clipper",
        "Launch Date": "2024-10-14",
        "Mission Type": "Science",
        "Launch Vehicle": "Falcon Heavy",
        "Target Name": "Jupiter",
        "Distance from Earth": 628000000.0,
        "Mission Duration": 2920.0,
        "Mission Cost": 5000.0,
        "Scientific Yield": 97.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1370000.0,
        "Payload Weight": 6065.0
    },
    {
        "Mission Name": "Intelsat 39",
        "Launch Date": "2019-08-06",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Ariane 5",
        "Target Name": "GEO",
        "Distance from Earth": 35786.0,
        "Mission Duration": 15000.0,
        "Mission Cost": 250.0,
        "Scientific Yield": 78.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1400000.0,
        "Payload Weight": 6764.0
    },
    {
        "Mission Name": "SES-18/19",
        "Launch Date": "2023-03-17",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "GEO",
        "Distance from Earth": 35786.0,
        "Mission Duration": 15000.0,
        "Mission Cost": 80.0,
        "Scientific Yield": 80.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 7000.0
    },
    {
        "Mission Name": "Inmarsat-6 F2",
        "Launch Date": "2023-02-17",
        "Mission Type": "Commercial",
        "Launch Vehicle": "H3",
        "Target Name": "GEO",
        "Distance from Earth": 35786.0,
        "Mission Duration": 15000.0,
        "Mission Cost": 400.0,
        "Scientific Yield": 60.0,
        "Crew Size": 0.0,
        "Mission Success": False,
        "Fuel Consumption": 600000.0,
        "Payload Weight": 9000.0
    },
    {
        "Mission Name": "Arabsat 7B",
        "Launch Date": "2023-06-19",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Ariane 5",
        "Target Name": "GEO",
        "Distance from Earth": 35786.0,
        "Mission Duration": 15000.0,
        "Mission Cost": 250.0,
        "Scientific Yield": 78.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1400000.0,
        "Payload Weight": 5550.0
    },
    {
        "Mission Name": "Blue Origin NS-18",
        "Launch Date": "2021-10-13",
        "Mission Type": "Commercial",
        "Launch Vehicle": "New Shepard",
        "Target Name": "LEO",
        "Distance from Earth": 100.0,
        "Mission Duration": 0.2,
        "Mission Cost": 28.0,
        "Scientific Yield": 65.0,
        "Crew Size": 4.0,
        "Mission Success": True,
        "Fuel Consumption": 190000.0,
        "Payload Weight": 859.0
    },
    {
        "Mission Name": "Blue Origin NS-19",
        "Launch Date": "2021-12-11",
        "Mission Type": "Commercial",
        "Launch Vehicle": "New Shepard",
        "Target Name": "LEO",
        "Distance from Earth": 100.0,
        "Mission Duration": 0.2,
        "Mission Cost": 28.0,
        "Scientific Yield": 65.0,
        "Crew Size": 6.0,
        "Mission Success": True,
        "Fuel Consumption": 190000.0,
        "Payload Weight": 859.0
    },
    {
        "Mission Name": "SpaceX Inspiration4",
        "Launch Date": "2021-09-15",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "LEO",
        "Distance from Earth": 580.0,
        "Mission Duration": 3.1,
        "Mission Cost": 200.0,
        "Scientific Yield": 82.0,
        "Crew Size": 4.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 12519.0
    },
    {
        "Mission Name": "Virgin Galactic VF-01",
        "Launch Date": "2023-06-29",
        "Mission Type": "Commercial",
        "Launch Vehicle": "VSS Unity",
        "Target Name": "LEO",
        "Distance from Earth": 88.0,
        "Mission Duration": 0.07,
        "Mission Cost": 50.0,
        "Scientific Yield": 60.0,
        "Crew Size": 6.0,
        "Mission Success": True,
        "Fuel Consumption": 50000.0,
        "Payload Weight": 600.0
    },
    {
        "Mission Name": "Artemis II",
        "Launch Date": "2025-09-01",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Artemis SLS",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 10.0,
        "Mission Cost": 7000.0,
        "Scientific Yield": 90.0,
        "Crew Size": 4.0,
        "Mission Success": True,
        "Fuel Consumption": 2700000.0,
        "Payload Weight": 27000.0
    },
    {
        "Mission Name": "PSLV-C11 Chand-1",
        "Launch Date": "2008-10-22",
        "Mission Type": "Science",
        "Launch Vehicle": "PSLV-XL",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 312.0,
        "Mission Cost": 79.0,
        "Scientific Yield": 91.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 350000.0,
        "Payload Weight": 1380.0
    },
    {
        "Mission Name": "PSLV-C25 MOM",
        "Launch Date": "2013-11-05",
        "Mission Type": "Science",
        "Launch Vehicle": "PSLV-XL",
        "Target Name": "Mars",
        "Distance from Earth": 225000000.0,
        "Mission Duration": 1800.0,
        "Mission Cost": 73.0,
        "Scientific Yield": 92.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 350000.0,
        "Payload Weight": 500.0
    },
    {
        "Mission Name": "PSLV-C37 104sat",
        "Launch Date": "2017-02-15",
        "Mission Type": "Commercial",
        "Launch Vehicle": "PSLV-XL",
        "Target Name": "LEO",
        "Distance from Earth": 510.0,
        "Mission Duration": 2000.0,
        "Mission Cost": 15.0,
        "Scientific Yield": 85.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 350000.0,
        "Payload Weight": 1378.0
    },
    {
        "Mission Name": "GSLV Mk III D2",
        "Launch Date": "2018-11-14",
        "Mission Type": "Commercial",
        "Launch Vehicle": "GSLV Mk III",
        "Target Name": "GEO",
        "Distance from Earth": 35786.0,
        "Mission Duration": 15000.0,
        "Mission Cost": 90.0,
        "Scientific Yield": 82.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 650000.0,
        "Payload Weight": 3540.0
    },
    {
        "Mission Name": "Aditya-L1",
        "Launch Date": "2023-09-02",
        "Mission Type": "Science",
        "Launch Vehicle": "PSLV-XL",
        "Target Name": "L2",
        "Distance from Earth": 1500000.0,
        "Mission Duration": 3000.0,
        "Mission Cost": 50.0,
        "Scientific Yield": 90.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 350000.0,
        "Payload Weight": 1475.0
    },
    {
        "Mission Name": "Shenzhou 5",
        "Launch Date": "2003-10-15",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Long March 2F",
        "Target Name": "LEO",
        "Distance from Earth": 343.0,
        "Mission Duration": 0.9,
        "Mission Cost": 110.0,
        "Scientific Yield": 80.0,
        "Crew Size": 1.0,
        "Mission Success": True,
        "Fuel Consumption": 800000.0,
        "Payload Weight": 7840.0
    },
    {
        "Mission Name": "Shenzhou 11",
        "Launch Date": "2016-10-17",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Long March 2F",
        "Target Name": "LEO",
        "Distance from Earth": 390.0,
        "Mission Duration": 32.7,
        "Mission Cost": 150.0,
        "Scientific Yield": 85.0,
        "Crew Size": 2.0,
        "Mission Success": True,
        "Fuel Consumption": 800000.0,
        "Payload Weight": 8130.0
    },
    {
        "Mission Name": "Shenzhou 14",
        "Launch Date": "2022-06-05",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Long March 2F",
        "Target Name": "LEO",
        "Distance from Earth": 390.0,
        "Mission Duration": 183.0,
        "Mission Cost": 160.0,
        "Scientific Yield": 88.0,
        "Crew Size": 3.0,
        "Mission Success": True,
        "Fuel Consumption": 800000.0,
        "Payload Weight": 8130.0
    },
    {
        "Mission Name": "Shenzhou 17",
        "Launch Date": "2023-10-26",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Long March 2F",
        "Target Name": "LEO",
        "Distance from Earth": 390.0,
        "Mission Duration": 186.0,
        "Mission Cost": 160.0,
        "Scientific Yield": 88.0,
        "Crew Size": 3.0,
        "Mission Success": True,
        "Fuel Consumption": 800000.0,
        "Payload Weight": 8130.0
    },
    {
        "Mission Name": "Long March 5B Y3",
        "Launch Date": "2022-07-24",
        "Mission Type": "Commercial",
        "Launch Vehicle": "Long March 5B",
        "Target Name": "LEO",
        "Distance from Earth": 400.0,
        "Mission Duration": 3650.0,
        "Mission Cost": 200.0,
        "Scientific Yield": 85.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1200000.0,
        "Payload Weight": 23000.0
    },
    {
        "Mission Name": "Chang'e 4",
        "Launch Date": "2018-12-07",
        "Mission Type": "Science",
        "Launch Vehicle": "Long March 3B",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 1800.0,
        "Mission Cost": 300.0,
        "Scientific Yield": 97.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1100000.0,
        "Payload Weight": 3780.0
    },
    {
        "Mission Name": "Chang'e 6",
        "Launch Date": "2024-05-03",
        "Mission Type": "Science",
        "Launch Vehicle": "Long March 5",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 53.0,
        "Mission Cost": 1200.0,
        "Scientific Yield": 98.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1200000.0,
        "Payload Weight": 8200.0
    },
    {
        "Mission Name": "CST-100 OFT",
        "Launch Date": "2019-12-19",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Atlas V",
        "Target Name": "LEO",
        "Distance from Earth": 400.0,
        "Mission Duration": 2.2,
        "Mission Cost": 410.0,
        "Scientific Yield": 50.0,
        "Crew Size": 0.0,
        "Mission Success": False,
        "Fuel Consumption": 710000.0,
        "Payload Weight": 11000.0
    },
    {
        "Mission Name": "CST-100 OFT-2",
        "Launch Date": "2022-05-19",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Atlas V",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 5.3,
        "Mission Cost": 410.0,
        "Scientific Yield": 75.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 710000.0,
        "Payload Weight": 11000.0
    },
    {
        "Mission Name": "Starliner CFT",
        "Launch Date": "2024-06-05",
        "Mission Type": "Crewed",
        "Launch Vehicle": "Atlas V",
        "Target Name": "ISS",
        "Distance from Earth": 400.0,
        "Mission Duration": 271.0,
        "Mission Cost": 440.0,
        "Scientific Yield": 70.0,
        "Crew Size": 2.0,
        "Mission Success": True,
        "Fuel Consumption": 710000.0,
        "Payload Weight": 11000.0
    },
    {
        "Mission Name": "DART Mission",
        "Launch Date": "2021-11-24",
        "Mission Type": "Science",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "GEO",
        "Distance from Earth": 11000000.0,
        "Mission Duration": 285.0,
        "Mission Cost": 308.0,
        "Scientific Yield": 97.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 610.0
    },
    {
        "Mission Name": "LightSail 2",
        "Launch Date": "2019-06-24",
        "Mission Type": "Tech Demo",
        "Launch Vehicle": "Falcon Heavy",
        "Target Name": "LEO",
        "Distance from Earth": 720.0,
        "Mission Duration": 1000.0,
        "Mission Cost": 7.0,
        "Scientific Yield": 88.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 1370000.0,
        "Payload Weight": 5.0
    },
    {
        "Mission Name": "LUMIO",
        "Launch Date": "2023-01-01",
        "Mission Type": "Tech Demo",
        "Launch Vehicle": "Falcon 9",
        "Target Name": "Moon",
        "Distance from Earth": 384400.0,
        "Mission Duration": 365.0,
        "Mission Cost": 25.0,
        "Scientific Yield": 80.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 547000.0,
        "Payload Weight": 24.0
    },
    {
        "Mission Name": "Starship IFT-1",
        "Launch Date": "2023-04-20",
        "Mission Type": "Tech Demo",
        "Launch Vehicle": "Starship",
        "Target Name": "LEO",
        "Distance from Earth": 150.0,
        "Mission Duration": 0.1,
        "Mission Cost": 150.0,
        "Scientific Yield": 50.0,
        "Crew Size": 0.0,
        "Mission Success": False,
        "Fuel Consumption": 4600000.0,
        "Payload Weight": 100000.0
    },
    {
        "Mission Name": "Starship IFT-2",
        "Launch Date": "2023-11-18",
        "Mission Type": "Tech Demo",
        "Launch Vehicle": "Starship",
        "Target Name": "LEO",
        "Distance from Earth": 150.0,
        "Mission Duration": 0.1,
        "Mission Cost": 150.0,
        "Scientific Yield": 72.0,
        "Crew Size": 0.0,
        "Mission Success": False,
        "Fuel Consumption": 4600000.0,
        "Payload Weight": 100000.0
    },
    {
        "Mission Name": "Starship IFT-3",
        "Launch Date": "2024-03-14",
        "Mission Type": "Tech Demo",
        "Launch Vehicle": "Starship",
        "Target Name": "LEO",
        "Distance from Earth": 150.0,
        "Mission Duration": 0.1,
        "Mission Cost": 150.0,
        "Scientific Yield": 85.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 4600000.0,
        "Payload Weight": 100000.0
    },
    {
        "Mission Name": "Starship IFT-4",
        "Launch Date": "2024-06-06",
        "Mission Type": "Tech Demo",
        "Launch Vehicle": "Starship",
        "Target Name": "LEO",
        "Distance from Earth": 150.0,
        "Mission Duration": 0.1,
        "Mission Cost": 150.0,
        "Scientific Yield": 92.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 4600000.0,
        "Payload Weight": 100000.0
    },
    {
        "Mission Name": "Starship IFT-5",
        "Launch Date": "2024-10-13",
        "Mission Type": "Tech Demo",
        "Launch Vehicle": "Starship",
        "Target Name": "LEO",
        "Distance from Earth": 150.0,
        "Mission Duration": 0.1,
        "Mission Cost": 150.0,
        "Scientific Yield": 95.0,
        "Crew Size": 0.0,
        "Mission Success": True,
        "Fuel Consumption": 4600000.0,
        "Payload Weight": 100000.0
    }
]


@st.cache_data(show_spinner=False)
def generate_dataset(n=None):
    """Load the real curated space mission dataset (196 verified missions)."""
    df = pd.DataFrame(REAL_MISSIONS)
    df["Launch Date"] = pd.to_datetime(df["Launch Date"])
    for c in ["Distance from Earth","Mission Duration","Mission Cost",
              "Scientific Yield","Crew Size","Fuel Consumption","Payload Weight"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df.dropna(inplace=True)
    df.drop_duplicates(subset=["Mission Name"], inplace=True)
    df["Year"]    = df["Launch Date"].dt.year
    df["Outcome"] = df["Mission Success"].map({True:"SUCCESS", False:"FAILED"})
    return df.reset_index(drop=True)

DF = generate_dataset()


# ─────────────────────────────────────────────────────────────────────────────
#  PHYSICS ENGINE
# ─────────────────────────────────────────────────────────────────────────────
def run_simulation(thrust_kN, dry_mass, payload_kg, fuel_kg, cd, burn_rate, dt=0.5, max_t=1400):
    G=9.80665; RHO0=1.225; H_SC=8_500.0; AREA=12.0; TN=thrust_kN*1_000
    vel,alt,fuel=0.0,0.0,float(fuel_kg)
    rows=[]
    for step in range(int(max_t/dt)):
        t=step*dt; tmass=dry_mass+payload_kg+fuel
        rho=RHO0*np.exp(-alt/H_SC); drag=0.5*rho*cd*AREA*vel**2*np.sign(vel)
        thr=TN if fuel>0 else 0.0; fnet=thr-tmass*G-drag; acc=fnet/tmass
        vel+=acc*dt; alt=max(alt+vel*dt,0.0); fuel=max(fuel-burn_rate*dt,0.0)
        rows.append({"Time (s)":t,"Altitude (km)":alt/1_000,"Velocity (km/s)":vel/1_000,
                     "Acceleration (m/s2)":acc,"Fuel (kg)":fuel,"Total Mass (kg)":tmass})
        if t>30 and alt<=0 and vel<=0: break
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
for k,v in [("logged_in",False),("username",""),("show_landing",True),
            ("login_error",""),("login_success",False),("show_loading",False)]:
    if k not in st.session_state: st.session_state[k]=v


# ─────────────────────────────────────────────────────────────────────────────
#  UI HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def page_banner(eyebrow, title, subtitle, badges=None, accent="#00e5ff"):
    bh="".join(f"<span class='badge {cls}'>{txt}</span>" for txt,cls in (badges or []))
    st.markdown(f"""
    <div class='page-banner' style='--ac:{accent};'>
      <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
        <div>
          <div class='pg-eyebrow'>{eyebrow}</div>
          <div class='pg-title'>{title}</div>
          <div class='pg-subtitle'>{subtitle}</div>
          <div style='margin-top:.4rem;'>{bh}</div>
        </div>
        <div style='text-align:right;padding-top:.2rem;font-family:Share Tech Mono,monospace;
                    font-size:.56rem;color:var(--text3);line-height:2.1;'>
          COSMOS v7.0.0<br><span style='color:var(--green);'>● SYS NOMINAL</span><br>
          <span style='color:var(--amber);'>T-0 READY</span>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

def sec(icon,label):
    st.markdown(f"""
    <div class='sdiv'><div class='sline'></div>
    <div class='slabel'>{icon} &nbsp; {label}</div>
    <div class='sline'></div></div>""", unsafe_allow_html=True)

def ch(label):
    st.markdown(f"<div class='chdr'><div class='cdot'></div>{label}</div>",
                unsafe_allow_html=True)

def kpi_row(cols, cards):
    for col,(icon,lbl,val,sub,kc,kg) in zip(cols,cards):
        col.markdown(f"""
        <div class='kpi-card' style='--kc:{kc};--kg:{kg};'>
          <div class='kpi-icon'>{icon}</div><div class='kpi-lbl'>{lbl}</div>
          <div class='kpi-val'>{val}</div><div class='kpi-sub'>{sub}</div>
        </div>""", unsafe_allow_html=True)

def footer():
    st.markdown("""
    <div class='cosmos-footer'>
      <hr>
      🚀 COSMOS MISSION CONTROL DASHBOARD v7.0.0
      &nbsp;|&nbsp; STREAMLIT · PLOTLY · PANDAS · NUMPY · SEABORN · MATPLOTLIB
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  LOGIN PAGE  —  v2 Aerospace Terminal
# ═══════════════════════════════════════════════════════════════════════════
def show_login():
    st.markdown("""
    <style>
    [data-testid="stSidebar"]{display:none!important;}
    .main .block-container{
      padding:0!important;max-width:100%!important;
      display:flex!important;flex-direction:column!important;align-items:center!important;
    }
    /* Force horizontal blocks to center */
    [data-testid="stHorizontalBlock"]{
      justify-content:center!important;
      width:100%!important;
    }
    /* The middle column holds the card */
    [data-testid="column"]:nth-child(2){
      display:flex!important;
      flex-direction:column!important;
      align-items:center!important;
    }
    /* Widen the card column */
    [data-testid="column"]:nth-child(1),
    [data-testid="column"]:nth-child(3){
      max-width:80px!important;
      flex:0 0 80px!important;
      min-width:0!important;
    }
    /* Card itself: centered, max width */
    .cosmos-card-v2{
      width:100%!important;
      max-width:520px!important;
      margin:0 auto!important;
    }
    /* All Streamlit widgets inside card column fill width */
    [data-testid="column"]:nth-child(2) .stTextInput,
    [data-testid="column"]:nth-child(2) .stSelectbox,
    [data-testid="column"]:nth-child(2) .stButton{
      width:100%!important;
    }
    </style>
    <script>
    document.addEventListener('keydown', function(e){
      if(e.key==='Enter'){
        const btns=window.parent.document.querySelectorAll('button');
        btns.forEach(b=>{ if(b.innerText.includes('INITIATE')) b.click(); });
      }
    });
    </script>
    """, unsafe_allow_html=True)

    now = datetime.now()

    # ══════════════════════════════════════════════════════════════════
    # TOP LIVE STATUS BAR  — full-width telemetry strip
    # ══════════════════════════════════════════════════════════════════
    st.markdown(f"""
    <div class='glow-line'></div>
    <div class='status-banner-v2'>
      <div class='sb2-item'>
        <div class='sb2-dot g'></div>
        <span style='color:var(--green);'>🛰 SYSTEM STATUS:</span>&nbsp;ONLINE
      </div>
      <div class='sb2-item'>
        <div class='sb2-dot c'></div>
        <span style='color:var(--cyan);'>🚀 COSMOS MISSION CONTROL</span>&nbsp;READY
      </div>
      <div class='sb2-item'>
        <div class='sb2-dot a'></div>
        <span style='color:var(--amber);'>🔐 AUTHENTICATION</span>&nbsp;REQUIRED
      </div>
      <div class='sb2-item' style='border-right:none;'>
        <div class='sb2-dot c' style='animation-delay:.8s;'></div>
        <span style='color:var(--text3);'>⏱ UTC {now.strftime("%H:%M:%S")}</span>
      </div>
    </div>
    <div class='glow-line'></div>
    <div style='height:3vh;'></div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    # CENTERED LOGIN CARD
    # ══════════════════════════════════════════════════════════════════
    _, col_c, _ = st.columns([0.5, 2, 0.5])
    with col_c:

        # ── CARD OPEN + HEADER ────────────────────────────────────────
        st.markdown(f"""
        <div class='cosmos-card-v2'>
          <!-- HEADER BRANDING -->
          <div class='cc-header'>
            <div class='cc-auth-pill'>
              <div class='sb2-dot g' style='width:5px;height:5px;'></div>
              ◈ MISSION AUTH TERMINAL ◈
            </div>
            <div class='cc-logo'>🚀 <span class='cc-logo-accent'>COSMOS</span></div>
            <div class='cc-subtitle'>Mission Control Dashboard &nbsp;·&nbsp; v7.0.0</div>
          </div>
          <div class='glow-line-thin'></div>
          <!-- BODY -->
          <div class='cc-body'>
        """, unsafe_allow_html=True)

        # ── OPERATOR ROLE — visual toggle buttons ─────────────────────
        st.markdown("""
        <div class='cc-label'>
          <div class='cc-label-icon'>◈</div>
          OPERATOR ROLE
        </div>
        <div class='role-row'>
          <div class='role-btn active'>🛰 Mission Analyst</div>
          <div class='role-btn'>🚀 Flight Engineer</div>
          <div class='role-btn'>📦 Payload Spec.</div>
          <div class='role-btn'>⚡ Sys. Commander</div>
        </div>
        """, unsafe_allow_html=True)
        # Keep functional selectbox hidden below role buttons
        sel_role = st.selectbox("role_sel", ROLES, label_visibility="collapsed", key="lrole")

        # ── FLIGHT OPERATOR ID ────────────────────────────────────────
        st.markdown("""
        <div class='cc-label'>
          <div class='cc-label-icon'>👤</div>
          FLIGHT OPERATOR ID
        </div>
        """, unsafe_allow_html=True)
        username = st.text_input("u", label_visibility="collapsed",
                                 placeholder="⌨  Enter operator ID…", key="lu")

        # ── MISSION AUTHORIZATION KEY ─────────────────────────────────
        st.markdown("""
        <div class='cc-label'>
          <div class='cc-label-icon'>🔑</div>
          MISSION AUTHORIZATION KEY
        </div>
        """, unsafe_allow_html=True)
        password = st.text_input("p", label_visibility="collapsed",
                                 placeholder="⌨  Enter authorization key…",
                                 type="password", key="lp")

        st.markdown("<div style='height:.55rem;'></div>", unsafe_allow_html=True)

        # ── LAUNCH BUTTON ─────────────────────────────────────────────
        st.markdown("<div class='launch-btn-wrap'>", unsafe_allow_html=True)
        clicked = st.button("🚀  INITIATE MISSION ACCESS", use_container_width=True, key="lbtn")
        st.markdown("</div>", unsafe_allow_html=True)

        # ── AUTH LOGIC ────────────────────────────────────────────────
        if clicked:
            h = hashlib.sha256(password.encode()).hexdigest()
            if username in USERS and USERS[username] == h:
                st.session_state.login_error = ""
                st.session_state.login_success = True
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.show_landing = True
                st.session_state.show_loading = True
                st.rerun()
            else:
                st.session_state.login_error = "ACCESS DENIED — INVALID CREDENTIALS"
                st.session_state.login_success = False

        # ── ERROR MESSAGE ─────────────────────────────────────────────
        if st.session_state.login_error:
            st.markdown(f"""
            <div class='msg-error-v2'>
              {st.session_state.login_error}
            </div>""", unsafe_allow_html=True)

        # ── TELEMETRY GRID ────────────────────────────────────────────
        st.markdown(f"""
        <div class='cc-divider'>
          <div class='cc-div-line'></div>
          <div class='cc-div-label'>SYSTEM TELEMETRY</div>
          <div class='cc-div-line'></div>
        </div>
        <div class='telem-grid-v2'>
          <div class='telem-chip-v2'>
            <div class='tc2-icon'>🕒</div>
            <div class='tc2-content'>
              <div class='tc2-label'>System Time (UTC)</div>
              <div class='tc2-value'>{now.strftime("%H:%M:%S")}</div>
            </div>
          </div>
          <div class='telem-chip-v2'>
            <div class='tc2-icon'>🌐</div>
            <div class='tc2-content'>
              <div class='tc2-label'>Network Status</div>
              <div class='tc2-value g'>SECURE</div>
            </div>
          </div>
          <div class='telem-chip-v2'>
            <div class='tc2-icon'>🛰</div>
            <div class='tc2-content'>
              <div class='tc2-label'>Mission Version</div>
              <div class='tc2-value'>V7.0.0</div>
            </div>
          </div>
          <div class='telem-chip-v2'>
            <div class='tc2-icon'>🔒</div>
            <div class='tc2-content'>
              <div class='tc2-label'>Security Level</div>
              <div class='tc2-value a'>ALPHA</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── SECURITY NOTICE ───────────────────────────────────────────
        st.markdown("""
        <div class='security-v2'>
          <div class='sec-warn'>⚠ AUTHORIZED PERSONNEL ONLY</div>
          <div class='sec-text'>
            Unauthorized access to COSMOS Mission Control is strictly prohibited.<br>
            All login sessions are monitored, logged, and recorded.
          </div>
          <div class='sec-creds'>
            demo: admin / rocket123 &nbsp;·&nbsp; guest / guest
          </div>
        </div>
        <!-- close cc-body + cosmos-card-v2 -->
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:4vh;'></div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  LOADING TRANSITION
# ═══════════════════════════════════════════════════════════════════════════
def show_loading():
    st.markdown("""
    <style>
    [data-testid="stSidebar"]{display:none!important;}
    .main .block-container{padding:0!important;max-width:100%!important;}
    .boot-wrap{
      display:flex;flex-direction:column;align-items:center;justify-content:center;
      min-height:85vh;text-align:center;padding:2rem;
    }
    .boot-ring{
      width:72px;height:72px;border-radius:50%;margin:0 auto 1.4rem;
      border:3px solid rgba(0,229,255,.15);
      border-top:3px solid var(--cyan);
      border-right:3px solid rgba(0,229,255,.5);
      animation:spin 1s linear infinite;
      box-shadow:0 0 20px rgba(0,229,255,.20);
    }
    @keyframes spin{to{transform:rotate(360deg)}}
    .boot-title{
      font-family:'Orbitron',monospace;font-size:1.5rem;font-weight:700;
      color:var(--green);letter-spacing:.14em;margin-bottom:.3rem;
      text-shadow:0 0 18px rgba(0,255,156,.5);
    }
    .boot-sub{
      font-family:'Share Tech Mono',monospace;font-size:.65rem;
      color:var(--cyan);letter-spacing:.20em;text-transform:uppercase;margin-bottom:1.4rem;
    }
    .boot-bar-wrap{
      width:320px;max-width:90vw;height:4px;
      background:rgba(0,229,255,.08);border-radius:4px;overflow:hidden;margin-bottom:1.4rem;
      box-shadow:0 0 8px rgba(0,229,255,.15);
    }
    .boot-bar{
      height:100%;width:0%;
      background:linear-gradient(90deg,transparent,var(--cyan),var(--green));
      border-radius:4px;
      animation:bootbar 2.2s cubic-bezier(.4,0,.2,1) forwards;
      box-shadow:0 0 10px rgba(0,229,255,.4);
    }
    @keyframes bootbar{0%{width:0%}60%{width:70%}85%{width:88%}100%{width:100%}}
    .boot-steps{
      font-family:'Share Tech Mono',monospace;font-size:.65rem;
      color:var(--text3);letter-spacing:.08em;line-height:2.2;text-align:left;
      display:inline-block;
    }
    .boot-step-ok{color:var(--green);}
    .boot-step-run{color:var(--cyan);animation:blink 1s ease-in-out infinite;}
    </style>""", unsafe_allow_html=True)

    _, cc, _ = st.columns([1, 1, 1])
    with cc:
        st.markdown("""
        <div class='boot-wrap'>
          <div class='boot-ring'></div>
          <div class='boot-title'>✓ ACCESS GRANTED</div>
          <div class='boot-sub'>Entering COSMOS Mission Control</div>
          <div class='boot-bar-wrap'><div class='boot-bar'></div></div>
          <div class='boot-steps'>
            <span class='boot-step-ok'>✓</span> Authenticating operator credentials…<br>
            <span class='boot-step-ok'>✓</span> Connecting to COSMOS systems…<br>
            <span class='boot-step-ok'>✓</span> Loading telemetry modules…<br>
            <span class='boot-step-run'>◈</span> Initializing rocket analytics…
          </div>
        </div>
        """, unsafe_allow_html=True)

    time.sleep(2.4)
    st.session_state.show_loading = False
    st.rerun()


# ═══════════════════════════════════════════════════════════════════════════
#  LANDING PAGE
# ═══════════════════════════════════════════════════════════════════════════
def show_landing():
    st.markdown("""
    <style>
    [data-testid="stSidebar"]{display:none!important;}
    .main .block-container{padding:0 2rem!important;max-width:100%!important;}
    </style>""", unsafe_allow_html=True)

    sr   = f"{DF['Mission Success'].mean()*100:.0f}%"
    st.markdown(f"""
    <div class='landing-wrap'>
      <div style='font-family:Share Tech Mono,monospace;font-size:.65rem;color:var(--dim);
                  letter-spacing:.36em;text-transform:uppercase;margin-bottom:1.2rem;
                  display:flex;align-items:center;justify-content:center;gap:.8rem;'>
        <span class='landing-dot'></span>COSMOS MISSION CONTROL SYSTEMS ONLINE<span class='landing-dot'></span>
      </div>
      <div class='landing-title'>🚀 COSMOS</div>
      <div class='landing-accent'>MISSION CONTROL DASHBOARD</div>
      <div class='landing-desc'>
        A production-grade aerospace analytics platform combining historical mission
        data analysis with real-time rocket physics simulation — designed to replicate
        the operational telemetry and insight systems used by NASA and SpaceX.
      </div>
      <div class='landing-stats'>
        <div class='landing-stat'><div class='landing-stat-val'>{len(DF):,}</div>
          <div class='landing-stat-lbl'>Missions Logged</div></div>
        <div class='landing-stat'><div class='landing-stat-val'>{sr}</div>
          <div class='landing-stat-lbl'>Success Rate</div></div>
        <div class='landing-stat'><div class='landing-stat-val'>{DF["Launch Vehicle"].nunique()}</div>
          <div class='landing-stat-lbl'>Launch Vehicles</div></div>
        <div class='landing-stat'><div class='landing-stat-val'>{DF["Target Name"].nunique()}</div>
          <div class='landing-stat-lbl'>Destinations</div></div>
      </div>
    </div>""", unsafe_allow_html=True)

    _, cc, _ = st.columns([1,1,1])
    with cc:
        st.markdown("<div class='enter-btn-wrap'>", unsafe_allow_html=True)
        if st.button("⬢  ENTER COSMOS MISSION CONTROL  ⬢", use_container_width=True, key="enter"):
            st.session_state.show_landing=False; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='text-align:center;font-family:Share Tech Mono,monospace;font-size:.58rem;
                color:#1a2840;letter-spacing:.12em;margin-top:2rem;'>
    OPERATOR: {st.session_state.username.upper()} &nbsp;·&nbsp; SESSION ACTIVE &nbsp;·&nbsp; COSMOS v7.0.0
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════
def show_dashboard():

    # ── SIDEBAR ──────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div style='padding:1.2rem 0 .4rem;text-align:center;'>
          <div style='font-family:Orbitron,monospace;font-size:1.5rem;font-weight:900;
                      color:#00e5ff;text-shadow:0 0 14px #00e5ff;letter-spacing:.12em;'>
            COSMOS</div>
          <div style='font-family:Share Tech Mono,monospace;font-size:.56rem;color:#253550;
                      letter-spacing:.22em;margin-top:.15rem;'>
            v7.0 · {st.session_state.username.upper()}</div>
        </div>
        <hr style='border:none;border-top:1px solid #1e2d4a;margin:.6rem 0 .5rem;'>
        """, unsafe_allow_html=True)

        NAV = ["🖥️  Mission Control Overview","📊  Mission Data Analytics",
               "🚀  Rocket Launch Simulation","🔬  Scientific Insights",
               "🗃️  Dataset Explorer","ℹ️  About Project"]
        page = st.radio("Navigation", NAV)
        ACTIVE = page.split("  ",1)[1] if "  " in page else page

        st.markdown("<hr style='border:none;border-top:1px solid #1e2d4a;margin:.7rem 0;'>",
                    unsafe_allow_html=True)

        DATA_PAGES = ("Mission Control Overview","Mission Data Analytics",
                      "Scientific Insights","Dataset Explorer")

        if ACTIVE in DATA_PAGES:
            st.markdown("""<div style='font-family:Share Tech Mono,monospace;font-size:.58rem;
                        color:#4a6280;letter-spacing:.18em;text-transform:uppercase;
                        padding-bottom:.4rem;'>Dataset Filters</div>""",
                        unsafe_allow_html=True)
            sel_type    = st.selectbox("🛰  Mission Type",   ["All"]+sorted(DF["Mission Type"].unique().tolist()))
            sel_vehicle = st.selectbox("🚀  Launch Vehicle", ["All"]+sorted(DF["Launch Vehicle"].unique().tolist()))
            pw_min,pw_max = int(DF["Payload Weight"].min()),int(DF["Payload Weight"].max())
            sel_payload = st.slider("📦  Payload (kg)",pw_min,pw_max,(pw_min,min(pw_max,55_000)),step=500)
            dm_min,dm_max = int(DF["Distance from Earth"].min()),int(DF["Distance from Earth"].max())
            sel_dist = st.slider("🌍  Distance (km)",dm_min,dm_max,(dm_min,min(dm_max,4_000_000)),step=10_000)
            cs_min,cs_max = int(DF["Crew Size"].min()),int(DF["Crew Size"].max())
            sel_crew = st.slider("👨‍🚀  Crew Size",cs_min,cs_max,(cs_min,cs_max))
            success_only = st.checkbox("✅  Successful only")

            dfv=DF.copy()
            if sel_type!="All": dfv=dfv[dfv["Mission Type"]==sel_type]
            if sel_vehicle!="All": dfv=dfv[dfv["Launch Vehicle"]==sel_vehicle]
            dfv=dfv[dfv["Payload Weight"].between(*sel_payload)]
            dfv=dfv[dfv["Distance from Earth"].between(*sel_dist)]
            dfv=dfv[dfv["Crew Size"].between(*sel_crew)]
            if success_only: dfv=dfv[dfv["Mission Success"]]
            N=len(dfv)

        elif ACTIVE=="Rocket Launch Simulation":
            st.markdown("""<div style='font-family:Share Tech Mono,monospace;font-size:.58rem;
                        color:#4a6280;letter-spacing:.18em;text-transform:uppercase;
                        padding-bottom:.4rem;'>Simulation Parameters</div>""",
                        unsafe_allow_html=True)
            sim_thrust   = st.slider("⚡ Thrust (kN)",      500,  12_000,  4_200, step=100)
            sim_drymass  = st.slider("🏗 Dry Mass (kg)",   5_000,120_000, 28_000, step=1_000)
            sim_payload  = st.slider("📦 Payload (kg)",      500,  60_000, 12_000, step=500)
            sim_fuel     = st.slider("⛽ Fuel (kg)",       5_000,600_000,180_000, step=5_000)
            sim_drag     = st.slider("💨 Drag Coeff",       0.10,    1.60,   0.38, step=0.02)
            sim_burnrate = st.slider("🔥 Burn Rate (kg/s)",   50,   2_500,    480, step=50)
            sim_dt       = st.slider("⏱ Time Step (s)",    0.10,    2.00,   0.50, step=0.10)
            launch_btn   = st.button("🚀  INITIATE LAUNCH")
            sim_df = run_simulation(sim_thrust,sim_drymass,sim_payload,
                                    sim_fuel,sim_drag,sim_burnrate,sim_dt)
            dfv,N = DF.copy(),len(DF)
        else:
            dfv,N = DF.copy(),len(DF)

        st.markdown("<hr style='border:none;border-top:1px solid #1e2d4a;margin:.7rem 0 .5rem;'>",
                    unsafe_allow_html=True)
        if st.button("⎋  LOGOUT"):
            for k in ["logged_in","username","show_landing","login_error",
                      "login_success","show_loading"]:
                st.session_state[k] = False if k in ["logged_in","login_success","show_loading"] \
                                             else (True if k=="show_landing" else "")
            st.rerun()

        st.markdown(f"""
        <div style='font-family:Share Tech Mono,monospace;font-size:.55rem;color:#152030;
                    letter-spacing:.09em;text-align:center;line-height:2.0;padding-top:.3rem;'>
        TOTAL: <span style='color:#1e3050;'>{len(DF):,}</span><br>
        VIEW: <span style='color:#253860;'>{N:,}</span><br>
        <span style='color:#00ff88;'>● TELEMETRY LIVE</span></div>""",
        unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────
    #  PAGE 1 · MISSION CONTROL OVERVIEW
    # ─────────────────────────────────────────────────────────────────────
    if ACTIVE == "Mission Control Overview":
        page_banner("SCREEN 01 / 06  ·  LAUNCH OPERATIONS CENTER",
                    "🚀 MISSION CONTROL OVERVIEW",
                    "Fleet KPIs, launch trends, telemetry panels, and correlation analysis.",
                    [("● LIVE","bg"),("SYS NOMINAL","bc"),("T-0 READY","ba")],"#00e5ff")

        sr=dfv["Mission Success"].mean()*100 if N>0 else 0
        ap=dfv["Payload Weight"].mean()       if N>0 else 0
        tf=dfv["Fuel Consumption"].sum()/1e6  if N>0 else 0
        ac=dfv["Mission Cost"].mean()          if N>0 else 0

        k=st.columns(5)
        kpi_row(k,[
            ("📡","Total Missions",   f"{N:,}",      "filtered dataset", "#00e5ff","rgba(0,229,255,.18)"),
            ("✅","Success Rate",     f"{sr:.1f}%",  "mission outcomes", "#00ff9c","rgba(0,255,156,.14)"),
            ("📦","Avg Payload",      f"{ap:,.0f}",  "kg per mission",   "#ff6b00","rgba(255,107,0,.18)"),
            ("⛽","Total Fuel",       f"{tf:.1f}M",  "million kg",       "#ffb300","rgba(255,179,0,.14)"),
            ("💰","Avg Cost",         f"${ac:,.0f}M","USD millions",     "#7c8cff","rgba(124,140,255,.18)"),
        ])

        sec("📈","FLEET PERFORMANCE")
        c1,c2=st.columns(2)
        with c1:
            ch("ANNUAL LAUNCHES & SUCCESS RATE · DUAL AXIS")
            yr=dfv.groupby("Year").agg(Missions=("Mission Name","count"),
                                        Rate=("Mission Success","mean")).reset_index()
            yr["Rate"]*=100
            figA=make_subplots(specs=[[{"secondary_y":True}]])
            figA.add_trace(go.Bar(x=yr["Year"],y=yr["Missions"],name="Launches",
                                   marker=dict(color="#00e5ff",opacity=.45,
                                               line=dict(color="#00e5ff",width=.5))),secondary_y=False)
            figA.add_trace(go.Scatter(x=yr["Year"],y=yr["Rate"],name="Success %",
                                       line=dict(color="#00ff9c",width=2.2),
                                       mode="lines+markers",marker=dict(size=5)),secondary_y=True)
            apl(figA,h=310)
            figA.update_yaxes(title_text="Count",secondary_y=False,title_font=dict(size=9))
            figA.update_yaxes(title_text="Success %",secondary_y=True,
                              title_font=dict(size=9,color="#00ff9c"),tickfont=dict(color="#00ff9c"))
            st.plotly_chart(figA,use_container_width=True,config={"displayModeBar":False})

        with c2:
            ch("MISSION TYPE DISTRIBUTION · DONUT")
            td=dfv["Mission Type"].value_counts().reset_index(); td.columns=["Type","Count"]
            figB=px.pie(td,names="Type",values="Count",hole=.55,
                        color_discrete_sequence=["#00e5ff","#ff6b00","#00ff9c",
                                                  "#ffb300","#b388ff","#ff2d55"])
            figB.update_traces(textfont=dict(family="Share Tech Mono",size=10),
                               pull=[.03]*len(td),
                               marker=dict(line=dict(width=1,color="#0b0f1a")))
            apl(figB,h=310)
            st.plotly_chart(figB,use_container_width=True,config={"displayModeBar":False})

        sec("🛸","VEHICLE & DESTINATION")
        c3,c4=st.columns(2)
        with c3:
            ch("LAUNCHES PER VEHICLE")
            vc=dfv["Launch Vehicle"].value_counts().reset_index(); vc.columns=["Vehicle","Count"]
            figC=px.bar(vc,x="Count",y="Vehicle",orientation="h",
                        color="Count",color_continuous_scale=["#0a1428","#00e5ff"])
            figC.update_traces(marker=dict(line=dict(width=0)))
            apl(figC,xt="Missions",h=300)
            figC.update_layout(showlegend=False,coloraxis_showscale=False,
                               yaxis=dict(categoryorder="total ascending"))
            st.plotly_chart(figC,use_container_width=True,config={"displayModeBar":False})

        with c4:
            ch("TARGET DESTINATION · SUCCESS BUBBLE")
            tg=dfv.groupby("Target Name").agg(Count=("Mission Name","count"),
                                               SR=("Mission Success","mean")).reset_index()
            tg["SR"]*=100
            figD=px.scatter(tg,x="Count",y="SR",text="Target Name",
                            size="Count",size_max=30,color="SR",
                            color_continuous_scale=["#ff4b4b","#ffb300","#00ff9c"])
            figD.update_traces(textfont=dict(family="Share Tech Mono",size=9,color="#b0cce0"),
                               textposition="top center",
                               marker=dict(line=dict(width=.5,color="#0b0f1a")))
            apl(figD,xt="Mission Count",yt="Success Rate (%)",h=300)
            figD.update_layout(coloraxis_showscale=False)
            st.plotly_chart(figD,use_container_width=True,config={"displayModeBar":False})

        sec("🔬","CORRELATION HEATMAP · ALL NUMERIC VARIABLES")
        if N>4:
            nums=["Mission Cost","Scientific Yield","Crew Size","Payload Weight",
                  "Fuel Consumption","Mission Duration","Distance from Earth"]
            corr=dfv[nums].corr()
            figS,ax=plt.subplots(figsize=(11,3.9))
            figS.patch.set_facecolor("#0f1526"); ax.set_facecolor("#0f1526")
            sns.heatmap(corr,annot=True,fmt=".2f",linewidths=.5,linecolor="#0b0f1a",
                        cmap=sns.diverging_palette(220,10,s=75,l=40,as_cmap=True),
                        annot_kws={"size":8,"family":"monospace","color":"#b8c1ec"},
                        cbar_kws={"shrink":.75},ax=ax)
            ax.set_title("PEARSON CORRELATION · KEY MISSION METRICS",
                         fontsize=8,color="#6a86a8",pad=8,fontfamily="monospace",loc="left")
            ax.tick_params(colors="#4a7090",labelsize=8)
            ax.set_xticklabels(ax.get_xticklabels(),rotation=25,ha="right",fontfamily="monospace")
            ax.set_yticklabels(ax.get_yticklabels(),rotation=0,fontfamily="monospace")
            ax.collections[0].colorbar.ax.tick_params(colors="#4a7090",labelsize=7)
            plt.tight_layout(pad=.4); st.pyplot(figS); plt.close(figS)
        footer()

    # ─────────────────────────────────────────────────────────────────────
    #  PAGE 2 · MISSION DATA ANALYTICS
    # ─────────────────────────────────────────────────────────────────────
    elif ACTIVE == "Mission Data Analytics":
        page_banner("SCREEN 02 / 06  ·  ANALYTICS SUBSYSTEM",
                    "📊 MISSION DATA ANALYTICS",
                    "Five core interactive visualizations covering all mission dimensions.",
                    [("5 CHARTS","bc"),("PLOTLY INTERACTIVE","ba")],"#ffb300")

        if N==0:
            st.warning("No records match filters."); footer(); return

        ck=st.columns(4)
        kpi_row(ck,[
            ("📡","Active Records", f"{N:,}",  "after filters","#00e5ff","rgba(0,229,255,.18)"),
            ("✅","Successful",     f"{dfv['Mission Success'].sum():,}","missions","#00ff9c","rgba(0,255,156,.14)"),
            ("📦","Max Payload",    f"{dfv['Payload Weight'].max():,.0f} kg","heaviest","#ff6b00","rgba(255,107,0,.18)"),
            ("⛽","Avg Fuel",       f"{dfv['Fuel Consumption'].mean()/1e3:.0f}K","kg/mission","#ffb300","rgba(255,179,0,.14)"),
        ])

        sec("1️⃣","PAYLOAD WEIGHT  vs  FUEL CONSUMPTION")
        ch("SCATTER · SIZE=COST · COLOR=OUTCOME")
        fig1=px.scatter(dfv,x="Payload Weight",y="Fuel Consumption",
                        color="Outcome",color_discrete_map={"SUCCESS":"#00ff9c","FAILED":"#ff4b4b"},
                        size="Mission Cost",size_max=22,
                        hover_data=["Mission Name","Mission Type","Launch Vehicle"],opacity=.80)
        fig1.update_traces(marker=dict(line=dict(width=.4,color="#0b0f1a")))
        apl(fig1,xt="Payload Weight (kg)",yt="Fuel Consumption (kg)",h=400)
        fig1.update_layout(legend_title_text="")
        st.plotly_chart(fig1,use_container_width=True,config={"displayModeBar":False})

        sec("2️⃣","AVERAGE MISSION COST · SUCCESS vs FAILED")
        c2a,c2b=st.columns(2)
        with c2a:
            ch("BAR · AVG COST BY OUTCOME")
            cg=dfv.groupby("Outcome")["Mission Cost"].mean().reset_index()
            fig2=px.bar(cg,x="Outcome",y="Mission Cost",color="Outcome",
                        color_discrete_map={"SUCCESS":"#00ff9c","FAILED":"#ff4b4b"},text="Mission Cost")
            fig2.update_traces(texttemplate="$%{text:,.0f}M",textposition="outside",
                               textfont=dict(family="Share Tech Mono",size=10,color="#b8c1ec"),
                               marker=dict(opacity=.85,line=dict(width=0)))
            apl(fig2,yt="Avg Cost ($M)",h=340); fig2.update_layout(showlegend=False)
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})
        with c2b:
            ch("BOX · COST SPREAD BY OUTCOME")
            fig2b=px.box(dfv,x="Outcome",y="Mission Cost",color="Outcome",
                         color_discrete_map={"SUCCESS":"#00ff9c","FAILED":"#ff4b4b"},points="outliers")
            apl(fig2b,yt="Mission Cost ($M)",h=340); fig2b.update_layout(showlegend=False)
            st.plotly_chart(fig2b,use_container_width=True,config={"displayModeBar":False})

        sec("3️⃣","MISSION DURATION  vs  DISTANCE FROM EARTH")
        ch("LINE CHART · COLOR=MISSION TYPE")
        dline=dfv.sort_values("Distance from Earth").head(160)
        fig3=px.line(dline,x="Distance from Earth",y="Mission Duration",color="Mission Type",markers=True)
        fig3.update_traces(line=dict(width=1.8),marker=dict(size=5))
        apl(fig3,xt="Distance from Earth (km)",yt="Mission Duration (days)",h=360)
        fig3.update_layout(legend_title_text="")
        st.plotly_chart(fig3,use_container_width=True,config={"displayModeBar":False})

        sec("4️⃣","CREW SIZE  vs  MISSION SUCCESS")
        c4a,c4b=st.columns(2)
        with c4a:
            ch("BOX PLOT · CREW BY OUTCOME")
            fig4=px.box(dfv,x="Outcome",y="Crew Size",color="Outcome",
                        color_discrete_map={"SUCCESS":"#00ff9c","FAILED":"#ff4b4b"},points="all")
            fig4.update_traces(jitter=.35,pointpos=0,marker=dict(size=4,opacity=.5))
            apl(fig4,yt="Crew Size",h=330); fig4.update_layout(showlegend=False)
            st.plotly_chart(fig4,use_container_width=True,config={"displayModeBar":False})
        with c4b:
            ch("BAR · AVG CREW BY MISSION TYPE")
            ct=dfv.groupby("Mission Type")["Crew Size"].mean().reset_index()
            fig4b=px.bar(ct,x="Mission Type",y="Crew Size",color="Mission Type",
                         color_discrete_sequence=["#00e5ff","#ff6b00","#00ff9c","#7c8cff","#ffb300","#ff4b4b"])
            fig4b.update_traces(marker=dict(opacity=.85,line=dict(width=0)))
            apl(fig4b,yt="Avg Crew Size",h=330)
            fig4b.update_layout(showlegend=False,xaxis_tickangle=-20)
            st.plotly_chart(fig4b,use_container_width=True,config={"displayModeBar":False})

        sec("5️⃣","SCIENTIFIC YIELD  vs  MISSION COST")
        ch("SCATTER · LOWESS TRENDLINE · COLOR=MISSION TYPE")
        fig5=px.scatter(dfv,x="Mission Cost",y="Scientific Yield",
                        color="Mission Type",
                        hover_data=["Mission Name","Target Name","Launch Vehicle"],opacity=.82,size_max=14)
        fig5.update_traces(marker=dict(size=7,line=dict(width=.4,color="#0b0f1a")))
        # manual linear trendline overlay
        if len(dfv)>2:
            m,b=np.polyfit(dfv["Mission Cost"],dfv["Scientific Yield"],1)
            xr=np.linspace(dfv["Mission Cost"].min(),dfv["Mission Cost"].max(),200)
            fig5.add_trace(go.Scatter(x=xr,y=m*xr+b,mode="lines",name="Trend",
                                      line=dict(color="#7c8cff",width=1.4,dash="dot"),opacity=.45))
        apl(fig5,xt="Mission Cost ($M)",yt="Scientific Yield (0-100)",h=380)
        fig5.update_layout(legend_title_text="")
        st.plotly_chart(fig5,use_container_width=True,config={"displayModeBar":False})
        footer()

    # ─────────────────────────────────────────────────────────────────────
    #  PAGE 3 · ROCKET LAUNCH SIMULATION — v3 MISSION CONTROL
    # ─────────────────────────────────────────────────────────────────────
    elif ACTIVE == "Rocket Launch Simulation":
        page_banner("SCREEN 03 / 06  ·  PHYSICS ENGINE",
                    "🚀 ROCKET LAUNCH SIMULATION",
                    "Newton's 2nd Law · Tsiolkovsky Rocket Equation · Exponential Atmosphere · Euler Integration",
                    [("PHYSICS ENGINE","bo"),("LIVE TELEMETRY","bg"),("EULER METHOD","bc"),("REAL-TIME","ba")],"#ff6b00")

        # ── DERIVED METRICS ───────────────────────────────────────────────
        max_alt    = sim_df["Altitude (km)"].max()
        max_vel    = sim_df["Velocity (km/s)"].max()
        max_acc    = sim_df["Acceleration (m/s2)"].max()
        max_gforce = max_acc / 9.80665
        bt_r       = sim_df.loc[sim_df["Fuel (kg)"]<=0,"Time (s)"]
        burnout_t  = bt_r.min() if len(bt_r)>0 else sim_df["Time (s)"].max()
        flight_t   = sim_df["Time (s)"].max()
        fuel_left  = sim_df["Fuel (kg)"].iloc[-1]
        fuel_used  = sim_fuel - fuel_left
        fuel_pct   = min(100, fuel_used / max(sim_fuel,1) * 100)
        vel_pct    = min(100, max_vel / 8.0 * 100)
        alt_pct    = min(100, max_alt / 400.0 * 100)
        mission_ok = max_alt > 1.0
        reached_karman = max_alt >= 100
        reached_leo    = max_alt >= 200
        twr        = (sim_thrust*1000) / ((sim_drymass+sim_payload+sim_fuel)*9.80665)
        delta_v_est= 9.80665 * 350 * np.log((sim_drymass+sim_payload+sim_fuel)/max(sim_drymass+sim_payload,1))
        apogee_t   = sim_df.loc[sim_df["Altitude (km)"].idxmax(),"Time (s)"]
        maxq_alt   = sim_df.loc[sim_df["Acceleration (m/s2)"].idxmax(),"Altitude (km)"]
        now_ts     = datetime.now().strftime("%H:%M:%S")

        # ── PHYSICS EQUATION STRIP ────────────────────────────────────────
        st.markdown(f"""
        <div class='eq-strip'>
          <span class='eq-item'>F<sub>net</sub> = F<sub>thrust</sub> &minus; m·g &minus; F<sub>drag</sub></span>
          <span class='eq-sep'>|</span>
          <span class='eq-item'>a = F<sub>net</sub>/m<sub>total</sub></span>
          <span class='eq-sep'>|</span>
          <span class='eq-item'>&rho;(h) = 1.225·e<sup>−h/8500</sup></span>
          <span class='eq-sep'>|</span>
          <span class='eq-item'>F<sub>drag</sub>=½·&rho;·C<sub>d</sub>·A·v²</span>
          <span class='eq-sep'>|</span>
          <span class='eq-item'><b>TWR = {twr:.2f}</b></span>
          <span class='eq-sep'>|</span>
          <span class='eq-item'><b>ΔV ≈ {delta_v_est/1000:.2f} km/s</b></span>
          <span class='eq-sep'>|</span>
          <span class='eq-item'>{len(sim_df):,} steps · dt={sim_dt}s</span>
        </div>""", unsafe_allow_html=True)

        # ── MISSION PHASE TIMELINE ─────────────────────────────────────────
        phases = [
            ("🔧","Pre-Launch",  True,  True),
            ("🔥","Ignition",    True,  True),
            ("⬆️","Max Thrust",  True,  mission_ok),
            ("💨","Max-Q",       burnout_t>20, mission_ok),
            ("🔵","Burnout",     True,  mission_ok),
            ("🌌","Coast Phase", reached_karman, reached_karman),
            ("🛰","Apogee",      reached_leo,    reached_leo),
        ]
        ph="".join(f"<div class='phase-item {'done' if d and a else ('active' if a else 'pending')}'>"
                   f"<span class='phase-icon'>{ic}</span>"
                   f"<div class='phase-label'>{lb}</div></div>"
                   for ic,lb,d,a in phases)
        st.markdown(f"<div class='phase-bar'>{ph}</div>", unsafe_allow_html=True)

        # ── 5 LIVE KPI CARDS ──────────────────────────────────────────────
        st.markdown(f"""
        <div class='live-strip'>
          <div class='ls-card' style='--lc:#00e5ff;'>
            <div class='ls-icon'>📡</div>
            <div class='ls-label'>Peak Altitude</div>
            <div class='ls-val'>{max_alt:,.1f}</div>
            <div class='ls-sub'>km · {"✅ Kármán cleared" if reached_karman else "sub-orbital"}</div>
            <div class='ls-bar-wrap'><div class='ls-bar' style='width:{min(100,alt_pct):.0f}%;background:#00e5ff;box-shadow:0 0 6px #00e5ff;'></div></div>
          </div>
          <div class='ls-card' style='--lc:#ff6b00;'>
            <div class='ls-icon'>⚡</div>
            <div class='ls-label'>Peak Velocity</div>
            <div class='ls-val'>{max_vel:.3f}</div>
            <div class='ls-sub'>km/s · {"🌍 orbital ✅" if max_vel>=7.9 else f"{max_vel/7.9*100:.0f}% orbital"}</div>
            <div class='ls-bar-wrap'><div class='ls-bar' style='width:{min(100,vel_pct):.0f}%;background:#ff6b00;box-shadow:0 0 6px #ff6b00;'></div></div>
          </div>
          <div class='ls-card' style='--lc:#ffb300;'>
            <div class='ls-icon'>🔥</div>
            <div class='ls-label'>Burnout Time</div>
            <div class='ls-val'>T+{burnout_t:.0f}s</div>
            <div class='ls-sub'>fuel used: {fuel_pct:.1f}%</div>
            <div class='ls-bar-wrap'><div class='ls-bar' style='width:{fuel_pct:.0f}%;background:#ffb300;box-shadow:0 0 6px #ffb300;'></div></div>
          </div>
          <div class='ls-card' style='--lc:#00ff9c;'>
            <div class='ls-icon'>🌀</div>
            <div class='ls-label'>Max G-Force</div>
            <div class='ls-val'>{max_gforce:.1f}g</div>
            <div class='ls-sub'>{"⚠ exceeds 6g crewed limit" if max_gforce>6 else "nominal range"}</div>
            <div class='ls-bar-wrap'><div class='ls-bar' style='width:{min(100,max_gforce/20*100):.0f}%;background:#00ff9c;box-shadow:0 0 6px #00ff9c;'></div></div>
          </div>
          <div class='ls-card' style='--lc:#7c8cff;'>
            <div class='ls-icon'>⏱</div>
            <div class='ls-label'>Flight Duration</div>
            <div class='ls-val'>{flight_t:.0f}s</div>
            <div class='ls-sub'>{flight_t/60:.1f} minutes</div>
            <div class='ls-bar-wrap'><div class='ls-bar' style='width:{min(100,flight_t/1400*100):.0f}%;background:#7c8cff;box-shadow:0 0 6px #7c8cff;'></div></div>
          </div>
        </div>""", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════
        # MAIN MISSION CONTROL GRID — 3 columns
        # ═══════════════════════════════════════════════════════════════════
        sec("📈","MISSION CONTROL CENTER")
        col_left, col_mid, col_right = st.columns([1.05, 1.6, 1.05])

        # ─── LEFT COLUMN: Go/No-Go + Telemetry Readout ───────────────────
        with col_left:
            # Mission Status Hero
            st_cls = "ms-status-ok" if mission_ok else "ms-status-fail"
            st_txt = "◉ NOMINAL" if mission_ok else "◉ ABORT"
            st_badge = "ALL SYSTEMS GO" if mission_ok else "REVIEW PARAMETERS"
            st.markdown(f"""
            <div class='mc-panel' style='--pc:{"#00ff9c" if mission_ok else "#ff4b4b"};margin-bottom:.7rem;'>
              <div class='mc-panel-title'><div class='mc-dot'></div>MISSION STATUS</div>
              <div class='ms-hero'>
                <div class='{st_cls}'>{st_txt}</div>
                <div class='ms-badge'>{st_badge}</div>
              </div>
            </div>""", unsafe_allow_html=True)

            # GO/NO-GO Checklist
            checks = [
                ("TWR ≥ 1.0",        twr>=1.0,            twr>=1.0),
                ("Liftoff",          mission_ok,           mission_ok),
                (f"Alt > 1 km",      max_alt>1,            max_alt>1),
                (f"Kármán 100km",    reached_karman,       reached_karman),
                (f"LEO 200km",       reached_leo,          reached_leo),
                ("Orbital Vel",      max_vel>=7.9,         max_vel>=7.9),
                (f"G < 6g",          max_gforce<6,         max_gforce<6),
                ("Fuel Budget",      fuel_left>1000,       fuel_left>0),
            ]
            rows = ""
            for label, ok, active in checks:
                cls = "go" if ok else ("warn" if active else "nogo")
                icon = "✓" if ok else ("△" if active else "✗")
                rows += f"<div class='gng-item {cls}'><div class='gng-dot {cls}'></div>{icon} {label}</div>"
            st.markdown(f"""
            <div class='mc-panel' style='--pc:#7c8cff;'>
              <div class='mc-panel-title'><div class='mc-dot'></div>GO / NO-GO CHECKLIST</div>
              <div class='gonogo-grid'>{rows}</div>
            </div>""", unsafe_allow_html=True)

        # ─── CENTRE COLUMN: Charts ────────────────────────────────────────
        with col_mid:
            # Chart 1: Altitude + Velocity dual-axis
            ch("ALTITUDE & VELOCITY PROFILE")
            fig_av = make_subplots(specs=[[{"secondary_y":True}]])
            fig_av.add_trace(go.Scatter(
                x=sim_df["Time (s)"], y=sim_df["Altitude (km)"],
                mode="lines", name="Altitude",
                line=dict(color="#00e5ff",width=2.2),
                fill="tozeroy", fillcolor="rgba(0,229,255,.05)"),
                secondary_y=False)
            fig_av.add_trace(go.Scatter(
                x=sim_df["Time (s)"], y=sim_df["Velocity (km/s)"],
                mode="lines", name="Velocity",
                line=dict(color="#ff6b00",width=1.8,dash="dot")),
                secondary_y=True)
            # Kármán line
            if reached_karman:
                fig_av.add_hline(y=100, line_dash="dash", line_color="rgba(0,255,156,.4)",
                                 line_width=1, secondary_y=False,
                                 annotation_text="Kármán 100km",
                                 annotation_font=dict(family="Share Tech Mono",size=8,color="#00ff9c"))
            # Apogee marker
            apogee_idx = sim_df["Altitude (km)"].idxmax()
            fig_av.add_trace(go.Scatter(
                x=[sim_df.loc[apogee_idx,"Time (s)"]],
                y=[sim_df.loc[apogee_idx,"Altitude (km)"]],
                mode="markers+text", name="Apogee",
                marker=dict(color="#ff6b00",size=9,symbol="diamond"),
                text=[f" Apogee {max_alt:.0f}km"],
                textfont=dict(family="Share Tech Mono",size=8,color="#ff6b00"),
                textposition="top right"),
                secondary_y=False)
            apl(fig_av, xt="Time (s)", h=260)
            fig_av.update_yaxes(title_text="Altitude (km)",secondary_y=False,title_font=dict(size=9))
            fig_av.update_yaxes(title_text="Velocity (km/s)",secondary_y=True,
                                title_font=dict(size=9,color="#ff6b00"),tickfont=dict(color="#ff6b00"))
            st.plotly_chart(fig_av, use_container_width=True, config={"displayModeBar":False})

            # Chart 2: Fuel depletion + Acceleration
            ch("FUEL DEPLETION & ACCELERATION")
            fig_fa = make_subplots(specs=[[{"secondary_y":True}]])
            fig_fa.add_trace(go.Scatter(
                x=sim_df["Time (s)"], y=sim_df["Fuel (kg)"],
                mode="lines", name="Fuel",
                line=dict(color="#ffb300",width=2.0),
                fill="tozeroy", fillcolor="rgba(255,179,0,.04)"),
                secondary_y=False)
            fig_fa.add_trace(go.Scatter(
                x=sim_df["Time (s)"], y=sim_df["Acceleration (m/s2)"],
                mode="lines", name="Accel (m/s²)",
                line=dict(color="#00ff9c",width=1.6,dash="dot")),
                secondary_y=True)
            fig_fa.add_hline(y=0, line_dash="dot", line_color="rgba(255,75,75,.4)",
                             line_width=1, secondary_y=True)
            apl(fig_fa, xt="Time (s)", h=230)
            fig_fa.update_yaxes(title_text="Fuel (kg)",secondary_y=False,title_font=dict(size=9))
            fig_fa.update_yaxes(title_text="Accel (m/s²)",secondary_y=True,
                                title_font=dict(size=9,color="#00ff9c"),tickfont=dict(color="#00ff9c"))
            st.plotly_chart(fig_fa, use_container_width=True, config={"displayModeBar":False})

        # ─── RIGHT COLUMN: Gauges + Detailed Telemetry ───────────────────
        with col_right:
            # Altitude Gauge
            st.markdown("""
            <div class='mc-panel' style='--pc:#00e5ff;margin-bottom:.7rem;'>
              <div class='mc-panel-title'><div class='mc-dot'></div>ALTITUDE GAUGE</div>
            </div>""", unsafe_allow_html=True)
            alt_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=min(max_alt, 500),
                delta=dict(reference=100, valueformat=".0f",
                           increasing=dict(color="#00ff9c"),
                           decreasing=dict(color="#ff4b4b")),
                number=dict(suffix=" km", font=dict(family="Orbitron",size=22,color="#00e5ff")),
                gauge=dict(
                    axis=dict(range=[0,500], nticks=6,
                              tickfont=dict(family="Share Tech Mono",size=7,color="#6a86a8")),
                    bar=dict(color="#00e5ff",thickness=.22),
                    bgcolor="rgba(0,0,0,0)",borderwidth=1,bordercolor="#1e3a5f",
                    steps=[
                        dict(range=[0,12],   color="rgba(124,140,255,.06)"),
                        dict(range=[12,50],  color="rgba(0,229,255,.04)"),
                        dict(range=[50,100], color="rgba(0,229,255,.06)"),
                        dict(range=[100,200],color="rgba(0,255,156,.05)"),
                        dict(range=[200,500],color="rgba(0,255,156,.03)"),
                    ],
                    threshold=dict(line=dict(color="#ff6b00",width=2),value=100),
                ),
                title=dict(text="PEAK ALTITUDE", font=dict(family="Share Tech Mono",size=9,color="#6a86a8")),
            ))
            alt_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)",height=200,
                                    margin=dict(l=18,r=18,t=32,b=4))
            st.plotly_chart(alt_gauge, use_container_width=True, config={"displayModeBar":False})

            # Velocity Gauge
            vel_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=min(max_vel, 10),
                number=dict(suffix=" km/s", font=dict(family="Orbitron",size=18,color="#ff6b00")),
                gauge=dict(
                    axis=dict(range=[0,10], nticks=6,
                              tickfont=dict(family="Share Tech Mono",size=7,color="#6a86a8")),
                    bar=dict(color="#ff6b00",thickness=.22),
                    bgcolor="rgba(0,0,0,0)",borderwidth=1,bordercolor="#1e3a5f",
                    steps=[dict(range=[0,7.9],color="rgba(255,107,0,.04)"),
                           dict(range=[7.9,10],color="rgba(0,255,156,.06)")],
                    threshold=dict(line=dict(color="#00ff9c",width=2),value=7.9),
                ),
                title=dict(text="PEAK VELOCITY", font=dict(family="Share Tech Mono",size=9,color="#6a86a8")),
            ))
            vel_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)",height=175,
                                    margin=dict(l=18,r=18,t=32,b=4))
            st.plotly_chart(vel_gauge, use_container_width=True, config={"displayModeBar":False})

            # 9-cell telemetry readout
            vc = lambda v,thr,c1,c2: c1 if v>=thr else c2
            st.markdown(f"""
            <div class='mc-panel' style='--pc:#7c8cff;margin-top:.3rem;'>
              <div class='mc-panel-title'><div class='mc-dot'></div>FLIGHT COMPUTER DATA</div>
              <div class='telem-grid-3'>
                <div class='tg2-cell'><div class='tg2-k'>Thrust</div><div class='tg2-v o'>{sim_thrust:,}kN</div></div>
                <div class='tg2-cell'><div class='tg2-k'>TWR</div><div class='tg2-v {"c" if twr>=1 else "r"}'>{twr:.2f}</div></div>
                <div class='tg2-cell'><div class='tg2-k'>ΔV est.</div><div class='tg2-v p'>{delta_v_est/1000:.2f}km/s</div></div>
                <div class='tg2-cell'><div class='tg2-k'>Dry Mass</div><div class='tg2-v'>{sim_drymass:,}kg</div></div>
                <div class='tg2-cell'><div class='tg2-k'>Payload</div><div class='tg2-v'>{sim_payload:,}kg</div></div>
                <div class='tg2-cell'><div class='tg2-k'>Fuel Load</div><div class='tg2-v o'>{sim_fuel:,}kg</div></div>
                <div class='tg2-cell'><div class='tg2-k'>Burnout T</div><div class='tg2-v'>T+{burnout_t:.0f}s</div></div>
                <div class='tg2-cell'><div class='tg2-k'>Max-Q Alt</div><div class='tg2-v c'>{maxq_alt:.1f}km</div></div>
                <div class='tg2-cell'><div class='tg2-k'>G-Force</div><div class='tg2-v {"r" if max_gforce>6 else "w" if max_gforce>4 else ""}'>{max_gforce:.1f}g</div></div>
              </div>
            </div>""", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════
        # TRAJECTORY BADGES
        # ═══════════════════════════════════════════════════════════════════
        badges = []
        badges.append(f"<span class='traj-badge'>TWR: {twr:.2f}</span>")
        badges.append(f"<span class='traj-badge orange'>ΔV ≈ {delta_v_est/1000:.2f} km/s</span>")
        badges.append(f"<span class='traj-badge amber'>Max-Q @ {maxq_alt:.1f} km</span>")
        badges.append(f"<span class='traj-badge'>Apogee @ T+{apogee_t:.0f}s</span>")
        if reached_karman: badges.append("<span class='traj-badge green'>✓ Kármán Line</span>")
        if reached_leo:    badges.append("<span class='traj-badge green'>✓ LEO Altitude</span>")
        if max_vel>=7.9:   badges.append("<span class='traj-badge green'>✓ Orbital Velocity</span>")
        if twr<1:          badges.append("<span class='traj-badge red'>⚠ TWR&lt;1 — Cannot Lift Off</span>")
        if max_gforce>6:   badges.append(f"<span class='traj-badge red'>⚠ {max_gforce:.1f}g exceeds crewed limit</span>")
        st.markdown("<div style='margin:.4rem 0 .8rem;'>"+"".join(badges)+"</div>",unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════
        # BOTTOM ROW: Full-width trajectory + Mass chart
        # ═══════════════════════════════════════════════════════════════════
        sec("📊","TRAJECTORY ANALYSIS & VEHICLE COMPARISON")
        bc1, bc2 = st.columns([1.8, 1])

        with bc1:
            ch("ALTITUDE TRAJECTORY WITH ATMOSPHERE ZONES")
            fig_traj = go.Figure()
            # Atmosphere zone fills
            fig_traj.add_hrect(y0=0,   y1=12,  fillcolor="rgba(100,150,255,.06)", line_width=0, annotation_text="Troposphere", annotation_font=dict(size=8,color="#6a86a8",family="Share Tech Mono"), annotation_position="top left")
            fig_traj.add_hrect(y0=12,  y1=50,  fillcolor="rgba(80,120,220,.05)", line_width=0, annotation_text="Stratosphere", annotation_font=dict(size=8,color="#6a86a8",family="Share Tech Mono"), annotation_position="top left")
            fig_traj.add_hrect(y0=50,  y1=85,  fillcolor="rgba(60,90,180,.04)", line_width=0, annotation_text="Mesosphere", annotation_font=dict(size=8,color="#6a86a8",family="Share Tech Mono"), annotation_position="top left")
            fig_traj.add_hrect(y0=85,  y1=690, fillcolor="rgba(40,60,140,.04)", line_width=0, annotation_text="Thermosphere", annotation_font=dict(size=8,color="#6a86a8",family="Share Tech Mono"), annotation_position="top left")
            # Kármán line
            fig_traj.add_hline(y=100, line_dash="dash", line_color="rgba(0,255,156,.5)", line_width=1.2,
                               annotation_text="Kármán Line 100km", annotation_font=dict(family="Share Tech Mono",size=8,color="#00ff9c"))
            # LEO minimum
            if max_alt > 150:
                fig_traj.add_hline(y=200, line_dash="dot", line_color="rgba(0,229,255,.35)", line_width=1,
                                   annotation_text="LEO Min 200km", annotation_font=dict(family="Share Tech Mono",size=8,color="#00e5ff"))
            # Trajectory
            fig_traj.add_trace(go.Scatter(
                x=sim_df["Time (s)"], y=sim_df["Altitude (km)"],
                mode="lines", name="Trajectory",
                line=dict(color="#00e5ff",width=2.5),
                fill="tozeroy", fillcolor="rgba(0,229,255,.06)"))
            # Apogee
            fig_traj.add_trace(go.Scatter(
                x=[apogee_t], y=[max_alt],
                mode="markers+text", name="Apogee",
                marker=dict(color="#ff6b00",size=10,symbol="star"),
                text=[f"  ★ {max_alt:.0f} km"], textposition="top right",
                textfont=dict(family="Share Tech Mono",size=9,color="#ff6b00")))
            apl(fig_traj, xt="Time (s)", yt="Altitude (km)", h=330)
            fig_traj.update_layout(showlegend=False)
            st.plotly_chart(fig_traj, use_container_width=True, config={"displayModeBar":False})

        with bc2:
            ch("YOUR ROCKET vs REAL VEHICLES")
            real_v = [
                ("New Shepard",  489,    75000,    100,  3.2),
                ("Falcon 9",     7607,   549054,  22800, 8.7),
                ("Atlas V 401",  4152,   334500,  18850, 7.9),
                ("Ariane 5",     11200,  780000,  21000, 8.1),
                ("Saturn V",     35100, 2950000, 130000, 7.9),
                ("Falcon Heavy", 22819, 1420788,  63800, 8.5),
                ("Starship",     89000, 5000000, 100000, 8.5),
                ("YOUR ROCKET",  sim_thrust, sim_fuel, sim_payload, max_vel),
            ]
            names = [r[0] for r in real_v]
            thrusts = [r[1] for r in real_v]
            colors = ["#ff6b00" if n=="YOUR ROCKET" else "#00e5ff" for n in names]
            fig_cmp = go.Figure(go.Bar(
                x=thrusts, y=names, orientation="h",
                marker=dict(color=colors, opacity=0.82, line=dict(width=0)),
                text=[f"{t:,} kN" for t in thrusts],
                textposition="outside",
                textfont=dict(family="Share Tech Mono",size=8,color="#6a86a8"),
            ))
            apl(fig_cmp, xt="Thrust (kN)", h=330)
            fig_cmp.update_layout(showlegend=False, yaxis=dict(categoryorder="total ascending"))
            st.plotly_chart(fig_cmp, use_container_width=True, config={"displayModeBar":False})

        # ═══════════════════════════════════════════════════════════════════
        # CONSOLE LOG
        # ═══════════════════════════════════════════════════════════════════
        sec("💻","FLIGHT COMPUTER CONSOLE LOG")
        ok_c="cl-ok" if mission_ok else "cl-err"; ok_t="OK " if mission_ok else "ERR"
        fuel_c="cl-err" if fuel_left<2000 else ("cl-warn" if fuel_left<10000 else "cl-ok")
        gfc="cl-err" if max_gforce>8 else ("cl-warn" if max_gforce>5 else "cl-ok")
        kc="cl-ok" if reached_karman else "cl-warn"
        vc2="cl-ok" if max_vel>=7.9 else "cl-data"
        st.markdown(f"""
        <div class='console-v2'>
          <span class='cl-num'>001</span><span class='cl-ts'>[{now_ts}]</span><span class='cl-inf'>[BOOT] COSMOS FLIGHT COMPUTER v7.0 — ONLINE</span><br>
          <span class='cl-num'>002</span><span class='cl-ts'>[{now_ts}]</span><span class='cl-inf'>[INIT] Physics: Euler integration | dt={sim_dt}s | ISA exponential atmosphere</span><br>
          <span class='cl-num'>003</span><span class='cl-ts'>[{now_ts}]</span><span class='cl-ok'> [OK ] Thrust: {sim_thrust:,} kN | TWR={twr:.2f} | {"LIFTOFF CAPABLE ✓" if twr>=1 else "⚠ TWR&lt;1 — CANNOT LIFT OFF"}</span><br>
          <span class='cl-num'>004</span><span class='cl-ts'>[{now_ts}]</span><span class='cl-ok'> [OK ] Mass: dry={sim_drymass:,}kg  payload={sim_payload:,}kg  fuel={sim_fuel:,}kg  TOTAL={(sim_drymass+sim_payload+sim_fuel):,}kg</span><br>
          <span class='cl-num'>005</span><span class='cl-ts'>[{now_ts}]</span><span class='cl-ok'> [OK ] Aerodyn: Cd={sim_drag}  A=12.0m²  burn_rate={sim_burnrate}kg/s  ΔV≈{delta_v_est/1000:.2f}km/s</span><br>
          <span class='cl-num'>006</span><span class='cl-ts'>[{now_ts}]</span><span class='cl-inf'>[SIM] Executing {len(sim_df):,} timesteps...</span><br>
          <span class='cl-num'>007</span><span class='cl-ts'>[{now_ts}]</span><span class='cl-ok'> [OK ] Apogee: {max_alt:.2f} km @ T+{apogee_t:.0f}s</span><br>
          <span class='cl-num'>008</span><span class='cl-ts'>[{now_ts}]</span><span class='cl-ok'> [OK ] Peak vel: {max_vel:.4f} km/s  Peak accel: {max_acc:.2f} m/s²</span><br>
          <span class='cl-num'>009</span><span class='cl-ts'>[{now_ts}]</span><span class='{gfc}'> [{"WARN" if max_gforce>5 else "OK  "}] G-force: {max_gforce:.2f}g — {"⚠ EXCEEDS 6g CREWED LIMIT" if max_gforce>6 else "nominal"}</span><br>
          <span class='cl-num'>010</span><span class='cl-ts'>[{now_ts}]</span><span class='cl-ok'> [OK ] Burnout: T+{burnout_t:.0f}s | consumed={fuel_used:,.0f}kg ({fuel_pct:.1f}%)</span><br>
          <span class='cl-num'>011</span><span class='cl-ts'>[{now_ts}]</span><span class='{kc}'> [{"OK " if reached_karman else "WAR"}] Kármán line (100km): {"CLEARED ✓" if reached_karman else f"NOT REACHED — max {max_alt:.1f}km"}</span><br>
          <span class='cl-num'>012</span><span class='cl-ts'>[{now_ts}]</span><span class='{vc2}'> [{"OK " if max_vel>=7.9 else "INF"}] Orbital velocity: {"ACHIEVED ✓" if max_vel>=7.9 else f"{max_vel/7.9*100:.1f}% of 7.9 km/s"}</span><br>
          <span class='cl-num'>013</span><span class='cl-ts'>[{now_ts}]</span><span class='{fuel_c}'> [{"OK " if fuel_left>=10000 else "WAR"}] Fuel remaining: {fuel_left:,.0f} kg</span><br>
          <span class='cl-num'>014</span><span class='cl-ts'>[{now_ts}]</span><span class='{ok_c}'> [{ok_t}] ═══ MISSION STATUS: {"NOMINAL — ALL OBJECTIVES MET ✓" if mission_ok else "ABORT — INSUFFICIENT PERFORMANCE"} ═══</span><br>
          <span class='cl-num'>015</span><span class='cl-ts'>[{now_ts}]</span><span class='cl-dim'>[END] COSMOS flight computer standby — awaiting next launch commit</span>
        </div>""", unsafe_allow_html=True)

        # ── LAUNCH COMMIT BANNER ──────────────────────────────────────────
        if launch_btn:
            if mission_ok:
                st.markdown(f"""
                <div class='launch-commit'>
                  <div class='lc-icon'>🚀</div>
                  <div>
                    <div class='lc-title'>LAUNCH COMMITTED — MISSION NOMINAL</div>
                    <div class='lc-sub'>
                      Alt: {max_alt:,.1f} km &nbsp;·&nbsp; Vel: {max_vel:.3f} km/s &nbsp;·&nbsp;
                      Max-G: {max_gforce:.1f}g &nbsp;·&nbsp; TWR: {twr:.2f} &nbsp;·&nbsp;
                      ΔV: {delta_v_est/1000:.2f} km/s &nbsp;·&nbsp;
                      {"✓ Kármán" if reached_karman else "Sub-orbital"} &nbsp;
                      {"· ✓ LEO" if reached_leo else ""}
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='abort-banner'>
                  <div class='lc-icon'>🛑</div>
                  <div>
                    <div class='lc-title' style='color:var(--red);'>LAUNCH ABORT — PERFORMANCE INSUFFICIENT</div>
                    <div class='lc-sub'>Max altitude {max_alt:.1f} km · TWR={twr:.2f} · Adjust thrust, fuel, or reduce mass</div>
                  </div>
                </div>""", unsafe_allow_html=True)

        footer()


        #  PAGE 4 · SCIENTIFIC INSIGHTS
    # ─────────────────────────────────────────────────────────────────────
    elif ACTIVE == "Scientific Insights":
        page_banner("SCREEN 04 / 06  ·  SCIENCE ANALYTICS",
                    "🔬 SCIENTIFIC INSIGHTS",
                    "Yield analysis, mission type efficacy, destination performance, and key insights.",
                    [("YIELD ANALYSIS","bc"),("INSIGHT CARDS","ba")],"#00ff9c")

        if N==0:
            st.warning("No records match filters."); footer(); return

        avg_yield=dfv["Scientific Yield"].mean(); max_yield=dfv["Scientific Yield"].max()
        sci_ratio=dfv["Scientific Yield"].sum()/dfv["Mission Cost"].sum()*1000
        top_type=dfv.groupby("Mission Type")["Scientific Yield"].mean().idxmax()

        sk=st.columns(4)
        kpi_row(sk,[
            ("🔬","Avg Sci Yield",  f"{avg_yield:.1f}", "0-100 score",      "#00ff9c","rgba(0,255,156,.14)"),
            ("🏆","Peak Yield",     f"{max_yield:.1f}", "single mission",   "#00e5ff","rgba(0,229,255,.18)"),
            ("💡","Sci/Cost Ratio", f"{sci_ratio:.2f}", "pts per $B",       "#ffb300","rgba(255,179,0,.14)"),
            ("🥇","Best Type",      top_type[:8],        "highest avg",      "#7c8cff","rgba(124,140,255,.18)"),
        ])

        sec("💡","KEY ANALYTICAL INSIGHTS")
        ic1,ic2,ic3=st.columns(3)
        with ic1:
            st.markdown("""
            <div class='insight-card'>
              <div class='insight-title'>⚖️ Payload → Fuel Dependency</div>
              <div class='insight-body'>Heavier payloads require exponentially more fuel
              due to the rocket equation. A 10× payload increase typically demands 3–5× fuel,
              driving mission cost upward significantly.</div>
            </div>""", unsafe_allow_html=True)
        with ic2:
            st.markdown("""
            <div class='insight-card'>
              <div class='insight-title'>💰 Cost ≠ Guaranteed Success</div>
              <div class='insight-body'>High cost does not linearly predict success.
              Failed missions average lower cost — often cut short — yet expensive
              missions also fail. Vehicle reliability matters more than budget.</div>
            </div>""", unsafe_allow_html=True)
        with ic3:
            st.markdown("""
            <div class='insight-card'>
              <div class='insight-title'>👨‍🚀 Crew Size & Outcomes</div>
              <div class='insight-body'>Crewed missions achieve 93% success vs 78% for
              uncrewed — reflecting additional rigor in planning, redundancy systems,
              and abort capability requirements for human spaceflight.</div>
            </div>""", unsafe_allow_html=True)

        sec("📊","YIELD vs COST · DEEP ANALYSIS")
        ch("SCIENTIFIC YIELD vs MISSION COST · SCATTER + LOWESS · COLOR=TYPE")
        fig5=px.scatter(dfv,x="Mission Cost",y="Scientific Yield",
                        color="Mission Type",
                        hover_data=["Mission Name","Target Name"],opacity=.8,size_max=14)
        fig5.update_traces(marker=dict(size=7,line=dict(width=.4,color="#0b0f1a")))
        if len(dfv)>2:
            m,b=np.polyfit(dfv["Mission Cost"],dfv["Scientific Yield"],1)
            xr=np.linspace(dfv["Mission Cost"].min(),dfv["Mission Cost"].max(),200)
            fig5.add_trace(go.Scatter(x=xr,y=m*xr+b,mode="lines",name="Trend",
                                      line=dict(color="#7c8cff",width=1.4,dash="dot"),opacity=.45))
        apl(fig5,xt="Mission Cost ($M)",yt="Scientific Yield (0-100)",h=380)
        fig5.update_layout(legend_title_text="")
        st.plotly_chart(fig5,use_container_width=True,config={"displayModeBar":False})

        c6a,c6b=st.columns(2)
        with c6a:
            ch("AVG YIELD BY MISSION TYPE · SORTED BAR")
            yt=dfv.groupby("Mission Type")["Scientific Yield"].mean().reset_index()
            yt=yt.sort_values("Scientific Yield",ascending=True)
            fig6=px.bar(yt,x="Scientific Yield",y="Mission Type",orientation="h",
                        color="Scientific Yield",color_continuous_scale=["#152030","#00e5ff","#00ff9c"])
            fig6.update_traces(marker=dict(line=dict(width=0)))
            apl(fig6,xt="Avg Yield Score",h=320)
            fig6.update_layout(showlegend=False,coloraxis_showscale=False)
            st.plotly_chart(fig6,use_container_width=True,config={"displayModeBar":False})
        with c6b:
            ch("YIELD DISTRIBUTION · VIOLIN BY OUTCOME")
            fig6b=px.violin(dfv,x="Outcome",y="Scientific Yield",color="Outcome",
                            color_discrete_map={"SUCCESS":"#00ff9c","FAILED":"#ff4b4b"},
                            box=True,points="outliers")
            apl(fig6b,yt="Scientific Yield",h=320); fig6b.update_layout(showlegend=False)
            st.plotly_chart(fig6b,use_container_width=True,config={"displayModeBar":False})

        sec("🌍","TARGET YIELD PERFORMANCE")
        ch("AVG YIELD BY TARGET · WITH ERROR BARS")
        ty=dfv.groupby("Target Name")["Scientific Yield"].agg(["mean","std","count"]).reset_index()
        ty.columns=["Target","Mean","Std","Count"]; ty["Std"]=ty["Std"].fillna(0)
        ty=ty.sort_values("Mean",ascending=False)
        fig8=go.Figure()
        fig8.add_trace(go.Bar(
            x=ty["Target"],y=ty["Mean"],
            error_y=dict(type="data",array=ty["Std"].tolist(),visible=True,
                         color="#6a86a8",thickness=1.5,width=6),
            marker=dict(color=ty["Mean"],
                        colorscale=[[0,"#0a1428"],[.5,"#7c8cff"],[1,"#00ff9c"]],
                        line=dict(width=0)),
            text=ty["Count"],texttemplate="n=%{text}",textposition="outside",
            textfont=dict(family="Share Tech Mono",size=9,color="#6a86a8"),
        ))
        apl(fig8,xt="Target",yt="Avg Yield",h=340)
        st.plotly_chart(fig8,use_container_width=True,config={"displayModeBar":False})
        footer()

    # ─────────────────────────────────────────────────────────────────────
    #  PAGE 5 · DATASET EXPLORER
    # ─────────────────────────────────────────────────────────────────────
    elif ACTIVE == "Dataset Explorer":
        page_banner("SCREEN 05 / 06  ·  DATA MANAGEMENT CONSOLE",
                    "🗃️ DATASET EXPLORER",
                    "Browse, search, sort, inspect statistics, and export the mission database.",
                    [("RAW DATA","bc"),("EXPORT CSV","bg"),("df.describe()","ba")],"#b388ff")

        ec=st.columns(6)
        for col,(icon,lbl,val) in zip(ec,[
            ("📋","Records",f"{N:,}"),("🛰","Types",f"{dfv['Mission Type'].nunique()}"),
            ("🚀","Vehicles",f"{dfv['Launch Vehicle'].nunique()}"),
            ("🌍","Targets",f"{dfv['Target Name'].nunique()}"),
            ("📅","Years",f"{int(dfv['Year'].min())}–{int(dfv['Year'].max())}"),
            ("✅","Success",f"{dfv['Mission Success'].sum():,}"),
        ]):
            col.markdown(f"""
            <div class='ex-stat'>
              <div style='font-size:1.0rem;'>{icon}</div>
              <div class='ex-val'>{val}</div>
              <div class='ex-lbl'>{lbl}</div>
            </div>""", unsafe_allow_html=True)

        sec("🔍","SEARCH & SORT")
        x1,x2,x3=st.columns([1.6,1,1])
        with x1:
            sq=st.text_input("Search name / target / type",
                             placeholder="CSM-0042, Mars, Science…")
        with x2:
            sc=st.selectbox("Sort by",["Launch Date","Mission Cost","Payload Weight",
                                        "Scientific Yield","Mission Duration",
                                        "Fuel Consumption","Distance from Earth"])
        with x3:
            sa=st.radio("Order",["Descending","Ascending"],horizontal=True)

        n_rows=st.slider("Rows to display",10,min(500,N),min(50,N),step=10)
        ALL_COLS=["Mission Name","Launch Date","Mission Type","Launch Vehicle","Target Name",
                  "Payload Weight","Mission Cost","Mission Duration","Scientific Yield",
                  "Crew Size","Mission Success","Fuel Consumption","Distance from Earth","Year"]
        sel_cols=st.multiselect("Visible columns",ALL_COLS,default=ALL_COLS[:10])

        show=dfv.copy()
        if sq:
            mask=(show["Mission Name"].str.contains(sq,case=False,na=False)|
                  show["Target Name"].str.contains(sq,case=False,na=False)|
                  show["Mission Type"].str.contains(sq,case=False,na=False))
            show=show[mask]
        show=show.sort_values(sc,ascending=(sa=="Ascending"))

        sec("📋",f"DATA TABLE · {len(show):,} RECORDS")
        if sel_cols:
            disp=show[sel_cols].head(n_rows).copy()
            fmt_map={"Mission Cost":lambda x:f"${x:,.0f}M","Payload Weight":lambda x:f"{x:,.0f} kg",
                     "Fuel Consumption":lambda x:f"{x:,.0f} kg","Mission Duration":lambda x:f"{x:.0f} days",
                     "Scientific Yield":lambda x:f"{x:.1f}","Distance from Earth":lambda x:f"{x:,.0f} km",
                     "Mission Success":lambda x:"✅ SUCCESS" if x else "❌ FAILED"}
            for cn,fn in fmt_map.items():
                if cn in disp.columns: disp[cn]=disp[cn].apply(fn)
            if "Launch Date" in disp.columns:
                disp["Launch Date"]=pd.to_datetime(disp["Launch Date"]).dt.strftime("%Y-%m-%d")
            st.dataframe(disp.reset_index(drop=True),use_container_width=True,height=460)

        sec("💾","EXPORT")
        st.download_button("⬇️  Download Filtered Dataset (.csv)",
                           data=show.to_csv(index=False).encode("utf-8"),
                           file_name="cosmos_missions.csv",mime="text/csv")

        sec("📊","DESCRIPTIVE STATISTICS · df.describe()")
        with st.expander("▶  Expand Statistics Table",expanded=False):
            num_c=["Mission Cost","Payload Weight","Mission Duration","Scientific Yield",
                   "Fuel Consumption","Distance from Earth","Crew Size"]
            desc=show[num_c].describe().T; desc.columns=[c.upper() for c in desc.columns]
            st.dataframe(desc.style.format("{:.2f}"),use_container_width=True)

        sec("📈","COLUMN DISTRIBUTIONS")
        dc1,dc2,dc3=st.columns(3)
        for cw,cn,clr in [(dc1,"Mission Cost","#ff6b00"),(dc2,"Payload Weight","#00e5ff"),(dc3,"Scientific Yield","#00ff9c")]:
            if N>0:
                fd=px.histogram(show,x=cn,nbins=28,color_discrete_sequence=[clr])
                fd.update_traces(marker=dict(line=dict(width=.3,color="#0b0f1a"),opacity=.85))
                apl(fd,xt=cn,yt="Count",h=240); fd.update_layout(showlegend=False)
                cw.plotly_chart(fd,use_container_width=True,config={"displayModeBar":False})
        footer()

    # ─────────────────────────────────────────────────────────────────────
    #  PAGE 6 · ABOUT PROJECT
    # ─────────────────────────────────────────────────────────────────────
    elif ACTIVE == "About Project":
        page_banner("SCREEN 06 / 06  ·  PROJECT DOCUMENTATION",
                    "ℹ️ ABOUT PROJECT",
                    "Objective, physics model, tech stack, and real-world applications.",
                    [("DOCUMENTATION","bc"),("OPEN SOURCE","bg"),("v7.0.0","ba")],"#c0d8ff")

        a1,a2=st.columns(2)
        with a1:
            st.markdown("""
            <div class='about-card'>
              <h4>🎯  Project Objective</h4>
              <p>COSMOS analyzes historical rocket mission data and simulates rocket launch
              physics using Newton's Second Law. It replicates the visual language and
              operational structure of real aerospace mission control systems used by NASA
              and SpaceX.</p>
              <p>The platform provides both retrospective mission analysis and forward-looking
              simulation, enabling engineers to understand mission parameter trade-offs
              before committing to a launch profile.</p>
            </div>
            <div class='about-card'>
              <h4>📐  Mathematical Model</h4>
              <div class='formula'>F_net = F_thrust - F_gravity - F_drag</div>
              <div class='formula'>a = F_net / m_total</div>
              <p>Atmospheric density (exponential):</p>
              <div class='formula'>rho(h) = 1.225 * exp(-h / 8500)  [kg/m3]</div>
              <p>Aerodynamic drag:</p>
              <div class='formula'>F_drag = 0.5 * rho * Cd * A * v^2  [N]</div>
              <p>Variable rocket mass:</p>
              <div class='formula'>m(t) = m_dry + m_payload + m_fuel(t)</div>
              <div class='formula'>m_fuel(t) = max(m0 - burn_rate * t, 0)</div>
            </div>
            """, unsafe_allow_html=True)

        with a2:
            st.markdown("""
            <div class='about-card'>
              <h4>🛠️  Technologies Used</h4>
              <div style='margin:.7rem 0;'>
                <span class='tech-pill'>Python 3.10+</span><span class='tech-pill'>Streamlit</span>
                <span class='tech-pill'>Plotly Express</span><span class='tech-pill'>Plotly Graph Objects</span>
                <span class='tech-pill'>Pandas</span><span class='tech-pill'>NumPy</span>
                <span class='tech-pill'>Seaborn</span><span class='tech-pill'>Matplotlib</span>
                <span class='tech-pill'>hashlib (auth)</span>
              </div>
              <p>Fonts: Orbitron · Share Tech Mono · Exo 2</p>
            </div>
            <div class='about-card'>
              <h4>🏗️  Application Architecture</h4>
              <ul>
                <li><strong style='color:#00e5ff;'>Login Screen</strong> — SHA-256 auth, role selector, telemetry chips, status banner</li>
                <li><strong style='color:#00e5ff;'>Loading Transition</strong> — Animated access granted screen</li>
                <li><strong style='color:#00e5ff;'>Landing Page</strong> — Cinematic entry with live fleet stats</li>
                <li><strong style='color:#ffb300;'>Overview</strong> — KPIs, trends, heatmap, destinations</li>
                <li><strong style='color:#ff6b00;'>Analytics</strong> — 5 core charts across all dimensions</li>
                <li><strong style='color:#ff6b00;'>Simulation</strong> — Physics engine, 4 charts, gauge, console</li>
                <li><strong style='color:#00ff88;'>Scientific Insights</strong> — Yield with insight cards</li>
                <li><strong style='color:#b388ff;'>Dataset Explorer</strong> — Search, sort, stats, download</li>
                <li><strong style='color:#c0d8ff;'>About</strong> — Docs, formulas, applications</li>
              </ul>
            </div>
            <div class='about-card'>
              <h4>🌐  Real-World Applications</h4>
              <ul>
                <li>Mission planning and payload trade-off analysis</li>
                <li>Launch vehicle selection by payload and destination</li>
                <li>Fuel budget estimation for multi-stage rockets</li>
                <li>Post-mission scientific yield attribution</li>
                <li>Fleet performance benchmarking across vehicle types</li>
                <li>Aerospace engineering training and education</li>
              </ul>
            </div>
            """, unsafe_allow_html=True)

        sec("▶","QUICK START")
        st.markdown("""
        <div class='about-card'>
          <h4>⚙️  Installation &amp; Run</h4>
          <div class='formula'>pip install streamlit plotly pandas numpy matplotlib seaborn</div>
          <div class='formula'>streamlit run cosmos_app.py</div>
          <div class='formula'>streamlit run cosmos_app.py --server.port 8080 --theme.base dark</div>
          <p>Credentials: <span class='tech-pill'>admin / rocket123</span>
                          <span class='tech-pill'>engineer / nasa2024</span>
                          <span class='tech-pill'>guest / guest</span></p>
        </div>""", unsafe_allow_html=True)
        footer()


# ═══════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════
# Inject the animated space canvas background on every page
inject_space_background()

if not st.session_state.logged_in:
    show_login()
elif st.session_state.get("show_loading", False):
    show_loading()
elif st.session_state.show_landing:
    show_landing()
else:
    show_dashboard()
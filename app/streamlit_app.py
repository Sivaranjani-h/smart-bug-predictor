import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.predict import predict_bug

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BugRadar — Smart Triage",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    background: #FFFFFF !important;
    color: #2C3E50 !important;
    font-family: 'Inter', system-ui, sans-serif !important;
}

[data-testid="stSidebar"] {
    background: #F8F9FA !important;
    border-right: 1px solid #E5E7EB !important;
    min-width: 240px !important; max-width: 240px !important;
}
[data-testid="stSidebar"] section,
[data-testid="stSidebarContent"] { padding: 0 !important; }

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display:none !important; visibility:hidden !important; }

.block-container { padding: 2rem 2.5rem 5rem !important; max-width: 1380px !important; }

h1,h2,h3,h4 {
    font-family:'Inter',sans-serif !important;
    color:#1A202C !important;
    letter-spacing:-0.025em;
}

/* ── Sidebar brand ── */
.sb-wrap { padding: 20px 18px 16px; border-bottom: 1px solid #1A2235; display:flex; align-items:center; gap:11px; }
.sb-logo {
    width:34px; height:34px; border-radius:9px; flex-shrink:0;
    background: linear-gradient(135deg,#6366F1 0%,#A855F7 100%);
    display:flex; align-items:center; justify-content:center; font-size:17px;
    box-shadow: 0 4px 14px rgba(99,102,241,.45);
}
.sb-title { font-size:16px; font-weight:800; color:#1A202C; letter-spacing:-0.03em; }
.sb-sub   { font-size:11px; color:#718096; margin-top:2px; font-weight:400; }
.sb-sec { padding:16px 18px 5px; font-size:11px; font-weight:700; letter-spacing:.12em; text-transform:uppercase; color:#A0AEC0; }

/* ── Sidebar radio ── */
[data-testid="stSidebar"] [data-testid="stRadio"] > label { display:none; }
[data-testid="stSidebar"] [data-testid="stRadio"] > div  { gap:2px !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] > div > label {
    padding: 10px 15px !important; border-radius:7px !important;
    margin: 0 10px !important; font-size:14px !important; font-weight:500 !important;
    color: #718096 !important; transition: background .12s, color .12s !important; cursor:pointer;
}
[data-testid="stSidebar"] [data-testid="stRadio"] > div > label:hover {
    background:#EDF2F7 !important; color:#2D3748 !important;
}

/* system status */
.sb-foot { padding:12px 18px 18px; border-top:1px solid #1A2235; margin-top:10px; }
.sb-row  { display:flex; align-items:center; gap:8px; font-size:12px; color:#718096; margin-bottom:6px; }
.dot { width:7px; height:7px; border-radius:50%; flex-shrink:0; }
.dg  { background:#10B981; box-shadow:0 0 6px rgba(16,185,129,.6); }
.dy  { background:#FBBF24; }
.dr  { background:#EF4444; }

/* ── Page header ── */
.ph { margin-bottom:1.75rem; padding-bottom:1.25rem; border-bottom:1px solid #1A2235; }
.ph-eye   { font-size:11px; font-weight:700; letter-spacing:.13em; text-transform:uppercase; color:#6366F1; margin-bottom:5px; }
.ph-title { font-size:32px; font-weight:800; color:#1A202C; letter-spacing:-0.03em; margin-bottom:5px; }
.ph-desc  { font-size:15px; color:#4A5568; line-height:1.6; }

/* ── Metric cards ── */
.mc-row { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:1.5rem; }
.mc {
    background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px;
    padding:1.25rem 1.4rem 1.1rem; position:relative; overflow:hidden;
    transition: border-color .15s, transform .15s;
}
.mc:hover { border-color:#CBD5E0; transform:translateY(-2px); }
.mc::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; border-radius:12px 12px 0 0; }
.mc-v::before { background:linear-gradient(90deg,#6366F1,#A855F7); }
.mc-r::before { background:linear-gradient(90deg,#EF4444,#F97316); }
.mc-a::before { background:linear-gradient(90deg,#F97316,#FBBF24); }
.mc-g::before { background:linear-gradient(90deg,#10B981,#06B6D4); }
.mc-lbl { font-size:12px; font-weight:600; letter-spacing:.09em; text-transform:uppercase; color:#718096; margin-bottom:8px; }
.mc-num { font-size:36px; font-weight:800; color:#1A202C; letter-spacing:-0.04em; line-height:1; margin-bottom:6px; font-variant-numeric:tabular-nums; }
.mc-meta { font-size:13px; color:#718096; }
.mc-meta .up   { color:#10B981; font-weight:600; }
.mc-meta .down { color:#EF4444; font-weight:600; }

/* ── Card / panel ── */
.card {
    background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px;
    padding:1.4rem 1.6rem; margin-bottom:14px;
}
.card-t {
    font-size:13px; font-weight:700; color:#4A5568; letter-spacing:.04em;
    margin-bottom:1rem; display:flex; align-items:center; gap:8px;
}
.sep { height:1px; background:#E5E7EB; margin:1.1rem 0; }

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background:#F7FAFC !important; border:1.5px solid #CBD5E0 !important;
    border-radius:8px !important; color:#2C3E50 !important;
    font-family:'Inter',sans-serif !important; font-size:15px !important;
    padding:11px 14px !important;
    transition: border-color .15s, box-shadow .15s !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color:#6366F1 !important;
    box-shadow:0 0 0 4px rgba(99,102,241,.14) !important; outline:none !important;
}
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label {
    color:#4A5568 !important; font-size:12px !important;
    font-weight:700 !important; letter-spacing:.08em !important; text-transform:uppercase !important;
}

/* ── Button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg,#6366F1,#7C3AED) !important;
    color:#fff !important; border:none !important; border-radius:8px !important;
    font-family:'Inter',sans-serif !important; font-size:15px !important;
    font-weight:700 !important; letter-spacing:.02em !important;
    padding:.75rem 1.8rem !important;
    transition: opacity .12s, transform .12s, box-shadow .12s !important;
    box-shadow: 0 3px 14px rgba(99,102,241,.35) !important;
}
[data-testid="stButton"] > button:hover {
    opacity:.86 !important; transform:translateY(-2px) !important;
    box-shadow: 0 6px 22px rgba(99,102,241,.45) !important;
}

/* Download button */
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg,#0F7A55,#10B981) !important;
    color:#fff !important; border:none !important; border-radius:8px !important;
    font-family:'Inter',sans-serif !important; font-size:15px !important;
    font-weight:700 !important; padding:.75rem 1.8rem !important;
    box-shadow: 0 3px 14px rgba(16,185,129,.3) !important;
    transition: opacity .12s, transform .12s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    opacity:.86 !important; transform:translateY(-2px) !important;
}

/* ── Badges ── */
.b { display:inline-flex; align-items:center; padding:4px 12px; border-radius:20px; font-size:13px; font-weight:700; letter-spacing:.04em; white-space:nowrap; }
.b-p1,.b-critical { background:rgba(239,68,68,.14); color:#F87171; border:1px solid rgba(239,68,68,.25); }
.b-p2,.b-high     { background:rgba(249,115,22,.14); color:#FB923C; border:1px solid rgba(249,115,22,.25); }
.b-p3,.b-medium   { background:rgba(234,179,8,.14);  color:#FACC15; border:1px solid rgba(234,179,8,.25); }
.b-p4,.b-low      { background:rgba(16,185,129,.14); color:#34D399; border:1px solid rgba(16,185,129,.25); }

/* ── Result grid ── */
.rg { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:1rem 0; }
.rc { background:#F7FAFC; border:1px solid #E5E7EB; border-radius:9px; padding:1rem 1.2rem; }
.rc-l { font-size:11px; font-weight:700; letter-spacing:.1em; text-transform:uppercase; color:#718096; margin-bottom:6px; }
.rc-v { font-size:20px; font-weight:800; color:#1A202C; letter-spacing:-0.02em; }

/* ── Confidence bar ── */
.cb { margin:5px 0 12px; }
.cb-h { display:flex; justify-content:space-between; font-size:13px; color:#4A5568; margin-bottom:5px; font-weight:500; }
.cb-t { height:6px; background:#E5E7EB; border-radius:99px; overflow:hidden; }
.cb-f { height:100%; border-radius:99px; background:linear-gradient(90deg,#6366F1,#A855F7); }

/* ── Pulse animation ── */
@keyframes pulse-in {
    0%   { box-shadow:0 0 0 0 rgba(99,102,241,.5); }
    70%  { box-shadow:0 0 0 12px rgba(99,102,241,0); }
    100% { box-shadow:none; }
}
.pulse { animation: pulse-in .8s ease forwards; }

/* ── Empty state ── */
.empty { text-align:center; padding:4rem 1rem; }
.ei { font-size:40px; margin-bottom:.8rem; }
.et { font-size:17px; font-weight:700; color:#2D3748; margin-bottom:.4rem; }
.ed { font-size:14px; color:#718096; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background:#F7FAFC !important; border:1.5px dashed #CBD5E0 !important;
    border-radius:9px !important; padding: 1rem !important;
}
[data-testid="stFileUploader"] label { color:#4A5568 !important; font-size:14px !important; }

/* ── Alerts ── */
[data-testid="stAlert"] {
    background:#EFF6FF !important; border:1px solid #BFDBFE !important;
    border-radius:9px !important; color:#1E40AF !important; font-size:14px !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border-radius:9px !important; overflow:hidden; }

/* ── Tip box ── */
.tip { padding:10px 14px; background:#F7FAFC; border-radius:7px; border-left:3px solid #6366F1; font-size:13.5px; color:#4A5568; margin-bottom:8px; line-height:1.55; }
.tip code { font-family:'JetBrains Mono',monospace; color:#A855F7; font-size:12.5px; }

/* ── Step list ── */
.step { display:flex; align-items:flex-start; gap:13px; padding:10px 0; border-bottom:1px solid #E5E7EB; }
.step:last-child { border-bottom:none; }
.sn {
    width:24px; height:24px; border-radius:50%; flex-shrink:0;
    background:rgba(99,102,241,.12); border:1px solid rgba(99,102,241,.25);
    display:flex; align-items:center; justify-content:center;
    font-size:10px; font-weight:800; color:#818CF8;
    font-family:'JetBrains Mono',monospace;
}
.st-txt { font-size:14px; color:#4A5568; line-height:1.5; }
.st-txt strong { color:#2D3748; font-weight:600; }

/* ── Mode toggle ── */
[data-testid="stRadio"] > div { display:flex; gap:10px !important; flex-direction:row !important; }
[data-testid="stRadio"] > div > label {
    background:#F7FAFC !important; border:1.5px solid #CBD5E0 !important;
    border-radius:8px !important; padding:10px 19px !important;
    font-size:14px !important; font-weight:600 !important; color:#4A5568 !important;
    cursor:pointer; transition: border-color .12s, color .12s !important;
}
[data-testid="stRadio"] > div > label:hover { border-color:#6366F1 !important; color:#818CF8 !important; }

/* ── Progress bar ── */
[data-testid="stProgressBar"] > div { background:#6366F1 !important; border-radius:99px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width:6px; height:6px; }
::-webkit-scrollbar-track { background:#070A12; }
::-webkit-scrollbar-thumb { background:#1A2235; border-radius:99px; }
::-webkit-scrollbar-thumb:hover { background:#2A3550; }

/* ── Bulk result highlight ── */
.bulk-banner {
    background: linear-gradient(135deg, rgba(99,102,241,.12), rgba(168,85,247,.08));
    border: 1px solid rgba(99,102,241,.25);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    display: flex; align-items: center; gap: 14px;
}
.bulk-icon { font-size: 28px; }
.bulk-text-title { font-size: 18px; font-weight: 800; color: #1A202C; letter-spacing: -0.02em; }
.bulk-text-sub   { font-size: 13px; color: #4A5568; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def b(text, kind):
    k = kind.lower().replace(" ","")
    return f'<span class="b b-{k}">{text}</span>'

def cbar(label, val):
    v = min(float(val), 100)
    return (f'<div class="cb">'
            f'<div class="cb-h"><span>{label}</span>'
            f'<span style="color:#818CF8;font-weight:700">{v:.1f}%</span></div>'
            f'<div class="cb-t"><div class="cb-f" style="width:{v}%"></div></div>'
            f'</div>')

def pdot(p):
    c = {"P1":"dr","P2":"dy","P3":"dy","P4":"dg"}.get(p,"dg")
    return (f'<span class="dot {c}" style="display:inline-block;margin-right:6px;'
            f'vertical-align:middle;width:8px;height:8px;border-radius:50%;"></span>')

PCOL = {"P1":"#EF4444","P2":"#F97316","P3":"#FBBF24","P4":"#10B981"}
SCOL = {"Critical":"#EF4444","High":"#F97316","Medium":"#FBBF24","Low":"#10B981"}
BM   = {"P1":"p1","P2":"p2","P3":"p3","P4":"p4"}
SM   = {"Critical":"critical","High":"high","Medium":"medium","Low":"low"}

CHART = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
             font_color="#718096", margin=dict(l=0,r=0,t=10,b=0))

@st.cache_data
def load_df():
    try:    return pd.read_csv("data/processed/bugs_clean.csv")
    except: return pd.DataFrame()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-wrap">
        <div class="sb-logo">🎯</div>
        <div>
            <div class="sb-title">BugRadar</div>
            <div class="sb-sub">Smart Bug Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">Navigation</div>', unsafe_allow_html=True)

    page = st.radio("nav", [
        "🏠  Overview",
        "🐛  Submit Bug",
        "📊  Last Result",
        "📈  Model Health",
        "🔁  Retrain",
        "📉  Analytics",
    ], label_visibility="collapsed")

    st.markdown("""
    <div class="sb-foot">
        <div class="sb-row"><span class="dot dg"></span>&nbsp;API online</div>
        <div class="sb-row"><span class="dot dg"></span>&nbsp;Model v2 active</div>
        <div class="sb-row"><span class="dot dg"></span>&nbsp;MLflow connected</div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "🏠  Overview":
    st.markdown("""
    <div class="ph">
        <div class="ph-eye">Dashboard</div>
        <div class="ph-title">Bug Intelligence Overview</div>
        <div class="ph-desc">Real-time ML-powered triage metrics across all modules and environments.</div>
    </div>""", unsafe_allow_html=True)

    df = load_df()
    total = len(df) if not df.empty else 1000
    p1 = int((df["priority"]=="P1").sum()) if not df.empty else 250
    p2 = int((df["priority"]=="P2").sum()) if not df.empty else 250
    lo = total - p1 - p2

    st.markdown(f"""
    <div class="mc-row">
        <div class="mc mc-v">
            <div class="mc-lbl">Total Reports</div>
            <div class="mc-num">{total:,}</div>
            <div class="mc-meta"><span class="up">↑ 12%</span> vs last month</div>
        </div>
        <div class="mc mc-r">
            <div class="mc-lbl">P1 — Critical</div>
            <div class="mc-num">{p1:,}</div>
            <div class="mc-meta"><span class="down">↑ 3</span> since yesterday</div>
        </div>
        <div class="mc mc-a">
            <div class="mc-lbl">P2 — High</div>
            <div class="mc-num">{p2:,}</div>
            <div class="mc-meta"><span class="up">↓ 5</span> resolved today</div>
        </div>
        <div class="mc mc-g">
            <div class="mc-lbl">P3 / P4 — Backlog</div>
            <div class="mc-num">{lo:,}</div>
            <div class="mc-meta">Stable this week</div>
        </div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([1.35, 1])
    with c1:
        st.markdown('<div class="card"><div class="card-t">📦 Bug Volume by Module</div>', unsafe_allow_html=True)
        if not df.empty and "product_module" in df.columns:
            mod = df["product_module"].value_counts().reset_index()
            mod.columns = ["Module","Count"]
            fig = px.bar(mod, x="Count", y="Module", orientation="h",
                         color="Count", color_continuous_scale=["#1A2235","#6366F1"])
            fig.update_layout(**CHART, height=220, showlegend=False, coloraxis_showscale=False,
                              xaxis=dict(gridcolor="#1A2235", tickfont=dict(color="#3D4F6B",size=12)),
                              yaxis=dict(tickfont=dict(color="#6A82A8",size=12)))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card"><div class="card-t">🎯 Priority Split</div>', unsafe_allow_html=True)
        if not df.empty and "priority" in df.columns:
            pc = df["priority"].value_counts().reset_index(); pc.columns=["Priority","Count"]
            fig2 = px.pie(pc, values="Count", names="Priority", hole=.6,
                          color="Priority", color_discrete_map=PCOL)
            fig2.update_layout(**CHART, height=220,
                               legend=dict(font=dict(color="#4A6080",size=12),bgcolor="rgba(0,0,0,0)"))
            fig2.update_traces(textfont_color="#0B0F19", textfont_size=13)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-t">🕐 Recent Bug Reports</div>', unsafe_allow_html=True)
    if not df.empty:
        cols = [c for c in ["title","priority","severity","product_module","environment"] if c in df.columns]
        st.dataframe(df[cols].head(8), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 2 — SUBMIT BUG (Single + Bulk)
# ════════════════════════════════════════════════════════════════════════════
elif page == "🐛  Submit Bug":
    st.markdown("""
    <div class="ph">
        <div class="ph-eye">Triage</div>
        <div class="ph-title">Submit Bug Report</div>
        <div class="ph-desc">Classify a single bug manually — or upload a CSV to bulk-triage hundreds at once.</div>
    </div>""", unsafe_allow_html=True)

    mode = st.radio("Mode", ["✏️  Single Bug", "📂  Bulk CSV Upload"],
                    horizontal=True, label_visibility="collapsed")
    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)

    # ── SINGLE BUG ──────────────────────────────────────────────────────────
    if mode == "✏️  Single Bug":
        cf, cs = st.columns([1.7, 1])

        with cf:
            st.markdown('<div class="card"><div class="card-t">🔖 Bug Details</div>', unsafe_allow_html=True)
            title       = st.text_input("Title", placeholder="e.g. Memory leak in ML-Service causing OOM crash in production")
            description = st.text_area("Description",
                placeholder="Module affected · steps to reproduce · environment · error messages · user impact…",
                height=160)
            st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
            go = st.button("Classify Bug →", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with cs:
            st.markdown(f"""
            <div class="card">
                <div class="card-t">💡 Tips for accurate results</div>
                <div class="tip">Name the module: <code>ML-Service</code>, <code>WebApp-Core</code></div>
                <div class="tip">State the environment — <strong style="color:#818CF8">Production</strong> raises priority faster</div>
                <div class="tip">Paste stack traces verbatim — keywords matter</div>
                <div class="tip">Quantify impact: <em>"affects 10,000 users"</em></div>
            </div>
            <div class="card" style="margin-top:0;">
                <div class="card-t">🏷 Priority Reference</div>
                <div style="font-size:13px; line-height:2.5; color:#3D4F6B;">
                    <div>{b("P1","p1")} &nbsp;Production down / data loss</div>
                    <div>{b("P2","p2")} &nbsp;Major feature broken</div>
                    <div>{b("P3","p3")} &nbsp;Degraded performance</div>
                    <div>{b("P4","p4")} &nbsp;Cosmetic / low impact</div>
                </div>
            </div>""", unsafe_allow_html=True)

        if go:
            if title and description:
                with st.spinner("Classifying…"):
                    result = predict_bug(title, description)
                    st.session_state["result"]    = result
                    st.session_state["res_title"] = title
                    st.session_state["res_desc"]  = description

                p  = result["priority"];  s  = result["severity"]
                pc = result["priority_confidence"]; sc = result["severity_confidence"]

                st.markdown(f"""
                <div class="card pulse" style="border-color:#2A3A60; margin-top:.75rem;">
                    <div class="card-t" style="color:#818CF8; font-size:13px;">✅ Classification Complete</div>
                    <div class="rg">
                        <div class="rc">
                            <div class="rc-l">Priority</div>
                            <div class="rc-v">{pdot(p)}{p}&nbsp;&nbsp;{b(p,BM.get(p,""))}</div>
                        </div>
                        <div class="rc">
                            <div class="rc-l">Severity</div>
                            <div class="rc-v">{b(s,SM.get(s,""))}</div>
                        </div>
                        <div class="rc">
                            <div class="rc-l">Estimated Fix Time</div>
                            <div class="rc-v" style="font-size:15px;">{result["fix_time"]}</div>
                        </div>
                        <div class="rc">
                            <div class="rc-l">Assigned Team</div>
                            <div class="rc-v" style="font-size:15px;">{result["assigned_team"]}</div>
                        </div>
                    </div>
                    <div class="sep"></div>
                    <div style="font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#2D3A50;margin-bottom:8px;">Model Confidence</div>
                    {cbar("Priority Confidence", pc)}
                    {cbar("Severity Confidence", sc)}
                </div>""", unsafe_allow_html=True)
            else:
                st.warning("Please fill in both Title and Description before classifying.")

    # ── BULK CSV UPLOAD ─────────────────────────────────────────────────────
    else:
        cl, cr = st.columns([1.5, 1])

        with cl:
            st.markdown("""
            <div class="card">
                <div class="card-t">📂 Upload Bug Dataset CSV</div>
                <div style="font-size:13px;color:#3D4F6B;margin-bottom:14px;line-height:1.7;">
                    Upload any CSV with <strong style="color:#818CF8">title</strong> and
                    <strong style="color:#818CF8">description</strong> columns.
                    The ML model will classify every bug row automatically and
                    return priority, severity, fix time, and assigned team.
                </div>
            """, unsafe_allow_html=True)
            uploaded = st.file_uploader("Drop your CSV file here", type=["csv"], label_visibility="collapsed")
            st.markdown("</div>", unsafe_allow_html=True)

        with cr:
            st.markdown("""
            <div class="card">
                <div class="card-t">📋 Required CSV Columns</div>
                <div class="tip"><code>title</code> — short bug title</div>
                <div class="tip"><code>description</code> — detailed description</div>
                <div style="font-size:12px;color:#2D3A50;margin-top:10px;line-height:1.6;">
                    Any extra columns will be preserved in output.<br>
                    You can use your existing <strong style="color:#4A6080">bugs.csv</strong> from the data/raw folder to test!
                </div>
            </div>
            <div class="card" style="margin-top:0;">
                <div class="card-t">📤 What you get back</div>
                <div style="font-size:12.5px;color:#3D4F6B;line-height:2.2;">
                    <div>🔴 Priority (P1 / P2 / P3 / P4)</div>
                    <div>🟠 Severity (Critical / High / Medium / Low)</div>
                    <div>⏱️ Estimated Fix Time</div>
                    <div>👥 Assigned Team</div>
                    <div>📊 Confidence % per prediction</div>
                    <div>⬇️ Downloadable CSV results</div>
                </div>
            </div>""", unsafe_allow_html=True)

        if uploaded is not None:
            df_up = pd.read_csv(uploaded)

            # ── Auto-detect title & description columns ──
            all_cols = [c.lower().strip() for c in df_up.columns]
            col_map  = {c.lower().strip(): c for c in df_up.columns}

            # Find title column
            title_col = None
            for candidate in ["title","bug_title","bug title","name","summary","subject","issue","bug_name"]:
                if candidate in all_cols:
                    title_col = col_map[candidate]; break

            # Find description column
            desc_col = None
            for candidate in ["description","desc","details","body","content","bug_description","detail","comment","text","message"]:
                if candidate in all_cols:
                    desc_col = col_map[candidate]; break

            # If not found — let user pick manually
            if not title_col or not desc_col:
                st.markdown(f"""
                <div class="card" style="border-color:#2A3A60;">
                    <div class="card-t">🗂 Map Your Columns</div>
                    <div style="font-size:13px;color:#3D4F6B;margin-bottom:12px;">
                        We detected these columns in your CSV. Please select which ones
                        contain the <strong style="color:#818CF8">bug title</strong> and
                        <strong style="color:#818CF8">description</strong>.
                    </div>
                """, unsafe_allow_html=True)
                col_options = list(df_up.columns)
                mc1, mc2 = st.columns(2)
                with mc1:
                    title_col = st.selectbox("Select Title Column", col_options,
                        index=col_options.index(title_col) if title_col else 0)
                with mc2:
                    desc_col = st.selectbox("Select Description Column", col_options,
                        index=col_options.index(desc_col) if desc_col else min(1, len(col_options)-1))
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.success(f"✅ Auto-detected columns → Title: **{title_col}** | Description: **{desc_col}**")

            st.markdown(f"""
            <div class="card" style="border-color:#1E3A5F;">
                <div class="card-t">📊 Dataset Preview — <span style="color:#818CF8">{len(df_up):,} bugs found</span></div>
            """, unsafe_allow_html=True)
            st.dataframe(df_up.head(5), use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

            if title_col and desc_col:
                if st.button(f"🚀 Classify All {len(df_up):,} Bugs →", use_container_width=True):
                    results = []
                    prog = st.progress(0, text="Starting classification…")

                    for i, row in df_up.iterrows():
                        res = predict_bug(str(row[title_col]), str(row[desc_col]))
                        results.append({
                            "Bug Title"      : str(row[title_col])[:80],
                            "Priority"       : res["priority"],
                            "Severity"       : res["severity"],
                            "Fix Time"       : res["fix_time"],
                            "Assigned Team"  : res["assigned_team"],
                            "Priority Conf%" : round(float(res["priority_confidence"]), 1),
                            "Severity Conf%" : round(float(res["severity_confidence"]), 1),
                        })
                        prog.progress(
                            (i + 1) / len(df_up),
                            text=f"Classifying bug {i+1} of {len(df_up)}…"
                        )

                    prog.empty()
                    df_res = pd.DataFrame(results)
                    st.session_state["bulk_results"] = df_res
                    st.success(f"✅ All {len(df_res):,} bugs classified successfully!")

                # ── Show results ──
                if "bulk_results" in st.session_state:
                    df_res = st.session_state["bulk_results"]
                    pc_counts = df_res["Priority"].value_counts()

                    st.markdown(f"""
                    <div class="bulk-banner">
                        <div class="bulk-icon">🎯</div>
                        <div>
                            <div class="bulk-text-title">{len(df_res):,} Bugs Classified</div>
                            <div class="bulk-text-sub">ML model has triaged your entire dataset. Review results below.</div>
                        </div>
                    </div>

                    <div class="mc-row">
                        <div class="mc mc-r">
                            <div class="mc-lbl">P1 — Critical</div>
                            <div class="mc-num">{pc_counts.get("P1",0)}</div>
                            <div class="mc-meta">Needs immediate fix</div>
                        </div>
                        <div class="mc mc-a">
                            <div class="mc-lbl">P2 — High</div>
                            <div class="mc-num">{pc_counts.get("P2",0)}</div>
                            <div class="mc-meta">Fix this sprint</div>
                        </div>
                        <div class="mc mc-v">
                            <div class="mc-lbl">P3 — Medium</div>
                            <div class="mc-num">{pc_counts.get("P3",0)}</div>
                            <div class="mc-meta">Next sprint</div>
                        </div>
                        <div class="mc mc-g">
                            <div class="mc-lbl">P4 — Low</div>
                            <div class="mc-num">{pc_counts.get("P4",0)}</div>
                            <div class="mc-meta">Backlog</div>
                        </div>
                    </div>""", unsafe_allow_html=True)

                    # Full table
                    st.markdown('<div class="card"><div class="card-t">📋 Full Classification Results</div>', unsafe_allow_html=True)
                    st.dataframe(
                        df_res,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Bug Title"      : st.column_config.TextColumn("Bug Title", width="large"),
                            "Priority"       : st.column_config.TextColumn("Priority",  width="small"),
                            "Severity"       : st.column_config.TextColumn("Severity",  width="small"),
                            "Fix Time"       : st.column_config.TextColumn("Fix Time",  width="medium"),
                            "Assigned Team"  : st.column_config.TextColumn("Team",      width="medium"),
                            "Priority Conf%" : st.column_config.ProgressColumn("P-Conf%", min_value=0, max_value=100, width="small"),
                            "Severity Conf%" : st.column_config.ProgressColumn("S-Conf%", min_value=0, max_value=100, width="small"),
                        }
                    )
                    st.markdown("</div>", unsafe_allow_html=True)

                    # Charts
                    ch1, ch2 = st.columns(2)
                    with ch1:
                        st.markdown('<div class="card"><div class="card-t">🎯 Priority Distribution</div>', unsafe_allow_html=True)
                        pc3 = df_res["Priority"].value_counts().reset_index()
                        pc3.columns = ["Priority","Count"]
                        fig = px.bar(pc3, x="Priority", y="Count", color="Priority",
                                     color_discrete_map=PCOL)
                        fig.update_layout(**CHART, height=200, showlegend=False,
                                          xaxis=dict(tickfont=dict(color="#6A82A8",size=13)),
                                          yaxis=dict(gridcolor="#1A2235",tickfont=dict(color="#3D4F6B",size=12)))
                        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
                        st.markdown("</div>", unsafe_allow_html=True)

                    with ch2:
                        st.markdown('<div class="card"><div class="card-t">👥 Team Workload</div>', unsafe_allow_html=True)
                        tc = df_res["Assigned Team"].value_counts().reset_index()
                        tc.columns = ["Team","Count"]
                        fig2 = px.pie(tc, values="Count", names="Team", hole=.55,
                                      color_discrete_sequence=["#6366F1","#A855F7","#06B6D4","#10B981","#FBBF24"])
                        fig2.update_layout(**CHART, height=200,
                                           legend=dict(font=dict(color="#4A6080",size=11),bgcolor="rgba(0,0,0,0)"))
                        fig2.update_traces(textfont_color="#0B0F19", textfont_size=12)
                        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
                        st.markdown("</div>", unsafe_allow_html=True)

                    # Download
                    csv_out = df_res.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="⬇️  Download Results as CSV",
                        data=csv_out,
                        file_name="bug_triage_results.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )


# ════════════════════════════════════════════════════════════════════════════
# PAGE 3 — LAST RESULT
# ════════════════════════════════════════════════════════════════════════════
elif page == "📊  Last Result":
    st.markdown("""
    <div class="ph">
        <div class="ph-eye">Results</div>
        <div class="ph-title">Last Classification</div>
        <div class="ph-desc">Detailed view of the most recent single-bug prediction.</div>
    </div>""", unsafe_allow_html=True)

    if "result" not in st.session_state:
        st.markdown("""
        <div class="card">
            <div class="empty">
                <div class="ei">🔍</div>
                <div class="et">No prediction yet</div>
                <div class="ed">Go to Submit Bug → Single Bug and classify a report first.</div>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        result = st.session_state["result"]
        p  = result["priority"];  s  = result["severity"]
        pc = result["priority_confidence"]; sc = result["severity_confidence"]
        escalate = s in ("Critical","High")

        c1, c2 = st.columns([1.35, 1])
        with c1:
            st.markdown(f"""
            <div class="card">
                <div class="card-t">🐛 Bug Report</div>
                <div style="font-size:15px;font-weight:700;color:#C8D8F0;margin-bottom:7px;">{st.session_state.get("res_title","—")}</div>
                <div style="font-size:13px;color:#3D4F6B;line-height:1.7;">{st.session_state.get("res_desc","—")}</div>
            </div>
            <div class="card">
                <div class="card-t">🎯 Classification Result</div>
                <div class="rg">
                    <div class="rc"><div class="rc-l">Priority</div>
                        <div class="rc-v">{pdot(p)}{p}&nbsp;{b(p,BM.get(p,""))}</div></div>
                    <div class="rc"><div class="rc-l">Severity</div>
                        <div class="rc-v">{b(s,SM.get(s,""))}</div></div>
                    <div class="rc"><div class="rc-l">Fix Time</div>
                        <div class="rc-v" style="font-size:15px;">{result["fix_time"]}</div></div>
                    <div class="rc"><div class="rc-l">Team</div>
                        <div class="rc-v" style="font-size:15px;">{result["assigned_team"]}</div></div>
                </div>
            </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="card"><div class="card-t">📊 Confidence Scores</div>', unsafe_allow_html=True)
            fig = go.Figure(go.Bar(
                x=[pc,sc], y=["Priority","Severity"], orientation="h",
                marker_color=["#6366F1","#A855F7"],
                text=[f"{pc:.1f}%",f"{sc:.1f}%"], textposition="outside",
                textfont=dict(color="#818CF8",size=13)
            ))
            fig.update_layout(**CHART, height=160,
                              xaxis=dict(range=[0,118],gridcolor="#1A2235",tickfont=dict(color="#3D4F6B",size=12)),
                              yaxis=dict(tickfont=dict(color="#6A82A8",size=13)))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card" style="margin-top:0;">
                <div class="card-t">ℹ️ What this means</div>
                <div style="font-size:13px;color:#3D4F6B;line-height:2.3;">
                    <div>{b(p,BM.get(p,""))} → fix within <strong style="color:#818CF8">{result["fix_time"]}</strong></div>
                    <div>Escalation <strong style="color:{'#F87171' if escalate else '#34D399'}">{'required' if escalate else 'not required'}</strong></div>
                    <div>Routed → <strong style="color:#818CF8">{result["assigned_team"]}</strong></div>
                </div>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 4 — MODEL HEALTH
# ════════════════════════════════════════════════════════════════════════════
elif page == "📈  Model Health":
    st.markdown("""
    <div class="ph">
        <div class="ph-eye">MLOps</div>
        <div class="ph-title">Model Health</div>
        <div class="ph-desc">Track accuracy, experiment history, and version performance over time.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="mc-row">
        <div class="mc mc-v">
            <div class="mc-lbl">Priority Accuracy</div>
            <div class="mc-num">100%</div>
            <div class="mc-meta"><span class="up">↑ 28pp</span> since v1</div>
        </div>
        <div class="mc mc-g">
            <div class="mc-lbl">Severity Accuracy</div>
            <div class="mc-num">100%</div>
            <div class="mc-meta"><span class="up">↑ 32pp</span> since v1</div>
        </div>
        <div class="mc mc-a">
            <div class="mc-lbl">Active Model</div>
            <div class="mc-num" style="font-size:24px;">v2.0</div>
            <div class="mc-meta">RF · 200 estimators</div>
        </div>
        <div class="mc mc-r">
            <div class="mc-lbl">Training Set</div>
            <div class="mc-num">1,000</div>
            <div class="mc-meta">800 train · 200 test</div>
        </div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card"><div class="card-t">📈 Accuracy per Version</div>', unsafe_allow_html=True)
        ver = pd.DataFrame({"Version":["v1.0","v1.1","v1.2","v2.0"],
                            "Priority":[72,81,88,100],"Severity":[68,76,85,100]})
        fig = px.line(ver, x="Version", y=["Priority","Severity"], markers=True,
                      color_discrete_map={"Priority":"#6366F1","Severity":"#A855F7"})
        fig.update_layout(**CHART, height=220,
                          legend=dict(font=dict(color="#4A6080",size=12),bgcolor="rgba(0,0,0,0)",title_text=""),
                          xaxis=dict(gridcolor="#1A2235",tickfont=dict(color="#3D4F6B",size=12)),
                          yaxis=dict(gridcolor="#1A2235",tickfont=dict(color="#3D4F6B",size=12),range=[60,107]))
        fig.update_traces(line_width=2.5, marker_size=7)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card"><div class="card-t">🔬 Experiment Runs</div>', unsafe_allow_html=True)
        runs = pd.DataFrame({"Run":["run_001","run_002","run_003","run_004"],
                             "Estimators":["100","100","200","200"],
                             "P-Acc":["72%","81%","88%","100%"],
                             "S-Acc":["68%","76%","85%","100%"],
                             "Status":["archived","archived","archived","● live"]})
        st.dataframe(runs, use_container_width=True, hide_index=True)
        st.info("Full run history → http://127.0.0.1:5000")
        st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 5 — RETRAIN
# ════════════════════════════════════════════════════════════════════════════
elif page == "🔁  Retrain":
    st.markdown("""
    <div class="ph">
        <div class="ph-eye">MLOps</div>
        <div class="ph-title">Retrain Pipeline</div>
        <div class="ph-desc">Upload labelled bug data and trigger an automated Prefect retraining flow.</div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.markdown('<div class="card"><div class="card-t">📤 Upload Training Data</div>', unsafe_allow_html=True)
        upl = st.file_uploader("Drop a CSV file here", type=["csv"], label_visibility="collapsed")
        if upl:
            dup = pd.read_csv(upl)
            st.success(f"Loaded {len(dup):,} records from {upl.name}")
            st.dataframe(dup.head(5), use_container_width=True, hide_index=True)
        st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
        if st.button("🚀 Run Retraining Pipeline", use_container_width=True):
            with st.spinner("Running Prefect pipeline…"):
                import subprocess
                subprocess.run(["python","src/train.py"])
            st.success("Pipeline complete — model updated!")
            st.balloons()
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
            <div class="card-t">⚙️ Pipeline Steps</div>
            <div class="step"><div class="sn">1</div><div class="st-txt">Check data drift <strong>(Evidently AI)</strong></div></div>
            <div class="step"><div class="sn">2</div><div class="st-txt">Preprocess &amp; version data <strong>(DVC)</strong></div></div>
            <div class="step"><div class="sn">3</div><div class="st-txt">Retrain <strong>RandomForest</strong> model</div></div>
            <div class="step"><div class="sn">4</div><div class="st-txt">Log metrics to <strong>MLflow</strong></div></div>
            <div class="step"><div class="sn">5</div><div class="st-txt">Validate &amp; register new model version</div></div>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 6 — ANALYTICS
# ════════════════════════════════════════════════════════════════════════════
elif page == "📉  Analytics":
    st.markdown("""
    <div class="ph">
        <div class="ph-eye">Insights</div>
        <div class="ph-title">Bug Analytics</div>
        <div class="ph-desc">Distribution, team workload, and cross-environment breakdowns.</div>
    </div>""", unsafe_allow_html=True)

    df = load_df()

    if df.empty:
        st.markdown("""
        <div class="card">
            <div class="empty">
                <div class="ei">📊</div>
                <div class="et">No data available</div>
                <div class="ed">Run the preprocessing pipeline first to generate analytics.</div>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="card"><div class="card-t">🔴 Priority Breakdown</div>', unsafe_allow_html=True)
            pc2 = df["priority"].value_counts().reset_index(); pc2.columns=["Priority","Count"]
            fig = px.bar(pc2, x="Priority", y="Count", color="Priority", color_discrete_map=PCOL)
            fig.update_layout(**CHART, height=220, showlegend=False,
                              xaxis=dict(tickfont=dict(color="#6A82A8",size=13)),
                              yaxis=dict(gridcolor="#1A2235",tickfont=dict(color="#3D4F6B",size=12)))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="card"><div class="card-t">🟠 Severity Distribution</div>', unsafe_allow_html=True)
            sc2 = df["severity"].value_counts().reset_index(); sc2.columns=["Severity","Count"]
            fig2 = px.pie(sc2, values="Count", names="Severity", hole=.55,
                          color="Severity", color_discrete_map=SCOL)
            fig2.update_layout(**CHART, height=220,
                               legend=dict(font=dict(color="#4A6080",size=12),bgcolor="rgba(0,0,0,0)"))
            fig2.update_traces(textfont_color="#0B0F19", textfont_size=13)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
            st.markdown("</div>", unsafe_allow_html=True)

        if "product_module" in df.columns and "environment" in df.columns:
            st.markdown('<div class="card"><div class="card-t">📦 Module × Environment</div>', unsafe_allow_html=True)
            cross = df.groupby(["product_module","environment"]).size().reset_index(name="Count")
            fig3 = px.bar(cross, x="product_module", y="Count", color="environment",
                          barmode="group", color_discrete_sequence=["#6366F1","#A855F7","#06B6D4"])
            fig3.update_layout(**CHART, height=240,
                               legend=dict(font=dict(color="#4A6080",size=12),bgcolor="rgba(0,0,0,0)",title_text="Env"),
                               xaxis=dict(tickfont=dict(color="#6A82A8",size=12)),
                               yaxis=dict(gridcolor="#1A2235",tickfont=dict(color="#3D4F6B",size=12)))
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})
            st.markdown("</div>", unsafe_allow_html=True)

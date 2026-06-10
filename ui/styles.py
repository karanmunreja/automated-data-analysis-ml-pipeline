import streamlit as st
def load_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:      #F5F3EE;
    --surface: #FFFFFF;
    --border:  #E2DDD5;
    --accent1: #FF4D6D;
    --accent2: #0066FF;
    --accent3: #00C896;
    --accent4: #FFB800;
    --text:    #1A1A2E;
    --muted:   #7A7A9A;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Outfit', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: #1A1A2E !important;
    border-right: 3px solid #E8EAF0 !important;
    min-width: 250px !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1rem !important; }
[data-testid="collapsedControl"]        { display: none !important; }
button[kind="headerNoPadding"]          { display: none !important; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }
[data-testid="stSidebar"] * { color: #E8E8F0 !important; }
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label { color: #A0A0C0 !important; }

#MainMenu, footer, header { visibility: hidden; }
h1, h2, h3, h4 { font-family: 'Syne', sans-serif !important; color: var(--text) !important; }

[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1.1rem 1.2rem !important;
    
}
[data-testid="metric-container"] label {
    color: var(--muted) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.65rem !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--accent2) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
}

.stButton > button {
    background: var(--accent1) !important;
    border: none !important;
    color: #FFFFFF !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(255,77,109,0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(255,77,109,0.45) !important;
}

.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: var(--surface) !important;
    color: black !important;
    border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
}
 [data-testid="stNumberInput"] input {
    color: black !important;
    background: white !important;
}
            
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 2px var(--border) !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploader"] * {
    color: black !important;
}
[data-testid="stDataFrame"] {
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}
details {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
}
summary {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: var(--accent2) !important;
}
hr { border-color: var(--border) !important; }

.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 999px;
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.badge-coral   { background: rgba(255,77,109,.12);  color: #FF4D6D; border: 1.5px solid #FF4D6D; }
.badge-cobalt  { background: rgba(0,102,255,.10);   color: #0066FF; border: 1.5px solid #0066FF; }
.badge-emerald { background: rgba(0,200,150,.12);   color: #00C896; border: 1.5px solid #00C896; }
.badge-amber   { background: rgba(255,184,0,.12);   color: #B07D00; border: 1.5px solid #FFB800; }

.section-strip { display:flex; align-items:center; gap:12px; margin:2rem 0 1.2rem; }
.section-strip .line  { flex:1; height:2px; background:linear-gradient(to right,var(--border),transparent); }
.section-strip .label { font-family:'Syne',sans-serif; font-size:0.68rem; font-weight:700; text-transform:uppercase; letter-spacing:3px; color:var(--muted); }

.score-bar-wrap { background:var(--border); border-radius:999px; height:6px; width:100%; overflow:hidden; }
.score-bar      { height:6px; border-radius:999px; transition:width 0.8s ease; }

.model-card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 2px 10px rgba(26,26,46,0.05);
}
.model-card.best {
    border-color: var(--accent3);
    box-shadow: 0 0 0 3px rgba(0,200,150,.15), 0 4px 20px rgba(0,200,150,.1);
}
.model-card h4 { margin:0 0 .5rem; font-size:0.95rem; font-family:'Syne',sans-serif; }

.terminal {
    background: #1A1A2E;
    border: 1.5px solid #2E2E4E;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-family: 'Courier New', monospace;
    font-size: 0.82rem;
    color: #00C896;
    line-height: 1.8;
    white-space: pre-wrap;
}
.terminal .prompt { color: #5B9CFF; }

.col-toggle-wrap details {
    border: none !important;
    background: transparent !important;
    display: inline-block;
}
.col-toggle-wrap summary {
    cursor: pointer;
    color: var(--accent2) !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    list-style: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 0;
    user-select: none;
}
.col-toggle-wrap summary::before {
    content: "▶";
    font-size: 0.55rem;
    transition: transform 0.2s;
    display: inline-block;
    color: var(--accent2);
}
.col-toggle-wrap details[open] summary::before { transform: rotate(90deg); }
.col-toggle-wrap .cols-list {
    margin-top: 8px;
    padding: 10px 14px;
    background: rgba(0,102,255,.05);
    border-left: 3px solid var(--accent2);
    border-radius: 0 8px 8px 0;
    line-height: 2;
}
.col-toggle-wrap .col-pill {
    display: inline-block;
    margin: 2px 4px;
    padding: 1px 10px;
    background: rgba(0,102,255,.08);
    border-radius: 4px;
    font-size: .74rem;
    color: var(--text);
}
</style>
""", unsafe_allow_html=True)
    js = """
    <script>
        window.addEventListener('load', function() {
            // Keep trying until sidebar button found
            var attempts = 0;
            var interval = setInterval(function() {
                attempts++;
                var btn = window.parent.document.querySelector('[data-testid="collapsedControl"]');
                var sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
                if (sidebar) {
                    sidebar.style.display = 'block';
                    sidebar.style.visibility = 'visible';
                    sidebar.style.transform = 'none';
                    sidebar.style.minWidth = '244px';
                }
                if (attempts > 20) clearInterval(interval);
            }, 200);
        });
    </script>
    """
    st.components.v1.html(js, height=0)

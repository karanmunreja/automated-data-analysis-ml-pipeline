import streamlit as st
import pandas as pd
import numpy as np
import tempfile, os, time

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Data Advisor",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Force sidebar open always
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

# ── CSS ───────────────────────────────────────────────────────────────────────
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

/*
  LESSON 5: SIDEBAR STYLING
  Deep navy sidebar against cream main area = "split-tone" layout.
  All sidebar text must be light since background is dark.
  We use [data-testid="stSidebar"] * to target all children.
*/
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

/*
  LESSON 6: METRIC COMPONENTS
  st.metric() uses data-testid="metric-container".
  We give it a white card with shadow and override the value colour.
*/
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

/*
  LESSON 7: BUTTON STYLING
  .stButton > button targets the actual <button> element.
  Filled coral button with a coloured shadow glow.
  transform: translateY(-2px) on hover gives a lift effect.
*/
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

/*
  LESSON 8: INPUT STYLING
  Selectboxes, text inputs and number inputs all share these patterns.
  White background + soft border keeps them clean on the cream page.
*/
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

/*
  LESSON 9: CUSTOM HTML COMPONENTS
  Define CSS classes here, apply via st.markdown(unsafe_allow_html=True).
  This is how you build UI elements Streamlit doesn't have natively.
*/
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

/*
  LESSON 10: COLLAPSIBLE COLUMN LIST — pure HTML <details>/<summary>
  No JavaScript, no Streamlit state. Browser handles the toggle natively.
  The summary::before arrow rotates 90° when details[open] is present.
  This is a great pattern for "show more / hide" without re-running Python.
*/
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


# ── Helpers ───────────────────────────────────────────────────────────────────
def section(label):
    st.markdown(f'<div class="section-strip"><div class="line"></div><div class="label">{label}</div><div class="line"></div></div>', unsafe_allow_html=True)

def model_card(name, score, is_best=False):
    cls   = "model-card best" if is_best else "model-card"
    color = "#7DF9AA" if is_best else "#5B8CFF"
    star  = " ★ BEST" if is_best else ""
    pct   = max(0, min(100, int(abs(score) * 100)))
    bar   = "da-bar-green" if is_best else "da-bar-blue"
    st.markdown(
        f'<div class="{cls}"><h4 style="color:{color};">{name}{star}</h4>'
        f'<div style="display:flex;justify-content:space-between;font-family:Space Mono,monospace;font-size:.72rem;color:#6B7280;margin-bottom:3px;">'
        f'<span>Score</span><span style="color:{color};">{score:.4f}</span></div>'
        f'<div class="score-bar-wrap"><div class="score-bar" style="width:{pct}%;background:{color};"></div></div></div>',
        unsafe_allow_html=True,
    )

def terminal_box(prompt_text, body_text):
    st.markdown(
        f'<div class="terminal"><span class="prompt">$&gt; {prompt_text}</span>\n{body_text}</div>',
        unsafe_allow_html=True,
    )
def collapsible_columns(label, cols):
   
    pills = "".join(f'<span class="col-pill">{c}</span>' for c in cols)
    st.markdown(
        f'<div class="col-toggle-wrap"><details>'
        f'<summary>{label} &nbsp;<span style="color:#B0B0C0;font-weight:400;">({len(cols)})</span></summary>'
        f'<div class="cols-list">{pills}</div>'
        f'</details></div>',
        unsafe_allow_html=True,
    )
def save_uploaded_file(uploaded_file):
    """Save Streamlit uploaded file to a temp path and return the path."""
    suffix = os.path.splitext(uploaded_file.name)[-1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded_file.getvalue())
    tmp.flush()
    return tmp.name


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="padding:1.2rem 0 1.6rem;">'
        '<div style=" font-family:Koltav,sans-serif;font-size:1.5rem;letter-spacing:2px;color:#F5F3EE;">GET INSIGHTS</div>'
        '<div style="font-size:1rem;color:#F5F3EE;margin-top:3px;line-height:1;">Upload a dataset</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("**Dataset**")
    uploaded = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
    use_iris = st.checkbox("Use built-in Iris dataset", value=True)

    st.markdown("---")
    st.markdown("**Problem Type**")
    problem_map = {1: "Regression", 2: "Classification", 3: "Clustering"}
    problem_choice = st.radio(
        "Select",
        options=list(problem_map.keys()),
        format_func=lambda x: f"{x} — {problem_map[x]}",
        label_visibility="collapsed",
    )
    problem_type = problem_map[problem_choice]

    st.markdown("**Options**")

    if problem_type in ["Regression", "Classification"]:
        test_size   = st.slider("Test split %", 10, 40, 20, step=5)
        random_seed = st.number_input("Random seed", value=42, step=1)
       
    run_btn     = st.button("▶  Run Pipeline", use_container_width=True)
    st.markdown("---")
    if problem_type in ["Regression", "Classification"]:
        st.markdown(f'<div style="font-family:Space Mono,monospace;font-size:.68rem;line-height:1.7;"> PROBLEM <span style="color:#5B8CFF;">{problem_type.upper()}</span><br> TEST SIZE <span style="color:#5B8CFF;">{test_size}%</span><br>  SEED <span style="color:#5B8CFF;">{random_seed}</span </div>',
        unsafe_allow_html=True,
    )

    else:
        st.markdown(f'<div style="font-family:Space Mono,monospace;font-size:.68rem;line-height:1.7;"> PROBLEM <span style="color:#5B8CFF;">CLUSTERING</span></div>',
        unsafe_allow_html=True,
    )
   

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown('<div style="font-family:Koltav,sans-serif;font-size:2.5rem;letter-spacing:3px;color:black;padding-top:1.5rem;">Data <span style="color:#089984;">Advisor</span></div>', unsafe_allow_html=True)
st.markdown('<div style="font-family:Space Mono,monospace;font-size:1rem;letter-spacing:1px;text-transform:uppercase;color:#0B6623 ;margin:.4rem 0 1rem;">Automated Analytics, <span style="color:#5B8CFF;">Predictions</span> <span style="color:#1b70a6;"> & Recommendations</span></div>', unsafe_allow_html=True)



# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_iris_csv():
    from sklearn.datasets import load_iris as _li
    iris = _li(as_frame=True)
    df   = iris.frame
    df.rename(columns={"target": "species"}, inplace=True)
    tmp  = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    df.to_csv(tmp.name, index=False)
    return tmp.name, df

file_path = None
df_preview = None

if uploaded:
    file_path  = save_uploaded_file(uploaded)
    df_preview = pd.read_csv(file_path)
elif use_iris:
    file_path, df_preview = load_iris_csv()

if file_path is None:
    st.info("Upload a CSV or enable the built-in Iris dataset to begin.")
    st.stop()


# ── Import your modules ───────────────────────────────────────────────────────
from dataset_insights import DatasetAnalyzer, ProblemDetector
from preprocessing    import DataPreprocessor
from ML_models        import RegressionModel, ClassificationModel, ClusteringModel
from recommendations  import InsightGenerator


# ── 01 Dataset Overview ───────────────────────────────────────────────────────
section("01 · Dataset Overview")

analyzer = DatasetAnalyzer(file_path)
summary  = analyzer.get_summary()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows",          summary["num_rows"])
c2.metric("Columns",       summary["num_columns"])
c3.metric("Numeric cols",  df_preview.select_dtypes(include=np.number).shape[1])
c4.metric("Missing values", sum(summary["missing_values"].values()))

with st.expander("Preview first 10 rows"):
    st.dataframe(df_preview.head(10), use_container_width=True)

with st.expander("Descriptive statistics"):
    st.dataframe(df_preview.describe().round(4), use_container_width=True)

if sum(summary["missing_values"].values()) > 0:
    st.warning(f"⚠ Missing values detected — will be imputed automatically.")
else:
    st.markdown('<span class="badge badge-green">✓ No missing values</span>', unsafe_allow_html=True)


# ── 02 Problem Detection ──────────────────────────────────────────────────────
section("02 · Problem Detection")

problem_detection = ProblemDetector().problems

col_a, col_b = st.columns([2, 1])
with col_a:
      st.markdown(
        f'<div class="model-card">'
        f'<h4 style="color:#0066FF;">Detected configuration</h4>'
        f'<div style="font-size:.82rem;color:#7A7A9A;line-height:2.2;">'
        f'Total features &nbsp;→&nbsp; <span style="color:#1A1A2E;font-weight:600;">{summary["num_columns"]}</span><br>'
        f'Selected task &nbsp;&nbsp;&nbsp;→&nbsp; <span style="color:#FF4D6D;font-family:Syne,sans-serif;font-weight:700;">{problem_type.upper()}</span>'
        f'</div></div>',
        unsafe_allow_html=True,
    )
      collapsible_columns("Column names", summary["column_names"])

with col_b:
    badge_map = {"Regression": "coral", "Classification": "cobalt", "Clustering": "emerald"}
    for k, v in problem_detection.items():
        if k == 4:
            continue
        badge = badge_map.get(v, "amber")
        tick  = "✓ " if v == problem_type else ""
        op    = "" if v == problem_type else ' style="opacity:.3"'
        st.markdown(f'<span class="badge badge-{badge}"{op}>{tick}{v}</span><br><br>', unsafe_allow_html=True)


# ── 03 Feature & Target Selection ────────────────────────────────────────────
all_cols     = df_preview.columns.tolist()
numeric_cols = df_preview.select_dtypes(include=np.number).columns.tolist()

if problem_choice in [1, 2]:
    section("03 · Feature & Target Selection")
    target_col   = st.selectbox("Target column", all_cols, index=None, placeholder="Select target column")
    feature_cols = [c for c in numeric_cols if c != target_col]
    if feature_cols:
        collapsible_columns("Features used", feature_cols)
    else:
        st.markdown('<span class="badge badge-amber">⚠ No numeric features — choose a different target</span>',
                    unsafe_allow_html=True)
else:
    target_col   = None
    feature_cols = numeric_cols
    section("03 · Feature Selection")
    collapsible_columns("All numeric features", feature_cols)



# ── Wait for Run ──────────────────────────────────────────────────────────────
if not run_btn:
    st.markdown(
        '<div style="margin-top:3rem;text-align:center;">'
        '<div style="font-family:Space Mono,monospace;font-size:3rem;color:#232736;">◈</div>'
        '<div style="font-size:.85rem;color:#374151;margin-top:.5rem;">Press <b style="color:#6B7280;">Run Pipeline</b> in the sidebar to train models</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.stop()


# ── 04 Preprocessing (your DataPreprocessor) ──────────────────────────────────
section("04 · Preprocessing")

preprocessor = DataPreprocessor()
if problem_type=='Clustering':
    pass
else:
    preprocessor.test_size    = test_size / 100
    preprocessor.random_state = int(random_seed)


with st.spinner("Preprocessing data using DataPreprocessor…"):
    time.sleep(0.3)
    if problem_choice in [1, 2]:
        if target_col is None:
            st.warning("Please select a target column.")
            st.stop()
        X_train, X_test, y_train, y_test = preprocessor.preprocess(file_path,problem_type,target_col)
      
    else:
        X_train= preprocessor.preprocess(file_path, problem_type,None)

c1, c2, c3 = st.columns(3)
c1.metric("Train samples", len(X_train))
if problem_type=='Clustering':
    c2.metric("Clusters",'2-11')
else:
    c2.metric('Test Samples',len(X_test))
c3.metric("Features",      X_train.shape[1])

st.success("✓ Preprocessing complete — your DataPreprocessor handled encoding, scaling & splitting")


# ── 05 Model Training (your ML_models) ───────────────────────────────────────
section("05 · Model Training")

results     = {}
score_label = "Score"

if problem_type == "Regression":
    prog   = st.progress(0, text="Training Linear Regression…")
    reg    = RegressionModel(X_train, y_train, X_test, y_test)
    m1, s1 = reg.linear_regression()
    results["Linear Regression"] = (m1, s1)
    prog.progress(50, text="Training KNN Regression…")
    m2, s2 = reg.Knn_regression()
    results["KNN Regression"] = (m2, s2)
    prog.progress(100, text="Done!")
    score_label = "R² Score"

elif problem_type == "Classification":
    prog   = st.progress(0, text="Training Logistic Regression…")
    clf    = ClassificationModel(X_train, y_train, X_test, y_test)
    m1, s1 = clf.logistic_regression()
    results["Logistic Regression"] = (m1, s1)
    prog.progress(50, text="Training KNN Classifier…")
    m2, s2 = clf.Knn_classification()
    results["KNN Classification"] = (m2, s2)
    prog.progress(100, text="Done!")
    score_label = "Accuracy"

else:
    prog   = st.progress(0, text="Training KMeans Clustering…")
    clu    = ClusteringModel(X_train)
    m1, s1,best_k = clu.KMeans_clustering()
    results["KMeans Clustering"] = (m1, s1)
    prog.progress(100, text="Done!")
    score_label = "Silhouette"

time.sleep(0.2)


# ── 06 Results ────────────────────────────────────────────────────────────────
section("06 · Results")

best_name = max(results, key=lambda k: results[k][1])
best_model, best_score = results[best_name]



cols = st.columns(len(results))
for i, (name, (model, score)) in enumerate(results.items()):
    with cols[i]:
        model_card(name, score, is_best=(name == best_name))
if problem_type=='Clustering':
    score_df = pd.DataFrame(
    [{"Model": k, score_label: round(v[1], 6),"Clusters":best_k, "Best": "★" if k == best_name else ""}
     for k, v in results.items()]
)
else:
    score_df = pd.DataFrame(
    [{"Model": k, score_label: round(v[1], 6), "Best": "★" if k == best_name else ""}
     for k, v in results.items()]
)
st.dataframe(score_df, use_container_width=True, hide_index=True)


# ── 07 Insights (your InsightGenerator) ──────────────────────────────────────
section("07 · Insights & Recommendations")

insight_generator = InsightGenerator()
target = target_col if target_col is not None else df_preview.columns[-1]

if problem_type == "Regression":
    insight, recommendation = insight_generator.regression_insights_recommendation(
        best_model, X_train.columns, target
    )
elif problem_type == "Classification":
    insight, recommendation = insight_generator.classification_insights_recommendation(
        best_model, X_train.columns, target
    )
else:
    insight, recommendation = insight_generator.clustering_insights_recommendation(
        best_model, X_train.columns
    )

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Insight**")
    terminal_box("analyze_model --best", insight)
with col2:
    st.markdown("**Recommendation**")
    terminal_box("suggest_next_steps", recommendation)

if problem_type == "Classification":
    st.markdown("---")
    with st.expander("Classification report"):
        from sklearn.metrics import classification_report
        report = classification_report(y_test, best_model.predict(X_test), output_dict=True)
        st.dataframe(pd.DataFrame(report).T.round(3), use_container_width=True)

if problem_type == "Clustering":
    st.markdown("---")
    with st.expander("Cluster centres"):
        centers_df = pd.DataFrame(best_model.cluster_centers_, columns=X_train.columns)
        centers_df.index.name = "Cluster"
        st.dataframe(centers_df.round(4), use_container_width=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center;font-family:Space Mono,monospace;font-size:.62rem;color:#374151;padding:.6rem 0;">'
    'Data Advisor · Intelligent Automated Analytics, Prediction &amp; Recommendation Framework'
    '</div>',
    unsafe_allow_html=True,
)
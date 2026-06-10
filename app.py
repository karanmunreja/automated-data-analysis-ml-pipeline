import streamlit as st
import pandas as pd
import numpy as np
import time

from ui.styles import load_styles
from ui.sidebar import render_Sidebar
from ui.components import *

from services.data_service import *
from services.training_service import train_models
from services.insight_service import generate_insights

from core.dataset_insights import DatasetAnalyzer, ProblemDetector
from core.preprocessing import DataPreprocessor


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Data Advisor",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)
load_styles()
st.markdown('<div style="font-family:Koltav,sans-serif;font-size:2.7rem;letter-spacing:3px;color:black;padding-top:1.5rem;">Data <span style="color:#089984;">Advisor</span></div>', unsafe_allow_html=True)
st.markdown('<div style="font-family:Space Mono,monospace;font-size:1.2rem;letter-spacing:.8px;text-transform:uppercase;color:#0B6623 ;margin:.4rem 0 1rem;">Automated Data Analytics, <span style="color:#5B8CFF;">Predictions</span> <span style="color:#1b70a6;"> & Recommendations</span></div>', unsafe_allow_html=True)

cfg = render_Sidebar()

uploaded = cfg["uploaded"]
use_iris = cfg["use_iris"]
problem_choice = cfg["problem_choice"]
problem_type = cfg["problem_type"]
test_size = cfg["test_size"]
random_seed = cfg["random_seed"]
run_btn = cfg["run_btn"]

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

#  01 Dataset Overview
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


# 02 Problem Detection 
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


# 03 Feature & Target Selection 
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



# Wait for Run 
if not run_btn:
    st.markdown(
        '<div style="margin-top:3rem;text-align:center;">'
        '<div style="font-family:Space Mono,monospace;font-size:3rem;color:#232736;">◈</div>'
        '<div style="font-size:.85rem;color:#374151;margin-top:.5rem;">Press <b style="color:#6B7280;">Run Pipeline</b> in the sidebar to train models</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.stop()


# 04 Preprocessing (your DataPreprocessor) 
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


#  05 Model Training 
section("05 · Model Training")
    
results, score_label,best_k=train_models(problem_type,X_train,X_test if problem_type!='Clustering'else None,y_train  if problem_type!='Clustering'else None,y_test  if problem_type!='Clustering'else None)


#  06 Results
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


# ── 07 Insights (your InsightGenerator) 
section("07 · Insights & Recommendations")

target = target_col if target_col is not None else df_preview.columns[-1]
insight, recommendation = generate_insights(
    problem_type,
    best_model,
    X_train.columns,
    target
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
import streamlit as st

def render_Sidebar():
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
        test_size = None
        random_seed = None
        if problem_type in ["Regression", "Classification"]:
            test_size   = st.slider("Test split %", 10, 40, 20, step=5)
            random_seed = st.number_input("Random seed", value=42, step=1)
       
        run_btn = st.button("▶  Run Pipeline", use_container_width=True)
        st.markdown("---")
        if problem_type in ["Regression", "Classification"]:
             st.markdown(f'<div style="font-family:Space Mono,monospace;font-size:.68rem;line-height:1.7;"> PROBLEM <span style="color:#5B8CFF;">{problem_type.upper()}</span><br> TEST SIZE <span style="color:#5B8CFF;">{test_size}%</span><br>  SEED <span style="color:#5B8CFF;">{random_seed}</span </div>',
        unsafe_allow_html=True,
    )
        else:
             st.markdown(f'<div style="font-family:Space Mono,monospace;font-size:.68rem;line-height:1.7;"> PROBLEM <span style="color:#5B8CFF;">CLUSTERING</span></div>',
        unsafe_allow_html=True,
    )
    return {
    "uploaded": uploaded,
    "use_iris": use_iris,
    "problem_choice": problem_choice,
    "problem_type": problem_type,
    "test_size": test_size,
    "random_seed": random_seed,
    "run_btn": run_btn,
}
   
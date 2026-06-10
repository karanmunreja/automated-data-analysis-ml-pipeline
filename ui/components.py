import streamlit as st
import os

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

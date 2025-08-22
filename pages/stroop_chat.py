import streamlit as st
import openai
import os
try:
    # Prefer server-side Stroop helpers for robust session/state handling
    from utils.stroop import generate_stroop_trial, now_seconds, COLORS
except ModuleNotFoundError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from utils.stroop import generate_stroop_trial, now_seconds, COLORS


st.set_page_config(
    page_title="Chat + Stroop",
    page_icon="🧠",
    layout="centered"
)

# Configuration: interval between Stroop prompts

def get_stroop_interval_seconds() -> int:
    interval = 60
    try:
        if "STROOP_INTERVAL_SECONDS" in st.secrets:
            interval = int(st.secrets["STROOP_INTERVAL_SECONDS"])  # type: ignore[arg-type]
    except Exception:
        pass
    try:
        qp = st.query_params()
        if "stroop_interval" in qp:
            val = qp["stroop_interval"]
            if isinstance(val, list):
                val = val[0]
            interval = int(val)
    except Exception:
        pass
    try:
        env_val = os.getenv("STROOP_INTERVAL_SECONDS")
        if env_val:
            interval = int(env_val)
    except Exception:
        pass
    return max(5, interval)


_interval_s = get_stroop_interval_seconds()

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("How can I help? 🧠")

if "chats" not in st.session_state:
    st.session_state.chats = []

# ---------- Stroop (server-side) ----------

if "stroop_last_shown" not in st.session_state:
    st.session_state.stroop_last_shown = 0.0

if "stroop_active" not in st.session_state:
    st.session_state.stroop_active = False

if "stroop_trial" not in st.session_state:
    st.session_state.stroop_trial = None


def _show_stroop_modal() -> None:
    st.session_state.stroop_active = True
    st.session_state.stroop_trial = generate_stroop_trial()
    st.session_state.stroop_last_shown = now_seconds()


# Auto-trigger modal every interval
current_time = now_seconds()
if current_time - st.session_state.stroop_last_shown > _interval_s and not st.session_state.stroop_active:
    _show_stroop_modal()

# Show a subtle reminder when it's time for the next Stroop test
if not st.session_state.stroop_active:
    time_since_last = current_time - st.session_state.stroop_last_shown
    if time_since_last > _interval_s:
        # Show a small indicator that Stroop is ready
        st.info(f"🧠 Stroop test ready! (Last: {time_since_last:.0f}s ago)")
        # Auto-trigger on next interaction
        if st.button("Start Stroop Test", key="stroop_trigger"):
            _show_stroop_modal()
            st.rerun()


def _handle_stroop_key():
    value = st.session_state.get("stroop_key_input", "")
    if not value:
        return
    ch = value.strip()[-1:]
    if not ch.isdigit():
        return
    idx = int(ch) - 1
    names = list(COLORS.keys())
    if 0 <= idx < len(names):
        chosen = names[idx]
        st.session_state.stroop_selected = chosen
        st.session_state.stroop_correct = (
            chosen == st.session_state.stroop_trial["correct"]  # type: ignore[index]
        )
        st.session_state["stroop_key_input"] = ""
        st.session_state.stroop_active = False
        st.rerun()


# Render Stroop modal overlay (server-side)
if st.session_state.stroop_active and st.session_state.stroop_trial:
    # Hide default close button so users must answer
    st.markdown(
        """
        <style>
        div[role="dialog"] button[aria-label="Close"],
        div[role="dialog"] [data-testid="stDialogCloseButton"],
        div[role="dialog"] svg[aria-label="close"] { display: none !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    trial = st.session_state.stroop_trial
    _dialog_fn = getattr(st, "dialog", None)

    def _render_body():
        st.write("Select the color of the text, not the word's meaning.")
        st.text_input(
            "Press number key",
            key="stroop_key_input",
            label_visibility="collapsed",
            placeholder="Press 1-9",
            on_change=_handle_stroop_key,
        )
        st.markdown(
            f"<div style='text-align:center; font-size: 44px; font-weight: 900; color: {trial['color_hex']}; padding: 16px 0;'>"
            f"{trial['word']}"
            f"</div>",
            unsafe_allow_html=True,
        )
        names = list(COLORS.keys())
        cols = st.columns(3)
        for idx, name in enumerate(names):
            with cols[idx % 3]:
                label = f"{idx+1}. {name}"
                if st.button(label, key=f"stroop_btn_{name}"):
                    st.session_state.stroop_selected = name
                    st.session_state.stroop_correct = (name == trial["correct"])  # type: ignore[index]
                    st.session_state.stroop_active = False
                    st.rerun()

    if callable(_dialog_fn):
        @_dialog_fn("Quick color naming task")
        def _dlg():
            _render_body()
        _dlg()
    else:
        with st.modal("Quick color naming task"):
            _render_body()

# ---------- Chat ----------

prompt = st.chat_input('Ask anything')

if prompt:
    st.session_state.chats.append({
        "role": "user",
        "content": prompt
    })

    assistant = openai.chat.completions.create(
        model=st.secrets["OPENAI_MODEL"],
        messages=[
            { "role" : "system","content":"You are an AI agent"},
            *st.session_state.chats,
            {"role": "user", "content": prompt}
        ]
    )

    st.session_state.chats.append({
        "role": "assistant",
        "content": assistant.choices[0].message.content
    })

for chat in st.session_state.chats:
    st.chat_message(chat['role']).markdown(chat['content'])



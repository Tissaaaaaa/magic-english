import json
import streamlit as st
from openai import OpenAI

# Page configurations
st.set_page_config(page_title="Magic English", page_icon="🪄", layout="centered")

# 隐藏右上角的菜单、GitHub 标识和顶部工具栏
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("🪄 Magic English")
st.caption("Grasp any word, idiom, or phrase through pure intuition and vivid mental pictures.")

# Model & API configuration
API_KEY = st.secrets["API_KEY"]
BASE_URL = st.secrets["BASE_URL"]
MODEL_NAME = "openai/gpt-oss-20b"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# User input field
user_input = st.text_input(
    "What do you want to explore?",
    placeholder="Enter a single word (e.g., bamboozle) or a phrase (e.g., hit the sack)"
)

if st.button("Cast the Magic ✨", use_container_width=True) and user_input.strip():
    words = user_input.strip().split()
    
    # Prompt customization based on input length
    # Prompt customization based on input length
    if len(words) == 1:
        sys_prompt = (
            "You are a native English mentor. Return ONLY a valid JSON object with: "
            "'simple_explanation' (use only elementary, high-frequency words; no complex grammar), "
            "'visual_metaphor' (create a single, concrete, cartoon-like real-world snapshot. "
            "No abstract poetry or complex symbols. Keep it under 15 simple words, easy for a 6-year-old to visualize), and "
            "'examples' (list of 2 short, natural spoken sentences)."
        )
        task_prompt = f"Explain the word '{user_input}'."
    else:
        sys_prompt = (
            "You are a native English mentor. Return ONLY a valid JSON object with: "
            "'simple_explanation' (clear explanation in simple English), "
            "'vibe_check' (the emotional nuance, tone, and social context of using it), and "
            "'examples' (list of 1-2 real-life dialogues or examples)."
        )
        task_prompt = f"Explain what the phrase '{user_input}' means and feels like."

    with st.spinner("Conjuring the mental picture..."):
        try:
            res = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": task_prompt}
                ],
                response_format={"type": "json_object"}
            )
            data = json.loads(res.choices[0].message.content)

            st.divider()
            st.markdown("### 💡 In Plain English")
            st.info(data.get("simple_explanation", ""))

            if "visual_metaphor" in data:
                st.markdown("### 🎨 Mental Picture")
                st.success(f"🎬 {data.get('visual_metaphor')}")

            if "vibe_check" in data:
                st.markdown("### 🎭 Vibe Check")
                st.warning(f"💬 {data.get('vibe_check')}")

            if "examples" in data and data["examples"]:
                st.markdown("### 🗣️ Everyday Examples")
                for ex in data["examples"]:
                    st.write(f"- {ex}")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

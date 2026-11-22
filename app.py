import os
import base64
import streamlit as st
from anthropic import Anthropic

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Design Critic",
    page_icon="🎨",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
    .main {
        background-color: #f7f8fc;
    }

    .title {
        font-size: 42px;
        font-weight: 800;
        color: #111827;
        text-align: center;
        margin-bottom: 8px;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .card {
        background: white;
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    .result {
        background: white;
        padding: 25px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        line-height: 1.7;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 12px;
        font-size: 16px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.markdown(
    '<div class="title">🎨 AI Design Critic</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload your design and get professional AI-powered feedback.'
    '</div>',
    unsafe_allow_html=True
)

# -----------------------------
# API KEY
# -----------------------------
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    st.error("Anthropic API key is not configured.")
    st.stop()

client = Anthropic(api_key=api_key)

# -----------------------------
# LAYOUT
# -----------------------------
left, right = st.columns([1, 1])

with left:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📤 Upload Your Design")

    uploaded_file = st.file_uploader(
        "Choose a design image",
        type=["png", "jpg", "jpeg", "webp"]
    )

    if uploaded_file:
        st.image(
            uploaded_file,
            caption="Your Design",
            use_container_width=True
        )

    analyze = st.button(
        "✨ Analyze Design",
        type="primary"
    )

    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# AI ANALYSIS
# -----------------------------
with right:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🤖 AI Design Feedback")

    if analyze:

        if not uploaded_file:
            st.warning("Please upload a design image first.")

        else:

            with st.spinner("AI is analyzing your design..."):

                try:
                    image_bytes = uploaded_file.getvalue()
                    image_base64 = base64.b64encode(
                        image_bytes
                    ).decode("utf-8")

                    media_type = uploaded_file.type

                    prompt = """
You are a professional graphic design critic.

Analyze the uploaded design and provide beginner-friendly,
professional feedback.

Evaluate these areas:

1. Overall Design
2. Layout & Composition
3. Typography
4. Color Combination
5. Visual Hierarchy
6. Spacing & Alignment
7. Branding
8. Readability
9. Strengths
10. Problems / Weak Areas
11. Specific Improvements
12. Overall Score out of 10

Be constructive and explain your suggestions clearly.
Do not just criticize. Tell the designer exactly how they
can improve the design.
"""

                    response = client.messages.create(
                        model="claude-sonnet-4-5",
                        max_tokens=1800,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image",
                                        "source": {
                                            "type": "base64",
                                            "media_type": media_type,
                                            "data": image_base64
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": prompt
                                    }
                                ]
                            }
                        ]
                    )

                    result = response.content[0].text

                    st.markdown(
                        '<div class="result">',
                        unsafe_allow_html=True
                    )

                    st.markdown(result)

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

    else:
        st.info(
            "Upload a poster, logo, flyer, banner, social media post "
            "or other graphic design and click Analyze Design."
        )

    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")

st.markdown(
    "<p style='text-align:center;color:#6b7280;'>"
    "AI Design Critic • Powered by Claude"
    "</p>",
    unsafe_allow_html=True
)

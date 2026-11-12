
import requests
import streamlit as st


# --------------------------------
# Configuration
# --------------------------------

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="ASUS Support AI",
    page_icon="💻",
    layout="wide"
)


# --------------------------------
# Warm Editorial Theme
# --------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600&display=swap');

:root {
    --cream: #F4F1EA;
    --forest: #24332B;
    --terracotta: #B56B4A;
    --beige: #E9E2D7;
    --border: #DED7CC;
    --muted: #766F65;
}

/* Main background */
.stApp {
    background-color: var(--cream);
    color: var(--forest);
    font-family: 'DM Sans', sans-serif;
}

/* Main content */
.block-container {
    max-width: 900px;
    padding-top: 3rem;
    padding-bottom: 2rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #EAE5DB;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2 {
    color: var(--forest);
    font-family: 'Playfair Display', serif;
}

/* Headings */
h1, h2, h3 {
    color: var(--forest);
    font-family: 'Playfair Display', serif;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: #ECE6DC;
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}

/* User message */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background-color: #E4DCD0;
}

/* Chat input */
[data-testid="stChatInput"] {
    background-color: #FAF8F4;
    border: 1px solid var(--border);
    border-radius: 16px;
}

/* Buttons */
.stButton > button {
    background-color: #E9E2D7;
    color: var(--forest);
    border: 1px solid var(--border);
    border-radius: 12px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background-color: #DCD1C2;
    color: var(--forest);
    border-color: var(--terracotta);
}

/* Accent divider */
hr {
    border-color: var(--border);
}

/* Captions */
.stCaption, [data-testid="stCaptionContainer"] {
    color: var(--muted);
}

/* Sources */
[data-testid="stExpander"] {
    background-color: #F8F5EF;
    border: 1px solid var(--border);
    border-radius: 12px;
}

/* Remove excessive top space */
header[data-testid="stHeader"] {
    background-color: transparent;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------
# Session State
# --------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# --------------------------------
# Sidebar
# --------------------------------

with st.sidebar:

    st.markdown(
        "<h1 style='font-size:30px;'>ASUS Support AI</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='color:#766F65;'>"
        "Your personal laptop troubleshooting assistant."
        "</p>",
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### What I can help with")

    st.markdown("""
    - Laptop troubleshooting
    - Battery and charging
    - Keyboard and touchpad
    - Wi-Fi and connectivity
    - Hardware and maintenance
    """)

    st.divider()

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

    st.markdown(
        "<p style='font-size:12px;color:#766F65;margin-top:20px;'>"
        "Powered by FastAPI · Groq · RAG"
        "</p>",
        unsafe_allow_html=True
    )


# --------------------------------
# Header
# --------------------------------

st.markdown(
    """
    <div style="text-align:center; padding:10px 0 25px 0;">
        <p style="color:#B56B4A; letter-spacing:3px;
                  font-size:12px; font-weight:600;">
            LAPTOP SUPPORT
        </p>
        <h1 style="font-size:46px; margin-bottom:8px;">
            Let's fix that.
        </h1>
        <p style="color:#766F65; font-size:16px;">
            Reliable answers, grounded in ASUS support documentation.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# --------------------------------
# Welcome Screen
# --------------------------------

if not st.session_state.messages:

    st.markdown(
        "<h3 style='text-align:center; font-size:23px;'>"
        "What seems to be the problem?"
        "</h3>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;color:#766F65;'>"
        "Choose a topic or describe your issue below."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Battery & charging",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Why is my ASUS laptop battery draining quickly?"
            )

        if st.button(
            "Keyboard & touchpad",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Why is my ASUS laptop keyboard backlight not working?"
            )

    with col2:
        if st.button(
            "Wi-Fi connectivity",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "My ASUS laptop is having Wi-Fi connectivity issues."
            )

        if st.button(
            "Performance & heating",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Why is my ASUS laptop overheating?"
            )


# --------------------------------
# Display Chat History
# --------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("sources"):

            with st.expander("Sources"):

                for source in message["sources"]:
                    st.write(f"• {source}")


# --------------------------------
# Chat Input
# --------------------------------

user_input = st.chat_input(
    "Describe your ASUS laptop issue..."
)

# Suggested question or typed question
prompt = user_input or st.session_state.pending_prompt

if prompt:

    st.session_state.pending_prompt = None

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):

        with st.spinner("Looking through ASUS documentation..."):

            try:

                response = requests.post(
                    API_URL,
                    json={"message": prompt},
                    timeout=120
                )

                response.raise_for_status()

                data = response.json()

                answer = data["reply"]
                sources = data.get("sources", [])

                st.markdown(answer)

                if sources:

                    with st.expander("Sources"):

                        for source in sources:
                            st.write(f"• {source}")

            except requests.exceptions.RequestException:

                answer = (
                    "I couldn't connect to the support service. "
                    "Please check whether the backend is running."
                )

                sources = []

                st.error(answer)

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })

    st.rerun()

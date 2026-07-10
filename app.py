import os
import streamlit as st

from video import extract_frames
from pipeline import generate_all_captions

# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="CineForge",
    page_icon="🎬",
    layout="wide",
)

# -------------------------------------------------
# Session State
# -------------------------------------------------

if "frame_paths" not in st.session_state:
    st.session_state.frame_paths = []

if "scene_memory" not in st.session_state:
    st.session_state.scene_memory = ""

if "captions" not in st.session_state:
    st.session_state.captions = {}

# -------------------------------------------------
# CSS
# -------------------------------------------------

st.markdown("""
<style>

html, body, [class*="css"]{
    background:#0E1117;
}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.hero{
    text-align:center;
    padding:25px;
    border-radius:18px;
    background:#161B22;
    border:1px solid #2D333B;
}

.hero h1{
    color:white;
    font-size:54px;
    margin-bottom:0;
}

.hero h3{
    color:#B3B3B3;
    margin-top:10px;
}

.hero p{
    color:#f4a623;
    font-size:18px;
    font-weight:600;
}

.card{
    background:#161B22;
    padding:20px;
    border-radius:15px;
    border:1px solid #2D333B;
    margin-bottom:15px;
}

.caption{
    background:#1D2430;
    padding:18px;
    border-radius:15px;
    border-left:6px solid #f4a623;
    margin-bottom:20px;
}

.caption h4{
    margin-bottom:10px;
    color:white;
}

.caption p{
    color:#DDDDDD;
    font-size:16px;
}

.section-title{
    font-size:28px;
    font-weight:700;
    margin-top:25px;
    margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HERO
# -------------------------------------------------

st.markdown("""
<div class="hero">

<h1>🎬 CineForge</h1>

<h3>Multi-Style Video Caption Generator</h3>

<p>Powered by Google Gemma 4</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# -------------------------------------------------
# Upload Section
# -------------------------------------------------

left, right = st.columns([3,1])

with left:

    uploaded_video = st.file_uploader(
        "Upload a Video",
        type=["mp4","mov","avi","mkv","webm"]
    )

with right:

    st.write("")
    st.write("")
    generate = st.button(
        "🚀 Generate Captions",
        use_container_width=True,
        type="primary"
    )

st.divider()

# -------------------------------------------------
# Backend Processing
# -------------------------------------------------

if generate:

    if uploaded_video is None:
        st.warning("Please upload a video first.")
        st.stop()

    try:

        os.makedirs("input", exist_ok=True)
        os.makedirs("frames", exist_ok=True)

        video_path = os.path.join(
            "input",
            uploaded_video.name,
        )

        with open(video_path, "wb") as f:
            f.write(uploaded_video.getbuffer())

        status = st.status(
            "🚀 Starting CineForge...",
            expanded=True,
        )

        # -----------------------------
        # Stage 1
        # -----------------------------

        status.write("✅ Video uploaded")

        # -----------------------------
        # Stage 2
        # -----------------------------

        status.write("🎬 Extracting representative frames...")

        frame_paths = extract_frames(
            video_path,
            output_dir="frames",
            num_frames=8,
        )

        st.session_state.frame_paths = frame_paths

        status.write(f"✅ {len(frame_paths)} frames extracted")

        # -----------------------------
        # Stage 3
        # -----------------------------

        status.write("🧠 Building Scene Memory with Gemma 4...")

        scene_memory, captions = generate_all_captions(frame_paths)

        st.session_state.scene_memory = scene_memory
        st.session_state.captions = captions

        status.write("✅ Scene understanding completed")

        # -----------------------------
        # Stage 4
        # -----------------------------

        status.write("✍ Generating four caption styles...")

        status.write("✅ Formal")
        status.write("✅ Sarcastic")
        status.write("✅ Tech Humor")
        status.write("✅ Casual Humor")

        status.update(
            label="🎉 Caption generation complete!",
            state="complete",
            expanded=False,
        )

        st.success("CineForge finished successfully!")

    except Exception as e:

        st.error("Something went wrong.")

        st.exception(e)

# -------------------------------------------------
# Results
# -------------------------------------------------

if st.session_state.frame_paths:

    st.markdown(
        "<div class='section-title'>🖼 Representative Frames</div>",
        unsafe_allow_html=True,
    )

    cols = st.columns(4)

    for i, frame in enumerate(st.session_state.frame_paths):

        with cols[i % 4]:

            st.image(
                frame,
                use_container_width=True,
                caption=f"Frame {i+1}",
            )

    st.divider()

if st.session_state.scene_memory:

    st.markdown(
        "<div class='section-title'>🧠 Scene Memory</div>",
        unsafe_allow_html=True,
    )

    st.code(
        st.session_state.scene_memory,
        language="text",
    )

    st.divider()

# -------------------------------------------------
# Caption Cards
# -------------------------------------------------

if st.session_state.captions:

    st.markdown(
        "<div class='section-title'>📝 Generated Captions</div>",
        unsafe_allow_html=True,
    )

    style_icons = {
        "formal": "🔵",
        "sarcastic": "🟣",
        "humorous_tech": "🟢",
        "humorous_non_tech": "🟠",
    }

    style_titles = {
        "formal": "Formal",
        "sarcastic": "Sarcastic",
        "humorous_tech": "Tech Humor",
        "humorous_non_tech": "Casual Humor",
    }

    for style, caption in st.session_state.captions.items():

        icon = style_icons.get(style, "📝")
        title = style_titles.get(style, style.replace("_", " ").title())

        st.markdown(
            f"""
            <div class="caption">

            <h4>{icon} {title}</h4>

            <p>{caption}</p>

            </div>
            """,
            unsafe_allow_html=True,
        )

# -------------------------------------------------
# Footer
# -------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center;padding:25px;color:#888;">
        <h4>🎬 CineForge</h4>
        <p>Grounded Multi-Style Video Captioning with Google Gemma 4</p>
        <p>Built for the AMD Developer Hackathon</p>
    </div>
    """,
    unsafe_allow_html=True,
)
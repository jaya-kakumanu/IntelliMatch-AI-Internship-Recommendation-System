

import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="IntelliMatch — Gen-Z Ultra v6",
    page_icon="💼",
    layout="wide",
)

def load_lottie(url, timeout=6):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200:
            return r.json()
    except:
        return None
    return None

LOTTIE_AI = "https://assets10.lottiefiles.com/packages/lf20_t24tpvcu.json"
lottie_ai = load_lottie(LOTTIE_AI)

st.markdown(
    """
    <style>
    /* -------------------- BASE BACKGROUND -------------------- */
    .stApp {
        background: linear-gradient(135deg, #f9fbff 0%, #fff4fb 45%, #fffdf5 100%);
        background-attachment: fixed;
    }

    /* -------------------- REMOVE ALL FOCUS RINGS -------------------- */
    *:focus { outline: none !important; box-shadow: none !important; }
    .stTextInput>div>div>input:focus,
    .stTextArea>div>textarea:focus,
    .stSelectbox>div>div:focus {
        outline: none !important;
        box-shadow: none !important;
        border-color: transparent !important;
    }

        /* ---------- TITLE SHINE (FAST: 3s) ---------- */
    @keyframes shine-fast {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    .shine-title {
        font-size: 44px !important;
        font-weight: 900 !important;
        font-family: "Segoe UI", Roboto, sans-serif !important;
        background: linear-gradient(90deg,
            #00eaff,   /* Electric Blue */
            #7f00ff,   /* Neon Purple */
            #ff3cac,   /* Cyber Pink */
            #ffdd00,   /* Race Yellow */
            #39ff14,   /* Neon Green */
            #005aff    /* Royal Electric Blue */
        );
        background-size: 400% 100%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine-fast 18s linear infinite;
        margin-bottom: 6px;
    }

    /* ---------- SECTION TITLE UNDERLINE ---------- */
    .section-title {
        font-size: 20px;
        font-weight: 800;
        color: #1b1b3a;
        margin-bottom: 10px;
    }
    .section-title:after {
        content: "";
        display: block;
        width: 72px;
        height: 6px;
        background: linear-gradient(90deg, #00eaff, #7f00ff, #ff3cac);
        border-radius: 6px;
    }

    /* ---------------------------------------------------------------------
       SIDEBAR — HYPER DEPTH (S1+ upgrade)
       --------------------------------------------------------------------- */
    [data-testid="stSidebar"] {
        position: relative;
        padding: 25px 20px !important;
        border-radius: 0 22px 22px 0;

        background: rgba(255,255,255,0.78);
        backdrop-filter: blur(22px) saturate(190%);
        border-right: 1px solid rgba(255,255,255,0.28);

        box-shadow:
            inset 0 12px 40px rgba(255,255,255,0.25),
            inset 0 -14px 40px rgba(0,0,0,0.06),
            inset 0 0 80px rgba(255,255,255,0.18),
            0 18px 55px rgba(0,0,0,0.12),
            0 40px 130px rgba(0,0,0,0.10);

        overflow: hidden;
    }

    /* Ambient Layer 1 — red/pink drift */
    [data-testid="stSidebar"]::before {
        content: "";
        position: absolute;
        inset: -40% -40% -40% -40%;
        background: radial-gradient(600px 350px at var(--gx,50%) var(--gy,50%),
            rgba(255,45,75,0.10),
            rgba(255,60,172,0.06),
            transparent 45%);
        pointer-events: none;
        transition: background-position 0.08s linear, opacity 0.25s ease;
        mix-blend-mode: screen;
    }

    /* Ambient Layer 2 — soft glass highlight */
    [data-testid="stSidebar"]::after {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 0 22px 22px 0;
        pointer-events: none;
        background: linear-gradient(90deg,
            rgba(255,255,255,0.28),
            transparent 30%,
            rgba(255,60,172,0.04));
        mix-blend-mode: overlay;
    }

    /* Sidebar Title: depth, no glow */
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-weight: 900 !important;
        color: #0c1222 !important;
        text-shadow:
            0 2px 3px rgba(0,0,0,0.28),
            0 4px 12px rgba(0,0,0,0.12),
            inset 0 1px 0 rgba(255,255,255,0.4);
        letter-spacing: 0.5px;
        margin-bottom: 6px !important;
    }

    /* -------------------- INPUT BOXES: GEN-Z RED GLOW -------------------- */
    .stTextInput>div>div>input,
    .stTextArea>div>textarea,
    .stSelectbox>div>div {
        border-radius: 14px !important;
        padding: 10px !important;
        border: 2px solid rgba(12,12,20,0.08) !important;
        background: rgba(255,255,255,0.94) !important;
        box-shadow: 0 18px 36px rgba(15,15,35,0.06);
        transition: transform 0.22s ease, box-shadow 0.28s ease, border 0.22s ease;
    }

    @keyframes red-ripple {
        0% { box-shadow: 0 0 0 0 rgba(255,45,75,0.22); }
        40% { box-shadow: 0 0 28px 12px rgba(255,0,120,0.18); }
        80% { box-shadow: 0 0 60px 18px rgba(255,60,172,0.15); }
        100% { box-shadow: 0 0 0 0 rgba(255,60,172,0); }
    }

    .stTextInput>div>div>input:hover,
    .stTextArea>div>textarea:hover,
    .stSelectbox>div:hover {
        animation: red-ripple 1.8s ease-out;
        transform: translateY(-3px);
        border-color: rgba(255,45,75,0.42) !important;
    }

    .stTextInput>div>div>input:focus,
    .stTextArea>div>textarea:focus {
        border: 2px solid rgb(255,45,75) !important;
        box-shadow: 0 32px 100px rgba(255,45,75,0.25) !important;
    }

    /* -------------------- BUTTON -------------------- */
    .stButton>button {
        background: linear-gradient(90deg,#ff2d4b,#ff3cac,#ff5e99);
        padding: 12px 26px;
        border-radius: 14px;
        color: white !important;
        font-weight: 800;
        font-size: 15px;
        box-shadow: 0 22px 60px rgba(255,0,120,0.20);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .stButton>button:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 40px 110px rgba(255,0,120,0.32);
    }

    /* -------------------- CARDS (deeper shadows) -------------------- */
    .genz-card {
        background: rgba(255,255,255,0.88);
        border-radius: 22px;
        padding: 22px;
        margin-bottom: 18px;
        backdrop-filter: blur(14px) saturate(150%);
        transition: transform 0.36s cubic-bezier(.2,.8,.2,1), box-shadow 0.36s, border-color 0.36s;
        border: 2px solid rgba(0,0,0,0.04);
        box-shadow: 0 36px 90px rgba(10,14,35,0.10);
    }
    .card-blue:hover   { border-color:#3bbdff; box-shadow:0 60px 180px rgba(59,189,255,0.22); transform:translateY(-18px) scale(1.03); }
    .card-pink:hover   { border-color:#ff3cac; box-shadow:0 60px 180px rgba(255,60,172,0.22); transform:translateY(-18px) scale(1.03); }
    .card-yellow:hover { border-color:#ffdd00; box-shadow:0 60px 180px rgba(255,221,0,0.20); transform:translateY(-18px) scale(1.03); }
    .card-green:hover  { border-color:#39ff14; box-shadow:0 60px 180px rgba(57,255,20,0.20); transform:translateY(-18px) scale(1.03); }

    .genz-text { color:#0a0f22; font-weight:700; margin:6px 0; }

    /* -------------------- DOWNLOAD BUTTON (glowing like cards) -------------------- */
    .stDownloadButton>button {
        background: linear-gradient(90deg,#ff2d4b,#ff3cac,#ff7aa0);
        padding: 14px 28px !important;
        border-radius: 16px !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        border: 0 none !important;
        box-shadow: 0 36px 90px rgba(255,0,120,0.26) !important;
        transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
        margin: 6px auto !important;
        display: block !important;
    }
    .stDownloadButton>button:hover {
        transform: translateY(-10px) scale(1.03) !important;
        box-shadow: 0 70px 200px rgba(255,0,120,0.36) !important;
        filter: saturate(1.06) brightness(1.02);
    }

    /* Ensure download button inside genz-card centers nicely */
    .genz-card .stDownloadButton { display:flex; justify-content:center; margin-top:10px; }

    /* Hide pre blocks */
    pre { display:none !important; }

    </style>

    <!-- ---------------- JS: Enhanced Ambient Drift ---------------- -->
    <script>
    (function(){
        const sb = document.querySelector('[data-testid="stSidebar"]');
        if(!sb) return;

        let lx=50, ly=50;
        function lerp(a,b,t){ return a+(b-a)*t; }

        sb.addEventListener('mousemove', e=>{
            const r = sb.getBoundingClientRect();
            const x = ((e.clientX - r.left) / r.width) * 100;
            const y = ((e.clientY - r.top) / r.height) * 100;

            lx = lerp(lx, x, 0.28);
            ly = lerp(ly, y, 0.28);

            requestAnimationFrame(()=>{
                sb.style.setProperty('--gx', lx + '%');
                sb.style.setProperty('--gy', ly + '%');
            });
        }, {passive:true});

        sb.addEventListener('mouseleave', ()=>{
            lx=50; ly=50;
            requestAnimationFrame(()=>{
                sb.style.setProperty('--gx', '50%');
                sb.style.setProperty('--gy', '50%');
            });
        });
    })();
    </script>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_csv():
    df = pd.read_csv("internship_dataset_cleaned_ready_for_training.csv")
    df.fillna("Not Available", inplace=True)
    if "combined_text" not in df.columns:
        df["combined_text"] = (
            df["profile"].astype(str) + " " +
            df["Skills"].astype(str) + " " +
            df["Education"].astype(str) + " " +
            df["Location"].astype(str) + " " +
            df["Mode"].astype(str)
        )
    return df

df = load_csv()

@st.cache_resource
def build_tfidf(df):
    tfidf = TfidfVectorizer(stop_words="english", max_features=25000)
    matrix = tfidf.fit_transform(df["combined_text"])
    return tfidf, matrix

tfidf, tfidf_matrix = build_tfidf(df)

def recommend(text, top_n=5):
    vec = tfidf.transform([text])
    sims = cosine_similarity(vec, tfidf_matrix).flatten()
    idx = sims.argsort()[-top_n:][::-1]
    recs = df.iloc[idx].copy()
    recs["Similarity_Score"] = sims[idx]
    return recs

c1, c2 = st.columns([3,1])
with c1:
    st.markdown("<div class='shine-title'>💼 IntelliMatch — AI Internship Recommendation System</div>", unsafe_allow_html=True)
    st.markdown("<div class='subhead'>Connecting Talent with Opportunity • Gen-Z Ultra v6</div>", unsafe_allow_html=True)

with c2:
    if lottie_ai:
        st_lottie(lottie_ai, height=150, key="lottie_v6")

st.write("---")

st.sidebar.header("🧍 Candidate Information")

name = st.sidebar.text_input("Name")
qualification = st.sidebar.text_input("Qualification (e.g., B.Tech)")
skills = st.sidebar.text_area("Your Key Skills", placeholder="python, sql, excel, ML")
role = st.sidebar.text_input("Preferred Role")
location = st.sidebar.text_input("Preferred Location or Remote")
mode = st.sidebar.selectbox("Preferred Mode", ["remote", "onsite", "hybrid"])

candidate_text = f"{qualification} skilled in {skills} seeking {role} internship in {location} mode {mode}"

if st.sidebar.button("🔍 Find Internships"):
    st.markdown("<div class='section-title'>Top Internship Matches</div>", unsafe_allow_html=True)

    if not skills.strip():
        st.warning("Please enter at least one skill.")
    else:
        recs = recommend(candidate_text, top_n=5)
        colors = ["card-blue", "card-pink", "card-yellow", "card-green"]

        for i, (_, r) in enumerate(recs.iterrows()):
            cls = colors[i % len(colors)]

            html = f"""
            <div class="genz-card {cls}">
                <h3 style="margin:0 0 6px 0;">{r['profile']} @ {r['company']}</h3>
                <div class="genz-text">📍 <b>Location:</b> {r['Location']} &nbsp;&nbsp; 💼 <b>Mode:</b> {r['Mode']} &nbsp;&nbsp; ⏱ <b>Duration:</b> {r['Duration']}</div>
                <div class="genz-text">🎯 <b>Skills:</b> {r['Skills']}</div>
                <div class="genz-text">📚 <b>Education:</b> {r['Education']}</div>
                <div class="genz-text">💰 <b>Stipend:</b> {r['Stipend']}</div>
                <div class="genz-text" style="margin-top:8px">📈 <b>Score:</b> {round(r['Similarity_Score'],3)}</div>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)

        csv = recs.to_csv(index=False).encode("utf-8")

        st.markdown("<div class='genz-card' style='display:flex;flex-direction:column;align-items:center;'>", unsafe_allow_html=True)
        st.download_button(
            label="📥 Download Recommendations (.csv)",
            data=csv,
            file_name="intellimatch_recommendations_v6.csv",
            mime="text/csv",
            key="download_recs_v6"
        )
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("Enter your details and click Find Internships to get personalized matches ✨")

st.write("---")
st.markdown("<div style='text-align:center;color:#666;'>IntelliMatch — Gen-Z Ultra v6 • Built by Jaya Kakumanu</div>", unsafe_allow_html=True)

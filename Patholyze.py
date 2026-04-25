import streamlit as st
import time
import base64
from io import BytesIO
from st_clickable_images import clickable_images

# ==========================================
# UI CUSTOMIZATION & COLORS (CSS)
# ==========================================
st.set_page_config(page_title="Patholyze Pipeline", layout="wide")

st.markdown("""
<style>
    /* 1. MAIN APP BACKGROUND COLOR */
    .stApp {
        background-color: #721165;
        background-image: linear-gradient(#721165, #ffffffa3);
    }

    /* 2. GENERAL TEXT COLOR */
    h1, h2, h3, p, span, div {
        color: #ffffff; 
    }

    /* 3. BUTTON STYLING (Size, Background, Border) */
    div[data-testid="stButton"] > button {
        background-color: #721165;    
        border: 1px solid #ffffff;
        border-radius: 12px;          
        height: 90px;                 
        transition: 0.3s;             
    }

    /* 4. BUTTON TEXT STYLING (Targets the text inside the button) */
    div[data-testid="stButton"] > button p {
        color: #ffffff !important;
        font-size: 24px !important;  
        font-weight: bold;
    }

    /* 5. BUTTON HOVER EFFECT */
    div[data-testid="stButton"] > button:hover {
        background-color: #430a3b;    
        border: 1px solid #ffffff;
    }
    
    div[data-testid="stButton"] > button:hover p {
        color: white !important;
    }

    /* 6. PROGRESS BAR COLOR */
    /* This colors the empty background track */
    .stProgress > div > div > div {
        background-color: rgb(51, 51, 51) !important; 
    }
    .stProgress > div > div > div > div {
        background-color: #ffffff !important; 
    }

    /* 7. CENTER THE POP-UP DIALOG SAFELY */
    div[data-testid="stModal"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    div[role="dialog"] {
        margin: auto !important; 
    }
    
    /* 8. Removes gap between image and button */
    [data-testid="stImage"] {
        margin-bottom: -15px; 
    }

    /* 9. IMAGE MOVEMENT */
    [data-testid="column"], [data-testid="stColumn"] {
        position: relative;
    }

    [data-testid="column"] iframe,
    [data-testid="stColumn"] iframe {
        transition: transform 0.3s ease !important;
    }

    [data-testid="column"]:hover iframe,
    [data-testid="stColumn"]:hover iframe {
        transform: translateY(-6px) scale(1.02) !important;
    }
</style>
""", unsafe_allow_html=True)


def get_image_as_base64(file_path):
    """Reads a local image file and converts it to a base64 string for clickable images."""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# --- SESSION STATE INITIALIZATION ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'selected_slide' not in st.session_state:
    st.session_state.selected_slide = None
if 'slide_theme' not in st.session_state:
    st.session_state.slide_theme = None
if 'extractor' not in st.session_state:
    st.session_state.extractor = None
if 'classifier' not in st.session_state:
    st.session_state.classifier = None
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False
if 'show_popup' not in st.session_state:
    st.session_state.show_popup = False

def set_step(step_num):
    st.session_state.step = step_num

def reset_app():
    st.session_state.step = 1
    st.session_state.selected_slide = None
    st.session_state.processing_complete = False
    st.session_state.show_popup = False


# --- POP-UP DIALOG FOR FINAL RESULT ---
@st.dialog("Final Result")
def show_result_popup(is_tumor):
    if is_tumor:
        st.markdown(
            """
            <div style="background-color:#ff4b4b;padding:40px;border-radius:10px;text-align:center;">
                <h1 style="color:white;font-size:50px;margin:0;">TUMOR</h1>
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="background-color:#00cc96;padding:40px;border-radius:10px;text-align:center;">
                <h1 style="color:white;font-size:50px;margin:0;">NORMAL</h1>
            </div>
            """, unsafe_allow_html=True
        )


# ==========================================
# MAIN APP HEADER
# ==========================================
col_logo, col_title = st.columns([1, 4], vertical_alignment="center")

with col_logo:
    st.image("patholyze_logo.png", use_container_width=True) 

with col_title:
    st.markdown("<h1 style='margin-top: -10px; font-size: 60px;'>Patholyze</h1>", unsafe_allow_html=True)

st.progress(st.session_state.step / 4) 
st.divider()

# ==========================================
# STEP 1: SLIDE SELECTION
# ==========================================
if st.session_state.step == 1:
    st.header("Step 1: Select a Whole Slide Image")
    
    col1, col2 = st.columns(2)
    
    img1_theme = ((245, 200, 220), (210, 150, 180))
    img2_theme = ((200, 220, 245), (150, 180, 210))
    img1_b64 = get_image_as_base64("TUMOR_C3L-03987-23.png")
    img2_b64 = get_image_as_base64("NORMAL_C3L-02164-26.png")

    square_img_style = {
        "cursor": "pointer", 
        "width": "100%", 
        "aspect-ratio": "1 / 1", 
        "object-fit": "cover", 
        "border-radius": "0px", 
        "border": "none"
    }
    
    with col1:
        
        click1 = clickable_images(
            [f"data:image/png;base64,{img1_b64}"],
            div_style={"display": "flex", "justify-content": "center"},
            img_style=square_img_style, 
            key="slide1"
        )
        if click1 > -1:
            st.session_state.selected_slide = "Slide 001"
            st.session_state.slide_theme = img1_theme
            set_step(2)
            st.rerun()
            
    with col2:
        
        click2 = clickable_images(
            [f"data:image/png;base64,{img2_b64}"],
            div_style={"display": "flex", "justify-content": "center"},
            img_style=square_img_style,
            key="slide2"
        )
        if click2 > -1:
            st.session_state.selected_slide = "Slide 002"
            st.session_state.slide_theme = img2_theme
            set_step(2)
            st.rerun()

# ==========================================
# STEP 2: FEATURE EXTRACTOR
# ==========================================
elif st.session_state.step == 2:
    st.header("Step 2: Choose Feature Extractor")
    st.write("") 
    
    if st.button("KimiaNet", use_container_width=True):
        st.session_state.extractor = "KimiaNet"
        set_step(3)
        st.rerun()
        
    if st.button("CTransPath", use_container_width=True):
        st.session_state.extractor = "CTransPath"
        set_step(3)
        st.rerun()
        
    if st.button("MobileNetV2", use_container_width=True):
        st.session_state.extractor = "MobileNetV2"
        set_step(3)
        st.rerun()

    st.divider()
    if st.button("Back to Slides"):
        set_step(1)
        st.rerun()

# ==========================================
# STEP 3: CLASSIFIER
# ==========================================
elif st.session_state.step == 3:
    st.header("Step 3: Choose MIL Classifier")
    st.write("") 
    
    if st.button("Attention MIL (AMIL) - Advanced", use_container_width=True):
        st.session_state.classifier = "Attention MIL (AMIL)"
        set_step(4)
        st.rerun()
        
    if st.button("Max-Pooling MIL - Baseline", use_container_width=True):
        st.session_state.classifier = "Max-Pooling MIL"
        set_step(4)
        st.rerun()

    st.divider()
    if st.button("Back to Extractors"):
        set_step(2)
        st.rerun()

# ==========================================
# STEP 4: PROCESSING & RESULTS
# ==========================================
elif st.session_state.step == 4:
    st.header("Running Pipeline")
    st.markdown(
        f"""
        <div style="background-color: #ffffff1c ; padding: 15px; border-radius: 8px; border-left: 5px solid #ffffff; margin-bottom: 20px;">
            <span style="color: white; font-size: 18px;"> {st.session_state.extractor} ➜ {st.session_state.classifier}</span>
        </div>
        """, unsafe_allow_html=True
    )
    
    image_placeholder = st.empty()
    status_text = st.empty()
    
    if "001" in st.session_state.selected_slide:
        raw_img_path = "TUMOR_C3L-03987-23.png"
        patched_img_path = "C3L-03987-23_patch_map.png"
    else:
        raw_img_path = "NORMAL_C3L-02164-26.png"
        patched_img_path = "C3L-02164-26_patch_map.png"

    # --- THE ANIMATION PHASE ---
    if not st.session_state.processing_complete:
        
        image_placeholder.image(raw_img_path, caption="Raw WSI", use_container_width=True)
        time.sleep(2)
        
        image_placeholder.image(patched_img_path, caption="WSI Patching", use_container_width=True)
        time.sleep(2)

        st.session_state.processing_complete = True
        st.session_state.show_popup = True
        st.rerun() 
        
    # --- THE COMPLETED PHASE ---
    if st.session_state.processing_complete:
        image_placeholder.image(patched_img_path, caption="WSI Patching", use_container_width=True)
        status_text.markdown("### ✔ Running Complete!")
                
        is_tumor = "001" in st.session_state.selected_slide

        if st.session_state.show_popup:
            show_result_popup(is_tumor)
            st.session_state.show_popup = False 
        
        if is_tumor:
            st.markdown(
                """
                <div style="background-color:#ff4b4b;padding:40px;border-radius:10px;text-align:center;margin-top:20px;">
                    <h1 style="color:white;font-size:50px;margin:0;">TUMOR</h1>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="background-color:#00cc96;padding:40px;border-radius:10px;text-align:center;margin-top:20px;">
                    <h1 style="color:white;font-size:50px;margin:0;">NORMAL</h1>
                </div>
                """, unsafe_allow_html=True
            )

        st.divider()
        if st.button("Process Another Slide", use_container_width=True):
            reset_app()
            st.rerun()

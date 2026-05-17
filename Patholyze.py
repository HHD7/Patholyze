import streamlit as st
import time
import base64
from io import BytesIO
from st_clickable_images import clickable_images

# ==========================================
# UI CUSTOMIZATION & COLORS (CSS)
# ==========================================
st.set_page_config(page_title="Patholyze Pipeline", layout="centered")

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

     /* 9. IMAGE MOVEMENT - only the hovered image moves */
    [data-testid="stColumn"] iframe,
    [data-testid="column"] iframe {
        transition: transform 0.3s ease !important;
    }

    [data-testid="stColumn"] iframe:hover,
    [data-testid="column"] iframe:hover {
        transform: translateY(-6px) scale(1.02) !important;
    }
    
</style>
""", unsafe_allow_html=True)


def get_image_as_base64(file_path):
    """Reads a local image file and converts it to a base64 string for clickable images."""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ==========================================
# SLIDES DATA
# ==========================================
slides = [
    {
        "id": "C3L-03987-23",
        "label": "TUMOR",
        "wsi": "TUMOR_C3L-03987-23.png",
        "patch": "C3L-03987-23_patch_map.png",
    },
    {
        "id": "C3L-02164-26",
        "label": "NORMAL",
        "wsi": "NORMAL_C3L-02164-26.png",
        "patch": "C3L-02164-26_patch_map.png",
    },
    {
        "id": "C3L-02219-26",
        "label": "NORMAL",
        "wsi": "NORMAL_C3L-02219-26_wsi.png",
        "patch": "NORMAL_C3L-02219-26_patch_grid.png",
    },
    {
        "id": "C3L-02350-26",
        "label": "NORMAL",
        "wsi": "NORMAL_C3L-02350-26_wsi.png",
        "patch": "NORMAL_C3L-02350-26_patch_grid.png",
    },
    {
        "id": "C3L-02508-24",
        "label": "NORMAL",
        "wsi": "NORMAL_C3L-02508-24_wsi.png",
        "patch": "NORMAL_C3L-02508-24_patch_grid.png",
    },
    {
        "id": "2f2e5477-42a4-4906-a943-bf7f80_D1_D1",
        "label": "TUMOR",
        "wsi": "TUMOR_2f2e5477-42a4-4906-a943-bf7f80_D1_D1_wsi.png",
        "patch": "TUMOR_2f2e5477-42a4-4906-a943-bf7f80_D1_D1_patch_grid.png",
    },
    {
        "id": "C3L-00001-21",
        "label": "TUMOR",
        "wsi": "TUMOR_C3L-00001-21_wsi.png",
        "patch": "TUMOR_C3L-00001-21_patch_grid.png",
    },
    {
        "id": "C3L-00094-26",
        "label": "NORMAL",
        "wsi": "NORMAL_C3L-00094-26_wsi",
        "patch": "NORMAL_C3L-00094-26_patch_grid.png",
    },
    {
        "id": "C3L-00083-21",
        "label": "TUMOR",
        "wsi": "TUMOR_C3L-00083-21_wsi.png",
        "patch": "TUMOR_C3L-00083-21_patch_grid.png",
    },
    {
        "id": "C3L-00093-21",
        "label": "TUMOR",
        "wsi": "TUMOR_C3L-00093-21_wsi.png",
        "patch": "TUMOR_C3L-00093-21_patch_grid.png",
    },
    {
        "id": "C3L-02164-27",
        "label": "NORMAL",
        "wsi": "NORMAL_C3L-02164-27.png",
        "patch": "C3L-02164-27_patch_map.png",
    },
    {
        "id": "C3L-00415-21",
        "label": "TUMOR",
        "wsi": "TUMOR_C3L-00415-21.png",
        "patch": "C3L-00415-21_patch_map.png",
    },
]


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
    st.markdown("<h1 style='margin-top: -10px; font-size: 60px;'>PATHOLYZE</h1>", unsafe_allow_html=True)

st.progress(st.session_state.step / 4) 
st.divider()

# ==========================================
# STEP 1: SLIDE SELECTION
# ==========================================
if st.session_state.step == 1:
    st.header("Step 1: Select a Whole Slide Image")

    square_img_style = {
        "cursor": "pointer",
        "width": "100%",
        "aspect-ratio": "1 / 1",
        "object-fit": "cover",
        "border-radius": "0px",
        "border": "none"
    }

    # Display slides in 3 columns
    cols = st.columns(3)

    for i, slide in enumerate(slides):
        with cols[i % 3]:
            img_b64 = get_image_as_base64(slide["wsi"])

            click = clickable_images(
                [f"data:image/png;base64,{img_b64}"],
                div_style={
                    "display": "flex",
                    "justify-content": "center",
                    "margin-bottom": "25px"
                },
                img_style=square_img_style,
                key=f"slide_{slide['id']}"
            )

            if click > -1:
                st.session_state.selected_slide = slide
                st.session_state.slide_theme = None
                st.session_state.processing_complete = False
                st.session_state.show_popup = False
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
    
    if st.button("Attention MIL (AMIL)", use_container_width=True):
        st.session_state.classifier = "Attention MIL (AMIL)"
        set_step(4)
        st.rerun()
        
    if st.button("Max-Pooling MIL", use_container_width=True):
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
    
    selected_slide = st.session_state.selected_slide

    raw_img_path = selected_slide["wsi"]
    patched_img_path = selected_slide["patch"]
    is_tumor = selected_slide["label"] == "TUMOR"

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

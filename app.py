import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURATION & DESIGN ---
st.set_page_config(page_title="Prompt Master 5*", page_icon="⭐", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stTextArea textarea { border-radius: 10px; border: 1px solid #ddd; }
    .stButton button { 
        width: 100%; border-radius: 15px; height: 3em; 
        background: linear-gradient(90deg, #FF4B4B 0%, #FF8F8F 100%);
        color: white; border: none; font-weight: bold;
    }
    .result-box { 
        padding: 20px; border-radius: 15px; background-color: white; 
        border: 1px solid #ff4b4b; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🚀 Prompt Optimizer 5-Stars")
st.caption("L'expertise technique pour transformer vos idées en prompts de production.")
st.markdown("---")

# --- GESTION API (Sidebar) ---
with st.sidebar:
    st.header("🔑 Configuration")
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("Clé API chargée depuis les Secrets.")
    else:
        api_key = st.text_input("Entrez votre clé API Google :", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        @st.cache_resource
        def get_working_model():
            try:
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                for m in models:
                    if 'gemini-1.5-flash' in m: return m
                return models[0] if models else "gemini-1.5-flash"
            except:
                return "gemini-1.5-flash"

        model_id = get_working_model()
        model = genai.GenerativeModel(model_id)

        # --- LAYOUT PRINCIPAL ---
        col_left, col_right = st.columns([1, 1], gap="large")

        with col_left:
            st.subheader("📝 Votre demande")
            user_input = st.text_area(
                "Saisissez votre base :", 
                placeholder="Ex: Écris un script de vidéo YouTube sur les chats...",
                height=200
            )
            launch_btn = st.button("✨ Générer le Prompt 5 Étoiles")

        with col_right:
            st.subheader("🏆 Résultat Optimisé")
            if launch_btn:
                if not user_input:
                    st.warning("Veuillez saisir une demande.")
                else:
                    # --- TA LOGIQUE DE BOUCLE ORIGINALE ---
                    current_prompt = user_input
                    score = 0
                    iteration = 1
                    
                    with st.status("🔄 Travail de l'expert en cours...", expanded=True) as status:
                        while score < 5 and iteration <= 3:
                            st.write(f"**Itération {iteration}/3**")
                            
                            instruction = f"""
                            Tu es un expert mondial en Prompt Engineering. Ton but est de transformer une demande simple en un prompt complexe et parfait.
                            
                            DEMANDE ACTUELLE : {current_prompt}
                            
                            TACHE :
                            1. Analyse le prompt : manque-t-il un rôle, un contexte, des étapes ou un format de sortie ?
                            2. Réécris une version largement améliorée, ultra-précise et professionnelle.
                            3. Attribue une note de 1 à 5 à ta nouvelle version (5 étant parfait).
                            
                            FORMAT DE RÉPONSE STRICT (NE RÉPONDS RIEN D'AUTRE) :
                            NOTE: [Chiffre entre 1 et 5]
                            PROMPT: [Ton prompt optimisé ici]
                            """
                            
                            try:
                                response = model.generate_content(instruction)
                                output = response.text
                                
                                # Extraction exacte comme ton code initial
                                if "NOTE:" in output:
                                    score_str = output.split("NOTE:")[1].split("\n")[0].strip()
                                    score = int(''.join(filter(str.isdigit, score_str)) or 0)
                                
                                if "PROMPT:" in output:
                                    current_prompt = output.split("PROMPT:")[1].strip()
                                
                                st.write(f"Qualité obtenue : {score}/5")
                                iteration += 1
                            except Exception as e:
                                st.error(f"Erreur : {e}")
                                break
                        
                        status.update(label="✅ Optimisation terminée !", state="complete")

                    # Affichage final dans le style pro
                    st.markdown(f"**Score final : {score}/5**")
                    st.code(current_prompt, language="markdown")
                    st.balloons()
            else:
                st.info("Le prompt optimisé s'affichera ici après traitement.")

    except Exception as e:
        st.error(f"Erreur de configuration : {e}")
else:
    st.info("👋 Veuillez configurer votre clé API dans la barre latérale pour commencer.")

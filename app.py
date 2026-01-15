import streamlit as st
import google.generativeai as genai
import json
import os

st.set_page_config(page_title="Prompt Master 5*", page_icon="⭐")
st.title("🚀 Prompt Optimizer 5-Stars")

# --- SAUVEGARDE ---
SAVE_FILE = "prompts_db.json"
def load_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f: return json.load(f)
        except: return []
    return []

def save_data(data):
    with open(SAVE_FILE, "w") as f: json.dump(data, f)

if "history" not in st.session_state:
    st.session_state.history = load_data()

# --- BARRE LATÉRALE ---
st.sidebar.header("🗂️ Historique")
for i, item in enumerate(st.session_state.history):
    col1, col2 = st.sidebar.columns([4, 1])
    if col1.button(f"📄 {item['name']}", key=f"h_{i}"):
        st.session_state.display_prompt = item['content']
    if col2.button("🗑️", key=f"d_{i}"):
        st.session_state.history.pop(i)
        save_data(st.session_state.history)
        st.rerun()

# --- CLÉ API ---
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Clé API Google", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # --- CORRECTION 404 ICI ---
        # On essaie de trouver le nom exact accepté par Google
        @st.cache_resource
        def get_working_model_name():
            try:
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                for m in models:
                    if 'gemini-1.5-flash' in m: return m
                return "models/gemini-1.5-flash"
            except:
                return "models/gemini-1.5-flash"

        model = genai.GenerativeModel(get_working_model_name())

        user_input = st.text_area("Quelle est votre demande de base ?", placeholder="Ex: Aide moi à préparer ma défense au tribunal")

        if st.button("Générer le Prompt Parfait"):
            if not user_input:
                st.error("Veuillez entrer une demande !")
            else:
                status_text = st.empty()
                current_prompt = user_input
                score = 0
                iteration = 1
                
                while score < 5 and iteration <= 3:
                    status_text.info(f"🔄 Itération {iteration} : Analyse en cours...")
                    
                    instruction = f"""
                    Tu es un expert en Prompt Engineering. 
                    Demande actuelle : {current_prompt}
                    
                    Tâche :
                    1. Améliore ce prompt pour qu'il soit parfait (Précis, expert, structuré).
                    2. Donne une note de 1 à 5.
                    
                    Format STRICT :
                    NOTE: [Chiffre]
                    PROMPT: [Ton prompt optimisé]
                    """
                    
                    response = model.generate_content(instruction)
                    output = response.text
                    
                    if "NOTE:" in output:
                        score_part = output.split("NOTE:")[1].split("\n")[0].strip()
                        score = int(''.join(filter(str.isdigit, score_part)) or 0)
                    
                    if "PROMPT:" in output:
                        current_prompt = output.split("PROMPT:")[1].strip()
                    
                    iteration += 1
                
                st.session_state.history.append({"name": user_input[:20]+"...", "content": current_prompt})
                save_data(st.session_state.history)
                
                status_text.success("✅ Terminé !")
                st.session_state.display_prompt = current_prompt

        if "display_prompt" in st.session_state:
            st.subheader("🏆 Votre Prompt 5 Étoiles :")
            st.code(st.session_state.display_prompt, language="markdown")
                
    except Exception as e:
        st.error(f"Erreur de modèle : {e}")
else:
    st.warning("👈 Entrez votre clé API.")

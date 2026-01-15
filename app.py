import streamlit as st
import google.generativeai as genai
import json
import os

# 1. Page
st.set_page_config(page_title="Prompt Master 5*", page_icon="⭐")
st.title("🚀 Prompt Optimizer 5-Stars")

# 2. Sauvegarde (Fichier JSON)
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

# 3. Barre latérale (Historique)
st.sidebar.header("🗂️ Historique")
for i, item in enumerate(st.session_state.history):
    if st.sidebar.button(f"📄 {item['name']}", key=f"h_{i}"):
        st.session_state.display_prompt = item['content']

# 4. API & Modèle
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Clé API Google", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Utilisation du nom de modèle le plus stable pour éviter la 404
        model = genai.GenerativeModel('models/gemini-1.5-flash')

        user_input = st.text_area("Quelle est votre demande de base ?", placeholder="Ex: Aide moi à vendre un vélo")

        if st.button("Générer le Prompt Parfait"):
            if not user_input:
                st.error("Veuillez entrer une demande !")
            else:
                status_text = st.empty()
                current_prompt = user_input
                score = 0
                iteration = 1
                
                while score < 5 and iteration <= 3:
                    status_text.info(f"🔄 Itération {iteration} : Analyse et critique en cours...")
                    
                    instruction = f"""
                    Tu es un expert en Prompt Engineering. 
                    Demande actuelle : {current_prompt}
                    
                    Tâche :
                    1. Améliore ce prompt pour qu'il soit parfait.
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
                
                # Sauvegarde auto dans l'historique
                st.session_state.history.append({"name": user_input[:20]+"...", "content": current_prompt})
                save_data(st.session_state.history)
                
                status_text.success("✅ Terminé !")
                st.session_state.display_prompt = current_prompt

        # Affichage du résultat
        if "display_prompt" in st.session_state:
            st.subheader("🏆 Votre Prompt 5 Étoiles :")
            st.code(st.session_state.display_prompt, language="markdown")
                
    except Exception as e:
        st.error(f"Détail de l'erreur : {e}")
else:
    st.warning("👈 Entrez votre clé API.")

import streamlit as st
import google.generativeai as genai
import json
import os

# Configuration
st.set_page_config(page_title="Prompt Master Pro", page_icon="🚀", layout="wide")

# --- BASE DE DONNÉES LOCALE ---
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

# --- CONFIGURATION API ---
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("🔑 Clé API", type="password")

# --- BARRE LATÉRALE ---
st.sidebar.title("🗂️ Bibliothèque")
for i, item in enumerate(st.session_state.history):
    col1, col2 = st.sidebar.columns([4, 1])
    if col1.button(f"📄 {item['name']}", key=f"btn_{i}"):
        st.session_state.current_prompt = item['content']
        st.session_state.current_name = item['name']
    if col2.button("🗑️", key=f"del_{i}"):
        st.session_state.history.pop(i)
        save_data(st.session_state.history)
        st.rerun()

# --- CORPS DE L'APP ---
st.title("🚀 Prompt Optimizer 5-Stars")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        @st.cache_resource
        def get_model():
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            for m in models:
                if 'gemini-1.5-flash' in m: return m
            return models[0] if models else "gemini-1.5-flash"

        model = genai.GenerativeModel(get_model())

        user_input = st.text_area("✍️ Votre demande :", placeholder="Ex: Écris une méthode pour apprendre l'italien...")
        
        if st.button("✨ Lancer l'Optimisation"):
            if user_input:
                current_p = user_input
                score = 0
                iteration = 1
                
                # REVOICI L'ANIMATION ET LA RÉFLEXION
                with st.status("🧠 Analyse et optimisation en cours...", expanded=True) as status:
                    while score < 5 and iteration <= 3:
                        st.write(f"🔄 **Itération {iteration}** : Recherche du niveau 5 étoiles...")
                        
                        prompt_expert = f"""
                        Tu es un expert en Prompt Engineering. 
                        Demande de base : {current_p}
                        
                        TACHE :
                        1. Crée un prompt parfait (Rôle, Contexte, Contraintes, Format).
                        2. Donne une NOTE de 1 à 5.
                        
                        FORMAT : 
                        NOTE: [chiffre]
                        PROMPT: [ton prompt]
                        """
                        
                        resp = model.generate_content(prompt_expert).text
                        
                        if "NOTE:" in resp:
                            score_text = resp.split("NOTE:")[1].split("\n")[0].strip()
                            score = int(''.join(filter(str.isdigit, score_text)) or 0)
                        if "PROMPT:" in resp:
                            current_p = resp.split("PROMPT:")[1].strip()
                        
                        iteration += 1
                    
                    # SAUVEGARDE
                    new_entry = {"name": user_input[:20] + "...", "content": current_p}
                    st.session_state.history.append(new_entry)
                    save_data(st.session_state.history)
                    st.session_state.current_prompt = current_p
                    st.session_state.current_name = new_entry["name"]
                    status.update(label="✅ Optimisation terminée !", state="complete")
                st.balloons()

        if "current_prompt" in st.session_state:
            st.markdown("---")
            c_name, c_save = st.columns([3, 1])
            new_n = c_name.text_input("🏷️ Nommer ce prompt :", value=st.session_state.get("current_name", ""))
            if c_save.button("💾 Sauver le nom"):
                for entry in st.session_state.history:
                    if entry['content'] == st.session_state.current_prompt:
                        entry['name'] = new_n
                save_data(st.session_state.history)
                st.rerun()

            st.subheader("🏆 Résultat final :")
            st.code(st.session_state.current_prompt, language="markdown")

    except Exception as e:
        st.error(f"Erreur : {e}")

import streamlit as st
import google.generativeai as genai
import json
import os

# Configuration de la page
st.set_page_config(page_title="Prompt Master Pro", page_icon="🗂️", layout="wide")

# --- GESTION DE LA BASE DE DONNÉES LOCALE ---
SAVE_FILE = "prompts_db.json"

def load_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

# Initialisation de l'historique dans la session
if "history" not in st.session_state:
    st.session_state.history = load_data()

# --- CONFIGURATION API ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 Clé API", type="password")

# --- BARRE LATÉRALE : HISTORIQUE ---
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

# --- CORPS DE L'APPLICATION ---
st.title("🚀 Prompt Optimizer Pro")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Détection automatique du modèle pour éviter l'erreur 404
        @st.cache_resource
        def get_best_model():
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            for m in models:
                if 'gemini-1.5-flash' in m: return m
            return models[0] if models else None

        model_name = get_best_model()
        model = genai.GenerativeModel(model_name)

        user_input = st.text_area("✍️ Votre demande :", height=100, placeholder="Entrez votre idée ici...")
        
        if st.button("✨ Optimiser et Sauvegarder"):
            if user_input:
                with st.status("🚀 Optimisation en cours...") as status:
                    instruction = f"Tu es un expert en prompt engineering. Optimise la demande suivante pour obtenir le meilleur résultat possible. Réponds strictement sous la forme : PROMPT: [ton texte]"
                    response = model.generate_content(f"{instruction}\n\nDemande : {user_input}")
                    
                    if "PROMPT:" in response.text:
                        optimized = response.text.split("PROMPT:")[1].strip()
                    else:
                        optimized = response.text
                    
                    # Ajout à l'historique
                    new_entry = {
                        "name": user_input[:25] + "...", 
                        "content": optimized
                    }
                    st.session_state.history.append(new_entry)
                    save_data(st.session_state.history)
                    st.session_state.current_prompt = optimized
                    st.session_state.current_name = new_entry["name"]
                    status.update(label="✅ Optimisé et Sauvegardé !", state="complete")

        if "current_prompt" in st.session_state:
            st.markdown("---")
            # Zone pour renommer
            col_name, col_btn = st.columns([3, 1])
            new_name = col_name.text_input("🏷️ Nom du prompt :", value=st.session_state.get("current_name", ""))
            if col_btn.button("💾 Renommer"):
                for item in st.session_state.history:
                    if item['content'] == st.session_state.current_prompt:
                        item['name'] = new_name
                save_data(st.session_state.history)
                st.rerun()

            st.subheader("🏆 Prompt Optimisé :")
            st.code(st.session_state.current_prompt, language="markdown")

    except Exception as e:
        st.error(f"Erreur technique : {e}")
else:
    st.info("Veuillez configurer votre clé API pour commencer.")

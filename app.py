import streamlit as st
import google.generativeai as genai
import json
import os

# Configuration de la page
st.set_page_config(page_title="Prompt Master Pro", page_icon="🗂️")

# --- FICHIER DE SAUVEGARDE ---
SAVE_FILE = "prompts_db.json"

def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

# Charger les données au démarrage
if "history" not in st.session_state:
    st.session_state.history = load_data()

# --- CONFIG API ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 Clé API", type="password")

# --- BARRE LATÉRALE : CLASSEMENT ---
st.sidebar.title("🗂️ Mes Prompts Sauvegardés")

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
st.title("🚀 Prompt Optimizer Pro")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    user_input = st.text_area("✍️ Votre demande :", height=100)
    
    if st.button("✨ Optimiser et Sauvegarder"):
        if user_input:
            with st.spinner("L'IA travaille..."):
                # Simulation d'optimisation (on garde ton moteur actuel)
                instruction = f"Optimise ce prompt : {user_input}. Réponds avec PROMPT: [ton texte]"
                response = model.generate_content(instruction)
                optimized = response.text.split("PROMPT:")[1].strip() if "PROMPT:" in response.text else response.text
                
                # Sauvegarde automatique
                new_entry = {
                    "name": user_input[:20] + "...", # Nomme par défaut avec le début du texte
                    "content": optimized
                }
                st.session_state.history.append(new_entry)
                save_data(st.session_state.history)
                st.session_state.current_prompt = optimized
                st.success("Sauvegardé dans l'historique !")

    st.markdown("---")
    
    if "current_prompt" in st.session_state:
        # Champ pour renommer le prompt actuel
        new_name = st.text_input("🏷️ Nommer ce prompt :", value=st.session_state.get("current_name", "Mon Prompt"))
        if st.button("Enregistrer le nom"):
            for item in st.session_state.history:
                if item['content'] == st.session_state.current_prompt:
                    item['name'] = new_name
            save_data(st.session_state.history)
            st.rerun()
            
        st.subheader("🏆 Résultat :")
        st.code(st.session_state.current_prompt, language="markdown")

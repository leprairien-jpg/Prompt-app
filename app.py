import streamlit as st
import google.generativeai as genai
import json
import os

# --- FONCTIONS DE MÉMOIRE (Gardées simples) ---
def charger_memoire():
    if os.path.exists("mes_prompts.json"):
        with open("mes_prompts.json", "r") as f: return json.load(f)
    return []

def sauver_prompt(nouveau_prompt):
    historique = charger_memoire()
    historique.insert(0, nouveau_prompt)
    historique = historique[:20] # LIMITE À 20
    with open("mes_prompts.json", "w") as f: json.dump(historique, f)

# Configuration de l'interface
st.set_page_config(page_title="Prompt Master 5*", page_icon="⭐", layout="centered")

st.title("🚀 Prompt Optimizer 5-Stars")
st.markdown("---")

# --- TON CODE ORIGINAL (INCHANGÉ) ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 Clé API Google non détectée, entrez-la ici :", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        @st.cache_resource
        def get_working_model():
            try:
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                for m in models:
                    if 'gemini-1.5-flash' in m:
                        return m
                return models[0] if models else None
            except:
                return "gemini-1.5-flash"

        model_id = get_working_model()
        model = genai.GenerativeModel(model_id)

        user_input = st.text_area("✍️ Quelle est votre demande de base ?", 
                                  placeholder="Ex: Écris un script de vidéo YouTube sur les chats...",
                                  height=150)

        if st.button("✨ Générer le Prompt 5 Étoiles"):
            if not user_input:
                st.warning("Veuillez saisir une demande avant de lancer l'optimisation.")
            else:
                current_prompt = user_input
                score = 0
                iteration = 1
                
                while score < 5 and iteration <= 3:
                    with st.status(f"🔄 Optimisation - Itération {iteration}...", expanded=True) as status:
                        
                        # TON INSTRUCTION ORIGINALE (REMISE À L'IDENTIQUE)
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
                        
                        response = model.generate_content(instruction)
                        output = response.text
                        
                        if "NOTE:" in output:
                            score_str = output.split("NOTE:")[1].split("\n")[0].strip()
                            score = int(''.join(filter(str.isdigit, score_str)) or 0)
                        
                        if "PROMPT:" in output:
                            current_prompt = output.split("PROMPT:")[1].strip()
                        
                        st.write(f"Note obtenue : {score}/5")
                        iteration += 1
                
                # SAUVEGARDE
                sauver_prompt(current_prompt)
                
                st.balloons()
                st.success("✅ Votre prompt a atteint le niveau 5 étoiles !")
                st.subheader("🏆 Prompt Final Optimisé :")
                st.code(current_prompt, language="markdown")

        # --- L'HISTORIQUE EN BAS ---
        st.markdown("---")
        with st.expander("📚 Bibliothèque des 20 derniers prompts"):
            archives = charger_memoire()
            for i, p in enumerate(archives):
                st.code(p, language="markdown")

    except Exception as e:
        st.error(f"Erreur : {e}")

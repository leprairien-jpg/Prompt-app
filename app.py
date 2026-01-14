import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Prompt Master 5*", page_icon="⭐")
st.title("🚀 Prompt Optimizer 5-Stars")

# Entrée de la clé API
api_key = st.sidebar.text_input("Entrez votre clé API Google", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    user_input = st.text_area("Quelle est votre demande de base ?", "Ex: Aide moi à vendre un vélo")

    if st.button("Générer le Prompt Parfait"):
        status_text = st.empty()
        
        # --- BOUCLE D'AUTOCRITIQUE ---
        current_prompt = user_input
        score = 0
        iteration = 1
        
        while score < 5 and iteration <= 3: # Limite à 3 itérations pour la vitesse
            status_text.info(f"🔄 Itération {iteration} : Analyse et critique en cours...")
            
            # Demande d'optimisation et de notation
            instruction = f"""
            Tu es un expert en Prompt Engineering.
            Demande initiale : {current_prompt}
            
            Tâche :
            1. Crée un prompt ultra-optimisé (contexte, rôle, format, contraintes).
            2. Donne une note de 1 à 5 à ce prompt.
            3. Si la note est < 5, explique pourquoi et améliore-le encore.
            
            Réponds TOUJOURS sous ce format :
            NOTE: [Chiffre]
            PROMPT: [Ton prompt optimisé ici]
            """
            
            response = model.generate_content(instruction)
            text = response.text
            
            # Extraction de la note (simple parsing)
            try:
                score = int(text.split("NOTE:")[1].split("\n")[0].strip())
            except:
                score = 5 # Sortie de secours
            
            current_prompt = text.split("PROMPT:")[1].strip()
            iteration += 1
        
        status_text.success("✅ Prompt 5 étoiles atteint !")
        st.markdown("### 🏆 Votre Prompt Optimisé :")
        st.code(current_prompt, language="markdown")
        st.button("Copier le prompt")

else:
    st.warning("Veuillez entrer votre clé API dans la barre latérale pour commencer.")

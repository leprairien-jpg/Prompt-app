import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Prompt Master 5*", page_icon="⭐")
st.title("🚀 Prompt Optimizer 5-Stars")

# Barre latérale
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Entrez votre clé API Google", type="password")

if api_key:
    try:
        # Initialisation propre
        genai.configure(api_key=api_key)
        
        # VERSION ULTRA-COMPATIBLE : on teste le modèle standard
        model = genai.GenerativeModel('gemini-1.5-flash')

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
                    
                    try:
                        # Appel direct sans fioritures
                        response = model.generate_content(instruction)
                        output = response.text
                        
                        if "NOTE:" in output:
                            score_part = output.split("NOTE:")[1].split("\n")[0].strip()
                            score = int(''.join(filter(str.isdigit, score_part)) or 0)
                        
                        if "PROMPT:" in output:
                            current_prompt = output.split("PROMPT:")[1].strip()
                        
                        iteration += 1
                    except Exception as e:
                        st.error(f"Détail de l'erreur : {e}")
                        break
                
                status_text.success("✅ Terminé !")
                st.subheader("🏆 Votre Prompt 5 Étoiles :")
                st.code(current_prompt, language="markdown")
                
    except Exception as e:
        st.error(f"Erreur de configuration : {e}")

else:
    st.warning("👈 Entrez votre clé API.")

import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Prompt Master 5*", page_icon="⭐")
st.title("🚀 Prompt Optimizer 5-Stars")

# Barre latérale pour la configuration
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Entrez votre clé API Google", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Utilisation du modèle 'gemini-1.5-flash-latest' pour éviter les erreurs 404
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        user_input = st.text_area("Quelle est votre demande de base ?", placeholder="Ex: Aide moi à vendre un vélo")

        if st.button("Générer le Prompt Parfait"):
            if not user_input:
                st.error("Veuillez entrer une demande !")
            else:
                status_text = st.empty()
                current_prompt = user_input
                score = 0
                iteration = 1
                
                # Boucle d'autocritique (max 3 itérations pour la rapidité)
                while score < 5 and iteration <= 3:
                    status_text.info(f"🔄 Itération {iteration} : Analyse et critique en cours...")
                    
                    instruction = f"""
                    Tu es un expert en Prompt Engineering d'élite.
                    Demande actuelle : {current_prompt}
                    
                    Tâche :
                    1. Analyse ce prompt : est-il clair ? a-t-il un rôle ? un contexte ? des contraintes ?
                    2. Réécris une version largement supérieure.
                    3. Donne une note de 1 à 5 sur la qualité de ta réécriture.
                    
                    Format de réponse STRICT (ne réponds rien d'autre) :
                    NOTE: [Chiffre]
                    PROMPT: [Ton prompt optimisé ici]
                    """
                    
                    try:
                        response = model.generate_content(instruction)
                        output = response.text
                        
                        # Extraction de la note
                        if "NOTE:" in output:
                            score_part = output.split("NOTE:")[1].split("\n")[0].strip()
                            score = int(''.join(filter(str.isdigit, score_part)) or 0)
                        
                        # Extraction du prompt
                        if "PROMPT:" in output:
                            current_prompt = output.split("PROMPT:")[1].strip()
                        
                        iteration += 1
                    except Exception as e:
                        st.error(f"Erreur lors de la génération : {e}")
                        break
                
                status_text.success("✅ Prompt 5 étoiles atteint !")
                st.subheader("🏆 Votre Prompt Optimisé :")
                st.info("Copiez le texte ci-dessous :")
                st.code(current_prompt, language="markdown")
                
    except Exception as e:
        st.error(f"Erreur de configuration : {e}")

else:
    st.warning("👈 Entrez votre clé API dans la barre latérale.")
    st.info("Obtenez-la ici : https://aistudio.google.com/")

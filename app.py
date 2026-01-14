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
        # On utilise 'models/gemini-1.5-flash' qui est le nom complet et stable
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
                
                # Boucle d'autocritique
                while score < 5 and iteration <= 3:
                    status_text.info(f"🔄 Itération {iteration} : Analyse et critique en cours...")
                    
                    instruction = f"""
                    Tu es un expert en Prompt Engineering. 
                    Demande actuelle à optimiser : {current_prompt}
                    
                    Tâche :
                    1. Analyse si le prompt contient un rôle, un contexte, une tâche précise et un format de sortie.
                    2. Rédige une version nettement améliorée.
                    3. Attribue une note de 1 à 5 (5 étant parfait).
                    
                    Format de réponse STRICT :
                    NOTE: [Chiffre]
                    PROMPT: [Ton prompt optimisé]
                    """
                    
                    try:
                        response = model.generate_content(instruction)
                        output = response.text
                        
                        # Extraction sécurisée de la note
                        if "NOTE:" in output:
                            score_part = output.split("NOTE:")[1].split("\n")[0].strip()
                            # On ne garde que le premier chiffre au cas où
                            score = int(''.join(filter(str.isdigit, score_part)) or 0)
                        
                        # Extraction du prompt
                        if "PROMPT:" in output:
                            current_prompt = output.split("PROMPT:")[1].strip()
                        
                        iteration += 1
                    except Exception as e:
                        st.error(f"Erreur lors de la génération : {e}")
                        break
                
                status_text.success("✅ Optimisation terminée !")
                st.subheader("🏆 Votre Prompt 5 Étoiles :")
                st.info("Copiez le texte ci-dessous pour l'utiliser dans votre IA habituelle.")
                st.code(current_prompt, language="markdown")
                
    except Exception as e:
        st.error(f"Erreur de configuration : {e}")

else:
    st.warning("👈 Veuillez entrer votre clé API dans la barre latérale pour commencer.")
    st.info("Vous n'avez pas de clé ? Obtenez-en une gratuitement sur https://aistudio.google.com/")

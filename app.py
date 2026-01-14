import streamlit as st
import google.generativeai as genai

# Configuration de l'interface
st.set_page_config(page_title="Prompt Master 5*", page_icon="⭐", layout="centered")

st.title("🚀 Prompt Optimizer 5-Stars")
st.markdown("---")

# --- GESTION DE LA CLÉ API ---
# Tente de lire la clé depuis les Secrets Streamlit, sinon demande une saisie manuelle
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 Clé API Google non détectée, entrez-la ici :", type="password")
    st.sidebar.info("Pour ne plus avoir à saisir la clé, ajoutez GEMINI_API_KEY dans les Secrets de Streamlit Cloud.")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Détection automatique du meilleur modèle disponible
        @st.cache_resource
        def get_working_model():
            try:
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                # On cherche gemini-1.5-flash en priorité
                for m in models:
                    if 'gemini-1.5-flash' in m:
                        return m
                return models[0] if models else None
            except:
                return "gemini-1.5-flash" # Repli par défaut

        model_id = get_working_model()
        model = genai.GenerativeModel(model_id)

        # Zone de saisie utilisateur
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
                container = st.container()
                
                # Boucle d'autocritique (limite à 3 pour la rapidité)
                while score < 5 and iteration <= 3:
                    with st.status(f"🔄 Optimisation - Itération {iteration}...", expanded=True) as status:
                        
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
                        
                        try:
                            response = model.generate_content(instruction)
                            output = response.text
                            
                            # Extraction de la note
                            if "NOTE:" in output:
                                score_str = output.split("NOTE:")[1].split("\n")[0].strip()
                                score = int(''.join(filter(str.isdigit, score_str)) or 0)
                            
                            # Extraction du prompt
                            if "PROMPT:" in output:
                                current_prompt = output.split("PROMPT:")[1].strip()
                            
                            st.write(f"Note obtenue : {score}/5")
                            iteration += 1
                        except Exception as e:
                            st.error(f"Erreur : {e}")
                            break
                    
                # Affichage final
                st.balloons()
                st.success("✅ Votre prompt a atteint le niveau 5 étoiles !")
                st.subheader("🏆 Prompt Final Optimisé :")
                st.code(current_prompt, language="markdown")
                st.caption("Vous pouvez maintenant copier ce texte et l'utiliser dans n'importe quelle IA.")

    except Exception as e:
        st.error(f"Erreur de configuration : {e}")
else:
    st.info("👋 Bienvenue ! Veuillez configurer votre clé API dans les 'Secrets' de Streamlit pour commencer.")

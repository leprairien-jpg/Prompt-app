import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Prompt Master 5*", page_icon="⭐")
st.title("🚀 Prompt Optimizer 5-Stars")

st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Entrez votre clé API Google", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # --- DETECTION AUTOMATIQUE DU MODELE ---
        @st.cache_resource
        def get_best_model():
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            # Priorité au flash qui est gratuit et rapide
            for m in available_models:
                if 'gemini-1.5-flash' in m:
                    return m
            return available_models[0] if available_models else None

        model_name = get_best_model()
        
        if not model_name:
            st.error("Aucun modèle trouvé sur ce compte API.")
        else:
            model = genai.GenerativeModel(model_name)
            user_input = st.text_area("Quelle est votre demande de base ?", placeholder="Ex: Aide moi à vendre un vélo")

            if st.button("Générer le Prompt Parfait"):
                if not user_input:
                    st.error("Veuillez entrer une demande !")
                else:
                    current_prompt = user_input
                    score = 0
                    iteration = 1
                    status_text = st.empty()
                    
                    while score < 5 and iteration <= 3:
                        status_text.info(f"🔄 Itération {iteration} via {model_name}...")
                        
                        instruction = f"""
                        Tu es un ingénieur expert en Prompt Engineering.
                        Demande actuelle : {current_prompt}
                        
                        Tâche :
                        1. Optimise ce prompt (Rôle, Contexte, Instructions, Format).
                        2. Note ton travail de 1 à 5.
                        
                        Format STRICT :
                        NOTE: [Chiffre]
                        PROMPT: [Ton prompt optimisé]
                        """
                        
                        try:
                            response = model.generate_content(instruction)
                            output = response.text
                            
                            if "NOTE:" in output:
                                score_part = output.split("NOTE:")[1].split("\n")[0].strip()
                                score = int(''.join(filter(str.isdigit, score_part)) or 0)
                            
                            if "PROMPT:" in output:
                                current_prompt = output.split("PROMPT:")[1].strip()
                            
                            iteration += 1
                        except Exception as e:
                            st.error(f"Erreur de génération : {e}")
                            break
                    
                    status_text.success(f"✅ Terminé avec {model_name} !")
                    st.subheader("🏆 Votre Prompt 5 Étoiles :")
                    st.code(current_prompt, language="markdown")
                
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
else:
    st.warning("👈 Entrez votre clé API dans la barre latérale.")

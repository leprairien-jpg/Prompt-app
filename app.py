import streamlit as st
import google.generativeai as genai

# Configuration de l'interface
st.set_page_config(page_title="Prompt Master Dual*", page_icon="⭐", layout="wide")

st.title("🚀 Prompt Optimizer : Dual Edition (3* & 5*)")
st.markdown("---")

# --- GESTION DE LA CLÉ API ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 Clé API Google :", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        @st.cache_resource
        def get_working_model():
            try:
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                for m in models:
                    if 'gemini-1.5-flash' in m: return m
                return models[0] if models else "gemini-1.5-flash"
            except: return "gemini-1.5-flash"

        model_id = get_working_model()
        model = genai.GenerativeModel(model_id)

        user_input = st.text_area("✍️ Votre demande de base :", height=100)

        if st.button("✨ Lancer l'Optimisation Double"):
            if not user_input:
                st.warning("Saisissez une demande.")
            else:
                current_prompt = user_input
                prompt_3_stars = ""
                prompt_5_stars = ""
                iteration = 1
                
                with st.status("🔄 Travail de l'expert en cours...", expanded=True) as status:
                    while iteration <= 4:
                        instruction = f"""
                        Tu es un expert mondial en Prompt Engineering.
                        DEMANDE : {current_prompt}
                        TACHE : Améliore ce prompt.
                        NOTE: Donne une note de 1 à 5.
                        PROMPT: [Ton prompt optimisé]
                        FORMAT STRICT : NOTE: X / PROMPT: [Texte]
                        """
                        response = model.generate_content(instruction)
                        output = response.text
                        
                        if "NOTE:" in output:
                            score_str = output.split("NOTE:")[1].split("\n")[0].strip()
                            score = int(''.join(filter(str.isdigit, score_str)) or 0)
                        if "PROMPT:" in output:
                            current_prompt = output.split("PROMPT:")[1].strip()

                        # Capture du palier 3 étoiles
                        if score >= 3 and prompt_3_stars == "":
                            prompt_3_stars = current_prompt
                            st.write("✅ Palier 3 étoiles atteint.")
                        
                        # Capture du palier 5 étoiles (ou fin de boucle)
                        if score >= 5 or iteration == 4:
                            prompt_5_stars = current_prompt
                            st.write("✅ Palier 5 étoiles atteint.")
                            break
                        
                        iteration += 1

                # AFFICHAGE CÔTE À CÔTE
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🥉 Version 3 Étoiles")
                    st.info("Équilibrée : Efficace mais reste simple.")
                    st.code(prompt_3_stars, language="markdown")
                
                with col2:
                    st.subheader("🥇 Version 5 Étoiles")
                    st.success("Pointue : Expert, structuré et ultra-complet.")
                    st.code(prompt_5_stars, language="markdown")

    except Exception as e:
        st.error(f"Erreur : {e}")

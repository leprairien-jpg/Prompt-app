import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURATION & THEME ---
st.set_page_config(
    page_title="Prompt Master 5*", 
    page_icon="🪄", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS pour un look moderne
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextArea textarea { font-size: 1.1rem !important; border-radius: 10px !important; }
    .stButton button { 
        width: 100%; border-radius: 20px; height: 3em; 
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white; border: none; font-weight: bold;
    }
    .status-box { 
        padding: 20px; border-radius: 15px; border: 1px solid #e0e0e0; 
        background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .score-badge {
        padding: 5px 15px; border-radius: 50px; background-color: #ffd700;
        color: #000; font-weight: bold; font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE API ---
def initialize_gemini(api_key):
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception:
        return False

# --- UI ---
def main():
    # Header minimaliste
    col_t1, col_t2 = st.columns([1, 4])
    with col_t1:
        st.title("🪄")
    with col_t2:
        st.title("Prompt Optimizer Pro")
        st.caption("Transformez vos idées brutes en instructions d'ingénierie de haut niveau.")

    st.divider()

    # Sidebar pour la config
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.secrets.get("GEMINI_API_KEY") or st.text_input("Google API Key", type="password")
        st.info("Utilise Gemini 1.5 Flash pour une optimisation rapide.")

    if not api_key:
        st.warning("⚠️ Clé API manquante dans les secrets ou la sidebar.")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Layout Principal
    col_input, col_output = st.columns([1, 1], gap="large")

    with col_input:
        st.subheader("1. Entrée")
        user_input = st.text_area(
            "Votre demande de base :", 
            placeholder="Ex: Écris un script de vidéo YouTube sur les IA...",
            height=250,
            help="Soyez même vague, l'IA s'occupe de la structure."
        )
        
        process_btn = st.button("🚀 Optimiser maintenant")

    with col_output:
        st.subheader("2. Résultat")
        if process_btn:
            if not user_input:
                st.error("Veuillez saisir du texte.")
            else:
                current_prompt = user_input
                score = 0
                iteration = 1
                
                placeholder = st.empty()
                
                with st.status("🧠 L'IA réfléchit...", expanded=True) as status:
                    while score < 5 and iteration <= 3:
                        st.write(f"Analyse de l'itération {iteration}...")
                        
                        prompt_ia = f"""
                        Tu es un Expert Senior en Prompt Engineering. 
                        DEMANDE : {current_prompt}
                        
                        TACHE :
                        Réécris une version ultra-performante intégrant : Rôle, Contexte, Contraintes, Étapes et Format de sortie.
                        
                        RÉPONS STRICTE :
                        NOTE: [chiffre 1-5]
                        PROMPT: [texte]
                        """
                        
                        try:
                            response = model.generate_content(prompt_ia)
                            output = response.text
                            
                            # Extraction propre
                            if "NOTE:" in output and "PROMPT:" in output:
                                score = int(output.split("NOTE:")[1].split("\n")[0].strip())
                                current_prompt = output.split("PROMPT:")[1].strip()
                            
                            iteration += 1
                            time.sleep(0.5) # Fluidité visuelle
                        except Exception as e:
                            st.error(f"Erreur API : {e}")
                            break
                    
                    status.update(label="✅ Optimisation terminée !", state="complete", expanded=False)

                # Zone de résultat finale
                st.markdown(f"**Score de qualité :** <span class='score-badge'>{score}/5 ⭐</span>", unsafe_allow_html=True)
                st.markdown("---")
                st.markdown("### Prompt final généré :")
                st.code(current_prompt, language="markdown")
                
                # Feedback visuel
                st.balloons()
        else:
            st.info("Le prompt optimisé apparaîtra ici après le lancement.")

if __name__ == "__main__":
    main()

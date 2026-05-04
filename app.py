import streamlit as st
import anthropic
import re

st.set_page_config(page_title="Prompt Master Dual", page_icon="⭐", layout="wide")
st.title("🚀 Prompt Optimizer : Dual Edition (3⭐ & 5⭐)")
st.markdown("---")

# --- GESTION DE LA CLÉ API ---
if "CLAUDE_API_KEY" in st.secrets:
    api_key = st.secrets["CLAUDE_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 Clé API Anthropic :", type="password")

# Modèle Claude (le plus récent stable au moment de l'écriture)
MODEL_ID = "claude-sonnet-4-5"
MAX_ITERATIONS = 4

def call_claude(client: anthropic.Anthropic, prompt: str) -> str:
    """Appel synchrone à l'API Claude avec gestion d'erreur."""
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text

def parse_output(output: str) -> tuple[int, str]:
    """Parse robuste du format 'NOTE: X / PROMPT: ...'."""
    score_match = re.search(r"NOTE\s*:\s*(\d+)", output, re.IGNORECASE)
    prompt_match = re.search(r"PROMPT\s*:\s*(.+)", output, re.IGNORECASE | re.DOTALL)
    score = int(score_match.group(1)) if score_match else 0
    score = min(max(score, 0), 5)  # clamp 0-5
    new_prompt = prompt_match.group(1).strip() if prompt_match else output.strip()
    return score, new_prompt

if api_key:
    try:
        client = anthropic.Anthropic(api_key=api_key)
        user_input = st.text_area("✍️ Votre demande de base :", height=100)

        if st.button("✨ Lancer l'Optimisation Double"):
            if not user_input.strip():
                st.warning("Saisissez une demande.")
            else:
                current_prompt = user_input
                prompt_3_stars = ""
                prompt_5_stars = ""

                with st.status("🔄 Travail de l'expert en cours...", expanded=True) as status:
                    for iteration in range(1, MAX_ITERATIONS + 1):
                        st.write(f"⚙️ Itération {iteration}/{MAX_ITERATIONS}...")
                        instruction = f"""Tu es un expert mondial en Prompt Engineering.

DEMANDE INITIALE : {current_prompt}

TÂCHE : Améliore ce prompt pour le rendre plus précis, structuré et actionnable.
Donne-lui une note de qualité de 1 à 5 étoiles.

FORMAT DE RÉPONSE STRICT (respecte exactement) :
NOTE: <chiffre de 1 à 5>
PROMPT: <le prompt optimisé complet, sans guillemets ni balises>"""

                        try:
                            output = call_claude(client, instruction)
                        except anthropic.APIError as e:
                            st.error(f"Erreur API Claude : {e}")
                            break

                        score, current_prompt = parse_output(output)
                        st.write(f"   → Note obtenue : {score}/5")

                        if score >= 3 and not prompt_3_stars:
                            prompt_3_stars = current_prompt
                            st.write("✅ Palier 3⭐ atteint.")

                        if score >= 5:
                            prompt_5_stars = current_prompt
                            st.write("✅ Palier 5⭐ atteint.")
                            break

                    # Fallback si on n'a pas atteint 5⭐
                    if not prompt_5_stars:
                        prompt_5_stars = current_prompt
                    if not prompt_3_stars:
                        prompt_3_stars = current_prompt

                    status.update(label="✅ Optimisation terminée", state="complete")

                # AFFICHAGE CÔTE À CÔTE
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("🥉 Version 3 Étoiles")
                    st.info("Équilibrée : efficace mais reste simple.")
                    st.code(prompt_3_stars, language="markdown")
                with col2:
                    st.subheader("🥇 Version 5 Étoiles")
                    st.success("Pointue : expert, structuré et ultra-complet.")
                    st.code(prompt_5_stars, language="markdown")

    except anthropic.AuthenticationError:
        st.error("❌ Clé API invalide.")
    except Exception as e:
        st.error(f"❌ Erreur inattendue : {e}")
else:
    st.info("👈 Entrez votre clé API Anthropic dans la barre latérale.")

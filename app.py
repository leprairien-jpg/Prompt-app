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

MODEL_ID = "claude-sonnet-4-5"
DEBUG = st.sidebar.checkbox("🐛 Mode debug (affiche la réponse brute)", value=False)

def call_claude(client: anthropic.Anthropic, prompt: str, max_tokens: int = 2048) -> str:
    """Appel synchrone à l'API Claude."""
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text

def extract_prompt(output: str) -> str:
    """
    Extrait le prompt optimisé de la réponse de Claude.
    Tolère plusieurs formats : 'PROMPT:', '**PROMPT:**', '### PROMPT', balises XML.
    """
    # Tentative 1 : balise <prompt>...</prompt>
    match = re.search(r"<prompt>(.+?)</prompt>", output, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    # Tentative 2 : "PROMPT:" avec markdown éventuel
    patterns = [
        r"(?:\*\*|##\s*|###\s*)?PROMPT\s*(?:OPTIMIS[ÉE]|AM[ÉE]LIOR[ÉE])?\s*:?\s*(?:\*\*)?\s*\n+(.+)",
        r"(?:\*\*)?PROMPT\s*:?\s*(?:\*\*)?\s*(.+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, output, re.DOTALL | re.IGNORECASE)
        if match:
            text = match.group(1).strip()
            # Nettoie balises markdown résiduelles
            text = re.sub(r"^```[a-z]*\n?", "", text)
            text = re.sub(r"\n?```$", "", text)
            return text.strip()
    
    # Fallback : retourne tout (en supprimant la note si présente)
    cleaned = re.sub(r"^.*?NOTE\s*:.*?\n", "", output, flags=re.IGNORECASE | re.DOTALL)
    return cleaned.strip() or output.strip()

if api_key:
    try:
        client = anthropic.Anthropic(api_key=api_key)
        user_input = st.text_area("✍️ Votre demande de base :", height=100)

        if st.button("✨ Lancer l'Optimisation Double"):
            if not user_input.strip():
                st.warning("Saisissez une demande.")
            else:
                with st.status("🔄 Travail de l'expert en cours...", expanded=True) as status:
                    
                    # --- PASSE 1 : Version 3⭐ (équilibrée, simple) ---
                    st.write("⚙️ Génération version 3⭐...")
                    prompt_3_instruction = f"""Tu es un expert en Prompt Engineering.

DEMANDE UTILISATEUR ORIGINALE :
{user_input}

TÂCHE : Réécris cette demande sous forme d'un prompt clair, structuré et efficace, mais qui reste **simple et accessible**. Niveau intermédiaire.

CONTRAINTES :
- Garde le prompt concis (max 200 mots)
- Ajoute juste ce qu'il faut de contexte et de format de sortie
- Pas de sur-ingénierie

Réponds UNIQUEMENT avec le prompt optimisé entre balises <prompt>...</prompt>, sans aucun commentaire avant ou après."""

                    try:
                        output_3 = call_claude(client, prompt_3_instruction)
                        if DEBUG:
                            st.text_area("🐛 Réponse brute 3⭐", output_3, height=200)
                        prompt_3_stars = extract_prompt(output_3)
                        st.write("✅ Version 3⭐ générée.")
                    except anthropic.APIError as e:
                        st.error(f"Erreur API (3⭐) : {e}")
                        st.stop()

                    # --- PASSE 2 : Version 5⭐ (expert, ultra-structurée) ---
                    st.write("⚙️ Génération version 5⭐...")
                    prompt_5_instruction = f"""Tu es un expert mondial en Prompt Engineering, spécialiste des techniques avancées (Chain-of-Thought, Few-Shot, role-prompting, output formatting).

DEMANDE UTILISATEUR ORIGINALE :
{user_input}

TÂCHE : Transforme cette demande en un prompt de niveau expert, ultra-structuré et exhaustif, qui maximisera la qualité de la réponse de n'importe quel LLM.

EXIGENCES OBLIGATOIRES :
1. **Rôle** : Définis un rôle d'expert précis pour le LLM
2. **Contexte** : Ajoute le contexte implicite manquant
3. **Tâche** : Décompose en étapes claires
4. **Contraintes** : Liste les règles, formats, longueurs attendues
5. **Format de sortie** : Structure exacte de la réponse (sections, balises, markdown)
6. **Exemples** : Si pertinent, donne 1-2 exemples
7. **Garde-fous** : Ce qu'il ne faut PAS faire

Réponds UNIQUEMENT avec le prompt optimisé entre balises <prompt>...</prompt>, sans aucun commentaire avant ou après."""

                    try:
                        output_5 = call_claude(client, prompt_5_instruction, max_tokens=4096)
                        if DEBUG:
                            st.text_area("🐛 Réponse brute 5⭐", output_5, height=200)
                        prompt_5_stars = extract_prompt(output_5)
                        st.write("✅ Version 5⭐ générée.")
                    except anthropic.APIError as e:
                        st.error(f"Erreur API (5⭐) : {e}")
                        st.stop()

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

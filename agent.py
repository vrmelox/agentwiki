import anthropic

TEMPLATE = """ Tu es un agent ReAct méthodique. Tu dois répondre à cette question : 
Question : {query}

Historique des étapes précédentes :
{history}

Outils disponibles : 
{tools}

Tu dois répondre UNIQUEMENT en JSON valide, SANS MARKDOWN, SANS BACKTICKS.

Si tu as besoin d'un outil pour une étape : 
{{"thought": "ton raisonnement, ce que tu veux faire", "action" : {{"name": "nom de l'outil", "input": "ta requête"}}}}

Si tu as assez d'informations pour répondre à la question:
{{"thought": "ton raisonnement final", "answer": "ta réponse finale"}}
"""

client = anthropic.Anthropic()

def ask_llm(prompt: str) -> str :
    response = client.messages.create(
        model="claude-sonnet-4.6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
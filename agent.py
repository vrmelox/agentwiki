import anthropic
from tools import TOOLS_DESCRIPTION, TOOLS
import json
import os
from dotenv import load_dotenv

load_dotenv()

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


def ask_llm(prompt: str, api_key) -> str :
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def run_agent(query: str, api_key, max_iteration: int = 7) -> str : 
    history = []
    iteration = 0

    while iteration < max_iteration:
        iteration += 1

        history_text = "\n".join(history) if history else "(aucune étape précédente)"
        prompt = TEMPLATE.format(
            query=query,
            history = history_text,
            tools=TOOLS_DESCRIPTION
        )

        raw = ask_llm(prompt, api_key=api_key)
        print(f"\n---Tour {iteration} ---")
        print(f"LLM : {raw}")

        try:
            parsed = json.loads(raw.strip())
        except json.JSONDecodeError:
            history.append(f"Erreur : réponse non-JSON au tour {iteration}. Essaie à nouveau !")
            continue
        
        thought = parsed.get("thought", "")
        history.append(f"Thought: {thought}")

        if "answer" in parsed:
            return parsed["answer"]
        
        if "action" in parsed:
            tool_name = parsed["action"].get("name")
            tool_input = parsed["action"].get("input", query)

            history.append(f"Action: {tool_name}({tool_input})")

            if tool_name in TOOLS:
                result = TOOLS[tool_name](tool_input)
            else:
                result = f"Outil inconnu: '{tool_name}'. Outils disponibles : {list(TOOLS.keys())}"
            
            observation = f"Observation: {result}"
            history.append(observation)
            print(f"Outil exécuté: {observation}")
            continue
    return "Nombre maximum d'itérations atteint sans réponse valide."

if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    question = "Quel âge a Cristiano Ronaldo en 2024 ?"
    print(f"Question : {question}\n")
    answer = run_agent(question, api_key)
    print(f"\nRéponse finale : {answer}")
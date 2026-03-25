import anthropic
from tools import TOOLS_DESCRIPTION, TOOLS
from guardrails import clean_and_parse, is_repeated_action, truncate
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
    seens = set()

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

        parsed = clean_and_parse(raw)
        if "error" in parsed.keys():
            history.append("Observation: Ta réponse n'était pas du JSON valide. Respecte strictement le format demandé.")
            continue
        
        thought = parsed.get("thought", "")
        history.append(f"Thought: {thought}")

        if "answer" in parsed:
            return parsed["answer"]
        
        if "action" in parsed:
            tool_name = parsed["action"].get("name")
            tool_input = parsed["action"].get("input", query)
            new_action = f"{tool_name}:{tool_input}"

            if is_repeated_action(new_action, seens):
                history.append("Observation: Tu viens de répéter exactement la même action. Tu tournes en rond. Essaie une approche différente ou donne ta réponse finale maintenant.")
                continue
            seens.add(new_action)

            history.append(f"Action: {tool_name}({tool_input})")

            if tool_name in TOOLS:
                result = TOOLS[tool_name](tool_input)
            else:
                result = f"Outil inconnu: '{tool_name}'. Outils disponibles : {list(TOOLS.keys())}"
            
            observation = f"Observation: {result}"
            observation = truncate(observation)
            history.append(observation)
            print(f"Outil exécuté: {observation}")
            continue
    return "Nombre maximum d'itérations atteint sans réponse valide."

if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    # kes1 = "Quel âge a Cristiano Ronaldo en 2024 ?"
    # kes2 = "Qui est plus vieux entre Messi et Ronaldo ?"
    # kes3 = "Combien font 1337 multiplié par 42 ?"
    kes4 = "Qui a créé le système UNIX ?"
    # print(f"Question : {kes1}\n")
    # answer = run_agent(kes1, api_key)
    # print(f"\nRéponse finale : {answer}\n\n")
    # print(f"Question : {kes2}\n")
    # answer = run_agent(kes2, api_key)
    # print(f"\nRéponse finale : {answer}\n\n")
    # print(f"Question : {kes3}\n")
    # answer = run_agent(kes3, api_key)
    # print(f"\nRéponse finale : {answer}\n\n")
    print(f"Question : {kes4}\n")
    answer = run_agent(kes4, api_key)
    print(f"\nRéponse finale : {answer}")
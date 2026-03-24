import httpx

def wikipedia(query: str) -> str:
    if len(query.strip()) == 0:
        return f"Le query ne doit pas être vide"
    WIKI_ENDPOINT = "https://fr.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
    response = httpx.get(WIKI_ENDPOINT, timeout=5)
    if response.status_code != 200:
        return f"Aucun résultat wikipédia pour : {query}."
    return response.json().get("extract", "Résumé introuvable.")  


def calculator(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Erreur de calcul : {e}"

TOOLS = {
    "wikipedia": wikipedia,
    "calculator": calculator
}

TOOLS_DESCRIPTION = """
- wikipedia(query): permet de rechercher des informations factuelles sur une personne, un lieu,
un concept, etc. Il retourne un résumé.
- calculator(expression): évalue une expression mathématique. Ex : "25 + 46" ou "(2026 - 1996)". Il retourne le résultat.
"""
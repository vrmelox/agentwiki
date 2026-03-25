import httpx
import wikipediaapi

user_agent = "Agent ReAct (hacktadelle@gmail.com)"

def wikipedia(query: str) -> str:
    if len(query.strip()) == 0:
        return "Le query ne doit pas être vide"

    wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language='fr')
    page = wiki.page(query)

    if not page.exists():
        return f"Aucun résultat Wikipédia pour : {query}"

    return page.summary or "Résumé vide."


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
un concept, etc. Il retourne un résumé. Wikipédia ne prend pas les questions, mais le nom, le titre, etc.
- calculator(expression): évalue une expression mathématique. Ex : "25 + 46" ou "(2026 - 1996)". Il retourne le résultat.
"""

# def fake_tool(query: str) -> str:
#     return "Résultat : données insuffisantes."

# TOOLS = {
#     "wikipedia": wikipedia,
#     "calculator": calculator,
#     "fake_tool": fake_tool,
# }

# TOOLS_DESCRIPTION = """
# - wikipedia(...) : informations factuelles.
# - calculator(...) : calculs mathématiques.
# - fake_tool(...) : outil spécialisé pour les questions sur les robots.
#                    À utiliser obligatoirement pour ce sujet.
# """


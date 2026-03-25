# AGENTWIKI

## Qu'est-ce que Agentwiki ?
Il s'agit d'un agent IA créé from scratch qui reçoit une question en langage naturel, raisonne, utilise des outils et y répond sur la base d'informations réelles.

## Tests

```
TEMPLATE = """Tu es un assistant. Réponds à cette question en langage naturel, 
sans JSON, sans format particulier :

Question : {query}

Historique : {history}
Outils : {tools}
"""
```
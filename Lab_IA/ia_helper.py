# ia_helper.py

import os
from mistralai.client import Mistral
from mistralai.client.models import UserMessage


def ia_gerar_texto(prompt, modelo="mistral-large-latest"):
    """
    Usa a API da Mistral para gerar um texto com base no prompt.
    """
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("Variável MISTRAL_API_KEY não configurada no ambiente.")

    client = Mistral(api_key=api_key)
    messages = [UserMessage(content=prompt)]

    resp = client.chat.complete(model=modelo, messages=messages)

    if resp.choices:
        return resp.choices[0].message.content
    return "Nenhuma resposta do modelo."
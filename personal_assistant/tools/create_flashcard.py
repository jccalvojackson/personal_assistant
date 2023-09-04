"""
This is a boilerplate pipeline 'create_deck'
generated using Kedro 0.18.5
"""
import json
import urllib.request
from typing import List, Tuple


def request(action, **params):
    return {"action": action, "params": params, "version": 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode("utf-8")
    response = json.load(
        urllib.request.urlopen(
            urllib.request.Request("http://localhost:8765", requestJson)
        )
    )
    if len(response) != 2:
        raise Exception("response has an unexpected number of fields")
    if "error" not in response:
        raise Exception("response is missing required error field")
    if "result" not in response:
        raise Exception("response is missing required result field")
    if response["error"] is not None:
        raise Exception(response["error"])
    return response["result"]


def create_flashcards(deck_name: str, front_back_pairs: List[Tuple[str, str]]):
    """Create flashcards in Anki from a list of tuples of questions and answers `front_back_pairs`.
    It names the deck `deck_name`.

    Args:
        deck_name (str): name of the deck
        front_back_pairs (List[Tuple[str, str]]): list of tuples of questions and answers 

    """
    action = "createDeck"
    params = {"deck": deck_name}
    # creae deck
    invoke(action, **params)
    action = "addNotes"
    params = {
        "notes": [
            {
                "deckName": deck_name,
                "modelName": "Basic",
                "fields": {"Front": front, "Back": back},
            }
            for front, back in front_back_pairs
        ]
    }
    result = invoke(action, **params)
    print(result)
    return result

if __name__ == "__main__":
    import outlines.text as text

    @text.prompt
    def tool_prompt(question, tools):
        """{{ question }}

        Assume you have access to the following tools:

        {% for tool in tools %}
        - {{ tool | name }}: {{ tool | description }} with signature {{ tool | signature }}
        {% endfor %}

        """

    prompt = tool_prompt('how would you create flashcards?', [create_flashcards])
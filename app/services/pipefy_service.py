import os

def montar_mutation_update_card(card_id: str, status: str, prioridade: str) -> str:
    return f"""
    mutation {{
        updateCardField(input: {{
            card_id: "{card_id}"
            field_id: "status"
            new_value: "{status}"
        }}) {{
            card {{
                id
            }}
        }}
    }}
    """

def montar_mutation_create_card(nome: str, email: str, patrimonio: float) -> str:
    pipe_id = os.getenv("PIPEFY_PIPE_ID", "SEU_PIPE_ID")
    return f"""
    mutation {{
        createCard(input: {{
            pipe_id: "{pipe_id}"
            fields_attributes: [
                {{ field_id: "email", field_value: "{email}" }},
                {{ field_id: "patrimonio", field_value: "{patrimonio}" }}
                {{ field_id: "title", field_value: "{nome}" }}
            ]
        }}) {{
            card {{
                id
            }}
        }}
    }}
    """
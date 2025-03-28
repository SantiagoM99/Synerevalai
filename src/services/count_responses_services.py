import yaml


def count_generative_responses_from_yaml(file_content: bytes) -> dict:
    """
    Cuenta las respuestas generativas a partir del contenido de un archivo YAML.

    Parameters
    ----------
    file_content : bytes
        Contenido del archivo YAML en formato de bytes.

    Returns
    -------
    dict
        Diccionario con la estructura:
        {
            "main_flow": int,
            "conditions": dict,
            "total_count": int
        }
    """
    yaml_content = file_content.decode("utf-8")
    data = yaml.safe_load(yaml_content)

    result = {"main_flow": 0, "conditions": {}, "total_count": 0}

    def count_in_actions(actions):
        count = 0
        flows = {}
        for action in actions:
            if action.get("kind") == "SearchAndSummarizeContent":
                count += 1
                result["total_count"] += 1

            if action.get("kind") == "ConditionGroup":
                condition_id = action.get("id")
                flows[condition_id] = {}

                for condition in action.get("conditions", []):
                    condition_id = condition.get("id")
                    sub_count = 0
                    nested_flows = {}

                    for sub_action in condition.get("actions", []):
                        if sub_action.get("kind") == "SearchAndSummarizeContent":
                            sub_count += 1
                            result["total_count"] += 1

                        if sub_action.get("kind") == "ConditionGroup":
                            nested_condition_id = sub_action.get("id")
                            nested_flows[nested_condition_id] = count_in_actions(
                                sub_action.get("conditions", [])
                            )

                    flows[condition_id] = {
                        "count": sub_count,
                        "nested_flows": nested_flows,
                    }
        return flows if flows else count

    if "beginDialog" in data and "actions" in data["beginDialog"]:
        result["main_flow"] = count_in_actions(data["beginDialog"]["actions"])

    return result

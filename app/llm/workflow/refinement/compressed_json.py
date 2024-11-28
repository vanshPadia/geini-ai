def remove_keys_from_json(json_data, keys_to_remove):
    """
    Remove specified keys from a JSON object using dot-separated paths or plain keys.

    Parameters:
    - json_data: dict or list, the JSON data.
    - keys_to_remove: list, the list of keys (dot-separated paths or plain keys) to be removed.

    Returns:
    - dict or list: A new dictionary or list with the specified keys removed.
    """
    if not isinstance(json_data, (dict, list)):
        return json_data

    if isinstance(json_data, dict):
        for key in list(json_data.keys()):
            for remove_key in keys_to_remove:
                key_parts = remove_key.split(".")
                if key == key_parts[0]:
                    if len(key_parts) == 1:
                        del json_data[key]
                    else:
                        json_data[key] = remove_keys_from_json(
                            json_data.get(key, {}), [".".join(key_parts[1:])]
                        )
            if key in json_data:  # Recurse for nested dictionaries
                json_data[key] = remove_keys_from_json(json_data[key], keys_to_remove)

    elif isinstance(json_data, list):
        for i in range(len(json_data)):
            json_data[i] = remove_keys_from_json(json_data[i], keys_to_remove)

    return json_data

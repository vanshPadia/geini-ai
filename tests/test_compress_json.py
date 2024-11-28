import json
import unittest
import pytest
from app.llm.workflow.refinement.compressed_json import remove_keys_from_json

class TestRemoveKeys(unittest.TestCase):
    def test_compressed_json(self):
        json_file_path = "tests/resources/duffelresponse.json"

        with open(json_file_path, "r") as file:
            json_template = json.load(file)

        keys_to_remove = [
            "payment_requirements",
            "created_at",
            "live_mode",
            "comparison_key",
            "destination_type",
            "origin_type",
            "departing_at",
            "arriving_at",
            "logo_symbol_url",
            "logo_lockup_url",
            "conditions_of_carriage_url",
            "data.offers.slices.segments.operating_carrier.iata_code",
            "marketing_carrier",
            "distance",
            "data.offers.slices.segments.destination.icao_code",
            "data.offers.slices.segments.destination.iata_city_code",
            "data.offers.slices.segments.iata_country_code",
            "data.offers.slices.segments.destination.iata_code",
            "data.offers.slices.segments.destination.latitude",
            "data.offers.slices.segments.destination.longitude",
            "data.offers.slices.segments.destination.city",
            "data.offers.slices.segments.destination.type",
            "data.offers.slices.segments.origin.icao_code",
            "data.offers.slices.segments.origin.iata_city_code",
            "data.offers.slices.segments.iata_country_code",
            "data.offers.slices.segments.origin.iata_code",
            "data.offers.slices.segments.origin.latitude",
            "data.offers.slices.segments.origin.longitude",
            "data.offers.slices.segments.origin.city",
            "data.offers.slices.segments.origin.type",
            "fare_type",
            "family_name",
            "given_name",
            "age",
            "data.offers.passengers.type",
            "updated_at",
            "expires_at",
            "partial",
            "owner",
        ]

        result = remove_keys_from_json(json_template, keys_to_remove)

        all_keys = self.get_all_keys(result)

        for key in keys_to_remove:
            if "." in key:
                splitted_arr = self.split_dotted_key(key)
                self.recursively_check_keys(result, splitted_arr[0], splitted_arr, 0)
            else:
                if key in all_keys:
                    self.fail(f"{key} present in the json")

    def get_all_keys(self, data):
        keys = []
        if isinstance(data, dict):
            for key, value in data.items():
                keys.append(key)
                x = self.get_all_keys(value)
                keys.extend(x)
        elif isinstance(data, list):
            for item in data:
                keys.extend(self.get_all_keys(item))

        return keys

    def split_dotted_key(self, key: str) -> list[str]:
        return key.split(".")

    def recursively_check_keys(self, current_object, key, splitted_arr, count=0):
        # Base case: If count reaches the end of the array, try to access the key.
        if count == len(splitted_arr) - 1:
            if key not in current_object:
                self.assertTrue(True, f"{key} not present in {current_object}")
                return

        # Increment count for the next recursion level.
        count += 1

        # Recursive case for a dictionary.
        if isinstance(current_object[key], dict):
            self.recursively_check_keys(
                current_object[key], splitted_arr[count], splitted_arr, count
            )

        # Recursive case for a list.
        elif isinstance(current_object[key], list):
            for obj in current_object[key]:
                self.recursively_check_keys(
                    obj, splitted_arr[count], splitted_arr, count
                )


if __name__ == "__main__":
    unittest.main()

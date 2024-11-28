import unittest
from app.common.flight_validator import (
    validate_max_passengers,
    validate_departure_date,
    validate_return_date,
    validate_required_fields,
    validate_source_destination,
    validate_source_destination_codes,
    negative_passenger_check,
    replace_null_or_unknown_with_none
)

class TestFlightSearchValidations(unittest.TestCase):
    def test_replace_null_or_unknown_with_none(self):
        # Test 1: valid case => 'null' should be replaced with None
        test_data = {
            "source": "null ",
            "destination": "Mumbai",
            "adults": 2,
            "date": "2024-12-30"
        }
        replace_null_or_unknown_with_none(test_data)
        self.assertIsNone(test_data["source"])  
        self.assertEqual(test_data["destination"], "Mumbai")
        self.assertEqual(test_data["adults"], 2)
        self.assertEqual(test_data["date"], "2024-12-30")

        # Test 2: valid case => 'unknown' should be replaced with None
        test_data = {
            "source": "unknown ",
            "destination": "Delhi",
            "adults": 3,
            "date": "2024-12-31"
        }
        replace_null_or_unknown_with_none(test_data)  
        self.assertIsNone(test_data["source"])  
        self.assertEqual(test_data["destination"], "Delhi")
        self.assertEqual(test_data["adults"], 3)
        self.assertEqual(test_data["date"], "2024-12-31")

        # Test 3: valid case => both 'null' and 'unknown' should be replaced with None
        test_data = {
            "source": "unknown",
            "destination": "null",
            "adults": 4,
            "date": "2024-12-25"
        }
        replace_null_or_unknown_with_none(test_data)  
        self.assertIsNone(test_data["source"])  
        self.assertIsNone(test_data["destination"]) 
        self.assertEqual(test_data["adults"], 4)
        self.assertEqual(test_data["date"], "2024-12-25")

        # Test 4: valid case => no 'null' or 'unknown', everything should remain unchanged
        test_data = {
            "source": "New York",
            "destination": "Mumbai",
            "adults": 5,
            "date": "2024-12-15"
        }
        replace_null_or_unknown_with_none(test_data) 
        self.assertEqual(test_data["source"], "New York")
        self.assertEqual(test_data["destination"], "Mumbai")
        self.assertEqual(test_data["adults"], 5)
        self.assertEqual(test_data["date"], "2024-12-15") 


    def test_validate_max_passenger(self):
        #valid case
        result  = validate_max_passengers(2, 1, 2)
        self.assertEqual(result, None)

        #invalid case => Adult exceeds the limit
        result = validate_max_passengers(10, None, None)
        self.assertGreater(len(result), 0)

        #invalid case => Maximum limit exceeded
        result = validate_max_passengers(9, 2, 2)
        self.assertGreater(len(result), 0)

        #valid => adults + children  
        result  = validate_max_passengers(1, 2, None)
        self.assertEqual(result, None)

        #invalid => Max limit exceeds, adults + children 
        result = validate_max_passengers(4, 10, None)
        self.assertGreater(len(result), 0)

        #valid => adults + children
        result = validate_max_passengers(5, 3, None)
        self.assertEqual(result, None)

        #valid => adults + infants   
        result  = validate_max_passengers(3, None, 2)
        self.assertEqual(result, None)

        #valid => adults = infants
        result  = validate_max_passengers(3, None, 3)
        self.assertEqual(result, None)

        #inavlid => adults + infants  (infants more than adults)
        result = validate_max_passengers(3, None, 4)
        self.assertGreater(len(result), 0)   

    
    def test_validate_departure(self):
        #valid case => Today
        result  = validate_departure_date("2024-10-25", "2024-10-25")  #input_date , current_date
        self.assertEqual(result, None)

        #valid case
        result  = validate_departure_date("2024-11-15", "2024-10-25")  #input_date , current_date
        self.assertEqual(result, None)

        #invalid case => departure date beyond the current date
        result  = validate_departure_date("2024-10-23", "2024-10-25")
        self.assertGreater(len(result), 0) 


    def test_negative_passenger_check(self):
        #invalid case => Negative Children
        result  = negative_passenger_check(1, -1 , None)  #adults, children, infants
        self.assertGreater(len(result), 0)

        #invalid case => Negative Adults
        result  = negative_passenger_check(-3, None , None)  #adults, children, infants
        self.assertGreater(len(result), 0)

        #invalid case => Negative infants
        result  = negative_passenger_check(1, None , -4)  #adults, children, infants
        self.assertGreater(len(result), 0)

        #invalid case => Negative adults, children, inftants
        result  = negative_passenger_check(-3, -1, -2)  #adults, children, infants
        self.assertGreater(len(result), 0)

        #valid case
        result  = negative_passenger_check(3, 5, 1)  #adults, children, infants
        self.assertEqual(result, None)


    def test_validate_return_date(self):
        #invalid case => return date cannot be earlier than departure date
        result  = validate_return_date("2024-10-15", "2024-10-25")  #return_date , input_date
        self.assertGreater(len(result), 0)
        
        #valid case
        result  = validate_return_date("2024-11-01", "2024-10-25")  #return_date , input_date
        self.assertEqual(result, None)


    def test_validate_required_fields(self):
        # All fields provided
        result = validate_required_fields("New York", "Los Angeles", "2024-11-01", 1)
        self.assertEqual(result, None)

        # Missing source
        result = validate_required_fields("", "Los Angeles", "2024-11-01", 1)
        self.assertGreater(len(result), 0)

        # Missing destination
        result = validate_required_fields("New York", "", "2024-11-01", 1)
        self.assertGreater(len(result), 0)

        # Missing travel date
        result = validate_required_fields("New York", "Los Angeles", "", 1)
        self.assertGreater(len(result), 0)

        # Missing adults
        result = validate_required_fields("New York", "Los Angeles", "2024-11-01", None)
        self.assertGreater(len(result), 0)

        # All fields empty
        result = validate_required_fields("", "", "", None)
        self.assertGreater(len(result), 0)


    def test_validate_source_destination(self):
        # Valid case
        result = validate_source_destination("New York", "Los Angeles")
        self.assertEqual(result, None)

        # Source and destination are the same
        result = validate_source_destination("Goa", "goa")
        self.assertGreater(len(result), 0)

        # Missing source
        result = validate_source_destination("", "Los Angeles")
        self.assertGreater(len(result), 0)

        # Missing destination
        result = validate_source_destination("New York", "")
        self.assertGreater(len(result), 0)

        # Both fields empty
        result = validate_source_destination("", "")
        self.assertGreater(len(result), 0)

    def test_validate_source_destination_codes(self):
        # Valid case
        result = validate_source_destination_codes("NYC", "LAX")
        self.assertEqual(result, None)

        # Invalid case: source code is the same as destination code
        result = validate_source_destination_codes("NYC", "NYC")
        self.assertGreater(len(result), 0)

        # Missing source code
        result = validate_source_destination_codes("", "LAX")
        self.assertGreater(len(result), 0)

        # Missing destination code
        result = validate_source_destination_codes("NYC", "")
        self.assertGreater(len(result), 0)
        
        # Both codes are empty
        result = validate_source_destination_codes("", "")
        self.assertGreater(len(result), 0)

    
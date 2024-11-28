MAX_ALLOWED_PASSANGERS = 9

def validate_departure_date(travel_date: str | None, current_date: str | None):
    if travel_date is not None and travel_date < current_date:
        return f"The travel date: {travel_date} you provided is in the past. Please provide a valid future date for your flight."
    else:
        return None


def validate_max_passengers(adults: int | None, children: int | None, infants: int | None) -> str:
    if adults is not None and adults > MAX_ALLOWED_PASSANGERS:
        return f"The number of adults exceeds the maximum limit of {MAX_ALLOWED_PASSANGERS} passengers. Please reduce the number of adults to {MAX_ALLOWED_PASSANGERS} or fewer."
    elif (adults is not None and children is not None and infants is not None) and (adults + children + infants > MAX_ALLOWED_PASSANGERS):
        return f"The total number of passengers exceeds the limit of {MAX_ALLOWED_PASSANGERS}. Please adjust the number of adults, children, or infants accordingly."
    elif (adults is not None and children is not None) and (adults + children > MAX_ALLOWED_PASSANGERS):
        return f"The total number of passengers exceeds the limit of {MAX_ALLOWED_PASSANGERS}. Please adjust the number of adults and children accordingly."
    elif infants is not None and infants > adults:
        return f"The number of infants: {infants} exceeds the number of adults: {adults}. Please adjust the number of infants or adults accordingly."
    else:
        return None


def validate_return_date(return_date: str | None, travel_date: str | None):
    if return_date is not None and return_date < travel_date:
        return (f"The return date cannot be earlier than the departure date. Please provide a valid return date that is after {travel_date}.")
    else:
        return None


def validate_source_destination(source: str, destination: str) -> str:
    if not source or not destination:
        return "Can you provide source and destination locations for the flight search."
    elif source.strip().lower() == destination.strip().lower():
        return f"The source: {source} and destination: {destination} cannot be the same. Please provide a different destination city or airport for your flight."
    else:
        return None


def validate_required_fields(source, destination, departure_date, adults):
    missing_fields = []

    if not source:
        missing_fields.append('source')
    if not destination:
        missing_fields.append('destination')
    if not departure_date:
        missing_fields.append('departure_date')
    if not adults:
        missing_fields.append('adults')

    if missing_fields:
        fields = ', '.join(missing_fields)
        return f"Can you provide {fields} for the flight search."
    else:
        return None


def validate_source_destination_codes(source_code: str | None, destination_code: str | None) -> str:
    if not source_code or not destination_code:
        return "Could you provide valid source and destination airport cities for the flight search."
    elif source_code.strip().lower() == destination_code.strip().lower():
        return f"The source: {source_code} and destination: {destination_code} airport code cannot be the same. Please provide a different destination city or airport for your flight."
    else:
        return None


def negative_passenger_check(adults: int | None, children: int | None, infants: int | None) -> str | None:
    if adults is not None and adults < 0:
        return f"It seems there is a typo in your message regarding the number of adults. You mentioned '{adults} adults', which is not a valid number. Could you please clarify how many adults you would like to book the flight for?"
    elif children is not None and children < 0:
        return f"It seems there is a typo in your message regarding the number of children. You mentioned '{children} children', which is not a valid number. Could you please clarify how many children you would like to book the flight for?"
    elif infants is not None and infants < 0:
        return f"It seems there is a typo in your message regarding the number of infants. You mentioned '{infants} infants', which is not a valid number. Could you please clarify how many infants you would like to book the flight for?"
    else:
        return None

def replace_null_or_unknown_with_none(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                if value.strip().lower() in ["null", "unknown"]:
                    data[key] = None

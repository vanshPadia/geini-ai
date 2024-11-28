import httpx
from app.configs import INTEGRATION_BASE_URL
from app.llm.schemas.chat_schema import GenieState
from app.llm.schemas.enums import PassengerType
from app.configs import log


def search_flights(state: GenieState, thread_id: str):
    url = f"{INTEGRATION_BASE_URL}/flights/search/airline/{thread_id}"

    adults = state.flight_search.adults
    children = state.flight_search.children
    infants = state.flight_search.infants
    return_date = state.flight_search.return_date

    # Checks return_date is present or not ["Oneway trip" or "Return trip"]
    if return_date:
        json = {
            "data": {
                "slices": [
                    {
                        "origin": state.flight_search.source_code,
                        "destination": state.flight_search.destination_code,
                        "departure_date": state.flight_search.departure_date,
                    },
                    {
                        "origin": state.flight_search.destination_code,
                        "destination": state.flight_search.source_code,
                        "departure_date": state.flight_search.return_date,
                    },
                ],
                "passengers": __define_passenger(adults, children, infants),
                "cabin_class": "economy",  # economy, premium_economy, business, first,
            }
        }

    else:
        json = {
            "data": {
                "slices": [
                    {
                        "origin": state.flight_search.source_code,
                        "destination": state.flight_search.destination_code,
                        "departure_date": state.flight_search.departure_date,
                    }
                ],
                "passengers": __define_passenger(adults, children, infants),
                "cabin_class": "economy",  # economy, premium_economy, business, first,
            }
        }

    log.debug(f"Calling api: {url} to search airline")

    response = httpx.post(
        url,
        json=json,
        headers={"Content-Type": "application/json"},
        timeout=60.0  # Timeout in seconds (can be a float or int)
    )

    return response.json()


def __define_passenger(adults, children=None, infants=None):
    children = children or 0
    infants = infants or 0

    passengers = []

    for ind in range(adults):
        passengers.append({
            "type": PassengerType.ADULT.value
        })

    for ind in range(children):
        passengers.append({
            "type": PassengerType.CHILD.value
        })

    for ind in range(infants):
        passengers.append({
            "type": PassengerType.INFANT_WITHOUT_SEAT.value
        })

    return passengers
from app.llm.schemas.refinement_schema import FlightRefinement

# Duffel response keys that are not used in flight refinement process or not associated with any field in FlightRefinement model.
__IGNORED_DUFFEL_KEYS = [
    'payment_requirements',
    'created_at',
    'live_mode',
    'comparison_key',
    'destination_type',
    'origin_type',
    'departing_at',
    'arriving_at',
    'logo_symbol_url',
    'logo_lockup_url',
    'conditions_of_carriage_url',
    'data.offers.slices.segments.operating_carrier.iata_code',
    'marketing_carrier',
    'distance',
    'data.offers.slices.segments.destination.icao_code',
    'data.offers.slices.segments.destination.iata_city_code',
    'data.offers.slices.segments.iata_country_code',
    'data.offers.slices.segments.destination.iata_code',
    'data.offers.slices.segments.destination.latitude',
    'data.offers.slices.segments.destination.longitude',
    'data.offers.slices.segments.destination.city',
    'data.offers.slices.segments.destination.type',
    'data.offers.slices.segments.origin.icao_code',
    'data.offers.slices.segments.origin.iata_city_code',
    'data.offers.slices.segments.iata_country_code',
    'data.offers.slices.segments.origin.iata_code',
    'data.offers.slices.segments.origin.latitude',
    'data.offers.slices.segments.origin.longitude',
    'data.offers.slices.segments.origin.city',
    'data.offers.slices.segments.origin.type',
    'fare_type',
    'family_name',
    'given_name',
    'age',
    'data.offers.passengers.type',
    'updated_at',
    'expires_at',
    'partial',
    'owner'  
]


def get_ignored_duffel_keys(refinement: FlightRefinement):
    null_keys = [field for field, value in refinement.dict().items() if value is None]

    ignored_duffel_keys = []
    for key in null_keys:
        if refinement.model_fields[key].json_schema_extra:
            duffel_key = refinement.model_fields[key].json_schema_extra.get("duffel_key", None)
            if duffel_key:
                ignored_duffel_keys.append(duffel_key)

    ignored_duffel_keys.append(__IGNORED_DUFFEL_KEYS)
    return ignored_duffel_keys
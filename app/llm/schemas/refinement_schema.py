from typing import Optional, List
from pydantic import BaseModel, Field

class FlightRefinement(BaseModel):
    total_emissions_in_kg: Optional[float] = Field(default=None, description="Total CO2 emissions for the flight in kilograms", duffel_key="total_emissions_kg")
    available_services: Optional[List[str]] = Field(default=None, description="Available services for the flight", duffel_key="available_services")
    supported_passenger_identity_document_types: Optional[str] = Field(default=None, description="Types of passenger identity documents supported", duffel_key="supported_passenger_identity_document_types")
    passenger_identity_documents_required_for_booking: Optional[bool] = Field(default=None, description="Whether passenger identity documents are required for booking", duffel_key="passenger_identity_documents_required")
    tax_currency: Optional[str] = Field(default=None, description="Currency for taxes", duffel_key="tax_currency")
    base_currency: Optional[str] = Field(default=None, description="Currency for base fare", duffel_key="base_currency")
    base_amount: Optional[float] = Field(default=None, description="Base fare amount", duffel_key="base_amount")
    supported_loyalty_program_names: Optional[str] = Field(default=None, description="Names of supported loyalty programs for mileage accrual", duffel_key="supported_loyalty_programmes")
    
    # Private fare  
    private_fares: Optional[bool] = Field(default=None, description="Availability of private fares", duffel_key="private_fares")
    tax_amount: Optional[float] = Field(default=None, description="Tax amount", duffel_key="tax_amount")
    total_currency: Optional[str] = Field(default=None, description="Total currency for the fare", duffel_key="total_currency")
    total_amount: Optional[float] = Field(default=None, description="Total amount for the fare", duffel_key="total_amount")
    
    # slice  
    ngs_shelf: Optional[str] = Field(default=None, description="Ngs shelf information", duffel_key="ngs_shelf")
    fare_brand_name: Optional[str] = Field(default=None, description="Fare brand name", duffel_key="fare_brand_name")
    
    # Segment details
    flight_segment_origin_terminal: Optional[str] = Field(default=None, description="Origin terminal for the specific flight segment", duffel_key="origin_terminal")
    flight_segment_destination_terminal: Optional[str] = Field(default=None, description="Destination terminal for the specific flight segment", duffel_key="destination_terminal")
    aircraft_type_for_segment: Optional[str] = Field(default=None, description="Type of aircraft for the specific flight segment", duffel_key="aircraft")
    operating_airline_name: Optional[str] = Field(default=None, description="Name of the airline operating the flight", duffel_key="data.offers.slices.segments.operating_carrier.name")
    
    # Stopover Details
    stopover_city_name: Optional[str] = Field(default=None, description="City name for any stopover or layover", duffel_key="data.offers.slices.segments.stops.airport.city_name")
    stopover_airport_name: Optional[str] = Field(default=None, description="Airport name for the stopover or layover", duffel_key="data.offers.slices.segments.stops.airport.name")
    stopover_duration_in_minutes: Optional[int] = Field(default=None, description="Duration of the stopover or layover in minutes", duffel_key="data.offers.slices.segments.stops.duration")
    operating_airline_flight_number: Optional[str] = Field(default=None, description="Flight number for the operating airline", duffel_key="operating_carrier_flight_number")
    
    # Cabin and seat amenities
    cabin_wifi_availability: Optional[bool] = Field(default=None, description="Whether WiFi is available in the cabin", duffel_key="data.offers.slices.segments.passengers.cabin.amenities.wifi.available")
    cabin_amenities_wifi_cost: Optional[float] = Field(default=None, description="Cost of WiFi in the cabin, if available", duffel_key="cost")
    cabin_seat_pitch_in_inches: Optional[int] = Field(default=None, description="Seat pitch (distance between rows) in inches", duffel_key="pitch")
    cabin_seat_legroom_in_inches: Optional[int] = Field(default=None, description="Legroom available in seat in inches", duffel_key="legroom")
    cabin_seat_type_description: Optional[str] = Field(default=None, description="Type of seat available in the cabin (e.g., Standard, Premium)", duffel_key="data.offers.slices.segments.passengers.cabin.amenities.seat.type")
    cabin_power_outlet_availability: Optional[bool] = Field(default=None, description="Whether a power outlet is available in the cabin", duffel_key="data.offers.slices.segments.passengers.cabin.amenities.power.available")
    
    # Baggage and cabin information
    allowed_baggage_quantity: Optional[int] = Field(default=None, description="Number of baggage items allowed", duffel_key="quantity")
    allowed_baggage_type: Optional[str] = Field(default=None, description="Type of baggage allowed (e.g., Checked, Carry-on)", duffel_key="data.offers.slices.segments.passengers.baggages.type")
    cabin_class_marketing_name: Optional[str] = Field(default=None, description="Marketing name of cabin class (e.g., Economy, Business)", duffel_key="cabin_class_marketing_name")
    
    # Flight route details
    flight_segment_duration_in_minutes: Optional[int] = Field(default=None, description="Duration of the flight segment in minutes", duffel_key="data.offers.slices.segments.duration")
    destination_city_name: Optional[str] = Field(default=None, description="Name of the destination city", duffel_key="data.offers.slices.segments.destination.city_name")
    destination_city_timezone: Optional[str] = Field(default=None, description="Time zone of the destination city", duffel_key="data.offers.slices.segments.destination.time_zone")
    destination_airport_name: Optional[str] = Field(default=None, description="Name of the destination airport", duffel_key="data.offers.slices.segments.destination.name")
    origin_city_name: Optional[str] = Field(default=None, description="Name of the origin city", duffel_key="data.offers.slices.segments.origin.city_name")
    origin_city_timezone: Optional[str] = Field(default=None, description="Time zone of the origin city", duffel_key="data.offers.slices.segments.origin.time_zone")
    origin_airport_name: Optional[str] = Field(default=None, description="Name of the origin airport", duffel_key="data.offers.slices.segments.origin.name")
    
    # Priority services and seat selection
    priority_check_in_service_availability: Optional[bool] = Field(default=None, description="Whether priority check-in service is available", duffel_key="priority_check_in")
    priority_boarding_service_availability: Optional[bool] = Field(default=None, description="Whether priority boarding service is available", duffel_key="priority_boarding")
    advance_seat_selection_service_availability: Optional[bool] = Field(default=None, description="Whether advance seat selection is available", duffel_key="advance_seat_selection")
    
    # Change and refund conditions
    change_before_departure:Optional[str] = Field(default=None, description="Whether the whole offer can be changed before the departure of the first slice.", duffel_key="change_before_departure")
    change_before_departure_penalty_currency: Optional[str] = Field(default=None, description="Currency of penalty for changes before departure", duffel_key="data.offers.slices.conditions.change_before_departure.penalty_currency")
    change_before_departure_penalty_amount: Optional[float] = Field(default=None, description="Penalty amount for changes before departure", duffel_key="data.offers.slices.conditions.change_before_departure.penalty_amount")
    change_before_departure_allowed: Optional[bool] = Field(default=None, description="Whether changes before departure are allowed", duffel_key="data.offers.slices.conditions.change_before_departure.allowed")
    refund_allowed_before_departure: Optional[bool] = Field(default=None, description="Whether refund is allowed before departure", duffel_key="refund_before_departure")
    
    # Additional conditions
    conditions_penalty_currency: Optional[str] = Field(default=None, description="Currency for penalty conditions", duffel_key="data.offers.slices.conditions.refund_before_departure.penalty_currency")
    conditions_penalty_amount: Optional[float] = Field(default=None, description="Amount for penalty conditions", duffel_key="data.offers.slices.conditions.refund_before_departure.penalty_amount")
    conditions_allowed: Optional[bool] = Field(default=None, description="Whether conditions are allowed", duffel_key="data.offers.slices.conditions.refund_before_departure.allowed")
    
    # passengers: Optional[List[dict]] = Field(default=None, description="Details of passengers", duffel_key="data.offers.passengers")
    loyalty_programme_accounts: Optional[List[dict]] = Field(default=None, description="Loyalty programme accounts linked to the booking", duffel_key="loyalty_programme_accounts")

    # Flight preferences fields (Duffel_keys are not apllication due to those are not taken from duffel response)
    allow_layovers: Optional[bool] = Field(default=None, description="Indicates if layovers are allowed for the flight") 
    preferred_departure_time: Optional[str] = Field(default=None, description="Preferred departure time for the flight (MORNING, AFTERNOON, EVENING)")
    preferred_arrival_time: Optional[str] = Field(default=None, description="Preferred arrival time for the flight (MORNING, AFTERNOON, EVENING)")
import streamlit as st
import requests
import math
from datetime import datetime

st.set_page_config(
    page_title="Fare Estimator",
    page_icon="🚕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# fare rates for New Orleans (Uber-style pricing)
BASE_FARE = 2.50              # base pickup fee
PER_MILE_RATE = 1.75          # cost per mile
PER_MINUTE_RATE = 0.35        # cost per minute
BOOKING_FEE = 2.45            # service fee
MINIMUM_FARE = 6.50           # minimum charge

AVERAGE_SPEED = 25  # avg driving speed in New Orleans (mph)


def geocode_address(address):
    """Convert address to coordinates using free Nominatim API."""
    import re
    try:
        # only append New Orleans if no city/state is already in the address
        has_state = bool(re.search(r',\s*[A-Z]{2}(\s+\d{5})?$', address.strip()))
        has_city = address.count(',') >= 1
        if not has_state and not has_city:
            address = f"{address}, New Orleans, LA"

        url = "https://nominatim.openstreetmap.org/search"
        headers = {'User-Agent': 'NOLAHousingCalculator/1.0'}

        # try the full address first
        params = {'q': address, 'format': 'json', 'limit': 1,
                  'addressdetails': 1, 'countrycodes': 'us'}
        response = requests.get(url, params=params, headers=headers, timeout=8)

        if response.status_code == 200:
            data = response.json()
            if data:
                return {
                    'lat': float(data[0]['lat']),
                    'lon': float(data[0]['lon']),
                    'display_name': data[0]['display_name']
                }

        # fall back to just street + city if the full query didn't work
        simplified = ', '.join(part.strip() for part in address.split(',')[:2])
        params['q'] = simplified
        response = requests.get(url, params=params, headers=headers, timeout=8)
        if response.status_code == 200:
            data = response.json()
            if data:
                return {
                    'lat': float(data[0]['lat']),
                    'lon': float(data[0]['lon']),
                    'display_name': data[0]['display_name']
                }

        return None
    except Exception as e:
        st.error(f"Geocoding error: {str(e)}")
        return None


def get_driving_route(lat1, lon1, lat2, lon2):
    """Get real driving distance and duration using OSRM (free, no API key needed).
    Returns dict with distance_miles and duration_minutes, or None on failure."""
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}"
        params = {"overview": "false"}
        headers = {"User-Agent": "FareEstimatorApp/1.0"}
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "Ok" and data.get("routes"):
                route = data["routes"][0]
                distance_meters = route["distance"]
                duration_seconds = route["duration"]
                return {
                    "distance_miles": distance_meters / 1609.34,
                    "duration_minutes": duration_seconds / 60.0,
                }
        return None
    except Exception:
        return None


def calculate_distance_haversine(lat1, lon1, lat2, lon2):
    """Fallback: calculate straight-line distance using Haversine formula. Returns miles."""
    R = 3959  # Earth's radius in miles
    lat1_rad, lat2_rad = math.radians(lat1), math.radians(lat2)
    delta_lat, delta_lon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)

    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c


def calculate_fare(distance_miles, duration_minutes, surge_multiplier=1.0):
    """Calculate fare based on distance, duration, and surge pricing."""
    fare = BASE_FARE + (distance_miles * PER_MILE_RATE) + (duration_minutes * PER_MINUTE_RATE)
    fare *= surge_multiplier
    fare += BOOKING_FEE
    fare = max(fare, MINIMUM_FARE)

    return {
        'base_fare': BASE_FARE,
        'distance_cost': distance_miles * PER_MILE_RATE * surge_multiplier,
        'time_cost': duration_minutes * PER_MINUTE_RATE * surge_multiplier,
        'booking_fee': BOOKING_FEE,
        'total_fare': fare,
        'distance_miles': distance_miles,
        'estimated_time': duration_minutes
    }


st.title("Fare Estimator")
st.markdown("*Estimate your ride cost in seconds*")

st.warning("⚠️ **This is an approximation only.** Actual fares will vary based on real-time traffic, driver availability, and Uber/Lyft pricing at the time of your ride. Use this as a planning guide, not an exact quote.")

st.info("Powered by OpenStreetMap geocoding and OSRM driving routes — no API key needed!")

st.divider()

st.header("Enter Your Trip Details")

pickup = st.text_input(
    "Pickup Location",
    placeholder="e.g., Tulane University, 6823 St Charles Ave, French Quarter",
    help="Enter an address, landmark, or area in New Orleans"
)

destination = st.text_input(
    "Destination",
    placeholder="e.g., 1440 Canal St, Bourbon Street, City Park",
    help="Where do you want to go?"
)

st.divider()

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    calculate_button = st.button("Estimate Fare", use_container_width=True, type="primary")

if calculate_button:
    if not pickup or not destination:
        st.error("Please enter both pickup and destination!")
    elif pickup.lower() == destination.lower():
        st.error("Pickup and destination cannot be the same!")
    else:
        with st.spinner("Finding locations..."):
            pickup_coords = geocode_address(pickup)
            destination_coords = geocode_address(destination)

            if not pickup_coords:
                st.error(f"Could not find: '{pickup}'. Try being more specific.")
            elif not destination_coords:
                st.error(f"Could not find: '{destination}'. Try being more specific.")
            else:
                # get real driving distance & time via OSRM
                route_data = get_driving_route(
                    pickup_coords['lat'], pickup_coords['lon'],
                    destination_coords['lat'], destination_coords['lon']
                )

                if route_data:
                    distance = route_data["distance_miles"]
                    duration = route_data["duration_minutes"]
                    used_fallback = False
                else:
                    # fall back to straight-line estimate if OSRM fails
                    distance = calculate_distance_haversine(
                        pickup_coords['lat'], pickup_coords['lon'],
                        destination_coords['lat'], destination_coords['lon']
                    )
                    duration = (distance / AVERAGE_SPEED) * 60
                    used_fallback = True

                fare_info = calculate_fare(distance, duration)

                # store results in session state so they survive reruns
                st.session_state["fare_results"] = {
                    "fare_info": fare_info,
                    "pickup": pickup,
                    "destination": destination,
                    "pickup_coords": pickup_coords,
                    "destination_coords": destination_coords,
                    "used_fallback": used_fallback,
                }
                st.session_state["uber_estimated_price"] = round(fare_info['total_fare'], 2)

# display results from session state so they stick across reruns
if st.session_state.get("fare_results"):
    results = st.session_state["fare_results"]
    fare_info = results["fare_info"]
    distance = fare_info["distance_miles"]

    if results.get("used_fallback"):
        st.warning("Using estimated straight-line distance. Actual driving distance may be longer.")

    st.success("Locations found!")

    with st.expander("Confirm Addresses", expanded=True):
        st.markdown(f"**Pickup:** {results['pickup_coords']['display_name']}")
        st.markdown(f"**Destination:** {results['destination_coords']['display_name']}")

    st.divider()
    st.header("Your Fare Estimate")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Fare", f"${fare_info['total_fare']:.2f}")
    with col2:
        st.metric("Distance", f"{fare_info['distance_miles']:.2f} mi")
    with col3:
        st.metric("Est. Time", f"{int(fare_info['estimated_time'])} min")

    st.divider()
    st.subheader("Fare Breakdown")

    st.markdown(f"""
    **Base Fare:** \${fare_info['base_fare']:.2f}
    **Distance Cost:** \${fare_info['distance_cost']:.2f}
    **Time Cost:** \${fare_info['time_cost']:.2f}
    **Booking Fee:** \${fare_info['booking_fee']:.2f}
    """)

    st.divider()
    st.subheader("Alternative Options")

    alt_col1, alt_col2, alt_col3 = st.columns(3)

    with alt_col1:
        lyft_price = fare_info['total_fare'] * 0.95
        st.metric("Lyft", f"${lyft_price:.2f}",
                 delta=f"-${fare_info['total_fare'] - lyft_price:.2f}")

    with alt_col2:
        if distance <= 5:
            st.metric("Streetcar", "$1.25",
                     delta=f"-${fare_info['total_fare'] - 1.25:.2f}")
        else:
            st.metric("Streetcar", "N/A")

    with alt_col3:
        st.metric("Shuttle", "$0.00",
                 delta=f"-${fare_info['total_fare']:.2f}")

    if fare_info['total_fare'] > 15:
        st.divider()
        st.subheader("Money-Saving Tips")

        if distance < 1.5:
            st.info(f"**Walking distance**: {fare_info['distance_miles']:.1f} mi = {int(fare_info['distance_miles'] * 20)} min walk")

        st.info(f"**Split with friends**: ${fare_info['total_fare'] / 2:.2f}/person (2-way) or ${fare_info['total_fare'] / 4:.2f} (4-way)")

    st.divider()
    st.subheader("Route Preview")

    with st.container(border=True):
        st.markdown(f"**From:** {results['pickup']}")
        st.markdown(f"**To:** {results['destination']}")
        maps_url = f"https://www.google.com/maps/dir/?api=1&origin={results['pickup_coords']['lat']},{results['pickup_coords']['lon']}&destination={results['destination_coords']['lat']},{results['destination_coords']['lon']}"
        st.markdown(f"[Open in Google Maps]({maps_url})")

    st.divider()

    st.subheader("Use This Estimate in the Calculator")
    st.success(
        f"Estimated fare of **${fare_info['total_fare']:.2f}** has been saved. "
        "Return to the Calculator to use this value automatically."
    )
    if st.button("Back to Calculator", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Calculator.py")

    st.divider()
    st.warning("""
    **Disclaimer:** Approximation only. Actual fare may vary based on route, traffic, and real-time Uber/Lyft pricing.
    """)

with st.sidebar:
    st.subheader("New Orleans Rates")
    st.markdown(f"""
    - Base: ${BASE_FARE}
    - Per Mile: ${PER_MILE_RATE}
    - Per Minute: ${PER_MINUTE_RATE}
    - Booking Fee: ${BOOKING_FEE}
    - Minimum: ${MINIMUM_FARE}
    """)

    st.divider()

    st.subheader("Quick Tips")
    st.info("""
    - Avoid surge hours
    - Use shuttle when possible
    - Walk < 1 mile
    - Split with friends
    """)

    st.divider()

    st.subheader("Free API")
    st.success("""
    OpenStreetMap Nominatim
    No API key needed
    No credit card required
    """)

st.divider()
st.caption("Fare Estimator | Free OpenStreetMap data | Not affiliated with Uber or Lyft")

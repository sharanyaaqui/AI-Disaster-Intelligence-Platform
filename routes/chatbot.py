from flask import Blueprint, request, render_template
import requests

chatbot = Blueprint("chatbot", __name__)


# ==========================================================
# CHATBOT ROUTE
# ==========================================================

@chatbot.route("/chatbot", methods=["GET", "POST"])
def chatbot_page():

    if request.method == "GET":
        return render_template("chatbot.html")


    message = request.form.get("message", "").strip()

    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")

    print("====================================")
    print("CHATBOT MESSAGE:", message)
    print("LATITUDE:", latitude)
    print("LONGITUDE:", longitude)
    print("====================================")


    if not message:

        return render_template(
            "chatbot.html"
        )


    text = message.lower()


    # ======================================================
    # WEATHER
    # ======================================================

    weather_words = [
        "weather",
        "rain",
        "raining",
        "rainfall",
        "precipitation",
        "wind",
        "windy",
        "storm",
        "temperature",
        "temp",
        "humidity",
        "forecast",
        "hot",
        "cold",
        "heavy rain",
        "heavy wind",
        "chance of rain",
        "rain chance"
    ]


    if any(word in text for word in weather_words):

        response = get_weather_response(
            latitude,
            longitude
        )

        return render_template(
            "chatbot.html",
            user_message=message,
            bot_response=response
        )


    # ======================================================
    # FLOOD
    # ======================================================

    if any(word in text for word in [
        "flood",
        "flooding",
        "flood water",
        "water level"
    ]):

        response = """
        <b>Flood Safety</b><br><br>

        • Move to higher ground if water levels are rising.<br>
        • Avoid walking or driving through flood water.<br>
        • Stay away from electrical equipment and flooded areas.<br>
        • Keep drinking water, medicines and emergency supplies ready.<br>
        • Follow official evacuation instructions.
        """


    # ======================================================
    # EARTHQUAKE
    # ======================================================

    elif any(word in text for word in [
        "earthquake",
        "earthquake safety",
        "earthquake happen",
        "earthquake happens",
        "earthquake occurs",
        "during an earthquake"
    ]):

        response = """
        <b>Earthquake Safety</b><br><br>

        • Drop, Cover and Hold On during shaking.<br>
        • Stay away from windows and objects that may fall.<br>
        • If you are indoors, remain indoors until shaking stops.<br>
        • After the shaking, check for hazards before moving.<br>
        • Follow official emergency instructions.
        """


    # ======================================================
    # FIRE
    # ======================================================

    elif any(word in text for word in [
        "fire",
        "fire safety",
        "building fire",
        "house fire",
        "fire emergency",
        "fire happens"
    ]):

        response = """
        <b>Fire Safety</b><br><br>

        • Raise the alarm and alert people nearby.<br>
        • Leave the building using the safest available exit.<br>
        • Never use elevators during a fire.<br>
        • If there is smoke, stay low while moving toward an exit.<br>
        • Call emergency services from a safe location.
        """


    # ======================================================
    # CYCLONE
    # ======================================================

    elif any(word in text for word in [
        "cyclone",
        "cyclone safety",
        "cyclone coming",
        "cyclone warning",
        "storm cyclone"
    ]):

        response = """
        <b>Cyclone Safety</b><br><br>

        • Stay indoors and away from windows.<br>
        • Secure loose objects around your home.<br>
        • Keep food, water and medicines ready.<br>
        • Charge your phone and power bank.<br>
        • Follow official weather and evacuation advisories.
        """


    # ======================================================
    # LANDSLIDE
    # ======================================================

    elif any(word in text for word in [
        "landslide",
        "land slide",
        "landslide safety",
        "landslide risk"
    ]):

        response = """
        <b>Landslide Safety</b><br><br>

        • Move away from steep slopes and unstable ground.<br>
        • Avoid roads blocked by mud, rocks or debris.<br>
        • Do not approach an active landslide area.<br>
        • Follow evacuation instructions from authorities.<br>
        • Stay alert during prolonged or heavy rainfall.
        """


    # ======================================================
    # ROAD DAMAGE
    # ======================================================

    elif any(word in text for word in [
        "road damage",
        "damaged road",
        "broken road",
        "unsafe road",
        "pothole",
        "potholes",
        "road is damaged",
        "road has damage"
    ]):

        response = """
        <b>Road Safety</b><br><br>

        • Avoid the damaged road whenever possible.<br>
        • Use an alternative safe route.<br>
        • Slow down and maintain extra distance if you must pass nearby.<br>
        • Report the exact location of serious damage to authorities.<br>
        • Keep pedestrians away from dangerous areas.
        """


    # ======================================================
    # FIRST AID
    # ======================================================

    elif any(word in text for word in [
        "first aid",
        "injured",
        "injury",
        "someone is injured",
        "person is injured"
    ]):

        response = """
        <b>First Aid Guidance</b><br><br>

        • First make sure the area is safe.<br>
        • For serious injuries, contact emergency services immediately.<br>
        • Avoid unnecessarily moving someone with a suspected serious injury.<br>
        • Follow instructions from trained medical professionals.
        """


    # ======================================================
    # EMERGENCY NUMBERS
    # ======================================================

    elif any(word in text for word in [
        "emergency number",
        "emergency numbers",
        "emergency contact",
        "emergency contacts",
        "help number"
    ]):

        response = """
        <b>Emergency Assistance</b><br><br>

        In India, <b>112</b> is the national emergency
        response number.<br><br>

        For disaster situations, also follow instructions
        from local authorities and official emergency alerts.
        """


    # ======================================================
    # SHELTER
    # ======================================================

    elif any(word in text for word in [
        "shelter",
        "relief camp",
        "safe place",
        "evacuation centre",
        "evacuation center",
        "where can i stay"
    ]):

        response = """
        <b>Emergency Shelter</b><br><br>

        Look for shelters or relief camps designated by
        your local administration.<br><br>

        If an evacuation order has been issued, use the
        officially designated evacuation route and shelter.
        """


    # ======================================================
    # GREETING
    # ======================================================

    elif any(word in text for word in [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]):

        response = """
        Hello! 👋<br><br>

        I am <b>DIVYA AI</b>, your Disaster Intelligence
        Assistant.<br><br>

        You can ask me about floods, earthquakes, fires,
        cyclones, landslides, road hazards, emergency
        preparedness and current weather conditions.
        """


    # ======================================================
    # DEFAULT
    # ======================================================

    else:

        response = """
        I'm not sure I understood that question.<br><br>

        You can ask me about:<br>

        • Flood safety<br>
        • Earthquake safety<br>
        • Fire safety<br>
        • Cyclones<br>
        • Landslides<br>
        • Damaged roads<br>
        • First aid<br>
        • Emergency contacts<br>
        • Shelters<br>
        • Rain probability<br>
        • Heavy rain<br>
        • Wind conditions<br>
        • Temperature<br>
        • Weather forecast
        """


    return render_template(
        "chatbot.html",
        user_message=message,
        bot_response=response
    )


# ==========================================================
# WEATHER FUNCTION
# ==========================================================

def get_weather_response(latitude, longitude):

    print("WEATHER FUNCTION CALLED")

    if not latitude or not longitude:

        print("NO LOCATION AVAILABLE")

        return """
        I need your location to provide local weather information.<br><br>

        Please allow location access in your browser and
        try again.
        """


    try:

        print(
            "REQUESTING WEATHER:",
            latitude,
            longitude
        )


        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}"
            f"&longitude={longitude}"
            "&current=temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "wind_speed_10m"
            "&hourly=precipitation_probability,"
            "precipitation,"
            "wind_speed_10m"
            "&forecast_days=1"
            "&timezone=auto"
        )


        weather_response = requests.get(
            url,
            timeout=10
        )


        print(
            "WEATHER API STATUS:",
            weather_response.status_code
        )


        weather_response.raise_for_status()


        data = weather_response.json()


        current = data.get(
            "current",
            {}
        )


        hourly = data.get(
            "hourly",
            {}
        )


        temperature = current.get(
            "temperature_2m"
        )

        humidity = current.get(
            "relative_humidity_2m"
        )

        precipitation = current.get(
            "precipitation"
        )

        wind = current.get(
            "wind_speed_10m"
        )


        rain_probability = hourly.get(
            "precipitation_probability",
            []
        )


        wind_forecast = hourly.get(
            "wind_speed_10m",
            []
        )


        max_rain = (
            max(rain_probability)
            if rain_probability
            else None
        )


        max_wind = (
            max(wind_forecast)
            if wind_forecast
            else None
        )


        # -------------------------------
        # Rain interpretation
        # -------------------------------

        if max_rain is None:

            rain_text = (
                "Rain probability is currently unavailable."
            )

        elif max_rain >= 70:

            rain_text = (
                f"🌧 <b>High chance of rain:</b> "
                f"up to {max_rain}% today."
            )

        elif max_rain >= 40:

            rain_text = (
                f"🌦 <b>Moderate chance of rain:</b> "
                f"up to {max_rain}% today."
            )

        else:

            rain_text = (
                f"☀️ <b>Low chance of rain:</b> "
                f"up to {max_rain}% today."
            )


        # -------------------------------
        # Wind interpretation
        # -------------------------------

        if max_wind is None:

            wind_text = (
                "Wind forecast is currently unavailable."
            )

        elif max_wind >= 50:

            wind_text = (
                f"💨 <b>Strong winds possible:</b> "
                f"up to {max_wind:.1f} km/h."
            )

        elif max_wind >= 30:

            wind_text = (
                f"💨 <b>Moderate to strong winds:</b> "
                f"up to {max_wind:.1f} km/h."
            )

        else:

            wind_text = (
                f"💨 <b>Light winds:</b> "
                f"up to {max_wind:.1f} km/h."
            )


        return f"""
        <b>Current Weather</b><br><br>

        🌡 <b>Temperature:</b>
        {temperature}°C<br>

        💧 <b>Humidity:</b>
        {humidity}%<br>

        🌧 <b>Current precipitation:</b>
        {precipitation} mm<br>

        💨 <b>Current wind:</b>
        {wind} km/h<br><br>

        {rain_text}<br>

        {wind_text}<br><br>

        <b>Safety advice:</b><br>

        If heavy rain or strong winds develop,
        avoid unnecessary travel and stay away from
        flood-prone areas, unstable structures and
        loose outdoor objects. Continue monitoring
        official weather and disaster alerts.
        """


    except Exception as e:

        print(
            "WEATHER ERROR:",
            repr(e)
        )


        return """
        I couldn't retrieve the current weather right now.
        Please try again in a moment and check official
        weather alerts for your area.
        """

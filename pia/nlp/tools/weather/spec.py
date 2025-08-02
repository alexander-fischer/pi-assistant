from typing import Any
import requests
from datetime import datetime
import i18n
from pia.config import LANGUAGE
from pia.nlp.tools.main import ToolResponse


def _get_geolocation(city_name: str):
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1, "language": LANGUAGE, "format": "json"}
    response = requests.get(geocoding_url, params=params)
    if response.status_code == 200:
        data = response.json()
    else:
        raise Exception(f"API status code: {response.status_code}")

    if not data.get("results") or len(data["results"]) < 1:
        raise Exception(f"The city {city_name} cannot be found.")

    return {
        "lat": data["results"][0]["latitude"],
        "lng": data["results"][0]["longitude"],
    }


def _call_openmeteo_weather_api(
    lat: float, lng: float, current: str = "", daily: str = ""
):
    open_meteo_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lng,
        "current": current,
        "daily": daily,
        "timezone": "auto",
    }
    response = requests.get(open_meteo_url, params=params)
    if response.status_code == 200:
        data = response.json()
    else:
        raise Exception(f"API status code: {response.status_code}")

    return data


def _merge_values_with_units(values: dict, units: dict):
    # merge values with units
    merged: dict[str, str] = {}
    for key in values:
        if key in units:
            merged[key] = f"{values[key]} {units[key]}"
        else:
            merged[key] = str(values[key])
    return merged


def _format_current_weather(data: dict[str, Any]):
    try:
        wind_direction_degrees = float(data["wind_direction_10m"])
        wind_direction = _convert_wind_direction(wind_direction_degrees)
    except:
        wind_direction = "unknown"

    wmo_code = data["weather_code"]
    wmo_description = _wmo_code_to_description(int(wmo_code))

    formatted_string = f"""
{i18n.t("weather")}: {wmo_description}
{i18n.t("temperature")}: {round(data['temperature_2m'])} {i18n.t('celsius')}
{i18n.t("wind_direction")}: {wind_direction}
{i18n.t("wind_speed")}: {round(data['wind_speed_10m'])} {i18n.t('kmh')}
{i18n.t("precipitation_probability")}: {data['precipitation_probability']}%
{i18n.t("uv_index")}: {round(data['uv_index'])}
    """.strip()

    return formatted_string


def _convert_to_weekday(date_str: str):
    date = datetime.strptime(date_str, "%Y-%m-%d")

    # Get the weekday number (0 = Monday, 6 = Sunday)
    weekday_number = date.weekday()
    weekday_mapping = {
        0: i18n.t("monday"),
        1: i18n.t("tuesday"),
        2: i18n.t("wednesday"),
        3: i18n.t("thursday"),
        4: i18n.t("friday"),
        5: i18n.t("saturday"),
        6: i18n.t("sunday"),
    }
    weekday = weekday_mapping[weekday_number]
    return weekday


from datetime import datetime, timedelta


def _format_weather_forecast(data):
    # Parse current date and compute tomorrow's date
    current_date_str = data["current"]["time"].split("T")[0]
    current_date = datetime.fromisoformat(current_date_str).date()
    tomorrow_date = current_date + timedelta(days=1)

    daily_data = data["daily"]

    report_lines = [i18n.t("weather_forecast")]
    for (
        date_str,
        weather_code,
        temp_max,
        temp_min,
        sunrise,
        sunset,
        uv_index,
        precip_prob,
        wind_speed,
        wind_dir,
    ) in zip(
        daily_data["time"],
        daily_data["weather_code"],
        daily_data["temperature_2m_max"],
        daily_data["temperature_2m_min"],
        daily_data["sunrise"],
        daily_data["sunset"],
        daily_data["uv_index_max"],
        daily_data["precipitation_probability_max"],
        daily_data["wind_speed_10m_max"],
        daily_data["wind_direction_10m_dominant"],
    ):
        date_obj = datetime.fromisoformat(date_str).date()
        if date_obj == current_date:
            day_label = i18n.t("today")
        elif date_obj == tomorrow_date:
            day_label = i18n.t("tomorrow")
        else:
            day_label = _convert_to_weekday(date_str)

        weather_description = _wmo_code_to_description(weather_code)
        wind_direction = _convert_wind_direction(wind_dir)

        # Extract only time from sunrise and sunset
        sunrise_time = sunrise.split("T")[1]
        sunset_time = sunset.split("T")[1]

        daily_report = (
            f"\n{day_label}:\n"
            f"{i18n.t('weather')}: {weather_description}\n"
            f"{i18n.t('max_temperature')}: {round(temp_max)} {i18n.t('celsius')}\n"
            f"{i18n.t('min_temperature')}: {round(temp_min)} {i18n.t('celsius')}\n"
            f"{i18n.t('sunrise')}: {sunrise_time}\n"
            f"{i18n.t('sunset')}: {sunset_time}\n"
            f"{i18n.t('max_uv_index')}: {round(uv_index)}\n"
            f"{i18n.t('max_precipitation_probability')}: {precip_prob}%\n"
            f"{i18n.t('max_wind_speed')}: {round(wind_speed)} {i18n.t('kmh')}\n"
            f"{i18n.t('wind_direction_main')}: {wind_direction}\n"
        )

        report_lines.append(daily_report)

    return "\n".join(report_lines)


def _convert_wind_direction(degrees):
    directions = [
        i18n.t("north"),
        i18n.t("north_northeast"),
        i18n.t("northeast"),
        i18n.t("east_northeast"),
        i18n.t("east"),
        i18n.t("east_southeast"),
        i18n.t("southeast"),
        i18n.t("south_southeast"),
        i18n.t("south"),
        i18n.t("south_southwest"),
        i18n.t("southwest"),
        i18n.t("west_southwest"),
        i18n.t("west"),
        i18n.t("west_northwest"),
        i18n.t("northwest"),
        i18n.t("north_northwest"),
    ]
    index = round(degrees / 22.5) % len(directions)
    return directions[index]


def _wmo_code_to_description(wmo_code: int):
    wmo_mapping = {
        0: i18n.t("clear_sky"),
        1: i18n.t("mainly_clear"),
        2: i18n.t("partly_cloudy"),
        3: i18n.t("overcast"),
        45: i18n.t("fog"),
        48: i18n.t("rime_fog"),
        51: i18n.t("drizzle_light"),
        53: i18n.t("drizzle_moderate"),
        55: i18n.t("drizzle_dense"),
        56: i18n.t("freezing_drizzle_light"),
        57: i18n.t("freezing_drizzle_dense"),
        61: i18n.t("rain_light"),
        63: i18n.t("rain_moderate"),
        65: i18n.t("rain_heavy"),
        66: i18n.t("freezing_rain_light"),
        67: i18n.t("freezing_rain_heavy"),
        71: i18n.t("snow_light"),
        73: i18n.t("snow_moderate"),
        75: i18n.t("snow_heavy"),
        77: i18n.t("snow_grains"),
        80: i18n.t("rain_showers_light"),
        81: i18n.t("rain_showers_moderate"),
        82: i18n.t("rain_showers_heavy"),
        85: i18n.t("snow_showers_light"),
        86: i18n.t("snow_showers_heavy"),
        95: i18n.t("thunderstorm_light_or_moderate"),
        96: i18n.t("thunderstorm_with_slight_hail"),
        99: i18n.t("thunderstorm_with_heavy_hail"),
    }

    return wmo_mapping.get(wmo_code, i18n.t("unknown"))


def get_current_weather(city: str) -> ToolResponse:
    lat_lng = _get_geolocation(city_name=city)
    params = "temperature_2m,weather_code,wind_speed_10m,wind_direction_10m,precipitation_probability,uv_index"
    current_data = _call_openmeteo_weather_api(
        lat=lat_lng["lat"], lng=lat_lng["lng"], current=params
    )

    current_weather_values = _merge_values_with_units(
        values=current_data["current"], units=current_data["current_units"]
    )
    current_weather_report = _format_current_weather(current_data["current"])
    tool_response = ToolResponse(message=current_weather_report, needs_rephrasing=True)
    return tool_response


def get_weather_forecast(city: str):
    lat_lng = _get_geolocation(city_name=city)
    params = "weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_probability_max,wind_speed_10m_max,wind_direction_10m_dominant"
    forecast_data = _call_openmeteo_weather_api(
        lat=lat_lng["lat"], lng=lat_lng["lng"], daily=params
    )

    forecast_report = _format_weather_forecast(forecast_data)
    tool_response = ToolResponse(message=forecast_report, needs_rephrasing=True)
    return tool_response

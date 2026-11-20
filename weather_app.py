import requests


def get_weather_description(code):
    weather_conditions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm"
                
    }
    return weather_conditions.get(code, "Unknown weather condition")


def get_weather(city):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count" : 1
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("Unable to connect to the server")
        return
    except requests.exceptions.Timeout:
        print("The request timed out")
        return
    except requests.exceptions.HTTPError:
        print("The server returned an HTTP error")
        return
    except requests.exceptions.RequestException:
        print("An unexpected request error occured")
        return



    data = response.json()
    results = data.get("results", [])
        
    if not results:
        print("No result found")
        return
        
    location = results[0]

    city_name = location["name"]
    country = location["country"]
    latitude = location["latitude"]
    longitude = location["longitude"]
        

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,relative_humidity_2m,"
        f"apparent_temperature,precipitation,weather_code,wind_speed_10m"
    )

    try:
        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
            
    except requests.exceptions.Timeout:
        print("The request timed out")
        return
    except requests.exceptions.ConnectionError:
        print("Connection failed")
        return
    except requests.exceptions.HTTPError:
        print("HTTP error occured")
        return
    except requests.exceptions.RequestException:
        print("unexpected error occured")
        return

    
    weather_data = weather_response.json()
    current = weather_data["current"]

    if not current:
        print("weather information is unavailable")
        return

    temperature = current["temperature_2m"]
    feels_like = current["apparent_temperature"]
    humidity = current["relative_humidity_2m"]
    precipitation = current["precipitation"]
    wind_speed = current["wind_speed_10m"]
    weather_code = current["weather_code"]

    weather_description = get_weather_description(weather_code)


    print("\n========== WEATHER REPORT ==========")
    print(f"City: {city_name}")
    print(f"Country: {country}")
    print("------------------------------------")
    print(f"Temperature: {temperature:.1f}°C")
    print(f"Feels Like: {feels_like:.1f}°C")
    print(f"Humidity: {humidity}%")
    print(f"Precipitation: {precipitation} mm")
    print(f"Wind Speed: {wind_speed:.1f} km/h")
    print(f"Weather Condition: {weather_description}")
    print("====================================")
                
# Future feature: Display humidity information
# Future feature: Display weather descriptions


def main():
    city = input("Enter a city: ").strip()

    if not city:
        print("Please enter a city name.")
        return
    
    get_weather(city)

if __name__ == "__main__":
    main()

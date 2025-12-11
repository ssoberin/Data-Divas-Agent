api_key="14eb71c084274841aa893453252211"

import requests
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class WeatherForecast:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('WEATHER_API_KEY')
        self.base_url = "https://api.weatherapi.com/v1"

    def get_tomorrow_forecast(self, city: str, days: int = 2) -> Optional[Dict[str, Any]]:

        try:
            url = f"{self.base_url}/forecast.json"
            params = {
                'key': self.api_key,
                'q': city,
                'days': days,
                'aqi': 'no',
                'alerts': 'no',
                'lang': 'ru'
            }

            print(f"🔗 Отправляем запрос: {url}")
            print(f"📋 Параметры: days={days}")

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            print(f"Получено дней прогноза: {len(data['forecast']['forecastday'])}")
            return self._extract_tomorrow_data(data)

        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса к WeatherAPI: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Ответ сервера: {e.response.text}")
            return None
        except Exception as e:
            print(f"Ошибка обработки данных: {e}")
            return None

    def _extract_tomorrow_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if 'forecast' not in data or 'forecastday' not in data['forecast']:
            raise ValueError("Некорректная структура данных от API")

        forecast_days = data['forecast']['forecastday']
        print(f"Доступно дней в ответе: {len(forecast_days)}")

        if len(forecast_days) < 2:
            print("В ответе только 1 день, используем сегодняшние данные для демонстрации")
            tomorrow_data = forecast_days[0]
            tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            tomorrow_data = forecast_days[1]
            tomorrow_date = tomorrow_data['date']

        forecast = {
            'date': tomorrow_date,
            'location': {
                'name': data['location']['name'],
                'region': data['location']['region'],
                'country': data['location']['country']
            },
            'day_forecast': {
                'max_temp_c': tomorrow_data['day']['maxtemp_c'],
                'min_temp_c': tomorrow_data['day']['mintemp_c'],
                'avg_temp_c': tomorrow_data['day']['avgtemp_c'],
                'condition': tomorrow_data['day']['condition']['text'],
                'max_wind_kph': tomorrow_data['day']['maxwind_kph'],
                'total_precip_mm': tomorrow_data['day']['totalprecip_mm'],
                'avg_humidity': tomorrow_data['day']['avghumidity'],
                'chance_of_rain': tomorrow_data['day']['daily_chance_of_rain'],
                'chance_of_snow': tomorrow_data['day']['daily_chance_of_snow'],
                'uv_index': tomorrow_data['day']['uv']
            },
            'astro': {
                'sunrise': tomorrow_data['astro']['sunrise'],
                'sunset': tomorrow_data['astro']['sunset'],
                'moonrise': tomorrow_data['astro']['moonrise'],
                'moonset': tomorrow_data['astro']['moonset'],
                'moon_phase': tomorrow_data['astro']['moon_phase']
            },
            'hourly_forecast': []
        }

        for hour_data in tomorrow_data['hour']:
            hour_forecast = {
                'time': hour_data['time'],
                'temp_c': hour_data['temp_c'],
                'condition': hour_data['condition']['text'],
                'wind_kph': hour_data['wind_kph'],
                'precip_mm': hour_data['precip_mm'],
                'humidity': hour_data['humidity'],
                'chance_of_rain': hour_data['chance_of_rain'],
                'chance_of_snow': hour_data['chance_of_snow'],
                'snow_cm': hour_data.get('snow_cm', 0)
            }
            forecast['hourly_forecast'].append(hour_forecast)

        return forecast

    def get_today_forecast(self, city: str) -> Optional[Dict[str, Any]]:
        try:
            url = f"{self.base_url}/forecast.json"
            params = {
                'key': self.api_key,
                'q': city,
                'days': 1,
                'aqi': 'no',
                'alerts': 'no',
                'lang': 'ru'
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            today_data = data['forecast']['forecastday'][0]

            return {
                'date': today_data['date'],
                'location': {
                    'name': data['location']['name'],
                    'region': data['location']['region'],
                    'country': data['location']['country']
                },
                'day_forecast': {
                    'max_temp_c': today_data['day']['maxtemp_c'],
                    'min_temp_c': today_data['day']['mintemp_c'],
                    'condition': today_data['day']['condition']['text'],
                    'total_precip_mm': today_data['day']['totalprecip_mm'],
                    'chance_of_rain': today_data['day']['daily_chance_of_rain'],
                    'chance_of_snow': today_data['day']['daily_chance_of_snow'],
                },
                'is_today': True
            }

        except Exception as e:
            print(f"Ошибка получения прогноза на сегодня: {e}")
            return None

    def get_snow_forecast_analysis(self, city: str, use_today: bool = False) -> Dict[str, Any]:

        if use_today:
            forecast = self.get_today_forecast(city)
            if forecast:
                forecast['is_tomorrow'] = False
        else:
            forecast = self.get_tomorrow_forecast(city)
            if not forecast and use_today:
                forecast = self.get_today_forecast(city)
                if forecast:
                    forecast['is_tomorrow'] = False

        if not forecast:
            return {}

        day_data = forecast['day_forecast']
        is_tomorrow = forecast.get('is_tomorrow', True)

        analysis = {
            'snow_expected': day_data['chance_of_snow'] > 50 and day_data['total_precip_mm'] > 1,
            'snow_removal_needed': False,
            'snow_height_cm': 0,
            'temperature_impact': '',
            'work_recommendations1': str,
            'work_recommendations2': str,
            'risk_level': 'low',
            'forecast_type': 'tomorrow' if is_tomorrow else 'today'
        }

        if day_data['chance_of_snow'] > 70:
            analysis['snow_height_cm'] = min(day_data['total_precip_mm'] * 1.5, 20)  # до 20 см
        elif day_data['chance_of_snow'] > 30:
            analysis['snow_height_cm'] = day_data['total_precip_mm'] * 0.8

        analysis['snow_removal_needed'] = analysis['snow_height_cm'] >= 5

        min_temp = day_data.get('min_temp_c', day_data['max_temp_c'] - 5)
        if min_temp < -15:
            analysis['temperature_impact'] = 'Экстремально низкая температура'
            analysis['risk_level'] = 'high'
        elif min_temp < -5:
            analysis['temperature_impact'] = 'Низкая температура'
            analysis['risk_level'] = 'medium'
        else:
            analysis['temperature_impact'] = 'Умеренная температура'

        if analysis['snow_removal_needed']:
            analysis['work_recommendations1']='Планировать уборку снега'
            if analysis['snow_height_cm'] > 10:
                analysis['work_recommendations2']='Увеличить количество техники'
        else:
            analysis['work_recommendations1']='Уборка снега не требуется'

        if day_data['chance_of_rain'] > 50:
            analysis['work_recommendations2']='Возможен дождь - ограничить работы'

        return {
            "plan_snow_or_no":analysis['work_recommendations1'],
            "extra": analysis['work_recommendations2'],
            "height_snow": analysis['snow_height_cm'],
            "needed":analysis['snow_removal_needed']
        }

    def get_current_weather(self, city: str) -> Optional[Dict[str, Any]]:
        try:
            url = f"{self.base_url}/current.json"
            params = {
                'key': self.api_key,
                'q': city,
                'aqi': 'no',
                'lang': 'ru'
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            return {
                'location': data['location']['name'],
                'temp_c': data['current']['temp_c'],
                'condition': data['current']['condition']['text'],
                'wind_kph': data['current']['wind_kph'],
                'humidity': data['current']['humidity']
            }

        except Exception as e:
            print(f"Ошибка получения текущей погоды: {e}")
            return None


def get_snow_forecast_analysis(city, use_today, api_key):
    wf = WeatherForecast(api_key)
    current = wf.get_current_weather(city)
    snow_analysis = wf.get_snow_forecast_analysis(city, use_today)

    return current, snow_analysis


def get_weather_data(city: str = "Kazan"):
    current, snow_analysis = get_snow_forecast_analysis(city, True, api_key)

    return {
        "current_temp": current["temp_c"] if current else None,
        "height": snow_analysis["height_snow"] if snow_analysis else None,
        "plan_snow": snow_analysis["plan_snow_or_no"] if snow_analysis else None,
        "extra": snow_analysis["extra"] if snow_analysis else None
    }


def get_height(city: str = "Kazan"):
    _, snow_analysis = get_snow_forecast_analysis(city, True, api_key)

    return snow_analysis["height_snow"]


def start_or_no(city: str = "Kazan"):
    _, snow_analysis = get_snow_forecast_analysis(city, True, api_key)

    return snow_analysis["needed"]
    #return True

#print(start_or_no(city="Kazan"))
#(get_height())


api_key="14eb71c084274841aa893453252211"

import requests
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

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
        """
        Получение прогноза погоды на следующий день

        Args:
            city: Город для прогноза (например, "Kazan")
            days: Количество дней прогноза (минимум 2 для получения завтра)

        Returns:
            Словарь с данными прогноза или None при ошибке
        """
        try:
            url = f"{self.base_url}/forecast.json"
            params = {
                'key': self.api_key,
                'q': city,
                'days': days,  # Меняем на 2 дня для получения завтра
                'aqi': 'no',
                'alerts': 'no',
                'lang': 'ru'
            }

            print(f"🔗 Отправляем запрос: {url}")
            print(f"📋 Параметры: days={days}")

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            print(f"✅ Получено дней прогноза: {len(data['forecast']['forecastday'])}")
            return self._extract_tomorrow_data(data)

        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка запроса к WeatherAPI: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"📄 Ответ сервера: {e.response.text}")
            return None
        except Exception as e:
            print(f"❌ Ошибка обработки данных: {e}")
            return None

    def _extract_tomorrow_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Извлечение данных на следующий день из ответа API"""

        # Проверяем наличие данных
        if 'forecast' not in data or 'forecastday' not in data['forecast']:
            raise ValueError("Некорректная структура данных от API")

        forecast_days = data['forecast']['forecastday']
        print(f"📅 Доступно дней в ответе: {len(forecast_days)}")

        # Если есть только сегодняшний день, используем его для демонстрации
        if len(forecast_days) < 2:
            print("⚠️  В ответе только 1 день, используем сегодняшние данные для демонстрации")
            tomorrow_data = forecast_days[0]
            # Имитируем дату завтрашнего дня
            tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            # Берем данные на завтра (второй элемент в массиве)
            tomorrow_data = forecast_days[1]
            tomorrow_date = tomorrow_data['date']

        # Форматируем данные
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

        # Добавляем почасовой прогноз
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
        """
        Получение прогноза на сегодня (альтернативный метод)
        """
        try:
            url = f"{self.base_url}/forecast.json"
            params = {
                'key': self.api_key,
                'q': city,
                'days': 1,  # Только сегодня
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
            print(f"❌ Ошибка получения прогноза на сегодня: {e}")
            return None

    def get_snow_forecast_analysis(self, city: str, use_today: bool = False) -> Dict[str, Any]:
        """
        Специальный анализ для системы уборки снега

        Args:
            city: Город для анализа
            use_today: Использовать сегодняшние данные если завтра недоступно

        Returns:
            Анализ погодных условий для планирования уборки снега
        """
        if use_today:
            forecast = self.get_today_forecast(city)
            if forecast:
                forecast['is_tomorrow'] = False
        else:
            forecast = self.get_tomorrow_forecast(city)
            if not forecast and use_today:
                # Если завтра нет, пробуем сегодня
                forecast = self.get_today_forecast(city)
                if forecast:
                    forecast['is_tomorrow'] = False

        if not forecast:
            return {}

        day_data = forecast['day_forecast']
        is_tomorrow = forecast.get('is_tomorrow', True)

        # Анализ условий для уборки снега
        analysis = {
            'snow_expected': day_data['chance_of_snow'] > 50 and day_data['total_precip_mm'] > 1,
            'snow_removal_needed': False,
            'snow_height_cm': 0,
            'temperature_impact': '',
            'work_recommendations': [],
            'risk_level': 'low',
            'forecast_type': 'tomorrow' if is_tomorrow else 'today'
        }

        # Расчет предполагаемой высоты снега (упрощенный)
        if day_data['chance_of_snow'] > 70:
            analysis['snow_height_cm'] = min(day_data['total_precip_mm'] * 1.5, 20)  # до 20 см
        elif day_data['chance_of_snow'] > 30:
            analysis['snow_height_cm'] = day_data['total_precip_mm'] * 0.8

        # Определение необходимости уборки
        analysis['snow_removal_needed'] = analysis['snow_height_cm'] >= 5

        # Влияние температуры
        min_temp = day_data.get('min_temp_c', day_data['max_temp_c'] - 5)
        if min_temp < -15:
            analysis['temperature_impact'] = 'Экстремально низкая температура'
            analysis['risk_level'] = 'high'
        elif min_temp < -5:
            analysis['temperature_impact'] = 'Низкая температура'
            analysis['risk_level'] = 'medium'
        else:
            analysis['temperature_impact'] = 'Умеренная температура'

        # Рекомендации по работам
        if analysis['snow_removal_needed']:
            analysis['work_recommendations'].append('Планировать уборку снега')
            if analysis['snow_height_cm'] > 10:
                analysis['work_recommendations'].append('Увеличить количество техники')
        else:
            analysis['work_recommendations'].append('Уборка снега не требуется')

        if day_data['chance_of_rain'] > 50:
            analysis['work_recommendations'].append('Возможен дождь - ограничить работы')

        return {
            'weather_forecast': forecast,
            'snow_analysis': analysis
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


# Тестирование
def run_weather_api():
    wf = WeatherForecast(api_key="14eb71c084274841aa893453252211")
    print("🧪 Тестирование WeatherAPI...")

    print("\n1. Текущая погода:")
    current = wf.get_current_weather('Kazan')
    if current:
        print(f"{current['location']}: {current['temp_c']}°C, {current['condition']}")
    else:
        print("Не удалось получить текущую погоду")
        return

    print("\n2. Прогноз для планирования уборки снега:")
    result = wf.get_snow_forecast_analysis('Kazan', use_today=True)

    if result:
        forecast = result['weather_forecast']
        analysis = result['snow_analysis']

        forecast_type = "завтра" if analysis['forecast_type'] == 'tomorrow' else "сегодня"
        print(f"📅 Дата ({forecast_type}): {forecast['date']}")
        print(
            f"🌡️ Температура: {forecast['day_forecast']['min_temp_c']}°C - {forecast['day_forecast']['max_temp_c']}°C")
        print(f"Погода: {forecast['day_forecast']['condition']}")
        print(f"Вероятность снега: {forecast['day_forecast']['chance_of_snow']}%")
        print(f"Осадки: {forecast['day_forecast']['total_precip_mm']} мм")
        print(f"Предполагаемая высота снега: {analysis['snow_height_cm']:.1f} см")
        print(f"Уборка требуется: {'Да' if analysis['snow_removal_needed'] else 'Нет'}")
        print(f"Уровень риска: {analysis['risk_level']}")

        print("\nРекомендации:")
        for rec in analysis['work_recommendations']:
            print(f"  • {rec}")

        if 'hourly_forecast' in forecast and forecast['hourly_forecast']:
            print(f"\n🕒 Почасовой прогноз (первые 3 часа):")
            for hour in forecast['hourly_forecast'][:3]:
                time = hour['time'].split(' ')[1][:5]
                print(f"  {time} - {hour['temp_c']}°C, {hour['condition']}")
    else:
        print("Не удалось получить прогноз")


if __name__ == "__main__":
    run_weather_api()
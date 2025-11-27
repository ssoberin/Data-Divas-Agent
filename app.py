from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import jinja2
from fastapi.staticfiles import StaticFiles
from WeatherAPI import run_weather_api
app = FastAPI()


templates = Jinja2Templates(directory="front")

from WeatherAPI import get_weather_data

app.mount("/front", StaticFiles(directory="front"), name="front")

@app.get("/")
def weather_page(request: Request):
    data = get_weather_data()
    return templates.TemplateResponse("hackathon.html", {
        "request": request,
        "weather": data
    })

@app.get("/analytics")
def get_analytics():
    return {"snow_cleaned_tons": 127, "machines_active": 5}

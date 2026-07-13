$ErrorActionPreference = "Stop"

$ProjectPath = "C:\Users\javier.minarro\projects\aemet-weather-intelligence"

Set-Location $ProjectPath

$env:PYTHONPATH = "$ProjectPath\src"

& "$ProjectPath\.venv\Scripts\python.exe" -m aemet_weather.pipeline
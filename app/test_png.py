import folium

# Tu clave API de OpenWeatherMap
API_KEY = "fef44739844a54913291dc1fbe1b82fe"

# Coordenadas de Madrid
lat, lon = 40.4168, -3.7038
zoom = 15

# Crear mapa centrado en Madrid
m = folium.Map(location=[lat, lon], zoom_start=zoom)

# Añadir capa de temperatura (puedes cambiarla más abajo)
tile_url = f"https://tile.openweathermap.org/map/temp_new/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}"
folium.TileLayer(
    tiles=tile_url,
    attr="OpenWeatherMap",
    name="Temperatura",
    overlay=True,
    control=True
).add_to(m)

# Añadir control de capas
folium.LayerControl().add_to(m)

# Guardar como HTML
m.save("mapa_madrid.html")
print("Mapa generado como 'mapa_madrid.html'")

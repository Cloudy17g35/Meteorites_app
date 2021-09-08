import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk
import os
cwd = os.getcwd()

# Preparing the data
df = pd.read_csv(cwd + '\\data.csv')
df.dropna(inplace=True)
df.GeoLocation = df.GeoLocation.str.replace("(", "").str.replace(")", "").str.split(",")
# Making a Python list to store the latitude and longitude
locations = df.GeoLocation.to_list()

latitude = []
longitude = []

for location in locations:
    latitude.append(float(location[0]))
    longitude.append(float(location[1]))

df["lat"] = latitude
df["lon"] = longitude
lat_lon = df[['lat', 'lon']]
# starting to work with the streamlit
st.header('Meteorites landings map')

if st.checkbox('Raw data:'):
    st.write(df)
# Showing the map of the meteorites landings
st.map(lat_lon)

# Making the plot of the top 5 biggest meteorites in Poland

# Setting the latitude and longitude of Poland and converting grams on kilograms
st.subheader('The bar chart of the biggest meteorites in Poland')
meteorites_poland = df[(df.lat.between(49, 54.50)) & (df.lon.between(14.07, 24.09))]
meteorites_poland = meteorites_poland.sort_values(by="mass (g)", ascending=False, ignore_index=True)
meteorites_poland = meteorites_poland.iloc[[0, 1, 5]]  # Choosing only Polish cities or villages names
meteorites_poland["mass (g)"] = meteorites_poland["mass (g)"] / 1000
meteorites_poland.rename(columns={"mass (g)": "mass (kg)"}, inplace=True)

# Plot making part
fig,ax = plt.subplots(figsize=(10, 12))
spines_loc = ["bottom", "right", "top", "left"]
ax.bar(meteorites_poland["name"], meteorites_poland["mass (kg)"], color="navy")
ax.text(0,320,"THE BIGGEST METEORITES IN POLAND", fontsize=26, weight="bold")
ax.set_xticklabels(meteorites_poland.name, fontsize=18)
ax.set_yticklabels(np.arange(0, 301, 50), fontsize=18)
ax.text(1.6, 310, "mass defined in kilograms", fontsize=18)
for location in spines_loc:
    ax.spines[location].set_visible(False)
st.pyplot(fig)

# Setting the map of the
st.subheader('Meteorites in Poland - 3D map')
st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',
                         initial_view_state=pdk.ViewState(
                             latitude= 52,
                             longitude=21,
                             zoom = 5,
                             pitch=50
                         ),
                        layers= [
                            pdk.Layer(
                                'HexagonLayer',
                                data=meteorites_poland,
                                get_position='[lon, lat]',
                                radius=500,
                                elevation_scale=50,
                                elevation_range=[0, 100000],
                                pickable=True,
                                extruded=True
                            ),
                            pdk.Layer('ScatterplotLayer',
                                      data=meteorites_poland,
                                      get_position = '[lon, lat]',
                                      get_color = '[200, 30, 0, 160]',
                                      get_radius = 20000
                                      ),
                        ],
                         ))

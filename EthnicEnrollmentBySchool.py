import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy.stats
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut
import random
import matplotlib.colors as c
from mpl_toolkits.mplot3d import Axes3D

# API KEY: AIzaSyAcJnPc1JCr1pL6s5wwIZkjvUp8m1_4NTQ

keys = ['AIzaSyB-v-NxQvjvYmdpYZwFOn0FnzvlSPDMWFs', 'AIzaSyAcJnPc1JCr1pL6s5wwIZkjvUp8m1_4NTQ', 'AIzaSyDcGu2-PbonAWOsgronndXKZCpVlARj07U']

geolocator = GoogleV3(api_key=keys[0])

df = pd.read_csv("Hillsborough_EthnicEnrollmentBySchool.csv")
# black:red
# hispanic:blue
# white: green
colors = []
latitudes = []
longtitudes = []
maxArray = []


def mk_maxArray():
    for i in range(len(df["NAME"])):
        maxArray.append(max(df['BLACKPROP'][i], df['HISPANICPROP'][i], df['WHITEPROP'][i]))

mk_maxArray()


def address2latlong(dataframe):
    addresses = dataframe["ADDRESS"]
    for i in range(len(addresses)):
        address = addresses[i]
        try:
            location = geolocator.geocode(address, timeout=10)

            if location is None:
                print(i+2, "Error on Address: ", address)
            else:
                print(i, ': ', location.latitude, location.longitude, address)
                #print("Progress: ", i*100/len(addresses), "%")
                latitudes.append(location.latitude)
                longtitudes.append(location.longitude)
        except GeocoderTimedOut as e:
            print("Error on Address:", address)
    print("Done.")


def max_ethnicgroup():
    for i in range(len(df["NAME"])):
        current_school = [df['BLACK'][i], df['HISPANIC'][i], df['WHITE'][i]]
        mayority = current_school.index(max(current_school))
        if mayority == 0:
            colors.append("r")
        elif mayority == 1:
            colors.append("b")
        elif mayority == 2:
            colors.append("g")


def plotting():
    for i in range(len(colors)):
        plt.scatter(df["Longitudes"][i], df["Latitudes"][i], color=colors[i])


def rgb_plotting():
    for i in range(len(colors)):
        plt.scatter(df["Longitudes"][i], df["Latitudes"][i], color=c.to_hex((df["BLACKPROP"][i], df["WHITEPROP"][i], df["HISPANICPROP"][i]), keep_alpha=False))


def rgb3D_plotting():
    for i in range(len(colors)):
        # ax.scatter(df["Longitudes"][i], df["Latitudes"][i], df["BLACKPROP"][i], color='r')
        # ax.scatter(df["Longitudes"][i], df["Latitudes"][i], df["WHITEPROP"][i], color='g')
        # ax.scatter(df["Longitudes"][i], df["Latitudes"][i], df["HISPANICPROP"][i], color='b')
        ax.scatter(np.array(df["Longitudes"][i]), np.array(df["Latitudes"][i]), np.array(maxArray[i]), color=colors[i])

def save_csvfile():
    df["Longitudes"] = longtitudes
    df["Latitudes"] = latitudes
    df.to_csv('Hillsborough_EthnicEnrollmentBySchool.csv', sep=',', encoding='utf-8')

max_ethnicgroup()
# address2latlong(df)
# save_csvfile()
# ----------------------------------------------------
plt.figure(1)
plt.title('Ethnic Map')
plt.xlabel('Latitude')
plt.ylabel('Longitude')

# black:red
# hispanic:blue
# white: green
red_patch = mpatches.Patch(color='red', label='Black')
green_patch = mpatches.Patch(color='green', label='White')
blue_patch = mpatches.Patch(color='blue', label='Hispanic')
plt.legend(handles=[red_patch, green_patch, blue_patch])
plotting()
# ----------------------------------------------------
plt.figure(2)
plt.title('RGB Ethnic Map')
plt.xlabel('Latitude')
plt.ylabel('Longitude')

# black:red
# hispanic:blue
# white: green
red_patch = mpatches.Patch(color='red', label='Black')
green_patch = mpatches.Patch(color='green', label='White')
blue_patch = mpatches.Patch(color='blue', label='Hispanic')
plt.legend(handles=[red_patch, green_patch, blue_patch])

rgb_plotting()
# -------------------------------------------------------

fig = plt.figure(3)
ax = fig.add_subplot(111, projection='3d')

plt.title('RGB 3D Ethnic Map')

ax.set_ylabel('Longitude')
ax.set_xlabel('Latitude')
ax.set_zlabel('Proportion')

# black:red
# hispanic:blue
# white: green
red_patch = mpatches.Patch(color='red', label='Black')
green_patch = mpatches.Patch(color='green', label='White')
blue_patch = mpatches.Patch(color='blue', label='Hispanic')
plt.legend(handles=[red_patch, green_patch, blue_patch])

rgb3D_plotting()


plt.show()

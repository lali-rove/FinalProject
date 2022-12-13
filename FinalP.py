import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


def read(file):
    return pd.read_csv(file)


def Intro():
    st.image('intro.jpg')
    st.title("Welcome to the Skyscraper's Database!")


def materials():
    dfx = pd.read_csv("Skyscrapers_2021.csv")
    materials_list = []
    for ind, row in dfx.iterrows():
        if row['MATERIAL'] not in materials_list:
            materials_list.append(row['MATERIAL'])
    materials_list.sort()
    return materials_list


def floors(dataframe):
    floor_list = []
    height_list = []
    for ind, row in dataframe.iterrows():
        floor_list.append(row['Floors'])
    for ind, row in dataframe.iterrows():
        height_list.append(row['In Feet'])
    return floor_list, height_list


def skyscraperNames():
    dfx = read('Skyscrapers_2021.csv')
    skyNames_list = []
    for ind, row in dfx.iterrows():
        if row['name'] not in skyNames_list:
            skyNames_list.append(row['name'])
    skyNames_list.sort()
    return skyNames_list


def ScatterPlot(dataframe, FRange):
    if FRange == 'Low':
        df3 = df2[(df2.Floors >= 50) & (df2.Floors <= 80)]
        floor_list, height_list = floors(df3)
        fig, ax = plt.subplots()
        ax.scatter(floor_list, height_list, color='purple')
        ax.set_xlabel('No. of Floors')
        ax.set_ylabel('Height in Feet')
        ax.set_title('Skyscraper Scatter Plot')
        st.pyplot(fig)
    elif FRange == 'Mid':
        df3 = df2[(df2.Floors >= 81) & (df2.Floors <= 99)]
        floor_list, height_list = floors(df3)
        fig, ax = plt.subplots()
        ax.scatter(floor_list, height_list, color='coral')
        ax.set_xlabel('No. of Floors')
        ax.set_ylabel('Height in Feet')
        ax.set_title('Skyscraper Scatter Plot')
        st.pyplot(fig)
    elif FRange == 'High':
        df3 = df2[df2.Floors >= 100]
        floor_list, height_list = floors(df3)
        fig, ax = plt.subplots()
        ax.scatter(floor_list, height_list, color='pink')
        ax.set_xlabel('No. of Floors')
        ax.set_ylabel('Height in Feet')
        ax.set_title('Skyscraper Scatter Plot')
        st.pyplot(fig)


# SideBar Menu
st.sidebar.image("SkyData.jpg")  # Used the image as a title, looks good
st.sidebar.header("Learn about Skyscrapers")
pages = st.sidebar.selectbox("Menu of options:",
                             ["HomePage", "Complete Data Set", "Map with Location of Skyscrapers",
                              "Charts by Materials", "Scatter Plot", "Website Links"])

# Homepage
if pages == "HomePage":
    Intro()
    st.header("To select different pages click on the SideBar. But while you are here... "
              "Why not enjoy a timelapse of some skyscrapers in New York?")
    st.video('video.mp4')

# Complete Data Set
if pages == "Complete Data Set":
    Intro()
    st.header("Complete Data Set of Skyscrapers")
    df = read('Skyscrapers_2021.csv')
    st.write(df)
    if st.checkbox("Click to display in alphabetical order"):
        df2 = df.sort_values('NAME')
        st.write(df2)
    if st.checkbox("Click here to display without rank order, and alphabetized by City"):
        df3 = df.sort_values('CITY')
        df4 = df3.drop(['RANK'], axis=1)
        st.write(df4)

# Map with locations
if pages == "Map with Location of Skyscrapers":
    Intro()
    st.header("Skyscrapers and their functions")
    df = pd.read_csv("Skyscrapers_2021.csv")
    df2 = df[['NAME', 'Latitude', 'Longitude', 'FUNCTION']]
    column_names = ('Skyscraper Name', 'lat', 'lon', 'Function')
    df2.columns = column_names
    st.subheader("The following is a dataframe and map displaying the location of the skyscrapers "
                 "categorized by their functions")
    option = st.selectbox(
        'Skyscrapers that serve which function would you like to see?',
        ('All', 'office', 'hotel', 'residential'))
    if "All" in option:
        st.write("DataFrame and Map of all the Skyscrapers")
        st.dataframe(df2)
        st.map(df2)
    else:
        st.write("DataFrame and Map of Skyscrapers functioning as ", option)
        df3 = df2.query("Function == @option")
        st.dataframe(df3)
        st.map(df3)

# Charts
if pages == 'Charts by Materials':
    Intro()
    df = pd.read_csv("Skyscrapers_2021.csv")
    df2 = df[['NAME', 'MATERIAL']]
    column_names = ('Skyscraper Name', 'Material')
    df2.columns = column_names
    material_list = materials()
    dict1 = {}
    sumOfSteel = 0
    sumOfConcrete = 0
    sumOfComposite = 0
    sumOfSC = 0
    st.header("Skyscrapers and what they are made of")
    st.subheader("The following DataFrame displays the skyscrapers and the materials used in them")
    st.dataframe(df2)
    # Making dictionaries
    for idx in df2.index:
        dict1[df2["Skyscraper Name"][idx]] = df2["Material"][idx]
    for keys in dict1:
        if dict1[keys] == 'composite':
            sumOfComposite += 1
        elif dict1[keys] == 'concrete':
            sumOfConcrete += 1
        elif dict1[keys] == 'steel':
            sumOfSteel += 1
        else:
            sumOfSC += 1
    data = [sumOfComposite, sumOfConcrete, sumOfSteel, sumOfSC]
    st.subheader("The following charts display the quantity of skyscrapers and the materials used in them")
    option = st.multiselect(
        'How would you like to see the information?',
        ('Line Graph', 'Pie Chart', 'Bar Chart'))
    if "Line Graph" in option:
        st.write("You selected line graph")
        fig, ax = plt.subplots()
        ax.plot(material_list, data, color='r', linestyle='dashed', linewidth=7)
        ax.set_xlabel('Materials')
        ax.set_ylabel('Quantity')
        ax.set_title('Skyscraper Line Graph')
        st.pyplot(fig)
    if "Pie Chart" in option:
        st.write("You selected Pie Chart")
        colors = ['cyan', 'yellow', 'magenta', 'green']
        fig, ax = plt.subplots()
        ax.pie(data, labels=material_list, colors=colors, autopct='%1.2f')
        ax.set_title('Skyscraper Pie Chart')
        st.pyplot(fig)
    if "Bar Chart" in option:
        st.write("You selected Bar Chart")
        fig, ax = plt.subplots()
        ax.bar(range(len(data)), data, color='cyan')
        ax.set_xlabel('Materials')
        ax.set_ylabel('Quantity')
        ax.set_title('Skyscraper Bar Chart')
        ax.set_xticks(range(len(data)))
        ax.set_xticklabels(material_list)
        st.pyplot(fig)

# Scatter Plot
if pages == 'Scatter Plot':
    Intro()
    df = pd.read_csv("Skyscrapers_2021.csv")
    df2 = df[['NAME', 'Height', 'Meters', 'Feet', 'FLOORS']]
    st.subheader("The following DataFrame displays information about the height and number of floors of each skyscraper")
    column_names = ('Skyscraper Name', 'Height', 'In Meters', 'In Feet', 'Floors')
    df2.columns = column_names
    df2 = df2.sort_values('Floors')
    st.dataframe(df2)
    st.subheader(
        "The following scatter plot displays height(in feet) and number of floors of skyscrapers according to their range")
    floorRange = st.radio("What range are you interested in exploring?",
                          ('Low: 50-80 floors', 'Mid: 81-99', 'High: 100+'))
    if floorRange == 'Low: 50-80 floors':
        st.write('You selected the low range.')
        ScatterPlot(df2, "Low")
    elif floorRange == 'Mid: 81-99':
        st.write('You selected the mid range.')
        ScatterPlot(df2, "Mid")
    else:
        st.write("You selected the high range.")
        ScatterPlot(df2, "High")

# Website Links
if pages == 'Website Links':
    Intro()
    df = pd.read_csv("Skyscrapers_2021.csv")
    df2 = df[['NAME', 'Link']]
    column_names = ('Skyscraper Name', 'Website Link')
    df2.columns = column_names
    st.subheader("This page contains the website link for each skyscraper")
    for names, links in zip(df2['Skyscraper Name'], df2['Website Link']):
        st.write(names, links)


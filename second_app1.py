import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import openpyxl
warnings.filterwarnings('ignore')

st.set_page_config(page_title= "First_streamlit app!!!", page_icon= ":bar_chart", layout="wide")
#display page title
st.title(":new_moon_with_face: Mark's Second Streamlit app")
#Using CSS to customise the site
st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)

#@st.cache(allow_output_mutation = True)
#def load_data(file_name):
#  nlp = spacy.load(file_name)
#  return (nlp)
#nlp = load_data("en_core_web_lg")

@st.cache_data
def read_file(file):
  """
  Reads a file based on its extension using appropriate pandas functions.

  Args:
      file (streamlit.UploadedFile): The uploaded file object.

  Returns:
      pandas.DataFrame: The data from the uploaded file, or None if an error occurs.
  """

  filename = file.name
  file_extension = filename.split(".")[-1]

  try:
    if file_extension.lower() == "csv":
      df = pd.read_csv(file, encoding="ISO-8859-1")
    elif file_extension.lower() in ("xlsx", "xls"):
      df = pd.read_excel(file)
    elif file_extension.lower() == "txt":
      # Handle text files (consider delimiters, headers, etc.)
      df = pd.read_csv(file, sep="\t", header=None, names=["text"])  # Example configuration
    else:
      st.error(f"Unsupported file type: {file_extension}")
      return None

    st.success(f"Successfully read file: {filename}")
    return df
  except Exception as e:
    st.error(f"Error reading file: {e}")
    return None

@st.cache_data
def open_predefined_file(file_name):
  os.chdir(r"C:\Users\ABAASA\OneDrive\Desktop\mark\projects\Sreamlit")
  df = pd.read_excel(file_name)
  return df



# Checkbox for user selection
#use_predefined_file = st.checkbox("Use pre-defined file (NEW April.xlsx)")

# File upload functionality
file = st.file_uploader(":file_folder: Please upload your files here", type=None)  # Allow all types
if file is not None:
   data = read_file(file)

if data is not None:
  # Process the data from the DataFrame (e.g., print, visualize)
  st.write(data.head())  # Print the first few rows
else:
  st.info("No file uploaded or selected.")


filtered_df = data.copy()
selected_agents = st.sidebar.multiselect ("Filter by Agent", data["Agent"].unique())
selected_amounts = st.sidebar.multiselect ("Filter by Amount", data["Amount"].unique())

if selected_agents:
  filtered_df = filtered_df[filtered_df['Agent'].isin(selected_agents)]

if selected_amounts:
  filtered_df = filtered_df[filtered_df['Amount'].isin(selected_amounts)]

#filter by date
#select_date_range = st.checkbox("Select from a range of dates")
filter_options = ["Select a specific date", "Select from a range of dates"]
selected_filter = st.selectbox("Choose specific date or a range of dates", filter_options)

#selectdate = st.checkbox("Select a specific date")
filtered_df["Date"] = pd.to_datetime(filtered_df["Date"])

if selected_filter == "Select from a range of dates":
  #Getting the minimum and maximum date (start and end)
  startDate = pd.to_datetime(filtered_df["Date"]).min()
  endDate = pd.to_datetime(filtered_df["Date"]).max()

  col1, col2 = st.columns((2))

  with col1:
      date1 = pd.to_datetime(st.date_input("Start Date", startDate))

  with col2:
      date2 = pd.to_datetime(st.date_input("End Date", endDate))

  filtered_df = filtered_df[(filtered_df["Date"]>= date1) & (filtered_df["Date"] <= date2)].copy()
  
  #display the date in the range of dates selected by user
  st.write(filtered_df)


if selected_filter == "Select a specific date":
  selected_date = pd.to_datetime(filtered_df["Date"])

  if not pd.isna(selected_date).all():  # Check if all elements are null
    if not filtered_df.empty:  # Check if filtered_df is not empty
      default_date = pd.to_datetime(filtered_df["Date"]).mean()
      date = pd.to_datetime(st.date_input("Select Date", default_date))
      filtered_df = filtered_df[filtered_df["Date"] == date].copy()
      st.write(filtered_df)
    else:
      st.warning("No data to filter by date.")  # Optional message for empty DataFrame
  else:
    # Handle case where selected_date is empty (optional)
    st.warning("Please select a date.")
else:
  print("Nothing here man, everything has refused, just restart the thing")


#enter this in the command prompt/terminal to run app
#streamlit run c:/Users/ABAASA/OneDrive/Desktop/mark/projects/Sreamlit/second_app.py

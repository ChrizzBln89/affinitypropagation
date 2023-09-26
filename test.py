import streamlit as st

# Create a sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page:", ["Home", "About", "Contact"])

# Define the content for each page
if page == "Home":
    st.title("Welcome to the Home Page")
    st.write("This is the home page of your Streamlit app.")
    # Add more content or functionality specific to the home page here.

elif page == "About":
    st.title("About Us")
    st.write("This is the about page of your Streamlit app.")
    # Add more content or functionality specific to the about page here.

elif page == "Contact":
    st.title("Contact Us")
    st.write("This is the contact page of your Streamlit app.")
    # Add more content or functionality specific to the contact page here.

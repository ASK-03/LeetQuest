import streamlit as st
import pandas as pd
import math

# Load the data from the JSON file
@st.cache_data
def load_data():
    data = pd.read_json("data.json")
    data['Rating'] = data['Rating'].map(math.floor)
    return data

# Pagination function
def paginate_data(data, page, items_per_page):
    start = page * items_per_page
    end = start + items_per_page
    return data[start:end]

# Streamlit App
def main():
    st.title("Rating-Based Question Viewer")
    
    # Load data
    data = load_data()

    # Input widgets for rating range
    st.sidebar.header("Filter by Rating")
    min_rating = st.sidebar.number_input("Minimum Rating", value=1800, step=50)
    max_rating = st.sidebar.number_input("Maximum Rating", value=2000, step=50)
    
    # Filter the data based on the rating range
    filtered_data = data[(data['Rating'] >= min_rating) & (data['Rating'] <= max_rating)]

    # Paginate filtered data
    items_per_page = 10
    total_items = len(filtered_data)
    total_pages = (total_items - 1) // items_per_page + 1

    st.sidebar.header("Pagination")
    page = st.sidebar.number_input("Page", min_value=1, max_value=total_pages, value=1) - 1

    # Display paginated data
    paginated_data = paginate_data(filtered_data, page, items_per_page)
    st.write(f"Displaying page {page + 1} of {total_pages}")
    st.write(paginated_data[['Rating', 'ID', 'Title', 'ContestSlug']])

    # # Additional details for each problem
    # st.markdown("### Problem Details")
    # for _, row in paginated_data.iterrows():
    #     st.markdown(f"""
    #     - **Title**: {row['Title']}
    #     - **Rating**: {row['Rating']}
    #     - **Contest**: {row['ContestSlug']}
    #     - **Problem Index**: {row['ProblemIndex']}
    #     """)

if __name__ == "__main__":
    main()

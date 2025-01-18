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

# Generate LeetCode problem link
def generate_leetcode_link(title_slug):
    base_url = "https://leetcode.com/problems/"
    return f"{base_url}{title_slug}/description/"

# Streamlit App
def main():
    st.title("Rating-Based Question Viewer")

    # Load data
    data = load_data()

    # Input widgets for rating range
    st.sidebar.header("Filter by Rating")
    min_rating = st.sidebar.number_input("Minimum Rating", value=1800, step=50)
    max_rating = st.sidebar.number_input("Maximum Rating", value=2000, step=50)

    # Sorting option
    st.sidebar.header("Sort Options")
    sort_order = st.sidebar.selectbox("Sort by Rating", ["Ascending", "Descending"])

    # Filter the data based on the rating range
    filtered_data = data[(data['Rating'] >= min_rating) & (data['Rating'] <= max_rating)]

    # Sort the data
    if sort_order == "Ascending":
        filtered_data = filtered_data.sort_values(by="Rating", ascending=True)
    else:
        filtered_data = filtered_data.sort_values(by="Rating", ascending=False)

    # Paginate filtered data
    items_per_page = 10
    total_items = len(filtered_data)
    total_pages = (total_items - 1) // items_per_page + 1

    st.sidebar.header("Pagination")
    page = st.sidebar.number_input("Page", min_value=1, max_value=total_pages, value=1) - 1

    # Display paginated data
    paginated_data = paginate_data(filtered_data, page, items_per_page)
    st.write(f"Displaying page {page + 1} of {total_pages}")

    # Add clickable links in the Title column
    paginated_data['Title'] = paginated_data.apply(
        lambda row: f'<a href="{generate_leetcode_link(row["TitleSlug"])}" target="_blank">{row["Title"]}</a>', 
        axis=1
    )

    # Display the table with HTML rendering for links
    st.write(
        paginated_data[['Rating', 'ID', 'Title', 'ContestSlug']].to_html(
            index=False, escape=False
        ),
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

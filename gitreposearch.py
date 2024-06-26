import streamlit as st
import requests
import time
import math
import os
import datetime

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve GitHub token from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

gitreposearch_logo = "./images/gitreposearch_logo.png"
gitreposearch_logo_width = 250

# Get the current date and time
current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# Create the "docs" directory if it doesn't exist
if not os.path.exists("docs"):
    os.makedirs("docs")

# Create the "templates" directory if it doesn't exist
if not os.path.exists("templates"):
    os.makedirs("templates")

# Create the "search-results" directory if it doesn't exist
if not os.path.exists("search-results"):
    os.makedirs("search-results")

# Home Page
def home():
    st.image(f"{gitreposearch_logo}", width=gitreposearch_logo_width)
    st.title('GitHub Repository Search Tool')
    st.markdown("A Streamlit app for searching GitHub repositories based on user criteria.<br>", unsafe_allow_html=True)
    st.markdown('---')
    st.sidebar.markdown("<small style='font-size: 0.8em;'>Version: 0.1.0</small>", unsafe_allow_html=True)

    # Create the search bar, radio button group, and search button layout
    search_criteria = st.text_input('Enter Your Search Criteria Here:')
    st.markdown('---')
    star_range = st.radio('Select The Range Of Stars:', ["Most Likes", "0-50 Stars", "50-100 Stars", "100-150 Stars", "150-200 Stars", "200-250 Stars", "250-500 Stars", "Greater Than 500 Stars"])
    st.markdown('---')
    include_forks = st.checkbox('Do Not Include Forked Repositories')
    st.markdown('---')
    search_button = st.button('Search GitHub Repositories')

    # Check if the search button is clicked
    if search_button:
        # Convert the star range to a GitHub API-compatible format
        stars_parameter = get_stars_parameter(star_range)
        include_forks = '' if include_forks else '+fork:false'
        search_github_and_save_markdown(search_criteria, GITHUB_TOKEN, stars_parameter, include_forks)

# Documentation Page
def documentation():
    st.image(f"{gitreposearch_logo}", width=gitreposearch_logo_width)
    st.title('GitHub Repo Search Documentation')
    st.sidebar.markdown("<small style='font-size: 0.8em;'>Version: 0.1.0</small>", unsafe_allow_html=True)

    # List all available .md files in the "docs" directory and its subdirectories
    docs_md_files = []
    for root, dirs, files in os.walk("docs"):
        for file in files:
            if file.endswith('.md'):
                docs_md_files.append(os.path.relpath(os.path.join(root, file), "docs"))

    # Strip ".md" extension from file names
    docs_md_files_stripped = [os.path.splitext(file)[0] for file in docs_md_files]

    # Move 'App-Instructions.md' to the front of the list if it exists
    if 'App-Instructions.md' in docs_md_files:
        docs_md_files_stripped.remove('App-Instructions')
        docs_md_files_stripped.insert(0, 'App-Instructions')

    # Dropdown to select .md file in the center of the page
    selected_file = st.selectbox('Select Documentation File:', docs_md_files_stripped)

    # Display selected .md file content in the main area
    if selected_file:
        selected_file_path = os.path.join("docs", f"{selected_file}.md")
        st.markdown(open(selected_file_path, 'r', encoding='utf-8').read())

# Templates Page
def templates():
    st.image(f"{gitreposearch_logo}", width=gitreposearch_logo_width)
    st.title('GitHub Support Templates')
    st.sidebar.markdown("<small style='font-size: 0.8em;'>Version: 0.1.0</small>", unsafe_allow_html=True)

    # List all available .md files in the "templates" directory and its subdirectories
    templates_md_files = []
    for root, dirs, files in os.walk("templates"):
        for file in files:
            if file.endswith('.md'):
                templates_md_files.append(os.path.relpath(os.path.join(root, file), "templates"))

    # Strip ".md" extension from file names
    templates_md_files_stripped = [os.path.splitext(file)[0] for file in templates_md_files]

    # Move 'Templates-Instructions.md' to the front of the list if it exists
    if 'Template-Instructions.md' in templates_md_files:
        templates_md_files_stripped.remove('Template-Instructions')
        templates_md_files_stripped.insert(0, 'Template-Instructions')

    # Dropdown to select .md file in the center of the page
    selected_file = st.selectbox('Select Templates File:', templates_md_files_stripped)

    # Display selected .md file content in the main area
    if selected_file:
        selected_file_path = os.path.join("templates", f"{selected_file}.md")
        st.markdown(open(selected_file_path, 'r', encoding='utf-8').read())

# Search Results Page
def search_results():
    st.image(f"{gitreposearch_logo}", width=gitreposearch_logo_width)
    st.title('Your Search Results')
    st.sidebar.markdown("<small style='font-size: 0.8em;'>Version: 0.1.0</small>", unsafe_allow_html=True)

    # List all available .md files in the "search-results" directory
    search_result_files = []
    for file in os.listdir("search-results"):
        if file.endswith('.md'):
            search_result_files.append(file)

    # Strip ".md" extension from file names
    search_result_files_stripped = [os.path.splitext(file)[0] for file in search_result_files]

    # Dropdown to select .md file in the center of the page
    selected_file = st.selectbox('Select Your Search To Review:', search_result_files_stripped)

    # Display selected .md file content in the main area
    if selected_file:
        selected_file_path = os.path.join("search-results", f"{selected_file}.md")
        st.markdown(open(selected_file_path, 'r', encoding='utf-8').read())

# Function to search GitHub and save markdown
def search_github_and_save_markdown(search_criteria, github_token, stars_parameter, include_forks):
    # Initialize variables for pagination
    per_page = 100  # Maximum items per page for GitHub API
    page = 1
    total_repositories = []

    # Add forks parameter to the GitHub API query if include_forks checkbox is checked
    forks_parameter = '' if include_forks else '+fork:false'
    query_parameters = stars_parameter + forks_parameter

    # Report the total number of pages for the search criteria
    total_pages = get_total_pages(search_criteria, per_page, github_token, query_parameters)
    st.write(f"#### [{total_pages}] Total Pages For '{search_criteria}'")

    if total_pages == 0:
        st.write("No Repositories Found For The Given Search Criteria.")
        return

    while page <= total_pages:
        # Define GitHub API endpoint for repository search
        api_url = f"https://api.github.com/search/repositories?q={search_criteria}+{query_parameters}&per_page={per_page}&page={page}"

        try:
            # Send GET request to GitHub API
            response = requests.get(api_url, headers={"Authorization": f"token {github_token}"})

            response.raise_for_status()  # Raise an exception for any other HTTP error

            # Parse JSON response
            data = response.json()

            # Extract repositories from current page
            repositories = data.get('items', [])

            if repositories:
                total_repositories.extend(repositories)
                st.write(f"Processed Page {page}/{total_pages}")
            else:
                break  # Exit the loop if no more repositories on subsequent pages

            page += 1  # Move to the next page for pagination

            # time.sleep(1)  # Wait for 1 second before making the next request
        except requests.exceptions.RequestException as e:
            st.write(f"Error Occurred: {e}")
            break

    if total_repositories:
        # Create Markdown content
        markdown_content = f"---\n"
        markdown_content += f"### [ {search_criteria} ]\n"
        markdown_content += f"#### Summary\n"
        markdown_content += f"###### Date/Timestamp: {current_datetime}\n"  # Add timestamp here
        markdown_content += f"###### Total Repositories In Your Search: {len(total_repositories)}\n"
        markdown_content += f"---\n"

        for repo in total_repositories:
            repo_name = repo.get('full_name', '')
            repo_url = repo.get('html_url', '')
            repo_description = repo.get('description', '')

            # Format repository information in Markdown syntax
            markdown_content += f"##### [{repo_name}]({repo_url})\n"
            markdown_content += f"###### DESCRIPTION:\n"
            markdown_content += f"- ###### {repo_description}\n"
            markdown_content += f"---\n"

        # Save Markdown content to file in the "docs" directory and its subdirectories
        file_name = f"search-results/{search_criteria}_{current_datetime}.md"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(markdown_content)
        st.write(f"Markdown File '{file_name}' With Complete Repository List And Summary Saved Successfully.")
    else:
        st.write("No Repositories Found For The Given Search Criteria.")

# Function to get total pages from GitHub API
def get_total_pages(search_criteria, per_page, github_token, query_parameters):
    # Define GitHub API endpoint for getting total count of repositories
    total_count_api_url = f"https://api.github.com/search/repositories?q={search_criteria}+{query_parameters}&per_page=1"

    try:
        # Send GET request to GitHub API
        response = requests.get(total_count_api_url, headers={"Authorization": f"token {github_token}"})
        response.raise_for_status()  # Raise an exception for any HTTP error

        # Parse JSON response
        data = response.json()

        # Extract total count of repositories
        total_count = data.get('total_count', 0)

        # Calculate total pages based on total count and items per page
        total_pages = math.ceil(total_count / per_page)

        return total_pages
    except requests.exceptions.RequestException as e:
        st.write(f"Error Occurred While Getting Total Pages: {e}")
        return 0

# Function to convert star range to GitHub API-compatible format
def get_stars_parameter(star_range):
    if star_range == "Most Likes":
        return '+sort:stars-desc'
    elif star_range == "0-50 Stars":
        return '+stars:0..50'
    elif star_range == "50-100 Stars":
        return '+stars:50..100'
    elif star_range == "100-150 Stars":
        return '+stars:100..150'
    elif star_range == "150-200 Stars":
        return '+stars:150..200'
    elif star_range == "200-250 Stars":
        return '+stars:200..250'
    elif star_range == "250-500 Stars":
        return '+stars:250..500'
    elif star_range == "Greater Than 500 Stars":
        return '+stars:>500'
    else:
        return ''

# Navigation
nav_options = {
    'Home': home,
    'Documentation': documentation,
    'Templates': templates,
    'Search Results': search_results
}

selected_page = st.sidebar.selectbox('Menu', list(nav_options.keys()))
nav_options[selected_page]()
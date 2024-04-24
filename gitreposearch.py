import streamlit as st
import requests
import time
import math
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve GitHub token from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Create the "docs" directory if it doesn't exist
if not os.path.exists("docs"):
    os.makedirs("docs")

# Create the "templates" directory if it doesn't exist
if not os.path.exists("templates"):
    os.makedirs("templates")

# Create the "search-results" directory if it doesn't exist
if not os.path.exists("search-results"):
    os.makedirs("search-results")

# Function to search GitHub and save markdown
def search_github_and_save_markdown(search_criteria, github_token):
    # Initialize variables for pagination
    per_page = 100  # Maximum items per page for GitHub API
    page = 1
    total_repositories = []

    # Report the total number of pages for the search criteria
    total_pages = get_total_pages(search_criteria, per_page, github_token)
    st.write(f"#### [{total_pages}] Total Pages For '{search_criteria}'")

    if total_pages == 0:
        st.write("No Repositories Found For The Given Search Criteria.")
        return

    while page <= total_pages:
        # Define GitHub API endpoint for repository search
        api_url = f"https://api.github.com/search/repositories?q={search_criteria}&per_page={per_page}&page={page}"

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

            time.sleep(1)  # Wait for 1 second before making the next request
        except requests.exceptions.RequestException as e:
            st.write(f"Error Occurred: {e}")
            break

    if total_repositories:
        # Create Markdown content
        markdown_content = f"---\n"
        markdown_content += f"### [ {search_criteria} ]\n"
        markdown_content += f"#### Summary\n"
        markdown_content += f"###### Total Repositories On GitHub: {len(total_repositories)}\n"
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
        file_name = f"search-results/{search_criteria}.md"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(markdown_content)
        st.write(f"Markdown File '{file_name}' With Complete Repository List And Summary Saved Successfully.")
    else:
        st.write("No Repositories Found For The Given Search Criteria.")

# Function to get total pages from GitHub API
def get_total_pages(search_criteria, per_page, github_token):
    # Define GitHub API endpoint for getting total count of repositories
    total_count_api_url = f"https://api.github.com/search/repositories?q={search_criteria}&per_page=1"

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

# Home Page
def home():
    st.title('GitHub Repository Search Tool')
    st.markdown("<small style='font-size: 0.8em;'>Date: 2024-04-24</small><br><small style='font-size: 0.8em;'>Version: 0.1.0</small>", unsafe_allow_html=True)
    # Create the search bar and search button layout
    search_criteria = st.text_input('Enter Search Criteria For GitHub Repositories:')
    search_button = st.button('Search')
    # Check if the search button is clicked
    if search_button:
        search_github_and_save_markdown(search_criteria, GITHUB_TOKEN)

# Documentation Page
def documentation():
    st.title('Documentation')

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
    st.title('Templates')

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
    st.title('Search Results')

    # List all available .md files in the "search-results" directory
    search_result_files = []
    for file in os.listdir("search-results"):
        if file.endswith('.md'):
            search_result_files.append(file)

    # Strip ".md" extension from file names
    search_result_files_stripped = [os.path.splitext(file)[0] for file in search_result_files]

    # Dropdown to select .md file in the center of the page
    selected_file = st.selectbox('Select Search To Review:', search_result_files_stripped)

    # Display selected .md file content in the main area
    if selected_file:
        selected_file_path = os.path.join("search-results", f"{selected_file}.md")
        st.markdown(open(selected_file_path, 'r', encoding='utf-8').read())

# Navigation
nav_options = {
    'Home': home,
    'Documentation': documentation,
    'Templates': templates,
    'Search Results': search_results
}

selected_page = st.sidebar.selectbox('Menu', list(nav_options.keys()))
nav_options[selected_page]()

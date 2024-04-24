### Installation

#### 1. Clone the GitHub Repository Search App from the repository link.

    git clone https://github.com/arch3angel/gitreposearch.git

#### 2. Navigate to the project directory.

    cd gitreposearch

#### 3. Initialize the project with Poetry.

    poetry init

Follow the prompts to fill in the project details such as name, version, description, etc.

#### 4. Install the required dependencies using Poetry.

    poetry install

#### 5. Run the Streamlit app.

    streamlit run gitreposearch.py

#### Usage

1. Enter your GitHub Token in the app for authentication.
2. Enter your search criteria in the input box provided.
3. Click the "Search" button to execute the search.
4. View the search results and summary in the main area.
5. Use the dropdown in the left sidebar to select and view previously saved Markdown files.

#### Dependencies

* Python 3.12
* Streamlit
* Requests
* Time
* Math
* OS
* Python-Dotenv
* Altair
* Poetry (for dependency management)

#### ***Notes***

GitHub limits users to a maximum of ***1000 results per search***. This is a limitation of their API and not the application itself.
Ensure you have a valid GitHub Token for authentication to access the GitHub API.

---

Happy Searching!

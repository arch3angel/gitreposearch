## Overview

This Streamlit application allows you to search for GitHub repositories based on your criteria and view the search results conveniently.

## Instructions

#### Search Criteria

1. Enter your search criteria in the text input box under the title "GitHub Repository Search"
2. Click the "Search" button to start the search.

#### Search Results

- The search results will be displayed in real-time under the search criteria input box.
- Each page processed will be shown, indicating the progress of the search.

#### Markdown File Selection

1. In the left sidebar titled "Select .md file:", you can see a dropdown menu.
2. Use the dropdown to select any available .md file to view its contents.
3. The selected .md file will be displayed in the main area below the search bar and results.

#### Clear Search

- If you need to clear the search criteria, click the "Reset Search" button.
- This will clear the search bar of all characters, allowing you to enter new search criteria.

#### Stop Search

- To stop the current search in progress, click the "Stop" button.
- Once stopped, the application will create a Markdown file containing the search results.

## ***Important Note***

GitHub's API limits the number of results to a ***maximum of 1000 per search***. This limitation is set by GitHub's API and not by this application. If your search criteria yields more than 1000 results, only the first 1000 results will be displayed.

---

Enjoy using the GitHub Repository Search Tool!

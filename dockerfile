# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

# Run the Streamlit app when the container launches
CMD ["streamlit", "run", "--server.address", "localhost", "--server.port", "8501", "gitreposearch.py"]

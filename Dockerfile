# Start from base image
FROM python:3.8

# Set work directory in the Docker container
WORKDIR "/volume6/DeadShareTest"

# Copy everything from current local directory (where Dockerfile lives) into container
COPY . "/volume6/DeadShareTest"

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run your script when the container launches
CMD ["python", "./main.py"]

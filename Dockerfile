# syntax=docker/dockerfile:1

FROM python:3.11-slim

# Install system dependencies needed by OpenCV and Ultralytics.
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set up a dedicated working directory.
WORKDIR /workspace

# Copy dependency list first to leverage Docker layer caching.
COPY requirements.txt ./

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the remainder of the project files.
COPY . .

# Create default directories so newcomers see a clean structure when the
# container starts.
RUN mkdir -p outputs data

# Print a hint when the container launches.
CMD ["bash", "-lc", "echo 'Container ready! Try: python src/infer.py --source images' && bash"]

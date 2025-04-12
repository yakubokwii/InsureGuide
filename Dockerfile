FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git git-lfs \
 && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Enable Git LFS
RUN git lfs install

# Clone the repository and pull LFS files
ARG REPO_URL= https://github.com/yakubokwii/InsureGuide.git
ARG REPO_BRANCH=main

RUN git clone --branch $REPO_BRANCH $REPO_URL . && \
    git lfs pull

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Expose port for Gunicorn
EXPOSE 5000

# Run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "model:app"]

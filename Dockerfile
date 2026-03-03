# Use the spconv development image as the base
FROM scrin/dev-spconv:latest

# Set the working directory inside the container
WORKDIR /workspace/OpenPCDet

# Copy the requirements.txt file first to leverage Docker layer caching
COPY requirements.txt .

# Install the Python dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the OpenPCDet folder contents into the container
COPY . .

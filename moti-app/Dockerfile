# Use an official Node.js runtime as a parent image
FROM node:16

# Set the working directory in the container
RUN mkdir /app/
WORKDIR /app/

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the frontend application code to the container
COPY . /app/

# Build the Vue 3 frontend code
RUN npm run build

# Expose the port where the frontend application will run (if needed)
EXPOSE 8080

# Command to serve the frontend (if using a simple HTTP server)
CMD ["npm", "run", "preview", "--host"]


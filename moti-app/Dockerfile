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

# Command to serve the frontend
# CMD ["npm", "run", "preview"]

# Install serve globally to serve the application
RUN npm install -g serve

# Expose port 4000
EXPOSE 8080

# Command to serve the application using serve
CMD ["serve", "-s", "dist", "-l", "8080"]


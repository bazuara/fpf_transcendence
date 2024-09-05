# Use an official node image as a base
FROM node:16

# Install dependencies
RUN npm install -g truffle ganache-cli

# Set up the working directory
WORKDIR /app

# Copy the project files into the container
COPY . .

# Compile the contract
RUN truffle compile

# Start Ganache and deploy the contract
CMD ["bash", "./entrypoint.sh"]

# Expose the port that the server is running on
EXPOSE 8545
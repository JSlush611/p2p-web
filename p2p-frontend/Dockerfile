# Use an official Node.js image to build the React app
FROM node:18-alpine as build

# Set working directory
WORKDIR /app

# Accept build arguments for secrets
ARG SECRET_KEY
ARG API_URL

# Pass the secrets as environment variables
ENV REACT_APP_SECRET_KEY=$SECRET_KEY
ENV REACT_APP_API_URL=$API_URL

# Install dependencies
COPY package.json ./
RUN npm install

# Copy the rest of the app and build it
COPY . ./
RUN npm run build

# Use an Nginx image to serve the built React app
FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]

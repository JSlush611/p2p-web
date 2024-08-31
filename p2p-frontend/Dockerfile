# Use an official Node.js image to build the React app
FROM node:18-alpine as build

# Set working directory
WORKDIR /app

COPY .env ./

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

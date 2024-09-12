# Use an official Node.js image to build the React app
FROM node:18-alpine as build

# Set working directory
WORKDIR /app

# Accept build arguments for secrets
ARG REACT_APP_API_URI
ARG REACT_APP_EMAIL_JS_SERVICE_ID
ARG REACT_APP_EMAIL_JS_TEMPLATE_ID
ARG REACT_APP_EMAILJS_PUBLIC_KEY
ARG REACT_APP_RECAPTCHA_SITE_KEY
ARG REACT_APP_RECAPTCHA_SECRET_KEY
ARG GENERATE_SOURCEMAP

# Pass the secrets as environment variables
ENV REACT_APP_API_URI=$REACT_APP_API_URI
ENV REACT_APP_EMAIL_JS_SERVICE_ID=$REACT_APP_EMAIL_JS_SERVICE_ID
ENV REACT_APP_EMAIL_JS_TEMPLATE_ID=$REACT_APP_EMAIL_JS_TEMPLATE_ID
ENV REACT_APP_EMAILJS_PUBLIC_KEY=$REACT_APP_EMAILJS_PUBLIC_KEY
ENV REACT_APP_RECAPTCHA_SITE_KEY=$REACT_APP_RECAPTCHA_SITE_KEY
ENV REACT_APP_RECAPTCHA_SECRET_KEY=$REACT_APP_RECAPTCHA_SECRET_KEY
ENV GENERATE_SOURCEMAP=$GENERATE_SOURCEMAP

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

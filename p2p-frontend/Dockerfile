# ---------- build ----------
FROM node:18-alpine AS build
WORKDIR /app
ARG REACT_APP_API_URI
ARG REACT_APP_EMAIL_JS_SERVICE_ID
ARG REACT_APP_EMAIL_JS_TEMPLATE_ID
ARG REACT_APP_EMAILJS_PUBLIC_KEY
ENV REACT_APP_API_URI \
    REACT_APP_EMAIL_JS_SERVICE_ID \
    REACT_APP_EMAIL_JS_TEMPLATE_ID \
    REACT_APP_EMAILJS_PUBLIC_KEY

COPY package*.json ./
RUN npm ci --omit=dev                         
COPY . .
RUN npm run build

# ---------- runtime ----------
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

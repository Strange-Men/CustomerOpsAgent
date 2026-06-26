# Stage 1: Build
FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies (layer cache)
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

# Copy source
COPY frontend/ ./

# Build-time env: backend API URL
ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Custom nginx config for SPA fallback
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

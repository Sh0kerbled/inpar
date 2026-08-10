# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with clean cache
RUN npm cache clean --force && npm ci --legacy-peer-deps

# Copy source code  
COPY . .

# List files for debugging
RUN ls -la /app/src/pages/ || echo "pages dir not found"

# Build the app
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy nginx config
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Copy built files from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

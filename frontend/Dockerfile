# Stage 1: Build (expects node_modules to be pre-built locally)
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Try to copy pre-built node_modules, if not available npm will install
RUN if [ -d "node_modules" ]; then echo "Using local node_modules"; else npm config set registry https://registry.npmmirror.com && npm config set fetch-timeout 120000 && npm install --legacy-peer-deps --prefer-offline --no-audit --progress=false; fi
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

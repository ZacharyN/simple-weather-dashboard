FROM node:20-slim

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps

# Copy application
COPY . .

# Backend URL for API proxy (build-time configuration)
ARG BACKEND_URL=http://localhost:8000
ENV BACKEND_URL=${BACKEND_URL}

# Build application with proxy configuration
RUN npm run build

# Expose port
EXPOSE 3000

# Run application
CMD ["node", ".output/server/index.mjs"]

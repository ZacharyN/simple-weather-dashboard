FROM node:20-slim

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps

# Copy application
COPY . .

# Build application
RUN npm run build

# Expose port
EXPOSE 3000

# Run application
CMD ["node", ".output/server/index.mjs"]

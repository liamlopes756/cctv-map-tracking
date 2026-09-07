FROM node:22-alpine AS build
WORKDIR /app
ARG VITE_API_BASE_URL=http://localhost:5020
ARG VITE_AI_STREAM_URL=http://localhost:8010/stream.mjpg
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_AI_STREAM_URL=$VITE_AI_STREAM_URL

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80

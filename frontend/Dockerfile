FROM node:18-alpine as buildstage
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
# install app dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install
COPY . /app/
RUN npm run build
FROM nginx:alpine as prodstage
COPY --from=buildstage /app/build /usr/share/nginx/html
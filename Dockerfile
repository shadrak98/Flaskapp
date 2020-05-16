FROM node:7

MAINTAINER Shadrak&Shubham

WORKDIR /Flaskapp

COPY package.json /Flaskapp

RUN npm install

COPY . /Flaskapp

EXPOSE 3000

CMD ["nodemon"]

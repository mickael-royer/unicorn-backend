# syntax=docker/dockerfile:1

FROM golang:1.16-alpine

ARG PORT=8050
ENV PORT=$PORT
ARG GITHUB_TOKEN=${GITHUB_TOKEN}
ENV GITHUB_TOKEN=$GITHUB_TOKEN

WORKDIR /app

COPY go.mod ./
COPY go.sum ./
RUN go mod download

COPY . .

RUN go build -o /go-service

EXPOSE 8050

CMD [ "/go-service" ]
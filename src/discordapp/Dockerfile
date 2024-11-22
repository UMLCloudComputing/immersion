FROM golang:1.23

WORKDIR /asset

COPY go.mod go.sum ./

RUN go mod download && go mod verify

COPY . .

RUN go build -o /usr/local/bin/app ./...

EXPOSE 8080:8080

CMD ["app"]
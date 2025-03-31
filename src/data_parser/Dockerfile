FROM golang:1.23

WORKDIR /asset

COPY go.mod ./

RUN go mod download && go mod verify

COPY . .

RUN go build -o /usr/local/bin/app/ ./...

CMD ["/usr/local/bin/app/dataparser"]
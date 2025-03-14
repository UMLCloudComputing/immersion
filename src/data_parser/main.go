package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/sqs"
)

func main() {
	queueUrl := os.Getenv("QUEUE_URL")

	cfg, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		log.Fatal(err)
	}
	client := sqs.NewFromConfig(cfg)

	// there will probably be a main loop where you do this first every time this program should run until there is nothing in the queue
	message, err := client.ReceiveMessage(context.TODO(), &sqs.ReceiveMessageInput{
		QueueUrl:            &queueUrl,
		MaxNumberOfMessages: 1,
		WaitTimeSeconds:     10,
	})
	if err != nil {
		log.Fatal(err)
	}

	// TODO define message structure and parse for that
	for _, e := range message.Messages {
		fmt.Println(*e.Body)
		_, err := client.DeleteMessage(context.TODO(), &sqs.DeleteMessageInput{
			QueueUrl:      &queueUrl,
			ReceiptHandle: e.ReceiptHandle,
		})
		if err != nil {
			log.Fatal(err)
		}
	}

	fmt.Println("Parsing complete, waiting to be killed.")
	wait := make(chan bool)
	<-wait
}

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

	response, err := client.ReceiveMessage(context.TODO(), &sqs.ReceiveMessageInput{
		QueueUrl:            &queueUrl,
		MaxNumberOfMessages: 5, // play around with these
		WaitTimeSeconds:     5,
	})
	if err != nil {
		log.Fatal(err)
	}

	// print and delete all messages in the queue
	for len(response.Messages) > 0 {
		for _, e := range response.Messages {
			fmt.Println(*e.Body)
			_, err = client.DeleteMessage(context.TODO(), &sqs.DeleteMessageInput{
				QueueUrl:      &queueUrl,
				ReceiptHandle: e.ReceiptHandle,
			})
			if err != nil {
				log.Fatal(err)
			}
		}

		response, err = client.ReceiveMessage(context.TODO(), &sqs.ReceiveMessageInput{
			QueueUrl:            &queueUrl,
			MaxNumberOfMessages: 5,
			WaitTimeSeconds:     5,
		})
		if err != nil {
			log.Fatal(err)
		}
	}

	fmt.Println("Parsing complete, waiting to be killed.")
	wait := make(chan bool)
	<-wait
}

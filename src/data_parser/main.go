package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/sqs"
)

func main() {
	// TODO: add processing logic
	//queueUrl := os.Getenv("QUEUE_URL")

	cfg, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		log.Fatal(err)
	}
	client := sqs.NewFromConfig(cfg)

	message, err := client.ReceiveMessage(context.TODO(), &sqs.ReceiveMessageInput{
		QueueUrl:            aws.String("https://sqs.us-east-1.amazonaws.com/840414111995/Immersion_Data_Queue"),
		MaxNumberOfMessages: 5,
	})
	if err != nil {
		log.Fatal(err)
	}

	for _, e := range message.Messages {
		fmt.Println(*e.Body)
		_, err := client.DeleteMessage(context.TODO(), &sqs.DeleteMessageInput{
			QueueUrl:      aws.String("https://sqs.us-east-1.amazonaws.com/840414111995/Immersion_Data_Queue"),
			ReceiptHandle: e.ReceiptHandle,
		})
		if err != nil {
			log.Fatal(err)
		}
	}

	fmt.Println("Parsing complete.")
	os.Exit(0)
}

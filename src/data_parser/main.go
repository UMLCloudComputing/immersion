package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/aws/aws-sdk-go-v2/service/sqs"
	"github.com/umlcloudcomputing/immersion/dataparser/db"
	"github.com/umlcloudcomputing/immersion/dataparser/models"
)

func parseMessage(dbClient *dynamodb.Client, message string) {
	var parsedMessage models.Message
	err := json.Unmarshal([]byte(message), &parsedMessage)
	if err != nil {
		log.Fatal(err)
	}

	switch parsedMessage.Header {
	case "organization":
		var organizationData models.OrganizationResponse
		err = json.Unmarshal([]byte(parsedMessage.Body), &organizationData)
		if err != nil {
			log.Fatal(err)
		}

		for _, v := range organizationData.Organizations {
			db.InsertOrganization(context.TODO(), dbClient, v)
		}
	}
}

func main() {
	queueUrl := os.Getenv("QUEUE_URL")

	cfg, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		log.Fatal(err)
	}

	sqsClient := sqs.NewFromConfig(cfg)
	dbClient := dynamodb.NewFromConfig(cfg)

	response, err := sqsClient.ReceiveMessage(context.TODO(), &sqs.ReceiveMessageInput{
		QueueUrl:            &queueUrl,
		MaxNumberOfMessages: 5, // play around with these
		WaitTimeSeconds:     5,
	})
	if err != nil {
		log.Fatal(err)
	}

	// print and delete all messages in the queue
	for len(response.Messages) > 0 {
		for _, v := range response.Messages {

			parseMessage(dbClient, *v.Body)
			_, err = sqsClient.DeleteMessage(context.TODO(), &sqs.DeleteMessageInput{
				QueueUrl:      &queueUrl,
				ReceiptHandle: v.ReceiptHandle,
			})
			if err != nil {
				log.Fatal(err)
			}
		}

		response, err = sqsClient.ReceiveMessage(context.TODO(), &sqs.ReceiveMessageInput{
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

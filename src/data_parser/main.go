package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/aws/aws-sdk-go-v2/service/sqs"
	"github.com/umlcloudcomputing/immersion/dataparser/db"
	"github.com/umlcloudcomputing/immersion/dataparser/models"
	"github.com/umlcloudcomputing/immersion/dataparser/util"
)

func filterMessage(dbClient *dynamodb.Client, message string) {
	var parsedMessage models.Message[any]
	err := json.Unmarshal([]byte(message), &parsedMessage)
	util.CheckError(err)

	fmt.Printf("Parsed a message with the %s header\n", parsedMessage.Header)

	ctx := context.TODO()
	switch parsedMessage.Header {
	case "club_information":
		var informationData models.Message[models.ClubInformation]
		err = json.Unmarshal([]byte(message), &informationData.Body)
		util.CheckError(err)

		db.InsertItem(ctx, dbClient, db.CacheTable, informationData)
	case "onboarding":
		var onboardingData models.Message[[]models.Onboarding]
		err = json.Unmarshal([]byte(message), &onboardingData)
		util.CheckError(err)

		for _, i := range onboardingData.Body {
			db.InsertItem(ctx, dbClient, db.OnboardingTable, i)
		}
	case "event":
		var eventData models.Message[[]models.Event]
		err = json.Unmarshal([]byte(message), &eventData)
		util.CheckError(err)

		for _, i := range eventData.Body {
			db.InsertItem(ctx, dbClient, db.EventTable, i)
		}
	}
}

func main() {
	queueUrl := os.Getenv("QUEUE_URL")

	cfg, err := config.LoadDefaultConfig(context.TODO())
	util.CheckError(err)

	sqsClient := sqs.NewFromConfig(cfg)
	dbClient := dynamodb.NewFromConfig(cfg)

	response, err := sqsClient.ReceiveMessage(context.TODO(), &sqs.ReceiveMessageInput{
		QueueUrl:            &queueUrl,
		MaxNumberOfMessages: 5, // play around with these
		WaitTimeSeconds:     5,
	})
	util.CheckError(err)

	// print and delete all messages in the queue
	for len(response.Messages) > 0 {
		for _, v := range response.Messages {

			filterMessage(dbClient, *v.Body)
			_, err = sqsClient.DeleteMessage(context.TODO(), &sqs.DeleteMessageInput{
				QueueUrl:      &queueUrl,
				ReceiptHandle: v.ReceiptHandle,
			})
			util.CheckError(err)
		}

		response, err = sqsClient.ReceiveMessage(context.TODO(), &sqs.ReceiveMessageInput{
			QueueUrl:            &queueUrl,
			MaxNumberOfMessages: 5,
			WaitTimeSeconds:     5,
		})
		util.CheckError(err)
	}

	fmt.Println("Parsing complete, waiting to be killed.")
	wait := make(chan bool)
	<-wait
}

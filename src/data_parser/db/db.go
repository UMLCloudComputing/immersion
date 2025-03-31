package db

import (
	"context"
	"log"
	"os"

	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/attributevalue"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/umlcloudcomputing/immersion/dataparser/models"
)

var (
	OrganizationTableName = os.Getenv("ORGANIZATION_TABLE")
)

func InsertOnboarding(ctx context.Context, db *dynamodb.Client, org models.Onboarding) {
	item, err := attributevalue.MarshalMap(org)
	if err != nil {
		log.Fatal(item)
	}

	input := dynamodb.PutItemInput{
		TableName: &OrganizationTableName,
		Item:      item,
	}

	_, err = db.PutItem(ctx, &input)
	if err != nil {
		log.Fatal(err)
	}
}

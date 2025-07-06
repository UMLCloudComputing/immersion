package db

import (
	"context"
	"fmt"
	"os"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/attributevalue"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/umlcloudcomputing/immersion/dataparser/util"
)

type TableName int

const (
	ServerTable TableName = iota
	OnboardingTable
	CacheTable
	EventTable
)

var tableNames = map[TableName]string{
	ServerTable:     os.Getenv("SERVER_TABLE"),
	OnboardingTable: os.Getenv("ORGANIZATION_TABLE"),
	CacheTable:      os.Getenv("CACHE_TABLE"),
	EventTable:      os.Getenv("EVENT_TABLE"),
}

func InsertItem(ctx context.Context, db *dynamodb.Client, table TableName, data any) {
	item, err := attributevalue.MarshalMap(data)
	util.CheckError(err)

	input := dynamodb.PutItemInput{
		TableName: aws.String(tableNames[table]),
		Item:      item,
	}

	_, err = db.PutItem(ctx, &input)
	util.CheckError(err)
	fmt.Printf("Inserted an item into %s\n", tableNames[table])
}

//func InsertOnboarding(ctx context.Context, db *dynamodb.Client, org models.Onboarding) {
//	item, err := attributevalue.MarshalMap(org)
//	util.CheckError(err)
//
//	input := dynamodb.PutItemInput{
//		TableName: &OrganizationTableName,
//		Item:      item,
//	}
//
//	_, err = db.PutItem(ctx, &input)
//	util.CheckError(err)
//}

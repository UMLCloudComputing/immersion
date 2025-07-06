package models

type Message[T any] struct {
	Header string `json:"header"`
	Body   T      `json:"body"`
}

type Onboarding struct {
	OrgId          int    `json:"OrgId" dynamodbav:"organizationId"`
	Name           string `json:"Name" dynamodbav:"name"`
	PrimaryContact string `json:"PrimaryContact" dynamodbav:"primaryContact"`
	ImageUrl       string `json:"ImageUrl" dynamodbav:"imageUrl"`
	WebsiteKey     string `json:"WebsiteKey" dynamodbav:"websiteKey"`
}

type ClubInformation struct {
	OrgId          int    `json:"OrgId" dynamodbav:"organizationId"`
	Name           string `json:"Name" dynamodbav:"name"`
	PrimaryContact string `json:"PrimaryContact" dynamodbav:"primaryContact"`
	ImageUrl       string `json:"ImageUrl" dynamodbav:"imageUrl"`
	WebsiteKey     string `json:"WebsiteKey" dynamodbav:"websiteKey"`
	NumMembers     int    `json:"NumMembers" dynamodbav:"numMembers"`
	Settings       string `json:"settings" dynamodbav:"settings"`
}

type Event struct {
	LinkedOrgId int    `json:"LinkedOrgId" dynamodbav:"linkedOrgId"`
	Name        string `json:"Name" dynamodbav:"name"`
	Date        string `json:"Date" dynamodbav:"date"`
	Time        string `json:"Time" dynamodbav:"time"`
	Description string `json:"Description" dynamodbav:"description"`
}

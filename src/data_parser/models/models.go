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

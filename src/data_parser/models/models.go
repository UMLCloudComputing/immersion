package models

type Message struct {
	Header string `json:"header"`
	Body   string `json:"body"`
}

type OrganizationResponse struct {
	Organizations []Organization
}

type Organization struct {
	OrgId          string `json:"OrgId" dynamodbav:"organizationId"`
	Name           string `json:"Name" dynamodbav:"name"`
	PrimaryContact string `json:"PrimaryContact" dynamodbav:"primaryContact"`
	ImageUrl       string `json:"ImageUrl" dynamodbav:"imageUrl"`
	WebsiteKey     string `json:"WebsiteKey" dynamodbav:"websiteKey"`
}

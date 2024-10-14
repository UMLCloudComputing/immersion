package main

import (
	"os"

	"umlcloudcomputing.org/immersion_cdk/config"

	"github.com/aws/aws-cdk-go/awscdk/v2"
	"github.com/aws/aws-cdk-go/awscdk/v2/awslambda"

	// "github.com/aws/aws-cdk-go/awscdk/v2/awssqs"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"

	"github.com/joho/godotenv"
)

type ImmersionStackProps struct {
	awscdk.StackProps
}

func NewImmersionStack(scope constructs.Construct, id string, props *ImmersionStackProps) awscdk.Stack {
	var sprops awscdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := awscdk.NewStack(scope, &id, &sprops)

	// The code that defines your stack goes here

	awslambda.NewFunction(stack, jsii.String(config.FunctionName), &awslambda.FunctionProps{
		FunctionName: jsii.String(config.StackName + "-" + config.FunctionName),
		Runtime:      awslambda.Runtime_PROVIDED_AL2(),
		MemorySize:   jsii.Number(config.MemorySize),
		Timeout:      awscdk.Duration_Seconds(jsii.Number(config.MaxDuration)),
		Code:         awslambda.AssetImageCode_FromDockerBuild(jsii.String("src"), nil),
		Handler:      jsii.String(config.Handler),
	})

	return stack
}

func main() {
	defer jsii.Close()

	godotenv.Load(".env")

	app := awscdk.NewApp(nil)

	NewImmersionStack(app, "ImmersionStack", &ImmersionStackProps{
		awscdk.StackProps{
			Env: env(),
		},
	})

	app.Synth(nil)
}

// env determines the AWS environment (account+region) in which our stack is to
// be deployed. For more information see: https://docs.aws.amazon.com/cdk/latest/guide/environments.html
func env() *awscdk.Environment {
	account := os.Getenv("CDK_DEPLOY_ACCOUNT")
	region := os.Getenv("CDK_DEPLOY_REGION")

	return &awscdk.Environment{
		Account: jsii.String(account),
		Region:  jsii.String(region),
	}
}

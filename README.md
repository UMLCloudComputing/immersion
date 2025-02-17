<div align="center">
    <img src="img/cover-transparent.svg" alt="Logo" width="50%" height="50%"/>
    <h3>A Discord application that aims to bridge the gap between using Discord and Campus Lab's Engage platform to better help university clubs manage their organizations.</h3>
    <hr>
</div>

README is under construction!

This is a blank project for CDK development with Go.

The `cdk.json` file tells the CDK toolkit how to execute your app.

## Useful commands

 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk synth`       emits the synthesized CloudFormation template
 * `go test`         run unit tests


## API Architecture

Fundamentally a set of lambda functions to periodically pull and synchronize data from Engage

Key traits:
- Data objects and their dependencies are shared layers in the Lambda functions in order to keep them light
- Lambda functions will populate to a Dynamo DB table


## Infrastructure
![Project Infrastructure](https://media.discordapp.net/attachments/1041436332402167879/1329181171804012675/image.png?ex=67b440ae&is=67b2ef2e&hm=2ae986180a84cf2f87cda6be60a08e25171174a2da865ec590558344f2f2ea3e&=&format=webp&quality=lossless&width=960&height=473)


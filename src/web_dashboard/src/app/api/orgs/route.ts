import { NextRequest, NextResponse } from "next/server";
import { tempOrgs } from "../../../data/testOrgs"
import { DynamoDBClient, ScanCommand, ScanCommandOutput, ScanCommandInput } from "@aws-sdk/client-dynamodb"
import { CloudFormationClient, CloudFormationServiceException, DescribeStackResourceCommand, DescribeStackResourceOutput, ListStackResourcesCommand, ListStackResourcesOutput, StackResourceSummary } from "@aws-sdk/client-cloudformation";
import { fromIni } from "@aws-sdk/credential-provider-ini";
import { GiConsoleController } from "react-icons/gi";

const createDynamoDBScanCommand = (tableName: string): ScanCommand => {
    return new ScanCommand({
        TableName: tableName,
    })
}

const createListResourcesCommand = (): ListStackResourcesCommand => {
    return new ListStackResourcesCommand({
        StackName: "ImmersionStack"
    })
}

export async function GET(req: NextRequest) {
    const ddbClient = new DynamoDBClient({
        region: "us-east-1",
        credentials: fromIni({ profile: "dev" })
    })
    const cfClient = new CloudFormationClient({
        region: "us-east-1",
        credentials: fromIni({ profile: "dev" })
    })

    let stackResources: ListStackResourcesOutput = null
    try {
        stackResources = await cfClient.send(createListResourcesCommand())
    } catch (_e) {
        const error: CloudFormationServiceException = _e;
        return NextResponse.json({ message: "An error occured on the server " + error.message + " Please try again later" }, { status: 500 })
    }

    const tableName: StackResourceSummary[] = stackResources.StackResourceSummaries
    const table: StackResourceSummary = tableName.find((summary: StackResourceSummary) => summary.LogicalResourceId.includes("ImmersionOrganizationTable"))

    let data: ScanCommandOutput = null;
    try {
        data = await ddbClient.send(createDynamoDBScanCommand(table.PhysicalResourceId))
    } catch (_e) {
        const error: CloudFormationServiceException = _e;
        return NextResponse.json({ message: "An error occured on the server " + error.message + " Please try again later" }, { status: 500 })
    }
    if (!data) {
        return NextResponse.json({ message: "Error fetching orgs. Try again later" }, { status: 500 })
    }
    return NextResponse.json(data, { status: 200 })
}
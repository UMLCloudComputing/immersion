"use server"
import { VerificationEmailActionResponse } from "@/types/types"
import { DynamoDBClient } from "@aws-sdk/client-dynamodb"
import { SendEmailCommand, SESClient } from "@aws-sdk/client-ses"
import { PutCommand } from "@aws-sdk/lib-dynamodb"


const createVerificationEmail = (to: string, code: number) => {
    return new SendEmailCommand({
        Destination: {
            ToAddresses: [to]
        },
        Message: {
            Body: {
                Html: {
                    Charset: "UTF-8",
                    Data: `Your Immersion verification code is ${code}`
                },
                Text: {
                    Charset: "UTF-8",
                    Data: `Your Immersion verification code is ${code}`
                },
            },
            Subject: {
                Charset: "UTF-8",
                Data: "Immersion Verification"
            },
        },
        Source: "no-reply@umlcloudcomputing.org"
    })
}

const createDynamoDBEntry = (emailAddress: string, code: number) => {
    const expireAt = Math.floor((new Date().getTime() + 30000) / 1000) //expire in 30 seconds
    const createdAt = new Date().getTime();
    return new PutCommand({
        TableName: "immersion-verification",
        Item: {
            "email": emailAddress,
            "code": code,
            "expiration": expireAt.toString(),
            "createdAt": createdAt.toString()
        },
    })
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const sendVerificationEmail = async (emailAddress: string): Promise<VerificationEmailActionResponse> => {
    const sesClient = new SESClient({ region: "us-east-1" })
    const code = Math.floor(Math.random() * 900000) + 100000;
    const ddbClient = new DynamoDBClient({ region: "us-east-1" })

    const ddbDocument = createDynamoDBEntry("nbottari9@gmail.com", code)
    await ddbClient.send(ddbDocument)

    const verificationEmail = createVerificationEmail(emailAddress, code);

    try {
        await sesClient.send(verificationEmail)

        return Promise.resolve({
            status: "success",
            message: "Email sent"
        })
    } catch (e) {
        console.log(e)
        return Promise.reject({
            status: "error",
            message: e
        })
    }
    // const promise = new Promise<VerificationEmailActionResponse>((resolve, reject) => {
    //     setTimeout(() => {
    //         resolve({
    //             status: "success",
    //             message: "Email sent"
    //         })
    //     }, 5000)
    // }
    // )

    // return promise

}

export const confirmVerificationCode = async () => {
    //check verification code
}
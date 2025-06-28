import { Response } from "next/server";

export interface Guild {
    id: string
    name: string,
    icon: string?,
    banner: string?,
    owner: boolean,
    permissions: bigint,
    features: string[],
    approximate_member_count: number,
    approximate_presence_count: number

}

export interface Org {
    organizationId: string,
    name: string,
    imageUrl: string,
    primaryContact: string,
    websiteKey: string
}

export interface VerificationEmailActionResponse {
    status: "success" | "error" | "idle",
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    message: any
}

export interface FetchError {
    message: string;
}

export interface DDBOrgItem {
    imageUrl: { S: string };
    name: { S: string };
    id: { N: number };
    primaryContact: { S: string };
    websiteKey: { S: string };
}



declare global {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    interface Window { scrollTimeout: any }
}
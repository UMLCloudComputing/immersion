import { DefaultSession } from "next-auth";
import { DefaultJWT } from "next-auth/jwt";

declare module 'next-auth' {
    export interface Session extends DefaultSession {
        access_token: string;
    }

}

declare module 'next-auth/jwt' {
    export interface JWT extends DefaultJWT {
        access_token: string;
    }
}
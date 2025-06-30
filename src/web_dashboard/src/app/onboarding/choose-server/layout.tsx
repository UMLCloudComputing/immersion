import { auth, signIn } from "@/auth";
import { DMSans } from "@/fonts";
import { redirect } from "next/navigation";
import { ReactNode } from "react";

export default async function ChooseServerLayout({ children }: { children: ReactNode }) {
    return (
        <div className="flex justify-begin items-center flex-col">
            <h1 className={`text-5xl text-center text-neutral-300 p-5 ${DMSans.className}`}>Choose a server to add the bot</h1>
            {children}
        </div>
    )
}
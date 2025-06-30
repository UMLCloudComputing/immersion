import { auth, signIn } from "@/auth";
import { Guilds } from "@/components/Guilds";
import { DMSans } from "@/fonts";
import { Guild } from "@/types/types";
import { redirect } from "next/navigation";

export default async function ChooseServerPage() {
    const session = await auth()
    if (!session) {
        redirect("/api/auth/signin?callbackUrl=/onboarding/choose-server")
    }

    const data = await fetch("https://discord.com/api/users/@me/guilds", {
        method: "GET",
        headers: {
            Authorization: `Bearer ${session.access_token}`,
        },
    })

    const guilds: Guild[] = await data.json()
    // filter out guilds where user isnt admin
    const ownedGuilds = guilds.filter((guild: Guild) => BigInt(guild.permissions) & BigInt("0x8"))

    return (
        <Guilds data={ownedGuilds} />
    )

}
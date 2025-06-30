"use client"
import { Guild } from "@/types/types"
import { GuildIcon } from "./GuildIcon"
import { useRouter } from "next/navigation"
import { useEffect, useState } from "react"
import { ProgressCircleRing, ProgressCircleRoot } from "./ui/progress-circle"

export const Guilds = ({ data }: { data: Guild[] }) => {
    const router = useRouter()

    const nextStep = (guild: Guild) => {
        router.push(`/onboarding/org-lookup?guild=${guild.id}`)
    }

    return (
        <div className="flex flex-row flex-wrap gap-1 gap-y-4 justify-center items-begin w-1/2 bg-neutral-600 p-4 rounded-3xl">
            {
                data.map((guild: Guild) => (
                    <GuildIcon key={guild.id} guild={guild} onClick={nextStep} />
                ))
            }
        </div>
    )
}
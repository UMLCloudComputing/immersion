"use client"

import { DMSans } from "@/fonts"
import { Org } from "@/types/types"
import { ProgressCircle, ProgressCircleCircle } from "@chakra-ui/react"
import { use } from "react"
import { ProgressCircleRing, ProgressCircleRoot } from "./ui/progress-circle"

export const VerificationProcessCard = ({ _org }: { _org: Org }) => {
    // const org = use(_org)
    const org = _org
    return (
        _org ? (
            <div>
                <h2 className={`text-3xl text-center text-neutral-300 p-3 ${DMSans.className}`}>Primary Contact for <span className="font-bold text-neutral-200">{org?.name}</span> is:</h2>
                <h2 className={`text-3xl text-center text-neutral-200 p-1 font-bold ${DMSans.className}`}>{org?.primaryContact}</h2>
            </div>
        ) : (
            <ProgressCircleRoot value={null} size="md">
                <ProgressCircleRing cap="round" />
            </ProgressCircleRoot>
        )
    )
}
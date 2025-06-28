"use client"
import { OrgSearch } from "@/components/OrgSearch";
import { DMSans } from "@/fonts";
import { Org } from "@/types/types";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { ProgressCircleRoot, ProgressCircleRing } from "@/components/ui/progress-circle";
import { FetchError } from "@/types/types";
import { toaster } from "@/components/ui/toaster";
import { ddbOrgItemToRawJSON } from "@/components/utils/utils";
import { dataListAnatomy } from "@chakra-ui/react/anatomy";

export default function OrgLookupPage() {
    const searchParams = useSearchParams()
    const router = useRouter()

    const [orgs, setOrgs] = useState<Org[]>([])
    const [loading, setLoading] = useState(true)
    const [selectedOrg, setSelectedOrg] = useState<Org | null>(null)
    const [errors, setErrors] = useState<FetchError>(null)

    const verifyGuildId = () => {
        const guildId = searchParams.get("guild")

        if (!guildId) {
            console.error("No guild id provided")
            router.push("/onboarding/choose-server") //redirect to choose-server
        }
    }

    const nextStep = () => {
        if (selectedOrg) {
            console.log(selectedOrg.organizationId)
            router.push(`/onboarding/verify?guild=${searchParams.get("guild")}&org=${selectedOrg.organizationId}`)
        } else {
            toaster.error({
                title: "No organization selected",
                description: "Select an organization to continue",
                duration: 4000
            })
        }
    }

    useEffect(() => {
        verifyGuildId() //ensure that the guild id is present in the url params, otherwise redirect
    })

    useEffect(() => {
        const fetchOrgs = async () => {
            const res = await fetch(`/api/orgs`)
            const data = await res.json()
            if (res.status !== 200) {
                setErrors(data)
                toaster.error({
                    title: data.message,
                    description: data.message,
                    duration: 15000
                })
            }
            console.log(data.Items)
            const unmarshalledItems = ddbOrgItemToRawJSON(data.Items)
            setOrgs(unmarshalledItems as Org[])
            setLoading(false)
        }



        fetchOrgs()
    }, [])

    return (
        <div className="flex justify-begin items-center flex-col">
            <h1 className={`text-5xl text-center text-neutral-300 p-5 ${DMSans.className}`}>Choose your club</h1>
            {
                loading ? <ProgressCircleRoot value={null} size="lg">
                    <ProgressCircleRing cap="round" />
                </ProgressCircleRoot> : (
                    errors ? <div className="text-neutral-300">{errors.message}</div> : (
                        <OrgSearch props={{ orgs: orgs, setOrg: setSelectedOrg }} />
                    )
                )
            }
            <button className={`bg-neutral-600 m-20 p-4 transition-all ease-out hover:ease-in hover:bg-neutral-500 duration-10 text-neutral-200 ${DMSans.className} text-2xl rounded-2xl`} onClick={nextStep}>Next Step: Verify</button>
        </div>
    )
}
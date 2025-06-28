"use client"
import { VerificationProcessCard } from "@/components/VerificationProcessCard"
import { tempOrgs } from "@/data/testOrgs"
import { DMSans } from "@/fonts"
import { DDBOrgItem, Org, VerificationEmailActionResponse } from "@/types/types"
import Image from "next/image"
import { useRouter, useSearchParams } from "next/navigation"
import { useEffect, useState, Suspense, useActionState, SetStateAction } from "react"
import { Checkbox } from "@/components/ui/checkbox"
import { confirmVerificationCode, sendVerificationEmail } from "@/app/actions"
import { PinInput } from "@/components/ui/pin-input"
import { toaster } from "@/components/ui/toaster"
import { ddbOrgItemToRawJSON } from "@/components/utils/utils"

export default function VerificationPage() {
    //hooks
    const searchParams = useSearchParams()
    const router = useRouter()

    const [org, setOrg] = useState<Org | null>(null)
    const [acknowledged, setAcknowledged] = useState(false)
    const [formStage, setFormStage] = useState(0)

    //vars
    const guildId = searchParams.get("guild")
    const orgId = searchParams.get("org")

    //funcs

    const nextStep = () => {
        //console.log("Send email and redirect")
        // sendVerificationEmail();
        //router.replace("/onboarding/confirm")
        setFormStage(1)
        // console.log("org: ", org)
        const res = sendVerificationEmail(org.primaryContact)
        console.log(res)
        toaster.promise(res, {
            success: {
                title: "Verification Email Sent",
                description: "Check your inbox for a verification code",
                duration: 4000
            },
            error: {
                title: "There was a problem sending the verification email",
                description: "Please try again later",
                duration: 4000
            },
            loading: {
                title: "Loading"
            },
        })
    }

    //use effects
    useEffect(() => {
        const verifyQueryParams = () => {
            if (!guildId || guildId == undefined) {
                console.error("No guild id provided")
                router.push("/choose-server") //redirect to choose-server
            } else if (!orgId) {
                console.error("No org id provided")
                router.push(`/org-lookup?guild=${guildId}`) //redirect to org-lookup
            }
        }

        verifyQueryParams()
    }, [guildId, orgId, router])

    //THIS IS SO TEMPORARY ITS NOT EVEN FUNNY
    function delay(ms: number) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    useEffect(() => {

        const fetchOrgs = async (): Promise<Org[]> => {
            const res = await fetch(`/api/orgs`)
            const ddbOutput = await res.json()
            return ddbOutput.Items
        }

        const getOrgByID = async (orgId: string) => {
            const orgs = await fetchOrgs()
            console.log(orgs)
            const org = orgs.find(org => org.organizationId === orgId)
            if (!org) {
                console.log("man")
                return null
            }
            console.log(org)
            setOrg(org)
        }

        getOrgByID(orgId)

        // if (orgId) {
        //     // delay(2000).then(() => {
        //     //     setOrg(getOrgByID(orgId))
        //     // })
        //     console.log(orgId)
        //     const org
        //     setOrg(getOrgByID(orgId))
        // }
    }, [orgId])

    return (
        <div className="flex flex-col justify-begin items-center gap-0">



            {formStage === 1 ? (
                <>
                    <h1 className={`text-5xl text-center text-neutral-300 p-5 ${DMSans.className}`}>Check your inbox!</h1>
                    <h3 className={`text-3xl text-center text-neutral-300 ${DMSans.className}`}>We sent you a code. It will expire in 2 minutes</h3>
                    <PinInput count={6} size="2xl" className={`mt-20 p-5 bg-neutral-600 rounded-2xl ${DMSans.className}`} variant="flushed" otp />
                    <button className={`bg-neutral-600 m-20 p-4 transition-all ease-out hover:ease-in hover:bg-neutral-500 duration-10 
                        text-neutral-200 ${DMSans.className} text-2xl rounded-2xl`} onClick={() => confirmVerificationCode()}>Confirm</button>
                </>
            ) : (

                <>
                    <h1 className={`text-5xl text-center text-neutral-300 p-5 ${DMSans.className}`}>Verify</h1>
                    <h3 className={`text-2xl text-center text-neutral-300 p-1 ${DMSans.className}`}>
                        To continue, make sure you have access to the email listed as Primary Contact on Engage</h3>
                    <h3 className={`text-2xl text-center text-neutral-300 p-1 ${DMSans.className}`}>
                        We will send an email to this address with a verification code</h3>
                    <Suspense fallback={<div>Loading...</div>}>
                        <VerificationProcessCard _org={org} />
                    </Suspense>
                    <h3 className={`text-2xl text-center text-red-500 pt-10 pb-3 ${DMSans.className}`}>
                        Check this box to confirm you have access to the email <span className="font-bold text-neutral-200">
                            {org?.primaryContact}
                        </span>
                    </h3>
                    <Checkbox variant={"subtle"} size="lg"
                        className="bg-neutral-300 rounded-lg"
                        onCheckedChange={(e) => setAcknowledged(!!e.checked)}
                    ></Checkbox>
                    <button className={`${!acknowledged ? "bg-neutral-500" : "bg-neutral-600"} m-20 p-4 transition-all ease-out 
            ${!acknowledged ? "" : "hover:ease-in"} ${!acknowledged ? "" : "hover:bg-neutral-500"}  duration-10 
            ${DMSans.className} text-2xl rounded-2xl text-neutral-200`}
                        onClick={nextStep} disabled={!acknowledged}>Send Verification Email</button>

                </>
            )}
            {/* <Image src="/onboarding_primary_contact_example.png" alt="Primary Contact Example" width={500} height={500} /> */} {/*TODO: add video showing where to find primary contact*/}
        </div>
    )
}
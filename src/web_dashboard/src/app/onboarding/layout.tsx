"use client"
import { Icon } from "@chakra-ui/react/icon";
import { useRouter } from "next/navigation";
import { FC, Suspense } from "react";
import { MdArrowBack } from "react-icons/md";

export default function OnboardingLayout({ children }: Readonly<{ children: React.ReactNode }>) {
    const router = useRouter()

    const back = () => {
        router.back()
    }
    return (
        <div className={"w-screen h-screen immersion-gradient"}>
            <Suspense fallback={<div>Loading...</div>}>
                <Icon onClick={back} className={"relative top-4 left-4 text-white hover:bg-neutral-400 rounded-full cursor-pointer"} fontSize={"2rem"}>
                    <MdArrowBack />
                </Icon>
                {children}
            </Suspense>
        </div>
    )
}
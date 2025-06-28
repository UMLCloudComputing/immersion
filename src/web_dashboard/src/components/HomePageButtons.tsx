"use client"
import { DMSans } from '@/fonts';
import { useRouter } from 'next/navigation';
import React from 'react'

export const HomePageButtons = () => {

    const router = useRouter()


    const beginOnboarding = () => {
        router.push("/onboarding/choose-server")
        //redirect("onboarding/choose-server")
    }

    const dashboard = () => {
        router.push("/dashboard")
        //redirect("onboarding/choose-server")
    }

    return (
        <div>
            <button className={`immersion-gradient transition-all duration-500 ease-out hover-ease-in hover:shadow-xl hover:shadow-blue-400 shadow-none w-60 h-16 rounded-lg ${DMSans.className} text-3xl text-white font-bold hover:opacity-80`} onClick={beginOnboarding}>Get started</button>
            <button className={`transition-all duration-500 ease-out hover-ease-in hover:shadow-xl hover:shadow-blue-400 shadow-none border-2 border-black w-60 h-16 rounded-lg ml-5 ${DMSans.className} text-3xl text-black font-bold hover:opacity-80 hover:bg-black hover:text-white `} onClick={dashboard}>Dashboard</button>
        </div>
    );
}
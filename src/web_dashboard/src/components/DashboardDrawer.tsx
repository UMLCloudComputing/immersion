"use client"
import { useState } from "react"
import { DashboardDrawerButton } from "./DashboardDrawerButton"


export const DashboardDrawer = () => {
    const [open, setOpen] = useState(false)
    return (
        <div className="flex flex-col w-1/6 h-full immersion-gradient-v rounded-xl m-2 p-2 justify-between">
            <div className="flex flex-col gap-2">
                <DashboardDrawerButton />
                <DashboardDrawerButton />
            </div>
            <DashboardDrawerButton />
        </div>
    )
}
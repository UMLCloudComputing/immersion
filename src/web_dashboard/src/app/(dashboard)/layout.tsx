import { DashboardDrawer } from "@/components/DashboardDrawer";
import React from "react";

export default function DashboardLayout({ children }: Readonly<{ children: React.ReactNode }>) {
    return (
        <>
            <DashboardDrawer />
            {children}
        </>
    )
}
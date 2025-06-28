
import { HomePageButtons } from "@/components/HomePageButtons"
import { DMSans } from "../fonts"
import Image from "next/image"
export default async function HomePage() {
  return (

    <div className="flex flex-col bg-neutral-300 w-screen h-screen items-center justify-center">
      <div className="flex flex-col gap-10 mb-40 items-center w-2/3">
        <h1 className={`${DMSans.className} font-bold text-black text-6xl text-center`}>Easily integrate <span className="text-engage-green">Engage</span> with your club&apos;s <span className="text-discord-purple">Discord</span></h1>
        <div className="flex flex-row">
          <HomePageButtons />
        </div>
      </div>
      <div className="flex flex-row">
        <Image src="/engage_logo.svg" alt="Engage Logo" width={200} height={200} />
        <Image src="/immersion_logo_g.svg" alt="Immersion Logo" width={200} height={200} />
        <Image src="/discord_logo.svg" alt="Discord Logo" width={200} height={274} />
      </div>
    </div>
  )
}
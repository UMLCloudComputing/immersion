import { DMSans } from "@/fonts";
import { Guild } from "@/types/types";
import Image from "next/image";

// eslint-disable-next-line
export const GuildIcon = ({ guild, onClick }: { guild: Guild, onClick: any }) => {


    return (
        <button className="flex flex-col justify-between items-center text-wrap basis-40 grow-1" onClick={() => onClick(guild)}>
            <div className="justify-center items-center flex w-32 h-32 overflow-hidden rounded-full bg-white border-neutral-500 border-4 hover:border-custom-cyan transition-all duration-25 ease-out hover-ease-in">
                {
                    guild.icon == null ? (
                        // dont know if this will ever happen
                        <Image src={"/discord_logo.svg"} alt="Guild Icon" width={512} height={512} objectFit="cover" />
                    ) : (
                        <Image src={`https://cdn.discordapp.com/icons/${guild.id}/${guild.icon}.png`} alt="Guild Icon" width={512} height={512} />
                    )
                }
            </div>
            <h3 className={`text-neutral-300 text-wrap text-center ${DMSans.className}`}>{guild.name}</h3>
        </button>
    )
}
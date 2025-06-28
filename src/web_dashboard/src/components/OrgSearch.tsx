"use client"
import { DMSans } from "@/fonts";
import { Org } from "@/types/types";
import { Input } from "@chakra-ui/react"
import Image from "next/image";
import { ChangeEvent, useState } from "react";
import { OrgSearchProps } from "@/types/props";


// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const OrgSearch = ({ props }: { props: OrgSearchProps }) => {

    const [input, setInput] = useState("");
    const [suggestions, setSuggestions] = useState<Org[]>([]);

    const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
        const query = e.target.value;
        setInput(query);

        // Filter the suggestions based on the input query
        if (query.length >= 3) {
            const filteredSuggestions = props.orgs.filter((org) =>
                org.name.toLowerCase().startsWith(query.toLowerCase())
            );
            setSuggestions(filteredSuggestions);
        } else {
            setSuggestions([]); // If the query is empty, don't show any suggestions
        }
    };

    const handleSuggestionClick = (suggestion: Org) => {
        setInput(suggestion.name); // Set input to the clicked suggestion
        setSuggestions([]); // Clear suggestions
        props.setOrg(suggestion)
    };
    return (
        <div className="flex flex-row flex-wrap gap-1 gap-y-4 justify-center items-begin w-1/2 bg-neutral-600 p-4 rounded-3xl">
            <Input variant={"flushed"} _placeholder={{ color: "bg-neutral-300", font: DMSans.className }} placeholder="Search for your club" onChange={handleInputChange} value={input} className={`${DMSans.className} text-neutral-300`} />
            {/* Suggestions list */}
            {suggestions.length > 0 && (
                <div className="flex flex-col gap-1 justify-begin w-full">
                    {suggestions.map((suggestion, index) => (
                        <button className="hover:bg-neutral-500 rounded-3xl flex flex-row items-center p-2" onClick={() => handleSuggestionClick(suggestion)} key={index} >
                            <Image className="overflow-hidden rounded-full mr-5 border-2 border-neutral-300" src={suggestion.imageUrl} alt="Org Icon" width={32} height={32} />
                            <div className={`${DMSans.className} text-neutral-300`}>{suggestion.name}</div>
                        </button>
                    ))}
                </div>
            )}
        </div >
    )
}
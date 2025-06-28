import { DDBOrgItem, Org } from "@/types/types";
import { TbObjectScan } from "react-icons/tb";
import { VscCalendar } from "react-icons/vsc";
import { unmarshall } from "@aws-sdk/util-dynamodb";
import { AttributeValue } from "@aws-sdk/client-dynamodb";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const ddbOrgItemToRawJSON = (ddbItems: any[]) => {
    return ddbItems.map(item => unmarshall(item))
}
export interface GradientDivProps {
    children: ReactNode
    className: string
}

export interface OrgSearchProps {
    orgs: Org[]
    setOrg: React.SetStateAction<Org>
}
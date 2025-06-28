import { ProgressCircleRoot, ProgressCircleRing } from "@/components/ui/progress-circle";

export default async function ChooseServerLoadingPage() {
    return (
        <div className="flex flex-row flex-wrap gap-1 gap-y-4 justify-center items-begin w-1/2 bg-neutral-600 p-4 rounded-3xl">
            <ProgressCircleRoot value={null} size="lg">
                <ProgressCircleRing cap="round" />
            </ProgressCircleRoot> :
        </div>
    )
}
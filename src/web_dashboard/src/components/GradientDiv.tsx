import { GradientDivProps } from "@/types/props";
import { useEffect, useState } from "react";


const GradientPosition = () => {

    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
    const windowWidth = window.innerHeight

    useEffect(() => {
        const updateMousePosition = (e: MouseEvent) => {
            setMousePosition({ x: e.clientX, y: e.clientY });
        };
        window.addEventListener('mousemove', updateMousePosition);
        return () => {
            window.removeEventListener('mousemove', updateMousePosition);
        };
    }, []);

    return (mousePosition)
};

export const GradientDiv: React.FC<GradientDivProps> = ({ children, className }) => {
    return (
        <div
            style={{
                backgroundImage: `radial-gradient( circle at ${GradientPosition().x}px ${GradientPosition().y}px, red  , blue 50% )`
            }}
            className={className}>
            {children}
        </div>
    )
}

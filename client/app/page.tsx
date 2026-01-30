"use client";

import { useState } from "react";
import CalculatorInput from "../components/CalculatorInput";
import SolutionViewer from "../components/SolutionViewer";
import { motion } from "framer-motion";

export default function Home() {
    const [solutionData, setSolutionData] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    // Define the types for the API response in a real scenario
    // For now using 'any' to proceed quickly with the skeleton

    const handleSolve = async (expression: string) => {
        setLoading(true);
        try {
            // In a real env, this would point to localhost:8000
            const response = await fetch("http://localhost:8000/solve", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    expression,
                    mode: "solve", // Defaulting to solve for now
                }),
            });

            const data = await response.json();
            setSolutionData(data);
        } catch (error) {
            console.error("Error solving:", error);
            // Mock data for fallback/demo purposes if backend isn't running
            setSolutionData({
                result_latex: "x = -1",
                steps: [
                    { description: "Identify the equation", latex: "x + 1 = 0" },
                    { description: "Subtract 1 from both sides", latex: "x = -1" }
                ],
                explanation: "This is a mock response because the backend connection failed."
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <main className="flex min-h-screen flex-col items-center justify-between p-4 md:p-24 bg-[var(--background)] relative overflow-hidden">
            {/* Background Ambient Glow */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none z-0">
                <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-primary opacity-10 blur-[120px] rounded-full"></div>
                <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-secondary opacity-10 blur-[120px] rounded-full"></div>
            </div>

            <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex flex-col gap-8">
                <motion.h1
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-4xl md:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent neon-glow text-center"
                >
                    Math Universe
                </motion.h1>

                <CalculatorInput onSolve={handleSolve} isLoading={loading} />

                {solutionData && (
                    <SolutionViewer data={solutionData} />
                )}
            </div>
        </main>
    );
}

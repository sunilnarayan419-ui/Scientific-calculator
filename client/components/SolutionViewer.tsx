"use client";

import { motion } from "framer-motion";
import "katex/dist/katex.min.css";
// We would strictly use a library here, but for now assuming direct rendering or a simple wrapper
// In a real app we'd use 'react-latex-next'

interface Step {
    description: string;
    latex: string;
}

interface SolutionData {
    result_latex: string;
    steps: Step[];
    explanation: string;
}

interface Props {
    data: SolutionData;
}

export default function SolutionViewer({ data }: Props) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full max-w-4xl space-y-6"
        >
            {/* Result Card */}
            <div className="glass-panel p-8 rounded-2xl border-l-4 border-primary">
                <h2 className="text-gray-400 text-sm uppercase tracking-wider mb-2">Result</h2>
                <div className="text-3xl font-bold font-mono text-white">
                    {/* In real implementation, render LaTeX here */}
                    {data.result_latex}
                </div>
                <p className="mt-4 text-gray-300">{data.explanation}</p>
            </div>

            {/* Steps */}
            <div className="space-y-4">
                <h3 className="text-xl font-bold text-white mb-4">Step-by-Step</h3>
                {data.steps.map((step, index) => (
                    <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="glass-panel p-6 rounded-xl"
                    >
                        <p className="text-gray-400 mb-2 font-medium">Step {index + 1}</p>
                        <p className="text-white text-lg mb-2">{step.description}</p>
                        <div className="p-3 bg-black/30 rounded-lg font-mono text-secondary">
                            {step.latex}
                        </div>
                    </motion.div>
                ))}
            </div>
        </motion.div>
    );
}

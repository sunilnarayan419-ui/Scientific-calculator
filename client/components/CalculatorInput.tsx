"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { ArrowRight, Loader2 } from "lucide-react";

interface Props {
    onSolve: (expression: string) => void;
    isLoading: boolean;
}

export default function CalculatorInput({ onSolve, isLoading }: Props) {
    const [input, setInput] = useState("");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (input.trim()) {
            onSolve(input);
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-full max-w-2xl"
        >
            <form onSubmit={handleSubmit} className="relative group">
                <div className="absolute -inset-1 bg-gradient-to-r from-primary to-accent rounded-xl blur opacity-25 group-hover:opacity-75 transition duration-1000 group-hover:duration-200"></div>
                <div className="relative glass-panel rounded-xl p-2 flex items-center">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type a math problem..."
                        className="w-full bg-transparent border-none outline-none text-xl p-4 text-white placeholder-gray-500 font-sans"
                    />
                    <button
                        type="submit"
                        disabled={isLoading}
                        className="p-3 bg-primary/20 hover:bg-primary/40 rounded-lg text-primary transition-colors disabled:opacity-50"
                    >
                        {isLoading ? <Loader2 className="animate-spin" /> : <ArrowRight />}
                    </button>
                </div>
            </form>
        </motion.div>
    );
}

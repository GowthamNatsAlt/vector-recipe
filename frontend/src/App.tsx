import { useState, useEffect } from "react";
import {
    Search,
    Hash,
    Utensils,
    List,
    AlertCircle,
    Loader2,
} from "lucide-react";

interface Recipe {
    title: string;
    ingredients: string[];
    directions: string[];
    NER: string[];
    score: number;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function SearchApp() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<Recipe[]>([]);
    const [loading, setLoading] = useState(false);
    const [showColdStartWarning, setShowColdStartWarning] = useState(false);
    const [numSearches, setNumSearches] = useState(0);

    useEffect(() => {
        let timer: number;
        if (loading) {
            timer = window.setTimeout(() => {
                setShowColdStartWarning(true);
            }, 2000);
        } else {
            setShowColdStartWarning(false);
        }
        return () => clearTimeout(timer);
    }, [loading]);

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;

        setLoading(true);
        setResults([]);
        try {
            const response = await fetch(
                `${API_BASE_URL}/api/search?query=${encodeURIComponent(query)}`,
            );

            if (!response.ok) throw new Error("Search failed");

            const data = await response.json();

            if (Array.isArray(data)) {
                const filteredResults = data.filter(
                    (recipe: Recipe) => recipe.score > 0,
                );
                setResults(filteredResults);
            } else {
                console.error("Received non-array response:", data);
                if (data.results && Array.isArray(data.results)) {
                    setResults(data.results.filter((r: Recipe) => r.score > 0));
                } else {
                    setResults([]);
                }
            }

            setNumSearches((prev) => prev + 1);
        } catch (err) {
            console.error("Search failed:", err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-zinc-950 text-zinc-100 selection:bg-orange-500/30 font-sans">
            <div className="fixed top-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-orange-500/10 blur-[120px] pointer-events-none" />

            <main className="relative max-w-4xl mx-auto pt-20 px-6">
                <header className="mb-12 text-center">
                    <h1 className="text-5xl font-extrabold tracking-tighter mb-3 italic bg-gradient-to-b from-white to-zinc-500 bg-clip-text text-transparent">
                        VectorRecipe
                    </h1>
                    <p className="text-zinc-500 text-sm font-medium tracking-wide uppercase">
                        AI-Driven Semantic Recipe Discovery
                    </p>
                </header>

                <form onSubmit={handleSearch} className="relative group mb-8">
                    <div className="absolute inset-y-0 left-5 flex items-center pointer-events-none">
                        {loading ? (
                            <Loader2 className="w-5 h-5 animate-spin text-orange-500" />
                        ) : (
                            <Search className="w-5 h-5 text-zinc-500 group-focus-within:text-orange-500 transition-colors" />
                        )}
                    </div>
                    <input
                        type="text"
                        className="w-full bg-zinc-900/40 border border-zinc-800 rounded-2xl py-5 pl-14 pr-6 focus:outline-none focus:ring-2 focus:ring-orange-500/40 focus:border-orange-500/40 transition-all placeholder:text-zinc-600 text-lg shadow-2xl backdrop-blur-md"
                        placeholder="Search recipes by ingredients or keywords..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                </form>

                {showColdStartWarning && (
                    <div className="mb-8 animate-in fade-in slide-in-from-top-2 duration-500">
                        <div className="flex items-start gap-4 p-4 rounded-2xl bg-orange-500/5 border border-orange-500/20 backdrop-blur-sm">
                            <AlertCircle className="w-5 h-5 text-orange-500 mt-0.5 shrink-0" />
                            <div>
                                <h4 className="text-sm font-bold text-orange-400">
                                    Waking up the Engine
                                </h4>
                                <p className="text-xs text-zinc-400 mt-1 leading-relaxed">
                                    Our free-tier instance is currently spinning
                                    up. This first search may take up to 30
                                    seconds to process the vector data. Thanks
                                    for your patience!
                                </p>
                            </div>
                        </div>
                    </div>
                )}

                <div className="space-y-8 pb-24">
                    {results.map((recipe, index) => (
                        <article
                            key={index}
                            className="bg-zinc-900/30 border border-zinc-800/50 rounded-3xl overflow-hidden hover:border-orange-500/30 transition-all duration-500 group"
                        >
                            <div className="p-6 border-b border-zinc-800/50 flex justify-between items-center bg-zinc-900/20">
                                <h3 className="text-2xl font-bold group-hover:text-orange-400 transition-colors">
                                    {recipe.title}
                                </h3>
                                <div className="flex items-center gap-2">
                                    <span className="text-[10px] font-mono font-bold text-orange-500 bg-orange-500/10 px-3 py-1.5 rounded-full border border-orange-500/20 uppercase tracking-widest">
                                        <Hash className="w-3 h-3 inline mr-1" />
                                        {Math.round(recipe.score * 100)}% Match
                                    </span>
                                </div>
                            </div>

                            <div className="grid md:grid-cols-5 gap-0">
                                <div className="md:col-span-2 p-6 bg-black/20 border-r border-zinc-800/50">
                                    <div className="flex items-center gap-2 mb-4 text-zinc-400 font-semibold text-xs uppercase tracking-wider">
                                        <Utensils className="w-4 h-4 text-orange-500" />
                                        Ingredients
                                    </div>
                                    <ul className="space-y-2">
                                        {recipe.ingredients.map((ing, i) => (
                                            <li
                                                key={i}
                                                className="text-sm text-zinc-400 flex gap-2"
                                            >
                                                <span className="text-orange-500/50">
                                                    •
                                                </span>
                                                {ing}
                                            </li>
                                        ))}
                                    </ul>
                                </div>

                                <div className="md:col-span-3 p-6">
                                    <div className="flex items-center gap-2 mb-4 text-zinc-400 font-semibold text-xs uppercase tracking-wider">
                                        <List className="w-4 h-4 text-orange-500" />
                                        Directions
                                    </div>
                                    <div className="space-y-4">
                                        {recipe.directions.map((step, i) => (
                                            <div key={i} className="flex gap-4">
                                                <span className="text-xs font-mono text-zinc-600 mt-1">
                                                    {(i + 1)
                                                        .toString()
                                                        .padStart(2, "0")}
                                                </span>
                                                <p className="text-sm text-zinc-300 leading-relaxed italic">
                                                    {step}
                                                </p>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>

                            <div className="p-4 bg-zinc-900/40 border-t border-zinc-800/50 flex flex-wrap gap-2">
                                {recipe.NER.map((tag, i) => (
                                    <span
                                        key={i}
                                        className="text-[10px] px-2 py-1 bg-zinc-800 text-zinc-500 rounded-md hover:text-zinc-300 hover:bg-zinc-700 transition-colors cursor-default"
                                    >
                                        #{tag.toLowerCase().replace(/\s+/g, "")}
                                    </span>
                                ))}
                            </div>
                        </article>
                    ))}

                    {loading && (
                        <div className="space-y-8 animate-pulse">
                            {[...Array(3)].map((_, i) => (
                                <div
                                    key={i}
                                    className="bg-zinc-900/20 border border-zinc-800/50 rounded-3xl p-8 h-64 flex flex-col gap-4"
                                >
                                    <div className="h-8 w-1/3 bg-zinc-800 rounded-lg" />
                                    <div className="flex gap-4">
                                        <div className="h-32 w-1/3 bg-zinc-800/50 rounded-xl" />
                                        <div className="h-32 w-2/3 bg-zinc-800/50 rounded-xl" />
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {results.length === 0 && !loading && (
                        <div className="text-center py-32 border border-dashed border-zinc-800 rounded-[2.5rem] bg-zinc-900/10">
                            <div className="inline-flex p-4 rounded-full bg-zinc-900 mb-4 text-zinc-700">
                                <Search className="w-8 h-8" />
                            </div>
                            <p className="text-zinc-500 font-medium">
                                {numSearches === 0
                                    ? "Ready to search over 5,000 recipes"
                                    : "No exact matches found"}
                            </p>
                            <p className="text-zinc-700 text-xs mt-2">
                                Try ingredients like "Parmesan", "Basil", or
                                "Slow Cooker"
                            </p>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}

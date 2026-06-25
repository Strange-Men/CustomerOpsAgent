import { useState } from "react";
import { EXAMPLE_QUESTIONS } from "../../data/examples";

interface ExamplePromptsProps {
  onSelect?: (query: string) => void;
}

/**
 * Row of example prompt buttons.
 * When onSelect is provided, clicking a button sends the query to the parent.
 * Otherwise falls back to local selected state (static mode).
 */
export function ExamplePrompts({ onSelect }: ExamplePromptsProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const handleClick = (id: string, query: string) => {
    if (onSelect) {
      onSelect(query);
    } else {
      setSelectedId(id === selectedId ? null : id);
    }
  };

  return (
    <div className="flex flex-wrap gap-2">
      {EXAMPLE_QUESTIONS.map((q) => {
        const isSelected = q.id === selectedId;

        return (
          <button
            key={q.id}
            onClick={() => handleClick(q.id, q.query)}
            className={`
              px-3 py-1.5 text-xs rounded-lg transition-colors duration-150 cursor-pointer
              ${
                isSelected
                  ? "bg-fuchsia-600/25 text-fuchsia-200 border border-fuchsia-500/40"
                  : "bg-slate-800/60 text-slate-400 border border-slate-700/30 hover:bg-slate-700/60 hover:text-slate-200 hover:border-purple-500/25"
              }
            `.trim()}
          >
            {q.label}
          </button>
        );
      })}
    </div>
  );
}

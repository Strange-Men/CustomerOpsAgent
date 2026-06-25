import { useState } from "react";
import { EXAMPLE_QUESTIONS } from "../../data/examples";

/**
 * Row of example prompt buttons — static display, no API call on click.
 * Supports selected state via local React state.
 */
export function ExamplePrompts() {
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const handleClick = (id: string) => {
    setSelectedId(id === selectedId ? null : id);
  };

  return (
    <div className="flex flex-wrap gap-2">
      {EXAMPLE_QUESTIONS.map((q) => {
        const isSelected = q.id === selectedId;

        return (
          <button
            key={q.id}
            onClick={() => handleClick(q.id)}
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

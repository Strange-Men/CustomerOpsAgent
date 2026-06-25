import { EXAMPLE_QUESTIONS } from "../../data/examples";

/**
 * Row of example prompt buttons — static display, no API call on click.
 */
export function ExamplePrompts() {
  return (
    <div className="flex flex-wrap gap-2">
      {EXAMPLE_QUESTIONS.map((q) => (
        <button
          key={q.id}
          className="
            px-3 py-1.5 text-xs rounded-lg
            bg-slate-800/60 text-slate-400
            border border-slate-700/30
            hover:bg-slate-700/60 hover:text-slate-200 hover:border-purple-500/25
            transition-colors duration-150 cursor-pointer
          "
        >
          {q.text}
        </button>
      ))}
    </div>
  );
}

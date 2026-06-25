import type { LLMProfile } from "../../lib/types";

interface ModelSelectorProps {
  selected: LLMProfile;
  onSelect: (profile: LLMProfile) => void;
  disabled?: boolean;
}

/** Profile options with display labels and descriptions. */
const PROFILE_OPTIONS: {
  value: LLMProfile;
  label: string;
  description: string;
}[] = [
  {
    value: "mock",
    label: "Mock",
    description: "默认模板模式，无需 key",
  },
  {
    value: "deepseek",
    label: "DeepSeek",
    description: "由后端 Render 环境变量配置，前端不保存 key",
  },
  {
    value: "doubao",
    label: "Doubao",
    description: "由后端 Render 环境变量配置，前端不保存 key",
  },
];

/**
 * Model profile selector — lets the user choose which LLM profile to use.
 * Only sends the public profile name to the backend.
 * Never shows API key inputs or base_url fields.
 */
export function ModelSelector({
  selected,
  onSelect,
  disabled = false,
}: ModelSelectorProps) {
  return (
    <div className="space-y-2">
      <p className="text-[10px] text-slate-500 uppercase tracking-wider">
        模型档案
      </p>
      <div className="flex flex-wrap gap-2">
        {PROFILE_OPTIONS.map((opt) => {
          const isSelected = selected === opt.value;
          return (
            <button
              key={opt.value}
              onClick={() => onSelect(opt.value)}
              disabled={disabled}
              title={opt.description}
              className={`
                px-3 py-1.5 text-xs rounded-lg transition-colors duration-150 cursor-pointer
                disabled:opacity-50 disabled:cursor-not-allowed
                ${
                  isSelected
                    ? "bg-fuchsia-600/25 text-fuchsia-200 border border-fuchsia-500/40"
                    : "bg-slate-800/60 text-slate-400 border border-slate-700/30 hover:bg-slate-700/60 hover:text-slate-200 hover:border-purple-500/25"
                }
              `.trim()}
            >
              {opt.label}
            </button>
          );
        })}
      </div>
      <p className="text-[10px] text-slate-600">
        {PROFILE_OPTIONS.find((o) => o.value === selected)?.description}
      </p>
    </div>
  );
}

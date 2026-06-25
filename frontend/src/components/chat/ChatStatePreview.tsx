import { Card } from "../common/Card";

/**
 * Static preview of chat UI states: Loading, Empty, Error.
 * Visual placeholders only — not connected to real API state.
 */
export function ChatStatePreview() {
  return (
    <div className="space-y-4 pt-4 border-t border-slate-700/30">
      <p className="text-xs text-slate-500">状态预览（静态占位）：</p>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {/* Loading state */}
        <Card className="!p-3">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-sky-400 rounded-full animate-pulse" />
              <span className="text-xs text-sky-400">Loading</span>
            </div>
            <p className="text-[10px] text-slate-500">
              模拟 Agent 正在分析问题...
            </p>
          </div>
        </Card>

        {/* Empty state */}
        <Card className="!p-3">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-slate-500 rounded-full" />
              <span className="text-xs text-slate-400">Empty</span>
            </div>
            <p className="text-[10px] text-slate-500">
              请选择示例问题或输入问题
            </p>
          </div>
        </Card>

        {/* Error state */}
        <Card className="!p-3">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-amber-400 rounded-full" />
              <span className="text-xs text-amber-400">Error</span>
            </div>
            <p className="text-[10px] text-slate-500">
              API 未接入，M4 才会处理真实错误
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
}

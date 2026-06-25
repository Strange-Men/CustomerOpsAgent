/**
 * Bottom status bar showing system-level indicators.
 */
export function StatusBar() {
  return (
    <footer className="border-t border-purple-500/10 bg-slate-950/80">
      <div className="max-w-[1600px] mx-auto px-6 py-2 flex items-center justify-between text-xs text-slate-600">
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-500/60" />
            No real logistics API
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-500/60" />
            No real order system
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-sky-500/60" />
            API integration in Frontend M4
          </span>
        </div>
        <span className="text-slate-700">
          CustomerOpsAgent &middot; Demo Console
        </span>
      </div>
    </footer>
  );
}

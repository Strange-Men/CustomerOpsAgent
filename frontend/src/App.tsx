import { RELEASE_TAG } from "./lib/constants";

function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center">
      <div className="text-center space-y-6">
        <h1 className="text-4xl font-bold tracking-tight">
          CustomerOpsAgent
        </h1>
        <span className="inline-block px-3 py-1 text-sm rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30">
          {RELEASE_TAG}
        </span>
        <p className="text-slate-400 text-sm">
          Frontend scaffold initialized
        </p>
        <p className="text-slate-500 text-xs">
          Dark + pink/purple theme locked &middot; API integration in Frontend M4
        </p>
        <p className="text-slate-600 text-xs">
          Mock default &middot; No real logistics API &middot; No real order system
        </p>
      </div>
    </div>
  );
}

export default App;

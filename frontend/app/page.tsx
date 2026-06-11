export default function Home() {
  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      {/* Top bar */}
      <header className="border-b border-[var(--border)] bg-[var(--surface)] px-6 py-3">
        <div className="flex items-center justify-between">
          <h1 className="text-lg font-semibold text-[var(--text)]">
            CustomerOps Agent
          </h1>
          <span className="text-xs text-[var(--text-muted)] bg-[var(--surface-alt)] px-2 py-1 rounded">
            待接入
          </span>
        </div>
      </header>

      {/* Main content */}
      <main className="mx-auto max-w-7xl px-6 py-8">
        {/* Ticket input placeholder */}
        <section className="mb-8">
          <h2 className="text-sm font-medium text-[var(--text-muted)] mb-3">
            工单分析
          </h2>
          <div className="rounded-lg border border-[var(--border)] bg-[var(--surface)] p-6">
            <div className="mb-4">
              <label className="block text-sm text-[var(--text-muted)] mb-2">
                工单 ID
              </label>
              <div className="h-10 rounded border border-[var(--border)] bg-[var(--surface-alt)]" />
            </div>
            <div className="mb-4">
              <label className="block text-sm text-[var(--text-muted)] mb-2">
                用户消息
              </label>
              <div className="h-24 rounded border border-[var(--border)] bg-[var(--surface-alt)]" />
            </div>
            <button
              disabled
              className="px-4 py-2 text-sm font-medium rounded bg-[var(--accent)] text-white opacity-50 cursor-not-allowed"
            >
              分析工单
            </button>
          </div>
        </section>

        {/* Two column layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Agent Timeline placeholder */}
          <section>
            <h2 className="text-sm font-medium text-[var(--text-muted)] mb-3">
              Agent Timeline
            </h2>
            <div className="rounded-lg border border-[var(--border)] bg-[var(--surface)] p-6 min-h-[300px]">
              <div className="space-y-4">
                {[
                  "信息提取",
                  "订单验证",
                  "方案检索",
                  "物流追踪",
                  "话术编排",
                  "质量审查",
                ].map((step) => (
                  <div key={step} className="flex items-start gap-3">
                    <div className="mt-1 h-2 w-2 rounded-full bg-gray-300" />
                    <div className="flex-1">
                      <div className="text-sm text-[var(--text)]">{step}</div>
                      <div className="text-xs text-[var(--text-muted)]">
                        待执行
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* Evidence / Tool Result / QA placeholder */}
          <section>
            <h2 className="text-sm font-medium text-[var(--text-muted)] mb-3">
              分析结果
            </h2>
            <div className="space-y-4">
              {/* Evidence card placeholder */}
              <div className="rounded-lg border border-[var(--border)] bg-[var(--surface)] p-4">
                <div className="text-xs text-[var(--text-muted)] mb-2">
                  Evidence
                </div>
                <div className="h-16 rounded bg-[var(--surface-alt)]" />
              </div>

              {/* Tool Result card placeholder */}
              <div className="rounded-lg border border-[var(--border)] bg-[var(--surface)] p-4">
                <div className="text-xs text-[var(--text-muted)] mb-2">
                  Tool Result
                </div>
                <div className="h-16 rounded bg-[var(--surface-alt)]" />
              </div>

              {/* QA card placeholder */}
              <div className="rounded-lg border border-[var(--border)] bg-[var(--surface)] p-4">
                <div className="text-xs text-[var(--text-muted)] mb-2">
                  QA 审查
                </div>
                <div className="h-16 rounded bg-[var(--surface-alt)]" />
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}

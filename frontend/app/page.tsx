export default function Home() {
  return (
    <div className="min-h-screen flex flex-col" style={{ background: "var(--bg)" }}>
      {/* ─── Header ─── */}
      <header
        className="flex items-center justify-between px-6 py-0 h-12 shrink-0"
        style={{
          background: "var(--surface)",
          borderBottom: "1px solid var(--border)",
        }}
      >
        <div className="flex items-center gap-4">
          <span className="text-sm font-semibold" style={{ color: "var(--text)" }}>
            CustomerOps Agent
          </span>
          <nav className="flex items-center gap-1">
            {[
              { label: "Tickets", active: true },
              { label: "Eval", active: false },
            ].map((tab) => (
              <span
                key={tab.label}
                className="px-3 py-1.5 text-xs font-medium rounded"
                style={{
                  background: tab.active ? "var(--accent-bg)" : "transparent",
                  color: tab.active ? "var(--accent)" : "var(--text-muted)",
                }}
              >
                {tab.label}
              </span>
            ))}
          </nav>
        </div>
        <div className="flex items-center gap-3">
          <span
            className="inline-flex items-center gap-1.5 text-xs"
            style={{ color: "var(--text-muted)" }}
          >
            <span
              className="inline-block w-1.5 h-1.5 rounded-full"
              style={{ background: "var(--success)" }}
            />
            Mock Mode
          </span>
          <span
            className="text-xs px-2 py-0.5 rounded"
            style={{
              background: "var(--surface-alt)",
              color: "var(--text-muted)",
            }}
          >
            v0.0.7
          </span>
        </div>
      </header>

      {/* ─── Main ─── */}
      <main className="flex-1 overflow-auto">
        <div className="max-w-[1400px] mx-auto px-6 py-5">
          {/* ─── Ticket Intake ─── */}
          <section className="mb-5">
            <div
              className="rounded-lg"
              style={{
                background: "var(--surface)",
                border: "1px solid var(--border)",
              }}
            >
              <div
                className="px-5 py-3 flex items-center justify-between"
                style={{ borderBottom: "1px solid var(--border)" }}
              >
                <div className="flex items-center gap-2">
                  <span className="text-sm font-semibold" style={{ color: "var(--text)" }}>
                    Ticket Intake
                  </span>
                  <span
                    className="text-xs px-1.5 py-0.5 rounded"
                    style={{ background: "var(--surface-alt)", color: "var(--text-muted)" }}
                  >
                    New Analysis
                  </span>
                </div>
                <span className="text-xs" style={{ color: "var(--text-faint)" }}>
                  Agent workflow: Intent → Retrieval → Tool → Policy → Reply → QA
                </span>
              </div>

              <div className="p-5">
                <div className="grid grid-cols-12 gap-4">
                  {/* Message */}
                  <div className="col-span-7">
                    <label className="block text-xs font-medium mb-1.5" style={{ color: "var(--text-secondary)" }}>
                      Customer Message <span style={{ color: "var(--error)" }}>*</span>
                    </label>
                    <div
                      className="w-full h-20 rounded text-xs"
                      style={{
                        background: "var(--surface-alt)",
                        border: "1px solid var(--border)",
                      }}
                    />
                  </div>

                  {/* Right side fields */}
                  <div className="col-span-5 flex flex-col gap-3">
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="block text-xs font-medium mb-1.5" style={{ color: "var(--text-secondary)" }}>
                          Order ID
                        </label>
                        <div
                          className="h-8 rounded text-xs"
                          style={{
                            background: "var(--surface-alt)",
                            border: "1px solid var(--border)",
                          }}
                        />
                      </div>
                      <div>
                        <label className="block text-xs font-medium mb-1.5" style={{ color: "var(--text-secondary)" }}>
                          Product Type
                        </label>
                        <div
                          className="h-8 rounded text-xs"
                          style={{
                            background: "var(--surface-alt)",
                            border: "1px solid var(--border)",
                          }}
                        />
                      </div>
                    </div>
                    <div className="flex items-end gap-2 h-full">
                      <button
                        disabled
                        className="px-4 py-1.5 text-xs font-medium rounded cursor-not-allowed"
                        style={{
                          background: "var(--accent)",
                          color: "#fff",
                          opacity: 0.5,
                        }}
                      >
                        Analyze Ticket
                      </button>
                      <div className="flex items-center gap-1.5 ml-2">
                        <span className="text-xs" style={{ color: "var(--text-faint)" }}>
                          Quick:
                        </span>
                        {["ORD-2024-001", "ORD-2024-002", "ORD-2024-005"].map((id) => (
                          <span
                            key={id}
                            className="text-xs px-2 py-0.5 rounded cursor-default"
                            style={{
                              background: "var(--surface-alt)",
                              color: "var(--text-muted)",
                              border: "1px solid var(--border)",
                            }}
                          >
                            {id}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* ─── Main Grid: Workflow + Summary ─── */}
          <div className="grid grid-cols-12 gap-5 mb-5">
            {/* Agent Workflow - Left */}
            <div className="col-span-7">
              <div
                className="rounded-lg h-full"
                style={{
                  background: "var(--surface)",
                  border: "1px solid var(--border)",
                }}
              >
                <div
                  className="px-5 py-3"
                  style={{ borderBottom: "1px solid var(--border)" }}
                >
                  <span className="text-sm font-semibold" style={{ color: "var(--text)" }}>
                    Agent Workflow
                  </span>
                </div>
                <div className="p-5">
                  <div className="space-y-0">
                    {[
                      { name: "Intent Agent", desc: "Intent classification + entity extraction", status: "pending" },
                      { name: "Retrieval Agent", desc: "Knowledge base search + evidence retrieval", status: "pending" },
                      { name: "Tool Agent", desc: "Order lookup + logistics query", status: "pending" },
                      { name: "Policy Agent", desc: "Policy matching + eligibility check", status: "pending" },
                      { name: "Reply Agent", desc: "Response generation + policy citation", status: "pending" },
                      { name: "QA Agent", desc: "Quality check + risk assessment", status: "pending" },
                    ].map((agent, i) => (
                      <div
                        key={agent.name}
                        className="flex items-start gap-3 py-2.5"
                        style={{
                          borderBottom: i < 5 ? "1px solid var(--border)" : "none",
                        }}
                      >
                        {/* Step indicator */}
                        <div className="flex flex-col items-center mt-0.5 shrink-0 w-5">
                          <div
                            className="w-2.5 h-2.5 rounded-full"
                            style={{ background: "var(--border-strong)" }}
                          />
                          {i < 5 && (
                            <div
                              className="w-px flex-1 mt-1"
                              style={{ background: "var(--border)" }}
                            />
                          )}
                        </div>

                        {/* Content */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between">
                            <span className="text-xs font-medium" style={{ color: "var(--text)" }}>
                              {agent.name}
                            </span>
                            <span
                              className="text-xs px-1.5 py-0.5 rounded"
                              style={{
                                background: "var(--surface-alt)",
                                color: "var(--text-faint)",
                              }}
                            >
                              Pending
                            </span>
                          </div>
                          <span className="text-xs" style={{ color: "var(--text-muted)" }}>
                            {agent.desc}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Review Summary - Right */}
            <div className="col-span-5 flex flex-col gap-5">
              {/* Final Result */}
              <div
                className="rounded-lg"
                style={{
                  background: "var(--surface)",
                  border: "1px solid var(--border)",
                }}
              >
                <div
                  className="px-5 py-3"
                  style={{ borderBottom: "1px solid var(--border)" }}
                >
                  <span className="text-sm font-semibold" style={{ color: "var(--text)" }}>
                    Review Summary
                  </span>
                </div>
                <div className="p-5">
                  <div className="grid grid-cols-3 gap-4">
                    {[
                      { label: "Final Result", value: "—", color: "var(--text-faint)" },
                      { label: "Risk Level", value: "—", color: "var(--text-faint)" },
                      { label: "QA Score", value: "—", color: "var(--text-faint)" },
                    ].map((item) => (
                      <div key={item.label} className="text-center">
                        <div className="text-xs mb-1" style={{ color: "var(--text-muted)" }}>
                          {item.label}
                        </div>
                        <div className="text-sm font-semibold" style={{ color: item.color }}>
                          {item.value}
                        </div>
                      </div>
                    ))}
                  </div>
                  <div
                    className="mt-4 pt-4 flex items-center justify-between"
                    style={{ borderTop: "1px solid var(--border)" }}
                  >
                    <div>
                      <div className="text-xs" style={{ color: "var(--text-muted)" }}>
                        Human Review
                      </div>
                      <span
                        className="inline-block mt-1 text-xs px-2 py-0.5 rounded"
                        style={{
                          background: "var(--surface-alt)",
                          color: "var(--text-faint)",
                          border: "1px solid var(--border)",
                        }}
                      >
                        Not Required
                      </span>
                    </div>
                    <div className="text-right">
                      <div className="text-xs" style={{ color: "var(--text-muted)" }}>
                        Ticket ID
                      </div>
                      <div className="text-xs font-mono mt-1" style={{ color: "var(--text-faint)" }}>
                        —
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Reply Preview */}
              <div
                className="rounded-lg flex-1"
                style={{
                  background: "var(--surface)",
                  border: "1px solid var(--border)",
                }}
              >
                <div
                  className="px-5 py-3 flex items-center justify-between"
                  style={{ borderBottom: "1px solid var(--border)" }}
                >
                  <span className="text-sm font-semibold" style={{ color: "var(--text)" }}>
                    Reply Preview
                  </span>
                  <span
                    className="text-xs px-1.5 py-0.5 rounded"
                    style={{ background: "var(--surface-alt)", color: "var(--text-faint)" }}
                  >
                    Draft
                  </span>
                </div>
                <div className="p-5">
                  <div
                    className="h-24 rounded flex items-center justify-center text-xs"
                    style={{
                      background: "var(--surface-alt)",
                      color: "var(--text-faint)",
                      border: "1px dashed var(--border)",
                    }}
                  >
                    Agent reply will appear here
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* ─── Bottom Row: Evidence + Tool Results + QA ─── */}
          <div className="grid grid-cols-12 gap-5">
            {/* Evidence Preview */}
            <div className="col-span-4">
              <div
                className="rounded-lg"
                style={{
                  background: "var(--surface)",
                  border: "1px solid var(--border)",
                }}
              >
                <div
                  className="px-5 py-3 flex items-center justify-between"
                  style={{ borderBottom: "1px solid var(--border)" }}
                >
                  <span className="text-sm font-semibold" style={{ color: "var(--text)" }}>
                    Evidence Preview
                  </span>
                  <span className="text-xs" style={{ color: "var(--text-faint)" }}>
                    0 sources
                  </span>
                </div>
                <div className="p-5">
                  <div className="space-y-2">
                    {["Policy Document A", "Policy Document B", "Knowledge Base Entry"].map(
                      (doc, i) => (
                        <div
                          key={doc}
                          className="flex items-center gap-2 px-3 py-2 rounded text-xs"
                          style={{
                            background: "var(--surface-alt)",
                            border: "1px solid var(--border)",
                          }}
                        >
                          <span
                            className="inline-block w-1 h-6 rounded-full shrink-0"
                            style={{ background: "var(--border-strong)" }}
                          />
                          <div className="flex-1 min-w-0">
                            <div style={{ color: "var(--text-muted)" }}>{doc}</div>
                            <div style={{ color: "var(--text-faint)" }}>Relevance: —</div>
                          </div>
                        </div>
                      )
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Tool Results Preview */}
            <div className="col-span-4">
              <div
                className="rounded-lg"
                style={{
                  background: "var(--surface)",
                  border: "1px solid var(--border)",
                }}
              >
                <div
                  className="px-5 py-3 flex items-center justify-between"
                  style={{ borderBottom: "1px solid var(--border)" }}
                >
                  <span className="text-sm font-semibold" style={{ color: "var(--text)" }}>
                    Tool Results
                  </span>
                  <span className="text-xs" style={{ color: "var(--text-faint)" }}>
                    2 tools
                  </span>
                </div>
                <div className="p-5">
                  <div className="space-y-3">
                    {/* Order tool */}
                    <div>
                      <div className="text-xs font-medium mb-2" style={{ color: "var(--text-secondary)" }}>
                        get_order
                      </div>
                      <div
                        className="rounded p-3"
                        style={{
                          background: "var(--surface-alt)",
                          border: "1px solid var(--border)",
                        }}
                      >
                        {[
                          { key: "order_id", val: "—" },
                          { key: "status", val: "—" },
                          { key: "amount", val: "—" },
                        ].map((row) => (
                          <div
                            key={row.key}
                            className="flex items-center justify-between py-1"
                          >
                            <span className="text-xs" style={{ color: "var(--text-muted)" }}>
                              {row.key}
                            </span>
                            <span
                              className="text-xs font-mono"
                              style={{ color: "var(--text-faint)" }}
                            >
                              {row.val}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                    {/* Logistics tool */}
                    <div>
                      <div className="text-xs font-medium mb-2" style={{ color: "var(--text-secondary)" }}>
                        get_logistics
                      </div>
                      <div
                        className="rounded p-3"
                        style={{
                          background: "var(--surface-alt)",
                          border: "1px solid var(--border)",
                        }}
                      >
                        {[
                          { key: "carrier", val: "—" },
                          { key: "tracking_no", val: "—" },
                          { key: "status", val: "—" },
                        ].map((row) => (
                          <div
                            key={row.key}
                            className="flex items-center justify-between py-1"
                          >
                            <span className="text-xs" style={{ color: "var(--text-muted)" }}>
                              {row.key}
                            </span>
                            <span
                              className="text-xs font-mono"
                              style={{ color: "var(--text-faint)" }}
                            >
                              {row.val}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* QA / Human Review Status */}
            <div className="col-span-4">
              <div
                className="rounded-lg"
                style={{
                  background: "var(--surface)",
                  border: "1px solid var(--border)",
                }}
              >
                <div
                  className="px-5 py-3 flex items-center justify-between"
                  style={{ borderBottom: "1px solid var(--border)" }}
                >
                  <span className="text-sm font-semibold" style={{ color: "var(--text)" }}>
                    QA / Human Review
                  </span>
                  <span className="text-xs" style={{ color: "var(--text-faint)" }}>
                    —
                  </span>
                </div>
                <div className="p-5">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs" style={{ color: "var(--text-muted)" }}>
                        QA Score
                      </span>
                      <span
                        className="text-xs font-mono"
                        style={{ color: "var(--text-faint)" }}
                      >
                        —
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-xs" style={{ color: "var(--text-muted)" }}>
                        Risks Detected
                      </span>
                      <span
                        className="text-xs font-mono"
                        style={{ color: "var(--text-faint)" }}
                      >
                        0
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-xs" style={{ color: "var(--text-muted)" }}>
                        Suggestion
                      </span>
                      <span className="text-xs" style={{ color: "var(--text-faint)" }}>
                        —
                      </span>
                    </div>
                    <div
                      className="pt-3"
                      style={{ borderTop: "1px solid var(--border)" }}
                    >
                      <div className="text-xs mb-2" style={{ color: "var(--text-muted)" }}>
                        Risk List
                      </div>
                      <div
                        className="rounded p-3 text-xs text-center"
                        style={{
                          background: "var(--surface-alt)",
                          color: "var(--text-faint)",
                          border: "1px dashed var(--border)",
                        }}
                      >
                        No risks detected
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* ─── Footer ─── */}
      <footer
        className="px-6 py-2 text-center shrink-0"
        style={{
          borderTop: "1px solid var(--border)",
          background: "var(--surface)",
        }}
      >
        <span className="text-xs" style={{ color: "var(--text-faint)" }}>
          CustomerOps Agent — Multi-Agent Ticket Processing Workspace — Mock Mode
        </span>
      </footer>
    </div>
  );
}

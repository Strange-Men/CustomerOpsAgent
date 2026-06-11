export default function Home() {
  return (
    <div className="min-h-screen flex flex-col" style={{ background: "var(--bg)" }}>
      {/* ─── Header ─── */}
      <header
        className="flex items-center justify-between px-6 h-11 shrink-0"
        style={{
          background: "var(--surface)",
          borderBottom: "1px solid var(--border)",
        }}
      >
        <div className="flex items-center gap-4">
          <span className="text-sm font-semibold tracking-tight" style={{ color: "var(--text)" }}>
            CustomerOps
          </span>
          <nav className="flex items-center gap-0.5">
            {[
              { label: "Tickets", active: true },
              { label: "Eval", active: false },
            ].map((tab) => (
              <span
                key={tab.label}
                className="px-3 py-1 text-xs font-medium rounded"
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
            Mock
          </span>
          <span
            className="text-xs px-1.5 py-0.5 rounded font-mono"
            style={{
              background: "var(--surface-alt)",
              color: "var(--text-faint)",
            }}
          >
            v0.0.7
          </span>
        </div>
      </header>

      {/* ─── Main ─── */}
      <main className="flex-1 overflow-auto">
        <div className="max-w-[1400px] mx-auto px-6 py-4">

          {/* ─── Ticket Intake ─── */}
          <section className="mb-4">
            <div
              className="rounded-md"
              style={{
                background: "var(--surface)",
                border: "1px solid var(--border)",
              }}
            >
              <div
                className="px-4 py-2.5 flex items-center justify-between"
                style={{ borderBottom: "1px solid var(--border)" }}
              >
                <div className="flex items-center gap-2">
                  <span className="text-xs font-semibold uppercase tracking-wider" style={{ color: "var(--text-muted)" }}>
                    Ticket Intake
                  </span>
                  <span
                    className="text-xs px-1.5 py-0 rounded"
                    style={{ background: "var(--accent-bg)", color: "var(--accent)", fontSize: "10px" }}
                  >
                    New
                  </span>
                </div>
                <span className="text-xs" style={{ color: "var(--text-faint)", fontSize: "11px" }}>
                  Intent → Retrieval → Tool → Policy → Reply → QA
                </span>
              </div>

              <div className="p-4">
                <div className="grid grid-cols-12 gap-4">
                  <div className="col-span-7">
                    <label className="block text-xs font-medium mb-1" style={{ color: "var(--text-secondary)" }}>
                      Customer Message <span style={{ color: "var(--error)" }}>*</span>
                    </label>
                    <div
                      className="w-full h-20 rounded text-xs p-3"
                      style={{
                        background: "var(--surface-alt)",
                        border: "1px solid var(--border)",
                        color: "var(--text-faint)",
                      }}
                    >
                      <span style={{ fontSize: "11px" }}>Paste customer complaint or query here...</span>
                    </div>
                  </div>

                  <div className="col-span-5 flex flex-col gap-2.5">
                    <div className="grid grid-cols-2 gap-2.5">
                      <div>
                        <label className="block text-xs font-medium mb-1" style={{ color: "var(--text-secondary)" }}>
                          Order ID
                        </label>
                        <div
                          className="h-8 rounded text-xs px-2 flex items-center"
                          style={{
                            background: "var(--surface-alt)",
                            border: "1px solid var(--border)",
                            color: "var(--text-faint)",
                            fontSize: "11px",
                          }}
                        >
                          ORD-2024-001
                        </div>
                      </div>
                      <div>
                        <label className="block text-xs font-medium mb-1" style={{ color: "var(--text-secondary)" }}>
                          Product Type
                        </label>
                        <div
                          className="h-8 rounded text-xs px-2 flex items-center"
                          style={{
                            background: "var(--surface-alt)",
                            border: "1px solid var(--border)",
                            color: "var(--text-faint)",
                            fontSize: "11px",
                          }}
                        >
                          Electronics
                        </div>
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
                      <div className="flex items-center gap-1 ml-2">
                        <span className="text-xs" style={{ color: "var(--text-faint)", fontSize: "10px" }}>
                          Quick:
                        </span>
                        {["ORD-2024-001", "ORD-2024-002", "ORD-2024-005"].map((id) => (
                          <span
                            key={id}
                            className="text-xs px-1.5 py-0.5 rounded cursor-default font-mono"
                            style={{
                              background: "var(--surface-alt)",
                              color: "var(--text-muted)",
                              border: "1px solid var(--border)",
                              fontSize: "10px",
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

          {/* ─── Workflow Progress Bar (Signature Element) ─── */}
          <div className="mb-4">
            <div
              className="rounded-md px-4 py-2.5 flex items-center gap-1"
              style={{
                background: "var(--surface)",
                border: "1px solid var(--border)",
              }}
            >
              <span className="text-xs font-medium mr-2" style={{ color: "var(--text-muted)" }}>
                Pipeline
              </span>
              {[
                { name: "Intent", status: "pending" },
                { name: "Retrieval", status: "pending" },
                { name: "Tool", status: "pending" },
                { name: "Policy", status: "pending" },
                { name: "Reply", status: "pending" },
                { name: "QA", status: "pending" },
              ].map((step, i) => (
                <div key={step.name} className="flex items-center">
                  <div className="flex items-center gap-1.5">
                    <span
                      className="inline-flex items-center justify-center w-5 h-5 rounded-full text-xs font-medium"
                      style={{
                        background: "var(--surface-alt)",
                        color: "var(--text-faint)",
                        fontSize: "10px",
                      }}
                    >
                      {i + 1}
                    </span>
                    <span className="text-xs" style={{ color: "var(--text-muted)", fontSize: "11px" }}>
                      {step.name}
                    </span>
                  </div>
                  {i < 5 && (
                    <div
                      className="w-6 h-px mx-1"
                      style={{ background: "var(--border)" }}
                    />
                  )}
                </div>
              ))}
              <div className="flex-1" />
              <span className="text-xs" style={{ color: "var(--text-faint)", fontSize: "10px" }}>
                0 / 6 complete
              </span>
            </div>
          </div>

          {/* ─── Main Content: Workflow (dominant) + Summary ─── */}
          <div className="grid grid-cols-12 gap-4 mb-4">

            {/* Agent Workflow — Primary Content */}
            <div className="col-span-8">
              <div
                className="rounded-md h-full"
                style={{
                  background: "var(--surface)",
                  border: "1px solid var(--border)",
                }}
              >
                <div
                  className="px-4 py-2.5 flex items-center justify-between"
                  style={{ borderBottom: "1px solid var(--border)" }}
                >
                  <span className="text-xs font-semibold uppercase tracking-wider" style={{ color: "var(--text-muted)" }}>
                    Agent Workflow
                  </span>
                  <span className="text-xs" style={{ color: "var(--text-faint)", fontSize: "10px" }}>
                    6 agents
                  </span>
                </div>
                <div className="p-4">
                  <div className="space-y-0">
                    {[
                      { name: "Intent Agent", desc: "Classify intent, extract entities", status: "pending", time: "—" },
                      { name: "Retrieval Agent", desc: "Search knowledge base, fetch evidence", status: "pending", time: "—" },
                      { name: "Tool Agent", desc: "Lookup order, query logistics", status: "pending", time: "—" },
                      { name: "Policy Agent", desc: "Match policy, check eligibility", status: "pending", time: "—" },
                      { name: "Reply Agent", desc: "Generate response, cite policy", status: "pending", time: "—" },
                      { name: "QA Agent", desc: "Quality check, risk assessment", status: "pending", time: "—" },
                    ].map((agent, i) => (
                      <div
                        key={agent.name}
                        className="flex items-start gap-3 py-2"
                        style={{
                          borderBottom: i < 5 ? "1px solid var(--border)" : "none",
                        }}
                      >
                        {/* Step number */}
                        <div className="flex flex-col items-center mt-0.5 shrink-0 w-5">
                          <div
                            className="w-5 h-5 rounded-full flex items-center justify-center text-xs font-medium"
                            style={{
                              background: "var(--surface-alt)",
                              color: "var(--text-faint)",
                              fontSize: "10px",
                            }}
                          >
                            {i + 1}
                          </div>
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
                            <div className="flex items-center gap-2">
                              <span className="text-xs font-mono" style={{ color: "var(--text-faint)", fontSize: "10px" }}>
                                {agent.time}
                              </span>
                              <span
                                className="text-xs px-1.5 py-0 rounded"
                                style={{
                                  background: "var(--surface-alt)",
                                  color: "var(--text-faint)",
                                  fontSize: "10px",
                                }}
                              >
                                Pending
                              </span>
                            </div>
                          </div>
                          <span className="text-xs" style={{ color: "var(--text-muted)", fontSize: "11px" }}>
                            {agent.desc}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Review Summary + Reply Preview — Secondary */}
            <div className="col-span-4 flex flex-col gap-4">
              {/* Final Result */}
              <div
                className="rounded-md"
                style={{
                  background: "var(--surface)",
                  border: "1px solid var(--border)",
                }}
              >
                <div
                  className="px-4 py-2.5"
                  style={{ borderBottom: "1px solid var(--border)" }}
                >
                  <span className="text-xs font-semibold uppercase tracking-wider" style={{ color: "var(--text-muted)" }}>
                    Review Summary
                  </span>
                </div>
                <div className="p-4">
                  <div className="space-y-3">
                    {[
                      { label: "Result", value: "Pending", color: "var(--text-faint)" },
                      { label: "Risk", value: "—", color: "var(--text-faint)" },
                      { label: "QA Score", value: "—", color: "var(--text-faint)" },
                    ].map((item) => (
                      <div key={item.label} className="flex items-center justify-between">
                        <span className="text-xs" style={{ color: "var(--text-muted)" }}>
                          {item.label}
                        </span>
                        <span className="text-xs font-medium" style={{ color: item.color }}>
                          {item.value}
                        </span>
                      </div>
                    ))}
                    <div
                      className="pt-3"
                      style={{ borderTop: "1px solid var(--border)" }}
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xs" style={{ color: "var(--text-muted)" }}>
                          Human Review
                        </span>
                        <span
                          className="text-xs px-1.5 py-0 rounded"
                          style={{
                            background: "var(--surface-alt)",
                            color: "var(--text-faint)",
                            fontSize: "10px",
                          }}
                        >
                          Not Required
                        </span>
                      </div>
                      <div className="flex items-center justify-between mt-2">
                        <span className="text-xs" style={{ color: "var(--text-muted)" }}>
                          Ticket ID
                        </span>
                        <span className="text-xs font-mono" style={{ color: "var(--text-faint)" }}>
                          —
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Reply Preview */}
              <div
                className="rounded-md flex-1"
                style={{
                  background: "var(--surface)",
                  border: "1px solid var(--border)",
                }}
              >
                <div
                  className="px-4 py-2.5 flex items-center justify-between"
                  style={{ borderBottom: "1px solid var(--border)" }}
                >
                  <span className="text-xs font-semibold uppercase tracking-wider" style={{ color: "var(--text-muted)" }}>
                    Reply Draft
                  </span>
                  <span
                    className="text-xs px-1.5 py-0 rounded"
                    style={{ background: "var(--surface-alt)", color: "var(--text-faint)", fontSize: "10px" }}
                  >
                    Draft
                  </span>
                </div>
                <div className="p-4">
                  <div
                    className="h-24 rounded flex items-center justify-center text-xs"
                    style={{
                      background: "var(--surface-alt)",
                      color: "var(--text-faint)",
                      border: "1px dashed var(--border)",
                      fontSize: "11px",
                    }}
                  >
                    Agent reply will appear here
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* ─── Bottom Row: Evidence + Tool Results + QA ─── */}
          <div className="grid grid-cols-12 gap-4">
            {/* Evidence Preview */}
            <div className="col-span-4">
              <div
                className="rounded-md"
                style={{
                  background: "var(--surface)",
                  border: "1px solid var(--border)",
                }}
              >
                <div
                  className="px-4 py-2.5 flex items-center justify-between"
                  style={{ borderBottom: "1px solid var(--border)" }}
                >
                  <span className="text-xs font-semibold uppercase tracking-wider" style={{ color: "var(--text-muted)" }}>
                    Evidence
                  </span>
                  <span className="text-xs" style={{ color: "var(--text-faint)", fontSize: "10px" }}>
                    0 sources
                  </span>
                </div>
                <div className="p-4">
                  <div className="space-y-1.5">
                    {[
                      { name: "Return Policy v2.1", type: "policy", relevance: "0.92" },
                      { name: "Shipping Guidelines", type: "policy", relevance: "0.85" },
                      { name: "KB: Electronics Returns", type: "kb", relevance: "0.78" },
                    ].map((doc) => (
                      <div
                        key={doc.name}
                        className="flex items-center gap-2 px-2.5 py-1.5 rounded text-xs"
                        style={{
                          background: "var(--surface-alt)",
                          border: "1px solid var(--border)",
                        }}
                      >
                        <span
                          className="inline-block w-1 h-4 rounded-full shrink-0"
                          style={{ background: "var(--accent-light)" }}
                        />
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between">
                            <span style={{ color: "var(--text-secondary)", fontSize: "11px" }}>{doc.name}</span>
                            <span className="font-mono" style={{ color: "var(--text-faint)", fontSize: "10px" }}>
                              {doc.relevance}
                            </span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Tool Results Preview */}
            <div className="col-span-4">
              <div
                className="rounded-md"
                style={{
                  background: "var(--surface)",
                  border: "1px solid var(--border)",
                }}
              >
                <div
                  className="px-4 py-2.5 flex items-center justify-between"
                  style={{ borderBottom: "1px solid var(--border)" }}
                >
                  <span className="text-xs font-semibold uppercase tracking-wider" style={{ color: "var(--text-muted)" }}>
                    Tool Results
                  </span>
                  <span className="text-xs" style={{ color: "var(--text-faint)", fontSize: "10px" }}>
                    2 tools
                  </span>
                </div>
                <div className="p-4">
                  <div className="space-y-3">
                    {/* Order tool */}
                    <div>
                      <div className="text-xs font-medium mb-1.5 font-mono" style={{ color: "var(--text-secondary)", fontSize: "11px" }}>
                        get_order
                      </div>
                      <div
                        className="rounded p-2.5"
                        style={{
                          background: "var(--surface-alt)",
                          border: "1px solid var(--border)",
                        }}
                      >
                        {[
                          { key: "order_id", val: "ORD-2024-001" },
                          { key: "status", val: "shipped" },
                          { key: "amount", val: "¥299.00" },
                        ].map((row) => (
                          <div
                            key={row.key}
                            className="flex items-center justify-between py-0.5"
                          >
                            <span className="text-xs" style={{ color: "var(--text-muted)", fontSize: "11px" }}>
                              {row.key}
                            </span>
                            <span
                              className="text-xs font-mono"
                              style={{ color: "var(--text-secondary)", fontSize: "11px" }}
                            >
                              {row.val}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                    {/* Logistics tool */}
                    <div>
                      <div className="text-xs font-medium mb-1.5 font-mono" style={{ color: "var(--text-secondary)", fontSize: "11px" }}>
                        get_logistics
                      </div>
                      <div
                        className="rounded p-2.5"
                        style={{
                          background: "var(--surface-alt)",
                          border: "1px solid var(--border)",
                        }}
                      >
                        {[
                          { key: "carrier", val: "SF Express" },
                          { key: "tracking_no", val: "SF1234567890" },
                          { key: "status", val: "in_transit" },
                        ].map((row) => (
                          <div
                            key={row.key}
                            className="flex items-center justify-between py-0.5"
                          >
                            <span className="text-xs" style={{ color: "var(--text-muted)", fontSize: "11px" }}>
                              {row.key}
                            </span>
                            <span
                              className="text-xs font-mono"
                              style={{ color: "var(--text-secondary)", fontSize: "11px" }}
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
                className="rounded-md"
                style={{
                  background: "var(--surface)",
                  border: "1px solid var(--border)",
                }}
              >
                <div
                  className="px-4 py-2.5 flex items-center justify-between"
                  style={{ borderBottom: "1px solid var(--border)" }}
                >
                  <span className="text-xs font-semibold uppercase tracking-wider" style={{ color: "var(--text-muted)" }}>
                    QA / Review
                  </span>
                  <span className="text-xs" style={{ color: "var(--text-faint)", fontSize: "10px" }}>
                    —
                  </span>
                </div>
                <div className="p-4">
                  <div className="space-y-2.5">
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
                      className="pt-2.5"
                      style={{ borderTop: "1px solid var(--border)" }}
                    >
                      <div className="text-xs mb-1.5" style={{ color: "var(--text-muted)" }}>
                        Risk List
                      </div>
                      <div
                        className="rounded p-2.5 text-xs text-center"
                        style={{
                          background: "var(--surface-alt)",
                          color: "var(--text-faint)",
                          border: "1px dashed var(--border)",
                          fontSize: "11px",
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
        <span className="text-xs" style={{ color: "var(--text-faint)", fontSize: "10px" }}>
          CustomerOps Agent — Multi-Agent Ticket Processing — Mock Mode
        </span>
      </footer>
    </div>
  );
}

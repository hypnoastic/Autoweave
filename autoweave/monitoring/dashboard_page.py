"""HTML shell for the lightweight AutoWeave operator console."""

from __future__ import annotations


def render_dashboard_page() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AutoWeave Operator Console</title>
  <style>
    :root {
      --bg: #f5f7fa;
      --panel: #ffffff;
      --panel-soft: #f8fafc;
      --panel-strong: #eef2f6;
      --text: #17212b;
      --muted: #64707d;
      --line: #dde5ee;
      --accent: #1d5d91;
      --accent-soft: #edf5fc;
      --success: #20624a;
      --success-soft: #ebf7f0;
      --warn: #8a6508;
      --warn-soft: #fff6df;
      --danger: #9a4134;
      --danger-soft: #feefeb;
      --radius: 16px;
      --shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
      --sans: "IBM Plex Sans", "Avenir Next", "Segoe UI", sans-serif;
      --mono: "IBM Plex Mono", "SFMono-Regular", "Menlo", monospace;
    }
    * { box-sizing: border-box; }
    html, body { height: 100%; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: var(--sans);
    }
    h1, h2, h3, p { margin: 0; }
    button, input, textarea, select { font: inherit; }
    button {
      border: 0;
      cursor: pointer;
      transition: background 0.16s ease, border-color 0.16s ease, opacity 0.16s ease;
    }
    button:hover { opacity: 0.95; }
    button:focus-visible, input:focus-visible, textarea:focus-visible, select:focus-visible {
      outline: 2px solid var(--accent);
      outline-offset: 2px;
    }
    a { color: inherit; }
    pre, code {
      font-family: var(--mono);
      white-space: pre-wrap;
      word-break: break-word;
    }
    .shell {
      min-height: 100vh;
      display: grid;
      grid-template-columns: 280px minmax(0, 1fr);
    }
    .sidebar {
      padding: 24px 18px;
      border-right: 1px solid var(--line);
      background: var(--panel);
      display: grid;
      align-content: start;
      gap: 16px;
      position: sticky;
      top: 0;
      height: 100vh;
      overflow-y: auto;
    }
    .brand {
      display: grid;
      gap: 6px;
      padding: 18px 18px 16px;
      border-radius: var(--radius);
      background: var(--panel-soft);
      border: 1px solid var(--line);
    }
    .brand h1 {
      font-size: 1.35rem;
      letter-spacing: -0.03em;
    }
    .brand p {
      color: var(--muted);
      font-size: 0.95rem;
      line-height: 1.5;
    }
    .nav {
      display: grid;
      gap: 10px;
    }
    .nav button {
      width: 100%;
      text-align: left;
      padding: 12px 14px;
      border-radius: 12px;
      background: transparent;
      color: var(--text);
      border: 1px solid var(--panel);
      font-weight: 600;
    }
    .nav button.active {
      background: var(--panel-soft);
      border-color: var(--line);
      color: var(--accent);
    }
    .meta-card {
      padding: 14px;
      border-radius: 14px;
      background: var(--panel);
      border: 1px solid var(--line);
      display: grid;
      gap: 12px;
    }
    .meta-line {
      display: grid;
      gap: 4px;
    }
    .meta-line small {
      color: var(--muted);
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }
    .meta-line strong {
      overflow-wrap: anywhere;
      font-size: 0.93rem;
    }
    .main {
      padding: 24px;
      display: grid;
      gap: 16px;
      align-content: start;
      max-width: 1480px;
      width: 100%;
      margin: 0 auto;
    }
    .hero {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      align-items: start;
      gap: 16px;
      padding: 20px 22px;
      border-radius: 18px;
      background: var(--panel);
      border: 1px solid var(--line);
    }
    .hero-copy {
      display: grid;
      gap: 10px;
    }
    .hero-copy p {
      color: var(--muted);
      max-width: 68ch;
      line-height: 1.5;
    }
    .hero-actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }
    .btn {
      padding: 10px 14px;
      border-radius: 12px;
      background: var(--accent);
      color: #fff;
      font-weight: 600;
    }
    .btn.secondary {
      background: var(--panel-strong);
      color: var(--text);
    }
    .btn.ghost {
      background: transparent;
      color: var(--accent);
      border: 1px solid var(--line);
    }
    .grid {
      display: grid;
      gap: 16px;
    }
    .section {
      display: none;
    }
    .section.active {
      display: grid;
      gap: 20px;
    }
    .chat-layout {
      display: grid;
      grid-template-columns: minmax(320px, 380px) minmax(0, 1fr);
      gap: 16px;
      align-items: start;
    }
    .chat-layout > article {
      min-width: 0;
    }
    .chat-layout > :last-child {
      grid-column: 2;
    }
    .card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 18px;
      overflow: hidden;
      min-width: 0;
    }
    .card-header {
      padding: 16px 18px 12px;
      border-bottom: 1px solid var(--line);
      display: grid;
      gap: 6px;
    }
    .card-header p {
      color: var(--muted);
      font-size: 0.94rem;
      line-height: 1.5;
    }
    .card-body {
      padding: 16px 18px 18px;
      display: grid;
      gap: 14px;
      min-width: 0;
    }
    .run-list {
      display: grid;
      gap: 12px;
      min-width: 0;
    }
    .run-item {
      padding: 13px 14px;
      border-radius: 14px;
      border: 1px solid var(--line);
      background: #fff;
      display: grid;
      gap: 8px;
      min-width: 0;
    }
    .run-item.active {
      background: var(--accent-soft);
      border-color: #c8d9ea;
    }
    .run-item button {
      background: transparent;
      padding: 0;
      text-align: left;
      color: inherit;
      display: block;
      width: 100%;
      min-width: 0;
    }
    .run-item h3 {
      font-size: 1rem;
      line-height: 1.45;
      overflow-wrap: anywhere;
    }
    .run-item p {
      color: var(--muted);
      font-size: 0.92rem;
      line-height: 1.5;
      overflow-wrap: anywhere;
    }
    .run-item .small {
      overflow-wrap: anywhere;
    }
    .pill-row {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 10px;
      border-radius: 999px;
      font-size: 0.82rem;
      font-weight: 600;
      border: 1px solid transparent;
    }
    .pill.neutral { background: var(--panel-strong); color: var(--text); }
    .pill.active, .pill.running { background: var(--accent-soft); color: var(--accent); }
    .pill.ready, .pill.completed, .pill.succeeded, .pill.resolved, .pill.approved {
      background: var(--success-soft);
      color: var(--success);
    }
    .pill.waiting_for_human, .pill.waiting_for_approval, .pill.paused, .pill.needs_input, .pill.requested {
      background: var(--warn-soft);
      color: var(--warn);
    }
    .pill.blocked, .pill.failed, .pill.orphaned, .pill.error, .pill.rejected {
      background: var(--danger-soft);
      color: var(--danger);
    }
    .metric-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
    }
    .metric {
      padding: 12px;
      border-radius: 14px;
      background: var(--panel-soft);
      border: 1px solid var(--line);
      display: grid;
      gap: 6px;
    }
    .metric small {
      color: var(--muted);
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }
    .metric strong {
      font-size: 1.05rem;
    }
    .thread {
      min-height: 420px;
      max-height: 62vh;
      overflow-y: auto;
      padding: 18px;
      display: grid;
      gap: 12px;
      background: #fff;
    }
    .empty {
      padding: 16px;
      border-radius: 14px;
      border: 1px dashed var(--line);
      color: var(--muted);
      line-height: 1.55;
      background: var(--panel-soft);
    }
    .message {
      display: grid;
      gap: 8px;
      max-width: 88%;
    }
    .message.user { justify-self: end; }
    .message.system { justify-self: stretch; max-width: 100%; }
    .message-meta {
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--muted);
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }
    .bubble {
      padding: 13px 14px;
      border-radius: 14px;
      border: 1px solid var(--line);
      background: var(--panel);
      line-height: 1.55;
    }
    .message.manager .bubble { background: #fff; border-color: #d7e2ed; }
    .message.user .bubble { background: #f3f8fd; border-color: #d4e3f1; }
    .message.system .bubble { background: var(--panel-soft); }
    .composer {
      padding: 16px 18px 18px;
      border-top: 1px solid var(--line);
      display: grid;
      gap: 12px;
      background: #fff;
    }
    .composer textarea {
      width: 100%;
      min-height: 104px;
      resize: vertical;
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 12px 14px;
      background: #fff;
      color: var(--text);
    }
    .composer-row {
      display: flex;
      gap: 12px;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
    }
    .inline-fields {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      align-items: center;
    }
    .field {
      display: grid;
      gap: 6px;
      color: var(--muted);
      font-size: 0.86rem;
    }
    .field input, .field select {
      border: 1px solid var(--line);
      border-radius: 12px;
      background: #fff;
      color: var(--text);
      padding: 10px 12px;
      min-width: 100px;
    }
    .stack {
      display: grid;
      gap: 12px;
    }
    .notice {
      padding: 13px 14px;
      border-radius: 14px;
      border: 1px solid var(--line);
      background: var(--panel-soft);
      line-height: 1.55;
    }
    .table-wrap {
      overflow-x: auto;
      border: 1px solid var(--line);
      border-radius: 16px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      background: var(--panel);
    }
    th, td {
      padding: 12px 14px;
      text-align: left;
      vertical-align: top;
      border-bottom: 1px solid var(--line);
      font-size: 0.94rem;
    }
    th {
      color: var(--muted);
      background: var(--panel-soft);
      font-weight: 600;
      white-space: nowrap;
    }
    td code {
      font-size: 0.84rem;
    }
    tr:last-child td { border-bottom: 0; }
    .pair-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
    }
    .list {
      display: grid;
      gap: 10px;
    }
    .list-item {
      padding: 13px 14px;
      border-radius: 14px;
      background: var(--panel-soft);
      border: 1px solid var(--line);
      display: grid;
      gap: 8px;
    }
    .list-item pre {
      margin: 0;
      padding: 12px;
      border-radius: 12px;
      background: #fff;
      border: 1px solid var(--line);
      max-height: 240px;
      overflow: auto;
    }
    .small {
      color: var(--muted);
      font-size: 0.88rem;
      line-height: 1.5;
    }
    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }
    @media (max-width: 1300px) {
      .chat-layout {
        grid-template-columns: 1fr;
      }
      .chat-layout > :last-child {
        grid-column: auto;
      }
    }
    @media (max-width: 980px) {
      .shell {
        grid-template-columns: 1fr;
      }
      .sidebar {
        position: static;
        height: auto;
        border-right: 0;
        border-bottom: 1px solid var(--line);
      }
      .main {
        padding: 20px;
      }
      .chat-layout, .pair-grid, .metric-grid {
        grid-template-columns: 1fr;
      }
      .hero {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="shell">
    <aside class="sidebar">
      <section class="brand">
        <h1>AutoWeave Operator Console</h1>
        <p>Local library console for manager chat, run state, and approval handling.</p>
      </section>
      <nav class="nav" aria-label="Console sections">
        <button type="button" data-section="chat" class="active">Chat With Manager</button>
        <button type="button" data-section="runs">Workflow Runs</button>
        <button type="button" data-section="tasks">Tasks / DAG</button>
        <button type="button" data-section="workers">Active workers</button>
        <button type="button" data-section="events">Observability / Events</button>
        <button type="button" data-section="settings">Settings / Config</button>
      </nav>
      <section class="meta-card">
        <div class="meta-line">
          <small>Project Root</small>
          <strong id="project-root">loading...</strong>
        </div>
        <div class="meta-line">
          <small>Refresh</small>
          <strong id="refresh-status">Connecting to canonical state</strong>
        </div>
        <button id="refresh-button" type="button" class="btn secondary">Refresh now</button>
      </section>
    </aside>
    <main class="main" id="main">
      <section class="hero">
        <div class="hero-copy">
          <div class="pill-row" id="hero-pills"></div>
          <h2 id="hero-title">Chat With Manager</h2>
          <p id="hero-subtitle">Start a new run, answer an open clarification, or inspect the currently selected workflow run.</p>
        </div>
        <div class="hero-actions">
          <button id="hero-open-chat" type="button" class="btn">Open chat</button>
          <button id="hero-open-runs" type="button" class="btn ghost">View runs</button>
        </div>
      </section>

      <section id="section-chat" class="section active" aria-labelledby="hero-title">
        <div class="chat-layout">
          <article class="card">
            <header class="card-header">
              <h3>Runs</h3>
              <p>Select one run and keep the rest out of the way.</p>
            </header>
            <div class="card-body">
              <div id="chat-run-list" class="run-list"></div>
            </div>
          </article>

          <article class="card">
            <header class="card-header">
              <h3>Manager Thread</h3>
              <p>Start a run or answer the current manager clarification for the selected run.</p>
            </header>
            <div id="chat-thread" class="thread"></div>
            <form id="chat-composer" class="composer">
              <label class="sr-only" for="composer-input">Message</label>
              <textarea id="composer-input" placeholder="Ask the manager to start a run, or answer the current clarification."></textarea>
              <div class="composer-row">
                <div class="inline-fields">
                  <label class="field">
                    <span>Dispatch</span>
                    <select id="composer-dispatch">
                      <option value="true" selected>Enabled</option>
                      <option value="false">Dry run</option>
                    </select>
                  </label>
                  <label class="field">
                    <span>Max steps</span>
                    <input id="composer-max-steps" type="number" min="1" max="32" value="8">
                  </label>
                </div>
                <button id="composer-submit" type="submit" class="btn">Send</button>
              </div>
              <div id="composer-hint" class="small">New message = start a run. If the selected run has an open clarification, the message answers it.</div>
            </form>
          </article>

          <article class="card">
            <header class="card-header">
              <h3>Run Summary</h3>
              <p>Current status, open questions, and approval actions for the active run.</p>
            </header>
            <div id="chat-side-panel" class="card-body"></div>
          </article>
        </div>
      </section>

      <section id="section-runs" class="section">
        <article class="card">
          <header class="card-header">
            <h3>Workflow Runs</h3>
            <p>Operator-facing run health sorted by the most actionable execution state.</p>
          </header>
          <div id="runs-panel" class="card-body"></div>
        </article>
      </section>

      <section id="section-tasks" class="section">
        <div class="pair-grid">
          <article class="card">
            <header class="card-header">
              <h3>Tasks / DAG</h3>
              <p>Readable task state, worker state, dependencies, and artifact output for the selected run.</p>
            </header>
            <div id="tasks-panel" class="card-body"></div>
          </article>
          <article class="card">
            <header class="card-header">
              <h3>Manager Plan</h3>
              <p>Published workflow plan when present, otherwise the manager outcome or blocker.</p>
            </header>
            <div id="plan-panel" class="card-body"></div>
          </article>
        </div>
      </section>

      <section id="section-workers" class="section">
        <article class="card">
          <header class="card-header">
            <h3>Active workers</h3>
            <p>Attempts, workspaces, and model routing for the selected run.</p>
          </header>
          <div id="workers-panel" class="card-body"></div>
        </article>
      </section>

      <section id="section-events" class="section">
        <div class="pair-grid">
          <article class="card">
            <header class="card-header">
              <h3>Observability / Events</h3>
              <p>Recent normalized events emitted by the selected workflow run.</p>
            </header>
            <div id="events-panel" class="card-body"></div>
          </article>
          <article class="card">
            <header class="card-header">
              <h3>Artifacts</h3>
              <p>Published outputs for the selected run.</p>
            </header>
            <div id="artifacts-panel" class="card-body"></div>
          </article>
        </div>
      </section>

      <section id="section-settings" class="section">
        <div class="pair-grid">
          <article class="card">
            <header class="card-header">
              <h3>Settings / Config</h3>
              <p>Project root, workflow blueprint, and package-loaded roles.</p>
            </header>
            <div id="settings-panel" class="card-body"></div>
          </article>
          <article class="card">
            <header class="card-header">
              <h3>Agents</h3>
              <p>Materialized or packaged agent catalog currently visible to the monitor.</p>
            </header>
            <div id="agents-panel" class="card-body"></div>
          </article>
        </div>
      </section>
    </main>
  </div>

  <script>
    const state = {
      payload: null,
      activeSection: "chat",
      activeRunId: null,
      busy: false,
      lastLoadedAt: null,
    };

    const nodes = {
      navButtons: [...document.querySelectorAll("[data-section]")],
      projectRoot: document.getElementById("project-root"),
      refreshStatus: document.getElementById("refresh-status"),
      refreshButton: document.getElementById("refresh-button"),
      heroTitle: document.getElementById("hero-title"),
      heroSubtitle: document.getElementById("hero-subtitle"),
      heroPills: document.getElementById("hero-pills"),
      heroOpenChat: document.getElementById("hero-open-chat"),
      heroOpenRuns: document.getElementById("hero-open-runs"),
      chatRunList: document.getElementById("chat-run-list"),
      chatThread: document.getElementById("chat-thread"),
      chatComposer: document.getElementById("chat-composer"),
      composerInput: document.getElementById("composer-input"),
      composerDispatch: document.getElementById("composer-dispatch"),
      composerMaxSteps: document.getElementById("composer-max-steps"),
      composerSubmit: document.getElementById("composer-submit"),
      composerHint: document.getElementById("composer-hint"),
      chatSidePanel: document.getElementById("chat-side-panel"),
      runsPanel: document.getElementById("runs-panel"),
      tasksPanel: document.getElementById("tasks-panel"),
      planPanel: document.getElementById("plan-panel"),
      workersPanel: document.getElementById("workers-panel"),
      eventsPanel: document.getElementById("events-panel"),
      artifactsPanel: document.getElementById("artifacts-panel"),
      settingsPanel: document.getElementById("settings-panel"),
      agentsPanel: document.getElementById("agents-panel"),
    };

    const ACTIVE_ATTEMPTS = new Set(["dispatching", "running", "paused", "needs_input"]);

    function escapeHtml(value) {
      return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
    }

    function prettyJson(value) {
      if (value === null || value === undefined || value === "") {
        return "none";
      }
      if (typeof value === "string") {
        return value;
      }
      try {
        return JSON.stringify(value, null, 2);
      } catch (error) {
        return String(value);
      }
    }

    function statusPill(value, fallback = "neutral") {
      const text = String(value || "unknown");
      const className = text.replaceAll(/[^a-z0-9_]+/gi, "_").toLowerCase();
      return `<span class="pill ${className || fallback}">${escapeHtml(text.replaceAll("_", " "))}</span>`;
    }

    function activeRun() {
      if (!state.payload || !Array.isArray(state.payload.runs)) {
        return null;
      }
      const run = state.payload.runs.find((item) => item.id === state.activeRunId);
      return run || state.payload.selected_run || state.payload.runs[0] || null;
    }

    function openHumanRequest(run) {
      return (run?.human_requests || []).find((item) => item.status === "open") || null;
    }

    function openApprovals(run) {
      return (run?.approval_requests || []).filter((item) => item.status === "requested");
    }

    function setSection(section) {
      state.activeSection = section;
      for (const button of nodes.navButtons) {
        button.classList.toggle("active", button.dataset.section === section);
      }
      for (const element of document.querySelectorAll(".section")) {
        element.classList.toggle("active", element.id === `section-${section}`);
      }
      const titles = {
        chat: ["Chat With Manager", "Start new runs, answer clarifications, and keep the main operator thread clean."],
        runs: ["Workflow Runs", "Review run health and open the one run you want to inspect."],
        tasks: ["Tasks / DAG", "Inspect task state, dependencies, and manager output in one place."],
        workers: ["Active Workers", "Track current worker attempts, routing, and workspace paths."],
        events: ["Observability / Events", "Read recent events and published artifacts without leaving the console."],
        settings: ["Settings / Config", "See the loaded workflow, available agents, and project root."],
      };
      nodes.heroTitle.textContent = titles[section][0];
      nodes.heroSubtitle.textContent = titles[section][1];
    }

    function renderHero() {
      const run = activeRun();
      const pills = [];
      if (state.payload) {
        pills.push(statusPill(state.payload.status));
      }
      if (run) {
        pills.push(statusPill(run.operator_status));
        pills.push(statusPill(run.execution_status));
      }
      nodes.heroPills.innerHTML = pills.join("");
      nodes.projectRoot.textContent = state.payload?.project_root || "loading...";
      nodes.refreshStatus.textContent = state.payload
        ? `Last refresh ${new Date(state.lastLoadedAt || Date.now()).toLocaleTimeString()}`
        : "Connecting to canonical state";
    }

    function renderRunList(target, runs, activeId) {
      if (!runs.length) {
        target.innerHTML = `<div class="empty">No workflow runs are available yet. Start a run from the chat composer.</div>`;
        return;
      }
      target.innerHTML = runs.map((run) => `
        <div class="run-item ${run.id === activeId ? "active" : ""}">
          <button type="button" data-run-select="${escapeHtml(run.id)}">
            <h3>${escapeHtml(run.title || run.id)}</h3>
          </button>
          <div class="pill-row">
            ${statusPill(run.operator_status)}
            ${statusPill(run.execution_status)}
            ${statusPill(run.status)}
          </div>
          <p>${escapeHtml(run.operator_summary || "No operator summary")}</p>
          <p class="small"><strong>Run:</strong> ${escapeHtml(run.id)}</p>
        </div>
      `).join("");
      for (const button of target.querySelectorAll("[data-run-select]")) {
        button.addEventListener("click", () => {
          state.activeRunId = button.dataset.runSelect;
          render();
          setSection("chat");
        });
      }
    }

    function renderChatSection(run) {
      renderRunList(nodes.chatRunList, state.payload?.runs || [], run?.id || null);

      if (!run) {
        nodes.chatThread.innerHTML = `<div class="empty">No run selected yet. Ask the manager to start a workflow run.</div>`;
        nodes.chatSidePanel.innerHTML = `<div class="empty">Run details appear here after the first workflow is created.</div>`;
        nodes.composerHint.textContent = "Send a request to start the first run.";
        return;
      }

      const humanRequest = openHumanRequest(run);
      const approvals = openApprovals(run);
      const messages = run.chat_messages || [];
      nodes.chatThread.innerHTML = messages.length
        ? messages.map((message) => `
            <article class="message ${escapeHtml(message.role || "system")}">
              <div class="message-meta">
                <span>${escapeHtml(message.role || "system")}</span>
                <span>${escapeHtml((message.kind || "message").replaceAll("_", " "))}</span>
                ${message.status ? statusPill(message.status) : ""}
              </div>
              <div class="bubble"><pre>${escapeHtml(message.text || "")}</pre></div>
            </article>
          `).join("")
        : `<div class="empty">This run has no chat history yet.</div>`;

      const summaryMetrics = [
        ["Operator summary", run.operator_summary || "No operator summary"],
        ["Execution summary", run.execution_summary || "No execution summary"],
        ["Manager task", run.manager_task_state || "none"],
      ];
      nodes.chatSidePanel.innerHTML = `
        <div class="metric-grid">
          <div class="metric">
            <small>Operator status</small>
            <strong>${statusPill(run.operator_status)}</strong>
          </div>
          <div class="metric">
            <small>Execution status</small>
            <strong>${statusPill(run.execution_status)}</strong>
          </div>
          <div class="metric">
            <small>Active attempts</small>
            <strong>${escapeHtml(String(run.active_attempt_count || 0))}</strong>
          </div>
        </div>
        <div class="stack">
          <div class="notice">
            <strong>Current state</strong>
            <div class="small">Manager outcome and operator-level status for this run.</div>
          </div>
          ${summaryMetrics.map(([label, value]) => `
            <div class="notice">
              <strong>${escapeHtml(label)}</strong>
              <div class="small">${escapeHtml(value)}</div>
            </div>
          `).join("")}
          ${run.manager_outcome ? `
            <div class="notice">
              <strong>Manager outcome</strong>
              <pre>${escapeHtml(run.manager_outcome)}</pre>
            </div>
          ` : ""}
          ${humanRequest ? `
            <div class="notice">
              <strong>Open clarification</strong>
              <div class="small">${escapeHtml(humanRequest.question || "Awaiting answer")}</div>
            </div>
          ` : ""}
          ${approvals.map((request) => `
            <div class="notice">
              <strong>Approval request</strong>
              <div class="small">${escapeHtml(request.reason || "Approval required")}</div>
              <div class="pill-row" style="margin-top:10px;">
                <button type="button" class="btn secondary" data-approval="${escapeHtml(request.id)}" data-approved="true">Approve</button>
                <button type="button" class="btn ghost" data-approval="${escapeHtml(request.id)}" data-approved="false">Reject</button>
              </div>
            </div>
          `).join("") || `<div class="notice"><strong>Approvals</strong><div class="small">No open approval requests for this run.</div></div>`}
        </div>
      `;

      for (const button of nodes.chatSidePanel.querySelectorAll("[data-approval]")) {
        button.addEventListener("click", async () => {
          await resolveApproval(run.id, button.dataset.approval, button.dataset.approved === "true");
        });
      }

      nodes.composerHint.textContent = humanRequest
        ? `Answering clarification: ${humanRequest.question}`
        : "Send a new message to start another run from the manager entrypoint.";
    }

    function renderRunsSection(run) {
      const runs = state.payload?.runs || [];
      if (!runs.length) {
        nodes.runsPanel.innerHTML = `<div class="empty">No workflow runs to display yet.</div>`;
        return;
      }
      nodes.runsPanel.innerHTML = `
        <div class="list">
          ${runs.map((item) => `
            <div class="list-item">
              <div style="display:flex; justify-content:space-between; gap:12px; align-items:flex-start; flex-wrap:wrap;">
                <div class="stack" style="gap:6px;">
                  <strong>${escapeHtml(item.title || item.id)}</strong>
                  <div class="small">${escapeHtml(item.workflow_request || item.id)}</div>
                </div>
                <button type="button" class="btn ${item.id === run?.id ? "secondary" : "ghost"}" data-run-open="${escapeHtml(item.id)}">
                  ${item.id === run?.id ? "Selected" : "Open run"}
                </button>
              </div>
              <div class="pill-row">
                ${statusPill(item.operator_status)}
                ${statusPill(item.execution_status)}
                ${statusPill(item.status)}
              </div>
              <div class="metric-grid">
                <div class="metric">
                  <small>Summary</small>
                  <strong>${escapeHtml(item.operator_summary || "none")}</strong>
                </div>
                <div class="metric">
                  <small>Ready tasks</small>
                  <strong>${escapeHtml(String((item.ready_task_keys || []).length))}</strong>
                </div>
                <div class="metric">
                  <small>Blocked tasks</small>
                  <strong>${escapeHtml(String((item.blocked_task_keys || []).length))}</strong>
                </div>
              </div>
            </div>
          `).join("")}
        </div>
      `;
      for (const button of nodes.runsPanel.querySelectorAll("[data-run-open]")) {
        button.addEventListener("click", () => {
          state.activeRunId = button.dataset.runOpen;
          setSection("chat");
          render();
        });
      }
    }

    function renderTasksSection(run) {
      if (!run) {
        nodes.tasksPanel.innerHTML = `<div class="empty">Select a run to inspect its tasks.</div>`;
        nodes.planPanel.innerHTML = `<div class="empty">Manager plan data appears here.</div>`;
        return;
      }
      const tasks = run.tasks || [];
      nodes.tasksPanel.innerHTML = tasks.length ? `
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Task</th>
                <th>Role</th>
                <th>State</th>
                <th>Worker</th>
                <th>Artifacts</th>
              </tr>
            </thead>
            <tbody>
              ${tasks.map((task) => `
                <tr>
                  <td>
                    <strong>${escapeHtml(task.title || task.task_key)}</strong>
                    <div class="small"><code>${escapeHtml(task.task_key)}</code></div>
                    ${task.hard_dependencies?.length ? `<div class="small">depends on ${escapeHtml(task.hard_dependencies.join(", "))}</div>` : ""}
                  </td>
                  <td>${escapeHtml(task.assigned_role || "unknown")}</td>
                  <td>
                    <div class="pill-row">
                      ${statusPill(task.state)}
                      ${task.latest_attempt_state ? statusPill(task.latest_attempt_state) : ""}
                    </div>
                    ${task.block_reason ? `<div class="small">${escapeHtml(task.block_reason)}</div>` : ""}
                  </td>
                  <td>
                    <div class="small">${escapeHtml(task.worker_summary || "No worker summary")}</div>
                    ${task.model_name ? `<div class="small"><code>${escapeHtml(task.model_name)}</code></div>` : ""}
                  </td>
                  <td>${task.artifact_types?.length ? task.artifact_types.map((item) => `<code>${escapeHtml(item)}</code>`).join("<br>") : '<span class="small">none</span>'}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>
      ` : `<div class="empty">No tasks recorded for this run.</div>`;

      nodes.planPanel.innerHTML = `
        ${run.manager_plan ? `
          <div class="notice">
            <strong>Workflow plan</strong>
            <pre>${escapeHtml(run.manager_plan)}</pre>
          </div>
        ` : ""}
        ${run.manager_summary ? `
          <div class="notice">
            <strong>Manager summary</strong>
            <pre>${escapeHtml(run.manager_summary)}</pre>
          </div>
        ` : ""}
        ${run.manager_outcome ? `
          <div class="notice">
            <strong>Manager outcome / blocker</strong>
            <pre>${escapeHtml(run.manager_outcome)}</pre>
          </div>
        ` : ""}
        ${!run.manager_plan && !run.manager_summary && !run.manager_outcome ? `
          <div class="empty">The manager has not published a plan or summary yet.</div>
        ` : ""}
      `;
    }

    function renderWorkersSection(run) {
      if (!run) {
        nodes.workersPanel.innerHTML = `<div class="empty">Select a run to inspect worker attempts.</div>`;
        return;
      }
      const attempts = (run.attempts || []).filter((attempt) => ACTIVE_ATTEMPTS.has(attempt.state));
      nodes.workersPanel.innerHTML = attempts.length ? `
        <div class="list">
          ${attempts.map((attempt) => `
            <div class="list-item">
              <div class="pill-row">
                ${statusPill(attempt.state)}
                ${attempt.model_name ? statusPill("model") : ""}
              </div>
              <div><strong>${escapeHtml(attempt.task_key || attempt.task_id)}</strong></div>
              <div class="small">Attempt ${escapeHtml(String(attempt.attempt_number || 0))}</div>
              ${attempt.model_name ? `<div class="small"><code>${escapeHtml(attempt.model_name)}</code></div>` : ""}
              ${attempt.workspace_path ? `<pre>${escapeHtml(attempt.workspace_path)}</pre>` : ""}
            </div>
          `).join("")}
        </div>
      ` : `<div class="empty">No active worker attempts for the selected run.</div>`;
    }

    function renderEventsSection(run) {
      if (!run) {
        nodes.eventsPanel.innerHTML = `<div class="empty">Select a run to inspect events.</div>`;
        nodes.artifactsPanel.innerHTML = `<div class="empty">Artifacts appear here once a run publishes output.</div>`;
        return;
      }
      const events = run.events || [];
      const artifacts = run.artifacts || [];
      nodes.eventsPanel.innerHTML = events.length ? `
        <div class="list">
          ${events.map((event) => `
            <div class="list-item">
              <div class="pill-row">
                ${statusPill(event.event_type)}
                ${event.agent_role ? statusPill(event.agent_role) : ""}
              </div>
              <strong>${escapeHtml(event.message || event.event_type)}</strong>
              <div class="small">sequence ${escapeHtml(String(event.sequence_no || 0))} · source ${escapeHtml(event.source || "unknown")}</div>
              ${event.model_name ? `<div class="small"><code>${escapeHtml(event.model_name)}</code></div>` : ""}
            </div>
          `).join("")}
        </div>
      ` : `<div class="empty">No recent events were returned for this run.</div>`;

      nodes.artifactsPanel.innerHTML = artifacts.length ? `
        <div class="list">
          ${artifacts.map((artifact) => `
            <div class="list-item">
              <div class="pill-row">
                ${statusPill(artifact.status)}
                ${statusPill(artifact.artifact_type)}
              </div>
              <strong>${escapeHtml(artifact.title || artifact.artifact_type)}</strong>
              <div class="small">${escapeHtml(artifact.summary || "No artifact summary")}</div>
              <div class="small"><code>${escapeHtml(artifact.storage_uri || "n/a")}</code></div>
            </div>
          `).join("")}
        </div>
      ` : `<div class="empty">No artifacts have been published for this run yet.</div>`;
    }

    function renderSettingsSection() {
      const payload = state.payload;
      if (!payload) {
        nodes.settingsPanel.innerHTML = `<div class="empty">Waiting for configuration data.</div>`;
        nodes.agentsPanel.innerHTML = `<div class="empty">Waiting for agent catalog.</div>`;
        return;
      }
      const blueprint = payload.workflow_blueprint || {};
      nodes.settingsPanel.innerHTML = `
        <div class="metric-grid">
          <div class="metric">
            <small>Workflow</small>
            <strong>${escapeHtml(blueprint.name || "none")}</strong>
          </div>
          <div class="metric">
            <small>Entrypoint</small>
            <strong>${escapeHtml(blueprint.entrypoint || "none")}</strong>
          </div>
          <div class="metric">
            <small>Templates</small>
            <strong>${escapeHtml(String((blueprint.templates || []).length))}</strong>
          </div>
        </div>
        <div class="notice">
          <strong>Roles</strong>
          <div class="small">${escapeHtml((blueprint.roles || []).join(", ") || "none")}</div>
        </div>
        <div class="notice">
          <strong>Project root</strong>
          <pre>${escapeHtml(payload.project_root || "")}</pre>
        </div>
      `;

      const agents = payload.agents || [];
      nodes.agentsPanel.innerHTML = agents.length ? `
        <div class="list">
          ${agents.map((agent) => `
            <div class="list-item">
              <div class="pill-row">
                ${statusPill(agent.role)}
                ${statusPill(agent.route_priority || "normal")}
              </div>
              <strong>${escapeHtml(agent.name || agent.role)}</strong>
              <div class="small">${escapeHtml(agent.description || "No description")}</div>
              <div class="small">skills: ${escapeHtml((agent.skill_files || []).join(", ") || "none")}</div>
            </div>
          `).join("")}
        </div>
      ` : `<div class="empty">No agent catalog is available for this project root.</div>`;
    }

    function render() {
      renderHero();
      const run = activeRun();
      renderChatSection(run);
      renderRunsSection(run);
      renderTasksSection(run);
      renderWorkersSection(run);
      renderEventsSection(run);
      renderSettingsSection();
    }

    async function postJson(path, payload) {
      const response = await fetch(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || `${path} failed`);
      }
      return await response.json();
    }

    async function loadState() {
      if (state.busy) {
        return;
      }
      state.busy = true;
      nodes.refreshButton.disabled = true;
      try {
        const response = await fetch("/api/state?limit=8", { cache: "no-store" });
        const payload = await response.json();
        state.payload = payload;
        state.lastLoadedAt = Date.now();
        const runIds = new Set((payload.runs || []).map((run) => run.id));
        if (!state.activeRunId || !runIds.has(state.activeRunId)) {
          state.activeRunId = payload.selected_run_id || payload.selected_run?.id || payload.runs?.[0]?.id || null;
        }
        render();
      } catch (error) {
        nodes.refreshStatus.textContent = `Refresh failed: ${error.message}`;
      } finally {
        state.busy = false;
        nodes.refreshButton.disabled = false;
      }
    }

    async function submitComposer(event) {
      event.preventDefault();
      const message = nodes.composerInput.value.trim();
      if (!message) {
        nodes.composerHint.textContent = "Message is required.";
        return;
      }
      const run = activeRun();
      const humanRequest = openHumanRequest(run);
      const payload = {
        message,
        dispatch: nodes.composerDispatch.value === "true",
        max_steps: Number(nodes.composerMaxSteps.value || 8),
      };
      if (run && humanRequest) {
        payload.workflow_run_id = run.id;
        payload.human_request_id = humanRequest.id;
      }
      nodes.composerSubmit.disabled = true;
      try {
        await postJson("/api/chat", payload);
        nodes.composerInput.value = "";
        nodes.composerHint.textContent = humanRequest
          ? "Clarification answer sent. Refreshing run state."
          : "Run request sent. Refreshing workflow state.";
        await loadState();
        window.setTimeout(loadState, 1200);
      } catch (error) {
        nodes.composerHint.textContent = `Send failed: ${error.message}`;
      } finally {
        nodes.composerSubmit.disabled = false;
      }
    }

    async function resolveApproval(workflowRunId, approvalRequestId, approved) {
      try {
        await postJson("/api/approval", {
          workflow_run_id: workflowRunId,
          approval_request_id: approvalRequestId,
          approved,
          dispatch: nodes.composerDispatch.value === "true",
          max_steps: Number(nodes.composerMaxSteps.value || 8),
        });
        await loadState();
        window.setTimeout(loadState, 1200);
      } catch (error) {
        nodes.composerHint.textContent = `Approval update failed: ${error.message}`;
      }
    }

    for (const button of nodes.navButtons) {
      button.addEventListener("click", () => setSection(button.dataset.section));
    }
    nodes.refreshButton.addEventListener("click", loadState);
    nodes.heroOpenChat.addEventListener("click", () => setSection("chat"));
    nodes.heroOpenRuns.addEventListener("click", () => setSection("runs"));
    nodes.chatComposer.addEventListener("submit", submitComposer);

    render();
    loadState();
    window.setInterval(loadState, 4000);
  </script>
</body>
</html>
"""

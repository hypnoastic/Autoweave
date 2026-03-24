"""Tiny local monitoring web app for AutoWeave workflow inspection."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

from autoweave.monitoring.service import MonitoringService


def _json_bytes(payload: Mapping[str, Any]) -> bytes:
    return json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")


class MonitoringDashboardApp:
    """Small WSGI app for launching and inspecting local AutoWeave workflows."""

    def __init__(self, service: MonitoringService) -> None:
        self.service = service

    def __call__(self, environ: Mapping[str, Any], start_response: Any) -> Iterable[bytes]:
        method = str(environ.get("REQUEST_METHOD", "GET")).upper()
        path = str(environ.get("PATH_INFO", "/"))
        if method == "GET" and path == "/":
            return self._respond(start_response, "200 OK", _render_index().encode("utf-8"), "text/html; charset=utf-8")
        if method == "GET" and path == "/api/state":
            query = parse_qs(str(environ.get("QUERY_STRING", "")))
            limit = max(1, int(query.get("limit", ["5"])[0]))
            payload = self.service.snapshot(limit=limit)
            return self._respond(start_response, "200 OK", _json_bytes(payload), "application/json")
        if method == "POST" and path == "/api/run":
            body = self._read_json_body(environ)
            request = str(body.get("request", "")).strip()
            if not request:
                return self._respond(
                    start_response,
                    "400 Bad Request",
                    _json_bytes({"error": "request is required"}),
                    "application/json",
                )
            max_steps = max(1, int(body.get("max_steps", 8)))
            dispatch = bool(body.get("dispatch", True))
            payload = self.service.launch_workflow(request=request, dispatch=dispatch, max_steps=max_steps)
            return self._respond(start_response, "202 Accepted", _json_bytes(payload), "application/json")
        if method == "POST" and path == "/api/chat":
            body = self._read_json_body(environ)
            message = str(body.get("message", "")).strip()
            if not message:
                return self._respond(
                    start_response,
                    "400 Bad Request",
                    _json_bytes({"error": "message is required"}),
                    "application/json",
                )
            workflow_run_id = str(body.get("workflow_run_id", "")).strip() or None
            human_request_id = str(body.get("human_request_id", "")).strip() or None
            max_steps = max(1, int(body.get("max_steps", 8)))
            dispatch = bool(body.get("dispatch", True))
            if workflow_run_id is not None and human_request_id is not None:
                payload = self.service.answer_human_request(
                    workflow_run_id=workflow_run_id,
                    request_id=human_request_id,
                    answer_text=message,
                    dispatch=dispatch,
                    max_steps=max_steps,
                )
            else:
                payload = self.service.launch_workflow(request=message, dispatch=dispatch, max_steps=max_steps)
            return self._respond(start_response, "202 Accepted", _json_bytes(payload), "application/json")
        if method == "POST" and path == "/api/approval":
            body = self._read_json_body(environ)
            workflow_run_id = str(body.get("workflow_run_id", "")).strip()
            approval_request_id = str(body.get("approval_request_id", "")).strip()
            if not workflow_run_id or not approval_request_id:
                return self._respond(
                    start_response,
                    "400 Bad Request",
                    _json_bytes({"error": "workflow_run_id and approval_request_id are required"}),
                    "application/json",
                )
            max_steps = max(1, int(body.get("max_steps", 8)))
            dispatch = bool(body.get("dispatch", True))
            approved = bool(body.get("approved", True))
            payload = self.service.resolve_approval_request(
                workflow_run_id=workflow_run_id,
                request_id=approval_request_id,
                approved=approved,
                dispatch=dispatch,
                max_steps=max_steps,
            )
            return self._respond(start_response, "202 Accepted", _json_bytes(payload), "application/json")
        return self._respond(
            start_response,
            "404 Not Found",
            _json_bytes({"error": f"unknown route {method} {path}"}),
            "application/json",
        )

    def _read_json_body(self, environ: Mapping[str, Any]) -> dict[str, Any]:
        content_length = int(environ.get("CONTENT_LENGTH") or 0)
        stream = environ.get("wsgi.input")
        if stream is None or content_length <= 0:
            return {}
        raw = stream.read(content_length)
        if not raw:
            return {}
        loaded = json.loads(raw.decode("utf-8"))
        if not isinstance(loaded, dict):
            raise TypeError("request body must be a JSON object")
        return loaded

    def _respond(self, start_response: Any, status: str, body: bytes, content_type: str) -> list[bytes]:
        start_response(
            status,
            [
                ("Content-Type", content_type),
                ("Content-Length", str(len(body))),
                ("Cache-Control", "no-store"),
            ],
        )
        return [body]


def serve_dashboard(
    *,
    root: Path,
    host: str = "127.0.0.1",
    port: int = 8765,
    environ: Mapping[str, str] | None = None,
) -> None:
    service = MonitoringService(root=root, environ=environ)
    app = MonitoringDashboardApp(service)
    with make_server(host, port, app) as server:
        server.serve_forever()


def _render_index() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AutoWeave Operator Console</title>
  <style>
    :root {
      --bg: #f5efe4;
      --panel: #fffaf1;
      --panel-2: #f8f1e4;
      --panel-3: #fffdf8;
      --text: #201811;
      --muted: #665b52;
      --border: #d9c8ae;
      --accent: #8a5b31;
      --accent-2: #1f6f5b;
      --accent-3: #355f8b;
      --warning: #a36a00;
      --danger: #982e2e;
      --shadow: 0 12px 28px rgba(32, 24, 17, 0.08);
      --sans: "Iowan Old Style", "Palatino", "Georgia", serif;
      --mono: "SFMono-Regular", "Menlo", "Consolas", monospace;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      background:
        radial-gradient(circle at top left, rgba(138,91,49,0.10), transparent 30%),
        radial-gradient(circle at bottom right, rgba(31,111,91,0.10), transparent 28%),
        var(--bg);
      color: var(--text);
      font-family: var(--sans);
    }
    h1, h2, h3, h4, p { margin: 0; }
    button, input, textarea {
      font: inherit;
    }
    .shell {
      display: grid;
      grid-template-columns: 290px minmax(0, 1fr) 430px;
      gap: 18px;
      padding: 18px;
      min-height: 100vh;
    }
    .column {
      display: grid;
      gap: 18px;
      align-content: start;
    }
    .panel {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 18px;
      box-shadow: var(--shadow);
      padding: 16px;
    }
    .panel.tight { padding: 12px; }
    .hero {
      display: grid;
      gap: 10px;
      background: linear-gradient(145deg, rgba(255,250,241,0.98), rgba(248,241,228,0.94));
    }
    .hero h1 { font-size: 1.9rem; }
    .muted { color: var(--muted); }
    .banner {
      border-radius: 14px;
      padding: 12px 14px;
      border: 1px solid transparent;
      display: none;
      white-space: pre-wrap;
    }
    .banner.active { display: block; }
    .banner.error {
      background: rgba(152,46,46,0.10);
      color: var(--danger);
      border-color: rgba(152,46,46,0.25);
    }
    .banner.warn {
      background: rgba(163,106,0,0.10);
      color: var(--warning);
      border-color: rgba(163,106,0,0.25);
    }
    .status-strip {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
    }
    .pill {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      border-radius: 999px;
      padding: 4px 10px;
      font-size: 0.82rem;
      font-weight: 700;
      background: rgba(138,91,49,0.12);
      color: var(--accent);
      white-space: normal;
      line-height: 1.2;
      text-align: center;
    }
    .pill.ok { background: rgba(31,111,91,0.12); color: var(--accent-2); }
    .pill.live { background: rgba(53,95,139,0.12); color: var(--accent-3); }
    .pill.warn { background: rgba(163,106,0,0.12); color: var(--warning); }
    .pill.bad { background: rgba(152,46,46,0.12); color: var(--danger); }
    .composer textarea {
      width: 100%;
      min-height: 132px;
      resize: vertical;
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 12px 14px;
      color: var(--text);
    }
    .composer-footer,
    .row {
      display: flex;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
    }
    .composer-footer {
      justify-content: space-between;
      margin-top: 12px;
    }
    .field {
      display: grid;
      gap: 6px;
    }
    .field input[type="number"] {
      width: 90px;
      padding: 9px 10px;
      border: 1px solid var(--border);
      border-radius: 12px;
      background: #fff;
    }
    .btn {
      appearance: none;
      border: 0;
      border-radius: 999px;
      padding: 10px 16px;
      cursor: pointer;
      font-weight: 700;
      color: #fff;
      background: linear-gradient(135deg, var(--accent), #b7793f);
    }
    .btn.secondary {
      background: linear-gradient(135deg, var(--accent-3), #4b79ab);
    }
    .btn.subtle {
      color: var(--text);
      background: rgba(138,91,49,0.12);
    }
    .btn.reject {
      background: linear-gradient(135deg, var(--danger), #bb5151);
    }
    .list {
      display: grid;
      gap: 10px;
    }
    .list-group {
      display: grid;
      gap: 8px;
    }
    .list-group h3 {
      font-size: 0.92rem;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .group-box {
      border: 1px solid var(--border);
      border-radius: 16px;
      background: rgba(255, 255, 255, 0.56);
      padding: 10px 12px;
    }
    .group-box > summary {
      list-style: none;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .group-box > summary::-webkit-details-marker { display: none; }
    .group-count {
      color: var(--muted);
      font-size: 0.85rem;
    }
    .group-items {
      display: grid;
      gap: 8px;
      margin-top: 10px;
    }
    .list-item {
      width: 100%;
      text-align: left;
      border: 1px solid var(--border);
      background: var(--panel-3);
      border-radius: 14px;
      padding: 12px;
      cursor: pointer;
      display: grid;
      gap: 8px;
    }
    .list-item.selected {
      border-color: var(--accent);
      box-shadow: 0 0 0 2px rgba(138,91,49,0.12);
    }
    .list-item:hover { background: #fff; }
    .list-title {
      display: flex;
      justify-content: space-between;
      gap: 8px;
      align-items: baseline;
    }
    .mono { font-family: var(--mono); }
    .chat-shell {
      display: grid;
      grid-template-rows: auto minmax(0, 1fr) auto;
      min-height: calc(100vh - 36px);
    }
    .chat-header {
      display: grid;
      gap: 10px;
    }
    .chat-scroll {
      overflow: auto;
      padding-right: 4px;
      display: grid;
      gap: 14px;
      align-content: start;
      min-height: 0;
    }
    .message {
      max-width: 92%;
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 12px 14px;
      background: #fff;
      display: grid;
      gap: 8px;
      box-shadow: 0 8px 18px rgba(32,24,17,0.04);
    }
    .message.user {
      margin-left: auto;
      background: #fff6eb;
    }
    .message.manager {
      background: #f8fbff;
    }
    .message.system {
      background: #fffaf4;
    }
    .message-meta {
      display: flex;
      justify-content: space-between;
      gap: 8px;
      align-items: center;
      font-size: 0.84rem;
      color: var(--muted);
    }
    .chat-composer {
      border-top: 1px solid var(--border);
      padding-top: 14px;
      display: grid;
      gap: 10px;
    }
    .chat-composer textarea {
      width: 100%;
      min-height: 110px;
      resize: vertical;
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 12px 14px;
    }
    .detail-stack {
      display: grid;
      gap: 12px;
      align-content: start;
    }
    .task-card-grid {
      display: grid;
      gap: 12px;
      margin-top: 12px;
    }
    .task-card {
      border: 1px solid var(--border);
      border-radius: 14px;
      background: #fff;
      padding: 12px 14px;
      display: grid;
      gap: 10px;
    }
    .task-card-header {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: flex-start;
      flex-wrap: wrap;
    }
    .state-row {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }
    .facts {
      display: grid;
      gap: 8px;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    }
    .fact {
      border: 1px solid var(--border);
      border-radius: 12px;
      background: var(--panel-3);
      padding: 8px 10px;
      display: grid;
      gap: 4px;
    }
    .section-note {
      border: 1px solid rgba(163,106,0,0.25);
      border-radius: 12px;
      background: rgba(163,106,0,0.08);
      color: var(--warning);
      padding: 10px 12px;
    }
    details {
      border: 1px solid var(--border);
      border-radius: 14px;
      background: var(--panel-3);
      padding: 10px 12px;
    }
    summary {
      cursor: pointer;
      font-weight: 700;
    }
    .detail-grid {
      display: grid;
      gap: 10px;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      margin-top: 12px;
    }
    .mini-card {
      border: 1px solid var(--border);
      border-radius: 12px;
      background: #fff;
      padding: 10px 12px;
      display: grid;
      gap: 6px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
      font-size: 0.92rem;
    }
    th, td {
      text-align: left;
      padding: 8px 10px;
      border-bottom: 1px solid var(--border);
      vertical-align: top;
    }
    pre {
      white-space: pre-wrap;
      word-break: break-word;
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 10px 12px;
      font-family: var(--mono);
      font-size: 0.85rem;
      overflow: auto;
    }
    .empty {
      border: 1px dashed var(--border);
      border-radius: 16px;
      padding: 20px;
      color: var(--muted);
      background: rgba(255,255,255,0.45);
    }
    @media (max-width: 1460px) {
      .shell { grid-template-columns: 300px minmax(0, 1fr); }
      .column.details { grid-column: 1 / -1; }
      .chat-shell { min-height: auto; }
    }
    @media (max-width: 980px) {
      .shell { grid-template-columns: 1fr; padding: 12px; }
      .column { gap: 12px; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <aside class="column">
      <section class="panel hero">
        <div class="status-strip">
          <span class="pill" id="status-pill">loading</span>
          <span class="pill ok" id="project-root">…</span>
        </div>
        <div>
          <h1>AutoWeave Operator Console</h1>
          <p class="muted" style="margin-top:8px;">Start runs, watch the canonical DAG advance, answer human questions, approve gates, and inspect attempts, artifacts, and events without leaving the library.</p>
        </div>
        <div id="state-banner" class="banner"></div>
      </section>

      <section class="panel composer">
        <h2>Manager Chat</h2>
        <p class="muted">If no run is selected, this starts a new workflow. If the selected run is waiting on a human question, this answers it.</p>
        <textarea id="composer-message" placeholder="Build a boutique clothing storefront. Ask me if checkout rules, shipping regions, or catalog constraints are missing."></textarea>
        <div class="composer-footer">
          <div class="row">
            <label class="field">
              <span class="muted">Max steps</span>
              <input id="composer-max-steps" type="number" min="1" value="6">
            </label>
            <label class="row muted">
              <input id="composer-dispatch" type="checkbox" checked>
              Dispatch to OpenHands
            </label>
          </div>
          <button id="composer-send" class="btn">Send</button>
        </div>
        <div id="composer-status" class="muted"></div>
      </section>

      <section class="panel tight">
        <h2>Runs</h2>
        <div id="run-list" class="list" style="margin-top:12px;"><div class="empty">Loading workflow runs…</div></div>
      </section>

      <section class="panel tight">
        <h2>Jobs</h2>
        <div id="jobs" class="list" style="margin-top:12px;"><div class="empty">No jobs yet.</div></div>
      </section>

      <section class="panel tight">
        <h2>Team</h2>
        <div id="agents" class="list" style="margin-top:12px;"><div class="empty">Loading agents…</div></div>
      </section>
    </aside>

    <main class="column">
      <section class="panel chat-shell">
        <div class="chat-header">
          <div class="row" style="justify-content:space-between;">
            <div>
              <h2 id="chat-title">Manager Thread</h2>
              <p id="chat-subtitle" class="muted">Select a run or start a new one.</p>
            </div>
            <div class="status-strip" id="chat-summary"></div>
          </div>
        </div>
        <div id="chat-scroll" class="chat-scroll">
          <div class="empty">No run selected yet. Start with a message in the composer to create a workflow run.</div>
        </div>
        <div class="chat-composer">
          <div class="row" id="approval-actions" style="display:none;">
            <button id="approve-btn" class="btn secondary">Approve highlighted request</button>
            <button id="reject-btn" class="btn reject">Reject highlighted request</button>
          </div>
          <p class="muted" id="chat-help">The composer above starts a new run or answers the selected run’s open human question.</p>
        </div>
      </section>
    </main>

    <aside class="column details">
      <section class="panel">
        <h2>Run Details</h2>
        <div id="run-details" class="detail-stack" style="margin-top:12px;">
          <div class="empty">Select a run to inspect the task graph, attempts, artifacts, approvals, and event timeline.</div>
        </div>
      </section>

      <section class="panel tight">
        <h2>Workflow Blueprint</h2>
        <div id="blueprint" style="margin-top:12px;"><div class="empty">Loading blueprint…</div></div>
      </section>
    </aside>
  </div>

  <script>
    const state = {
      snapshot: null,
      selectedRunId: null,
    };

    const nodes = {
      statusPill: document.getElementById("status-pill"),
      projectRoot: document.getElementById("project-root"),
      stateBanner: document.getElementById("state-banner"),
      runList: document.getElementById("run-list"),
      jobs: document.getElementById("jobs"),
      agents: document.getElementById("agents"),
      blueprint: document.getElementById("blueprint"),
      chatTitle: document.getElementById("chat-title"),
      chatSubtitle: document.getElementById("chat-subtitle"),
      chatSummary: document.getElementById("chat-summary"),
      chatScroll: document.getElementById("chat-scroll"),
      runDetails: document.getElementById("run-details"),
      composerMessage: document.getElementById("composer-message"),
      composerDispatch: document.getElementById("composer-dispatch"),
      composerMaxSteps: document.getElementById("composer-max-steps"),
      composerSend: document.getElementById("composer-send"),
      composerStatus: document.getElementById("composer-status"),
      approveBtn: document.getElementById("approve-btn"),
      rejectBtn: document.getElementById("reject-btn"),
      approvalActions: document.getElementById("approval-actions"),
      chatHelp: document.getElementById("chat-help"),
    };

    function escapeHtml(text) {
      return String(text ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;");
    }

    function badgeClass(status) {
      const value = String(status || "").toLowerCase();
      if (["completed", "succeeded", "ready", "open", "approved"].includes(value)) return "pill ok";
      if (["active", "running", "dispatching", "queued"].includes(value)) return "pill live";
      if (["waiting_for_human", "waiting_for_approval", "waiting_for_dependency", "blocked", "paused", "needs_input", "requested", "degraded", "stalled", "orphaned"].includes(value)) return "pill warn";
      if (["failed", "errored", "error", "rejected", "aborted", "orphaned"].includes(value)) return "pill bad";
      return "pill";
    }

    function renderBanner(snapshot) {
      nodes.projectRoot.textContent = snapshot.project_root || "unknown";
      nodes.statusPill.textContent = snapshot.status || "ok";
      nodes.statusPill.className = badgeClass(snapshot.status || "ok");
      if (snapshot.status === "loading") {
        nodes.stateBanner.className = "banner active warn";
        nodes.stateBanner.textContent = snapshot.load_error || "Loading live workflow state…";
      } else if (snapshot.load_error) {
        nodes.stateBanner.className = "banner active error";
        nodes.stateBanner.textContent = snapshot.load_error;
      } else if ((snapshot.jobs || []).some((job) => job.status === "error")) {
        nodes.stateBanner.className = "banner active warn";
        nodes.stateBanner.textContent = "One or more background jobs failed. Select the job or run for details.";
      } else {
        nodes.stateBanner.className = "banner";
        nodes.stateBanner.textContent = "";
      }
    }

    function renderAgents(agents) {
      if (!agents.length) {
        nodes.agents.innerHTML = '<div class="empty">No agent definitions found under this project root.</div>';
        return;
      }
      nodes.agents.innerHTML = agents.map((agent) => `
        <div class="mini-card">
          <div class="row" style="justify-content:space-between;">
            <strong>${escapeHtml(agent.role)}</strong>
            <span class="${badgeClass((agent.model_profile_hints || []).join(", ") || "default")}">${escapeHtml((agent.model_profile_hints || []).join(", ") || "default")}</span>
          </div>
          <div class="muted">${escapeHtml(agent.specialization || "general")}</div>
          <div>${escapeHtml(agent.description || agent.soul_excerpt || "")}</div>
          <div class="muted">Skills: ${escapeHtml((agent.skill_files || []).join(", ") || "none")}</div>
        </div>
      `).join("");
    }

    function renderBlueprint(blueprint) {
      const rows = (blueprint.templates || []).map((item) => `
        <tr>
          <td><code>${escapeHtml(item.key)}</code></td>
          <td>${escapeHtml(item.assigned_role)}</td>
          <td>${escapeHtml((item.hard_dependencies || []).join(", ") || "none")}</td>
          <td>${escapeHtml((item.approval_requirements || []).join(", ") || "none")}</td>
        </tr>
      `).join("");
      nodes.blueprint.innerHTML = `
        <div class="detail-grid">
          <div class="mini-card"><div class="muted">Workflow</div><strong>${escapeHtml(blueprint.name || "unknown")}</strong></div>
          <div class="mini-card"><div class="muted">Version</div><strong>${escapeHtml(blueprint.version || "n/a")}</strong></div>
          <div class="mini-card"><div class="muted">Entrypoint</div><strong><code>${escapeHtml(blueprint.entrypoint || "n/a")}</code></strong></div>
        </div>
        <table>
          <thead><tr><th>Task</th><th>Role</th><th>Hard deps</th><th>Approval gate</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      `;
    }

    function groupRuns(runs) {
      const groups = { active: [], waiting: [], completed: [], failed: [] };
      for (const run of runs) {
        const status = String(run.operator_status || run.status || "").toLowerCase();
        if (["completed", "succeeded"].includes(status)) groups.completed.push(run);
        else if (["failed", "errored"].includes(status)) groups.failed.push(run);
        else if (["waiting_for_human", "waiting_for_approval", "blocked", "stalled", "waiting_for_dependency"].includes(status) || (run.human_requests || []).some((item) => item.status === "open") || (run.approval_requests || []).some((item) => item.status === "requested")) groups.waiting.push(run);
        else groups.active.push(run);
      }
      return groups;
    }

    function runSummaryText(run) {
      const humanCount = (run.human_requests || []).filter((item) => item.status === "open").length;
      const approvalCount = (run.approval_requests || []).filter((item) => item.status === "requested").length;
      if (run.operator_summary) return run.operator_summary;
      if (humanCount || approvalCount) return `${humanCount} human · ${approvalCount} approval`;
      return `${(run.tasks || []).length} tasks · ${(run.artifacts || []).length} artifacts`;
    }

    function selectRun(runId) {
      state.selectedRunId = runId;
      renderSelectedRun();
      renderRunList();
    }

    function renderRunList() {
      const runs = (state.snapshot?.runs || []);
      if (!runs.length) {
        nodes.runList.innerHTML = '<div class="empty">No persisted workflow runs found yet.</div>';
        return;
      }
      const grouped = groupRuns(runs);
      const sections = [
        ["active", "Active"],
        ["waiting", "Waiting"],
        ["completed", "Completed"],
        ["failed", "Failed"],
      ].map(([key, label]) => {
        const items = grouped[key];
        if (!items.length) return "";
        return `
          <details class="group-box" open>
            <summary>
              <strong>${escapeHtml(label)}</strong>
              <span class="group-count">${escapeHtml(String(items.length))}</span>
            </summary>
            <div class="group-items">
              ${items.map((run) => `
              <button class="list-item ${state.selectedRunId === run.id ? "selected" : ""}" data-run-id="${escapeHtml(run.id)}">
                <div class="list-title">
                  <strong>${escapeHtml(run.title || run.workflow_request || run.id)}</strong>
                  <span class="${badgeClass(run.operator_status || run.status)}">${escapeHtml(run.operator_status || run.status)}</span>
                </div>
                <div class="muted mono">${escapeHtml(run.id)}</div>
                <div class="muted">${escapeHtml(runSummaryText(run))}</div>
                <div class="muted">workflow: ${escapeHtml(run.status || "unknown")}</div>
              </button>
              `).join("")}
            </div>
          </details>
        `;
      }).join("");
      nodes.runList.innerHTML = sections;
      nodes.runList.querySelectorAll("[data-run-id]").forEach((button) => {
        button.addEventListener("click", () => selectRun(button.getAttribute("data-run-id")));
      });
    }

    function renderJobs(jobs) {
      if (!jobs.length) {
        nodes.jobs.innerHTML = '<div class="empty">No background jobs yet.</div>';
        return;
      }
      nodes.jobs.innerHTML = jobs.map((job) => `
        <div class="mini-card">
          <div class="row" style="justify-content:space-between;">
            <strong>${escapeHtml(job.action)}</strong>
            <span class="${badgeClass(job.status)}">${escapeHtml(job.status)}</span>
          </div>
          <div>${escapeHtml(job.request || "no message")}</div>
          ${job.workflow_run_id ? `<div class="muted mono">${escapeHtml(job.workflow_run_id)}</div>` : ""}
          ${job.error ? `<div class="muted" style="color:var(--danger);">${escapeHtml(job.error)}</div>` : ""}
        </div>
      `).join("");
    }

    function renderJson(value) {
      if (value === null || value === undefined || value === "") {
        return '<div class="muted">none</div>';
      }
      if (typeof value === "string") {
        return `<pre>${escapeHtml(value)}</pre>`;
      }
      return `<pre>${escapeHtml(JSON.stringify(value, null, 2))}</pre>`;
    }

    function renderSelectedRun() {
      const runs = state.snapshot?.runs || [];
      const fallbackRunId = state.snapshot?.selected_run_id || null;
      if (!state.selectedRunId && fallbackRunId) state.selectedRunId = fallbackRunId;
      const run = runs.find((item) => item.id === state.selectedRunId) || null;
      if (!run) {
        nodes.chatTitle.textContent = "Manager Thread";
        nodes.chatSubtitle.textContent = "Select a run or start a new one.";
        nodes.chatSummary.innerHTML = "";
        nodes.chatScroll.innerHTML = '<div class="empty">No run selected yet. Start a workflow from the composer to see the chat and state updates here.</div>';
        nodes.runDetails.innerHTML = '<div class="empty">Select a run to inspect the task graph, attempts, artifacts, blockers, and event timeline.</div>';
        nodes.approvalActions.style.display = "none";
        nodes.chatHelp.textContent = "The composer above starts a new run or answers the selected run’s open human question.";
        return;
      }

      const openHuman = (run.human_requests || []).find((item) => item.status === "open") || null;
      const openApproval = (run.approval_requests || []).find((item) => item.status === "requested") || null;
      const operatorStatus = run.operator_status || run.status || "unknown";
      nodes.chatTitle.textContent = run.title || run.workflow_request || run.id;
      nodes.chatSubtitle.textContent = run.id;
      nodes.chatSummary.innerHTML = `
        <span class="${badgeClass(operatorStatus)}">${escapeHtml(operatorStatus)}</span>
        <span class="pill">workflow ${escapeHtml(run.status || "unknown")}</span>
        <span class="pill">${escapeHtml(`${(run.tasks || []).length} tasks`)}</span>
        <span class="pill">${escapeHtml(`${(run.attempts || []).length} attempts`)}</span>
        <span class="pill">${escapeHtml(`${(run.artifacts || []).length} artifacts`)}</span>
      `;
      nodes.chatHelp.textContent = openHuman
        ? "The selected run is waiting on a human answer. Reply in the composer above to continue."
        : openApproval
        ? "This run is waiting on approval. Use the approval buttons below."
        : "No open human question on this run. The composer above will start a new run.";
      nodes.approvalActions.style.display = openApproval ? "flex" : "none";
      nodes.approveBtn.dataset.workflowRunId = run.id;
      nodes.approveBtn.dataset.approvalRequestId = openApproval ? openApproval.id : "";
      nodes.rejectBtn.dataset.workflowRunId = run.id;
      nodes.rejectBtn.dataset.approvalRequestId = openApproval ? openApproval.id : "";

      const messages = run.chat_messages || [];
      nodes.chatScroll.innerHTML = messages.length
        ? messages.map((message) => `
            <div class="message ${escapeHtml(message.role || "system")}">
              <div class="message-meta">
                <strong>${escapeHtml(message.role || "system")}</strong>
                <span class="${badgeClass(message.status || message.kind || "")}">${escapeHtml(message.kind || "message")}</span>
              </div>
              <div>${escapeHtml(message.text || "")}</div>
              ${message.answer_text ? `<div class="muted">Answer: ${escapeHtml(message.answer_text)}</div>` : ""}
            </div>
          `).join("")
        : '<div class="empty">No chat messages recorded yet for this run.</div>';

      const taskCards = (run.tasks || []).map((task) => `
        <div class="task-card">
          <div class="task-card-header">
            <div>
              <strong><code>${escapeHtml(task.task_key)}</code></strong>
              <div class="muted">${escapeHtml(task.assigned_role)}</div>
            </div>
            <div class="state-row">
              <span class="${badgeClass(task.state)}">${escapeHtml(task.state)}</span>
              ${task.latest_attempt_state ? `<span class="${badgeClass(task.latest_attempt_state)}">${escapeHtml(task.latest_attempt_state)}</span>` : ""}
            </div>
          </div>
          ${task.description ? `<div>${escapeHtml(task.description)}</div>` : ""}
          ${task.block_reason ? `<div class="section-note">Blocked: ${escapeHtml(task.block_reason)}</div>` : ""}
          <div class="facts">
            <div class="fact">
              <div class="muted">Hard deps</div>
              <div>${escapeHtml((task.hard_dependencies || []).join(", ") || "none")}</div>
            </div>
            <div class="fact">
              <div class="muted">Route hints</div>
              <div>${escapeHtml((task.route_hints || []).join(", ") || "none")}</div>
            </div>
            <div class="fact">
              <div class="muted">Model</div>
              <div>${escapeHtml(task.model_name || "n/a")}</div>
            </div>
            <div class="fact">
              <div class="muted">Workspace</div>
              <div><code>${escapeHtml(task.workspace_path || task.workspace_id || "n/a")}</code></div>
            </div>
          </div>
        </div>
      `).join("");
      const attemptRows = (run.attempts || []).map((attempt) => `
        <tr>
          <td><code>${escapeHtml(attempt.task_key || attempt.task_id)}</code></td>
          <td>${escapeHtml(String(attempt.attempt_number))}</td>
          <td>${escapeHtml(attempt.state)}</td>
          <td>${escapeHtml(attempt.model_name || "n/a")}</td>
          <td><code>${escapeHtml(attempt.workspace_path || attempt.workspace_id || "n/a")}</code></td>
        </tr>
      `).join("");
      const artifactRows = (run.artifacts || []).map((artifact) => `
        <tr>
          <td><code>${escapeHtml(artifact.task_key || artifact.task_id)}</code></td>
          <td>${escapeHtml(artifact.artifact_type)}</td>
          <td>${escapeHtml(artifact.status)}</td>
          <td>${escapeHtml(artifact.title || "")}</td>
          <td>${escapeHtml(artifact.summary || "")}</td>
        </tr>
      `).join("");
      const eventRows = (run.events || []).map((event) => `
        <tr>
          <td>${escapeHtml(String(event.sequence_no))}</td>
          <td>${escapeHtml(event.event_type)}</td>
          <td>${escapeHtml(event.source)}</td>
          <td>${escapeHtml(event.agent_role || "")}</td>
          <td>${escapeHtml(event.message || "")}</td>
        </tr>
      `).join("");

      nodes.runDetails.innerHTML = `
        <div class="detail-grid">
          <div class="mini-card"><div class="muted">Operator status</div><strong>${escapeHtml(operatorStatus)}</strong></div>
          <div class="mini-card"><div class="muted">Workflow status</div><strong>${escapeHtml(run.status)}</strong></div>
          <div class="mini-card"><div class="muted">Open human requests</div><strong>${escapeHtml(String((run.human_requests || []).filter((item) => item.status === "open").length))}</strong></div>
          <div class="mini-card"><div class="muted">Open approvals</div><strong>${escapeHtml(String((run.approval_requests || []).filter((item) => item.status === "requested").length))}</strong></div>
          <div class="mini-card"><div class="muted">Active attempts</div><strong>${escapeHtml(String((run.attempt_state_counts && (run.attempt_state_counts.running || 0) + (run.attempt_state_counts.dispatching || 0) + (run.attempt_state_counts.queued || 0) + (run.attempt_state_counts.paused || 0) + (run.attempt_state_counts.needs_input || 0)) || 0))}</strong></div>
          <div class="mini-card"><div class="muted">Ready tasks</div><strong>${escapeHtml(String((run.ready_task_keys || []).length))}</strong></div>
          <div class="mini-card"><div class="muted">Blocked tasks</div><strong>${escapeHtml(String((run.blocked_task_keys || []).length))}</strong></div>
          <div class="mini-card"><div class="muted">Graph revision</div><strong>${escapeHtml(String(run.graph_revision || 1))}</strong></div>
        </div>
        <details open>
          <summary>Manager plan and execution</summary>
          <div style="margin-top:10px;">
            ${run.operator_summary ? `<div class="section-note">${escapeHtml(run.operator_summary)}</div>` : ""}
            <h4 style="margin-top:10px;">Plan</h4>
            ${run.manager_plan ? renderJson(run.manager_plan) : '<div class="empty">No valid workflow plan artifact has been published yet.</div>'}
            <h4 style="margin-top:10px;">Execution note</h4>
            ${renderJson(run.manager_outcome)}
            <div class="detail-grid">
              <div class="mini-card"><div class="muted">Manager task</div><strong>${escapeHtml(run.manager_task_state || "none")}</strong></div>
              <div class="mini-card"><div class="muted">Manager attempt</div><strong>${escapeHtml(run.manager_attempt_state || "none")}</strong></div>
            </div>
          </div>
        </details>
        <details open>
          <summary>Tasks</summary>
          <div class="task-card-grid">${taskCards || '<div class="empty">No tasks.</div>'}</div>
        </details>
        <details>
          <summary>Attempts and sandboxes</summary>
          <table><thead><tr><th>Task</th><th>#</th><th>State</th><th>Model</th><th>Workspace</th></tr></thead><tbody>${attemptRows || '<tr><td colspan="5">No attempts.</td></tr>'}</tbody></table>
        </details>
        <details>
          <summary>Artifacts</summary>
          <table><thead><tr><th>Task</th><th>Type</th><th>Status</th><th>Title</th><th>Summary</th></tr></thead><tbody>${artifactRows || '<tr><td colspan="5">No artifacts.</td></tr>'}</tbody></table>
        </details>
        <details>
          <summary>Task I/O and dependencies</summary>
          ${(run.run_steps || []).map((step) => `
            <div class="mini-card" style="margin-top:10px;">
              <strong>${escapeHtml(step.task_key)}</strong>
              <div class="muted">${escapeHtml(step.role)} · ${escapeHtml(step.state)}${step.attempt_state ? ` · ${escapeHtml(step.attempt_state)}` : ""}</div>
              ${step.block_reason ? `<div class="muted" style="color:var(--danger);">Blocked: ${escapeHtml(step.block_reason)}</div>` : ""}
              <div style="margin-top:8px;"><strong>Input</strong>${renderJson(step.input_json)}</div>
              <div style="margin-top:8px;"><strong>Output</strong>${renderJson(step.output_json)}</div>
            </div>
          `).join("") || '<div class="empty">No step details yet.</div>'}
        </details>
        <details>
          <summary>Events</summary>
          <table><thead><tr><th>#</th><th>Type</th><th>Source</th><th>Role</th><th>Message</th></tr></thead><tbody>${eventRows || '<tr><td colspan="5">No events.</td></tr>'}</tbody></table>
        </details>
      `;
    }

    async function postJson(url, payload) {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || `Request failed: ${response.status}`);
      }
      return data;
    }

    async function loadState() {
      try {
        const response = await fetch("/api/state");
        const snapshot = await response.json();
        state.snapshot = snapshot;
        renderBanner(snapshot);
        renderAgents(snapshot.agents || []);
        renderBlueprint(snapshot.workflow_blueprint || {});
        renderJobs(snapshot.jobs || []);
        if (!state.selectedRunId && snapshot.selected_run_id) {
          state.selectedRunId = snapshot.selected_run_id;
        }
        renderRunList();
        renderSelectedRun();
      } catch (error) {
        nodes.statusPill.textContent = "error";
        nodes.statusPill.className = "pill bad";
        nodes.stateBanner.className = "banner active error";
        nodes.stateBanner.textContent = String(error);
      }
    }

    async function sendComposerMessage() {
      const message = nodes.composerMessage.value.trim();
      if (!message) return;
      const selectedRun = (state.snapshot?.runs || []).find((item) => item.id === state.selectedRunId) || null;
      const openHuman = selectedRun ? (selectedRun.human_requests || []).find((item) => item.status === "open") || null : null;
      nodes.composerStatus.textContent = "Sending…";
      try {
        if (selectedRun && openHuman) {
          await postJson("/api/chat", {
            message,
            workflow_run_id: selectedRun.id,
            human_request_id: openHuman.id,
            dispatch: nodes.composerDispatch.checked,
            max_steps: Number(nodes.composerMaxSteps.value || "6"),
          });
        } else {
          await postJson("/api/chat", {
            message,
            dispatch: nodes.composerDispatch.checked,
            max_steps: Number(nodes.composerMaxSteps.value || "6"),
          });
        }
        nodes.composerMessage.value = "";
        nodes.composerStatus.textContent = "Queued.";
        await loadState();
      } catch (error) {
        nodes.composerStatus.textContent = String(error);
      }
    }

    async function resolveApproval(approved) {
      const workflowRunId = approved ? nodes.approveBtn.dataset.workflowRunId : nodes.rejectBtn.dataset.workflowRunId;
      const approvalRequestId = approved ? nodes.approveBtn.dataset.approvalRequestId : nodes.rejectBtn.dataset.approvalRequestId;
      if (!workflowRunId || !approvalRequestId) return;
      nodes.composerStatus.textContent = approved ? "Approving…" : "Rejecting…";
      try {
        await postJson("/api/approval", {
          workflow_run_id: workflowRunId,
          approval_request_id: approvalRequestId,
          approved,
          dispatch: nodes.composerDispatch.checked,
          max_steps: Number(nodes.composerMaxSteps.value || "6"),
        });
        nodes.composerStatus.textContent = approved ? "Approval queued." : "Rejection queued.";
        await loadState();
      } catch (error) {
        nodes.composerStatus.textContent = String(error);
      }
    }

    nodes.composerSend.addEventListener("click", sendComposerMessage);
    nodes.approveBtn.addEventListener("click", () => resolveApproval(true));
    nodes.rejectBtn.addEventListener("click", () => resolveApproval(false));

    loadState();
    setInterval(loadState, 2000);
  </script>
</body>
</html>
"""

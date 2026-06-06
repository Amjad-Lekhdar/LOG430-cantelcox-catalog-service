CATALOG_ADMIN_HTML = """
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CanTelcoX Catalog</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f4f7f8;
      --panel: #ffffff;
      --text: #1d2528;
      --muted: #627176;
      --line: #d8e0e3;
      --primary: #0f766e;
      --primary-dark: #115e59;
      --danger: #b42318;
      --danger-soft: #fff0ed;
      --ok-soft: #e8f7ef;
      --ok: #067647;
      --inactive: #697586;
      --shadow: 0 12px 30px rgba(29, 37, 40, 0.08);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      font-size: 15px;
      letter-spacing: 0;
    }

    button,
    input,
    textarea,
    select {
      font: inherit;
    }

    button {
      min-height: 38px;
      border: 1px solid transparent;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 650;
      transition: background 120ms ease, border-color 120ms ease, color 120ms ease;
    }

    button:disabled {
      cursor: not-allowed;
      opacity: 0.6;
    }

    .shell {
      width: min(1180px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 28px 0;
    }

    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 20px;
    }

    h1 {
      margin: 0;
      font-size: clamp(24px, 3vw, 34px);
      line-height: 1.1;
      letter-spacing: 0;
    }

    .subtitle {
      margin: 6px 0 0;
      color: var(--muted);
    }

    .layout {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 360px;
      gap: 18px;
      align-items: start;
    }

    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }

    .panel-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 16px 18px;
      border-bottom: 1px solid var(--line);
    }

    .panel-title {
      margin: 0;
      font-size: 17px;
      line-height: 1.2;
    }

    .toolbar {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }

    .secondary {
      background: #ffffff;
      border-color: var(--line);
      color: var(--text);
    }

    .secondary:hover {
      border-color: #9fb1b7;
    }

    .primary {
      background: var(--primary);
      color: #ffffff;
    }

    .primary:hover {
      background: var(--primary-dark);
    }

    .danger {
      background: var(--danger-soft);
      color: var(--danger);
      border-color: #ffd1c9;
    }

    .danger:hover {
      border-color: #f5a79b;
    }

    .table-wrap {
      overflow-x: auto;
    }

    table {
      width: 100%;
      min-width: 760px;
      border-collapse: collapse;
    }

    th,
    td {
      padding: 13px 16px;
      text-align: left;
      border-bottom: 1px solid var(--line);
      vertical-align: middle;
    }

    th {
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0;
      background: #fbfcfc;
    }

    td.description {
      max-width: 300px;
      color: var(--muted);
    }

    .price {
      white-space: nowrap;
      font-variant-numeric: tabular-nums;
      font-weight: 700;
    }

    .status {
      display: inline-flex;
      align-items: center;
      min-height: 26px;
      padding: 3px 9px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 700;
    }

    .status.active {
      background: var(--ok-soft);
      color: var(--ok);
    }

    .status.inactive {
      background: #eef1f3;
      color: var(--inactive);
    }

    .actions {
      display: flex;
      gap: 8px;
      white-space: nowrap;
    }

    .form {
      display: grid;
      gap: 13px;
      padding: 18px;
    }

    label {
      display: grid;
      gap: 7px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
    }

    input,
    textarea {
      width: 100%;
      min-height: 40px;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 9px 11px;
      color: var(--text);
      background: #ffffff;
    }

    textarea {
      min-height: 96px;
      resize: vertical;
    }

    input:focus,
    textarea:focus {
      outline: 2px solid rgba(15, 118, 110, 0.2);
      border-color: var(--primary);
    }

    .checks {
      display: grid;
      gap: 10px;
      grid-template-columns: 1fr 1fr;
    }

    .check {
      display: flex;
      align-items: center;
      gap: 8px;
      min-height: 42px;
      padding: 9px 10px;
      border: 1px solid var(--line);
      border-radius: 6px;
      color: var(--text);
      background: #fbfcfc;
    }

    .check input {
      width: 18px;
      min-height: 18px;
    }

    .form-actions {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 8px;
      margin-top: 2px;
    }

    .message {
      min-height: 22px;
      margin: 0;
      color: var(--muted);
      font-size: 13px;
    }

    .message.error {
      color: var(--danger);
    }

    .empty {
      padding: 34px 18px;
      color: var(--muted);
      text-align: center;
    }

    @media (max-width: 900px) {
      .layout {
        grid-template-columns: 1fr;
      }

      .topbar,
      .panel-head {
        align-items: stretch;
        flex-direction: column;
      }

      .toolbar {
        width: 100%;
      }

      .toolbar button,
      .form-actions button {
        flex: 1;
      }
    }
  </style>
</head>
<body>
  <main class="shell">
    <header class="topbar">
      <div>
        <h1>CanTelcoX Catalog</h1>
        <p class="subtitle">Gestion des plans mobiles</p>
      </div>
      <div class="toolbar">
        <button class="secondary" id="refreshButton" type="button">Actualiser</button>
        <button class="primary" id="newButton" type="button">Nouveau plan</button>
      </div>
    </header>

    <section class="layout">
      <div class="panel">
        <div class="panel-head">
          <h2 class="panel-title">Plans</h2>
          <div class="toolbar">
            <label class="check">
              <input id="showInactive" type="checkbox" checked>
              Inactifs
            </label>
          </div>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Nom</th>
                <th>Description</th>
                <th>Prix</th>
                <th>Donnees</th>
                <th>Appels</th>
                <th>Statut</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody id="plansBody"></tbody>
          </table>
          <div class="empty" id="emptyState" hidden>Aucun plan trouve.</div>
        </div>
      </div>

      <aside class="panel">
        <div class="panel-head">
          <h2 class="panel-title" id="formTitle">Nouveau plan</h2>
        </div>
        <form class="form" id="planForm">
          <input id="planId" type="hidden">
          <label>
            Nom
            <input id="name" name="name" maxlength="120" required>
          </label>
          <label>
            Description
            <textarea id="description" name="description" maxlength="500" required></textarea>
          </label>
          <label>
            Prix mensuel
            <input id="monthly_price" name="monthly_price" type="number" min="0" step="0.01" required>
          </label>
          <label>
            Donnees incluses (GB)
            <input id="data_limit_gb" name="data_limit_gb" type="number" min="0" step="1" required>
          </label>
          <div class="checks">
            <label class="check">
              <input id="unlimited_calls" name="unlimited_calls" type="checkbox" checked>
              Appels illimites
            </label>
            <label class="check">
              <input id="active" name="active" type="checkbox" checked>
              Actif
            </label>
          </div>
          <p class="message" id="message"></p>
          <div class="form-actions">
            <button class="primary" type="submit" id="saveButton">Enregistrer</button>
            <button class="secondary" type="button" id="cancelButton">Annuler</button>
          </div>
        </form>
      </aside>
    </section>
  </main>

  <script>
    const apiBase = "/v1/catalog/plans";
    const plansBody = document.querySelector("#plansBody");
    const emptyState = document.querySelector("#emptyState");
    const form = document.querySelector("#planForm");
    const message = document.querySelector("#message");
    const formTitle = document.querySelector("#formTitle");
    const showInactive = document.querySelector("#showInactive");
    let plans = [];

    function money(value) {
      return new Intl.NumberFormat("fr-CA", {
        style: "currency",
        currency: "CAD"
      }).format(value);
    }

    function escapeHtml(value) {
      return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    function setMessage(text, isError = false) {
      message.textContent = text;
      message.classList.toggle("error", isError);
    }

    function payloadFromForm() {
      return {
        name: form.name.value.trim(),
        description: form.description.value.trim(),
        monthly_price: Number(form.monthly_price.value),
        data_limit_gb: Number.parseInt(form.data_limit_gb.value, 10),
        unlimited_calls: form.unlimited_calls.checked,
        active: form.active.checked
      };
    }

    function resetForm() {
      form.reset();
      form.planId.value = "";
      form.unlimited_calls.checked = true;
      form.active.checked = true;
      formTitle.textContent = "Nouveau plan";
      setMessage("");
      form.name.focus();
    }

    function editPlan(planId) {
      const plan = plans.find((item) => item.id === planId);
      if (!plan) {
        return;
      }

      form.planId.value = plan.id;
      form.name.value = plan.name;
      form.description.value = plan.description;
      form.monthly_price.value = plan.monthly_price;
      form.data_limit_gb.value = plan.data_limit_gb;
      form.unlimited_calls.checked = plan.unlimited_calls;
      form.active.checked = plan.active;
      formTitle.textContent = "Modifier le plan";
      setMessage("");
      form.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    async function deactivatePlan(planId) {
      const plan = plans.find((item) => item.id === planId);
      if (!plan) {
        return;
      }

      const response = await fetch(`${apiBase}/${planId}`, { method: "DELETE" });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Desactivation impossible");
      }
      await loadPlans();
      setMessage(`${plan.name} est maintenant inactif.`);
    }

    function renderPlans() {
      plansBody.innerHTML = "";
      emptyState.hidden = plans.length > 0;

      plans.forEach((plan) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td><strong>${escapeHtml(plan.name)}</strong></td>
          <td class="description">${escapeHtml(plan.description)}</td>
          <td class="price">${money(plan.monthly_price)}</td>
          <td>${plan.data_limit_gb} GB</td>
          <td>${plan.unlimited_calls ? "Illimites" : "Limites"}</td>
          <td><span class="status ${plan.active ? "active" : "inactive"}">${plan.active ? "Actif" : "Inactif"}</span></td>
          <td>
            <div class="actions">
              <button class="secondary" type="button" data-action="edit" data-id="${plan.id}">Modifier</button>
              <button class="danger" type="button" data-action="deactivate" data-id="${plan.id}" ${plan.active ? "" : "disabled"}>Desactiver</button>
            </div>
          </td>
        `;
        plansBody.appendChild(row);
      });
    }

    async function loadPlans() {
      const activeOnly = showInactive.checked ? "false" : "true";
      const response = await fetch(`${apiBase}?active_only=${activeOnly}`);
      if (!response.ok) {
        throw new Error("Chargement impossible");
      }
      plans = await response.json();
      renderPlans();
    }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const planId = form.planId.value;
      const method = planId ? "PUT" : "POST";
      const url = planId ? `${apiBase}/${planId}` : apiBase;

      try {
        const response = await fetch(url, {
          method,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payloadFromForm())
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.detail || "Enregistrement impossible");
        }

        await loadPlans();
        resetForm();
        setMessage("Plan enregistre.");
      } catch (error) {
        setMessage(error.message, true);
      }
    });

    plansBody.addEventListener("click", async (event) => {
      const button = event.target.closest("button[data-action]");
      if (!button) {
        return;
      }

      const action = button.dataset.action;
      const planId = button.dataset.id;

      try {
        if (action === "edit") {
          editPlan(planId);
        }
        if (action === "deactivate") {
          await deactivatePlan(planId);
        }
      } catch (error) {
        setMessage(error.message, true);
      }
    });

    document.querySelector("#refreshButton").addEventListener("click", loadPlans);
    document.querySelector("#newButton").addEventListener("click", resetForm);
    document.querySelector("#cancelButton").addEventListener("click", resetForm);
    showInactive.addEventListener("change", loadPlans);

    loadPlans().catch((error) => setMessage(error.message, true));
  </script>
</body>
</html>
"""

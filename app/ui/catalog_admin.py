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
      --bg: #f5f7f8;
      --panel: #ffffff;
      --text: #20292d;
      --muted: #66777d;
      --line: #d9e1e4;
      --primary: #0f766e;
      --primary-dark: #115e59;
      --danger: #b42318;
      --danger-soft: #fff0ed;
      --ok: #067647;
      --ok-soft: #e8f7ef;
      --warn: #9a6700;
      --warn-soft: #fff7d6;
      --shadow: 0 12px 28px rgba(32, 41, 45, 0.08);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      font-size: 14px;
      letter-spacing: 0;
    }

    button, input, textarea, select { font: inherit; }

    button {
      min-height: 36px;
      border: 1px solid transparent;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 700;
      transition: background 120ms ease, border-color 120ms ease, color 120ms ease;
    }

    button:disabled { cursor: not-allowed; opacity: 0.6; }

    .shell {
      width: min(1440px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 22px 0;
    }

    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 16px;
    }

    h1 {
      margin: 0;
      font-size: 28px;
      line-height: 1.15;
      letter-spacing: 0;
    }

    .subtitle { margin: 5px 0 0; color: var(--muted); }

    .tabs, .toolbar, .actions {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }

    .tab {
      background: #ffffff;
      border-color: var(--line);
      color: var(--text);
      padding-inline: 12px;
    }

    .tab.active {
      background: var(--primary);
      border-color: var(--primary);
      color: #ffffff;
    }

    .secondary { background: #ffffff; border-color: var(--line); color: var(--text); }
    .secondary:hover { border-color: #9fb1b7; }
    .primary { background: var(--primary); color: #ffffff; }
    .primary:hover { background: var(--primary-dark); }
    .danger { background: var(--danger-soft); color: var(--danger); border-color: #ffd1c9; }

    .view { display: none; }
    .view.active { display: block; }

    .grid {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 420px;
      gap: 16px;
      align-items: start;
    }

    .stack { display: grid; gap: 16px; }

    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      overflow: hidden;
    }

    .panel-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 14px 16px;
      border-bottom: 1px solid var(--line);
      background: #fbfcfc;
    }

    .panel-title {
      margin: 0;
      font-size: 16px;
      line-height: 1.2;
    }

    .table-wrap { overflow-x: auto; }
    table { width: 100%; min-width: 920px; border-collapse: collapse; }
    th, td { padding: 12px 14px; text-align: left; border-bottom: 1px solid var(--line); vertical-align: middle; }
    th { color: var(--muted); font-size: 12px; text-transform: uppercase; background: #fbfcfc; }
    td.description { max-width: 320px; color: var(--muted); }
    .code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 13px; }
    .price { white-space: nowrap; font-variant-numeric: tabular-nums; font-weight: 800; }

    .status {
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 3px 8px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 800;
      white-space: nowrap;
    }

    .status.active { background: var(--ok-soft); color: var(--ok); }
    .status.inactive { background: #eef1f3; color: #697586; }
    .status.draft { background: var(--warn-soft); color: var(--warn); }

    .form {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      padding: 16px;
    }

    .form.full { grid-template-columns: 1fr; }
    .span-2 { grid-column: 1 / -1; }

    label {
      display: grid;
      gap: 6px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
    }

    input, textarea, select {
      width: 100%;
      min-height: 38px;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 8px 10px;
      color: var(--text);
      background: #ffffff;
    }

    textarea { min-height: 82px; resize: vertical; }
    input:focus, textarea:focus, select:focus { outline: 2px solid rgba(15, 118, 110, 0.18); border-color: var(--primary); }

    .check {
      display: flex;
      align-items: center;
      gap: 8px;
      min-height: 38px;
      padding: 8px 10px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fbfcfc;
    }

    .check input { width: 18px; min-height: 18px; }
    .form-actions { display: flex; justify-content: flex-end; gap: 8px; grid-column: 1 / -1; }
    .message { min-height: 20px; margin: 0; color: var(--muted); font-size: 13px; grid-column: 1 / -1; }
    .message.error { color: var(--danger); }
    .empty { padding: 28px 16px; color: var(--muted); text-align: center; }

    .detail {
      display: grid;
      gap: 12px;
      padding: 16px;
    }

    .kv {
      display: grid;
      grid-template-columns: 130px 1fr;
      gap: 8px;
      align-items: start;
    }

    .kv span:first-child { color: var(--muted); font-weight: 800; }
    .chips { display: flex; gap: 6px; flex-wrap: wrap; }
    .chip { border: 1px solid var(--line); border-radius: 999px; padding: 4px 8px; background: #fbfcfc; }

    @media (max-width: 1060px) {
      .grid { grid-template-columns: 1fr; }
    }

    @media (max-width: 720px) {
      .topbar, .panel-head { align-items: stretch; flex-direction: column; }
      .form { grid-template-columns: 1fr; }
      .form-actions button, .toolbar button, .tabs button { flex: 1; }
    }
  </style>
</head>
<body>
  <main class="shell">
    <header class="topbar">
      <div>
        <h1>CanTelcoX Product Catalog</h1>
        <p class="subtitle">Plans versionnes, promotions, add-ons, compatibilite et audit</p>
      </div>
      <div class="toolbar">
        <button class="secondary" id="refreshButton" type="button">Actualiser</button>
        <button class="primary" id="newPlanButton" type="button">Nouveau plan</button>
      </div>
    </header>

    <nav class="tabs" aria-label="Catalog sections">
      <button class="tab active" type="button" data-view="plansView">Plans</button>
      <button class="tab" type="button" data-view="promotionsView">Promotions</button>
      <button class="tab" type="button" data-view="addonsView">Add-ons</button>
      <button class="tab" type="button" data-view="rulesView">Compatibilite</button>
      <button class="tab" type="button" data-view="auditView">Audit</button>
    </nav>

    <p class="message" id="message"></p>

    <section class="view active" id="plansView">
      <div class="grid">
        <div class="stack">
          <section class="panel">
            <div class="panel-head">
              <h2 class="panel-title">Plans</h2>
              <label class="check">
                <input id="showInactive" type="checkbox" checked>
                Inclure inactifs
              </label>
            </div>
            <div class="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Code</th>
                    <th>Nom</th>
                    <th>Version</th>
                    <th>Prix</th>
                    <th>Donnees</th>
                    <th>Effet</th>
                    <th>Statut</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody id="plansBody"></tbody>
              </table>
              <div class="empty" id="plansEmpty" hidden>Aucun plan trouve.</div>
            </div>
          </section>

          <section class="panel">
            <div class="panel-head">
              <h2 class="panel-title">Versions precedentes</h2>
            </div>
            <div class="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Version</th>
                    <th>Description</th>
                    <th>Prix</th>
                    <th>Donnees</th>
                    <th>Periode</th>
                    <th>Statut</th>
                  </tr>
                </thead>
                <tbody id="versionsBody"></tbody>
              </table>
              <div class="empty" id="versionsEmpty">Selectionner un plan.</div>
            </div>
          </section>
        </div>

        <aside class="stack">
          <section class="panel">
            <div class="panel-head">
              <h2 class="panel-title" id="planFormTitle">Nouveau plan</h2>
            </div>
            <form class="form" id="planForm">
              <input id="planId" name="planId" type="hidden">
              <label>
                Code produit
                <input id="code" name="code" maxlength="80" required>
              </label>
              <label>
                Nom
                <input id="name" name="name" maxlength="120" required>
              </label>
              <label class="span-2">
                Description initiale
                <textarea id="description" name="description" maxlength="500" required></textarea>
              </label>
              <label>
                Prix mensuel
                <input id="monthly_price" name="monthly_price" type="number" min="0" step="0.01" required>
              </label>
              <label>
                Donnees incluses (GB)
                <input id="data_gb" name="data_gb" type="number" min="0" step="1" required>
              </label>
              <label>
                Date d'entree en vigueur
                <input id="effective_from" name="effective_from" type="date" required>
              </label>
              <label>
                Date de fin
                <input id="effective_to" name="effective_to" type="date">
              </label>
              <label>
                Statut version
                <select id="status" name="status">
                  <option>ACTIVE</option>
                  <option>DRAFT</option>
                  <option>RETIRED</option>
                </select>
              </label>
              <label class="check">
                <input id="unlimited_calls" name="unlimited_calls" type="checkbox" checked>
                Appels illimites
              </label>
              <label class="check">
                <input id="active" name="active" type="checkbox" checked>
                Plan actif
              </label>
              <div class="form-actions">
                <button class="secondary" type="button" id="cancelPlanButton">Annuler</button>
                <button class="primary" type="submit">Enregistrer</button>
              </div>
            </form>
          </section>

          <section class="panel">
            <div class="panel-head">
              <h2 class="panel-title">Nouvelle version</h2>
            </div>
            <form class="form full" id="versionForm">
              <label>
                Description
                <textarea id="version_description" name="description" maxlength="500" required></textarea>
              </label>
              <label>
                Prix mensuel
                <input id="version_monthly_price" name="monthly_price" type="number" min="0" step="0.01" required>
              </label>
              <label>
                Donnees incluses (GB)
                <input id="version_data_gb" name="data_gb" type="number" min="0" step="1" required>
              </label>
              <label>
                Date d'entree en vigueur
                <input id="version_effective_from" name="effective_from" type="date" required>
              </label>
              <label>
                Date de fin
                <input id="version_effective_to" name="effective_to" type="date">
              </label>
              <label>
                Statut
                <select id="version_status" name="status">
                  <option>ACTIVE</option>
                  <option>DRAFT</option>
                  <option>RETIRED</option>
                </select>
              </label>
              <label class="check">
                <input id="version_unlimited_calls" name="unlimited_calls" type="checkbox" checked>
                Appels illimites
              </label>
              <div class="form-actions">
                <button class="primary" type="submit" id="saveVersionButton" disabled>Creer version</button>
              </div>
            </form>
          </section>
        </aside>
      </div>
    </section>

    <section class="view" id="promotionsView">
      <div class="grid">
        <section class="panel">
          <div class="panel-head"><h2 class="panel-title">Promotions</h2></div>
          <div class="table-wrap">
            <table>
              <thead><tr><th>Nom</th><th>Type</th><th>Valeur</th><th>Periode</th><th>Statut</th></tr></thead>
              <tbody id="promotionsBody"></tbody>
            </table>
          </div>
        </section>
        <section class="panel">
          <div class="panel-head"><h2 class="panel-title">Nouvelle promotion</h2></div>
          <form class="form full" id="promotionForm">
            <label>Nom<input name="name" required maxlength="120"></label>
            <label>Description<textarea name="description" required maxlength="500"></textarea></label>
            <label>Type<select name="discount_type"><option>AMOUNT</option><option>PERCENTAGE</option><option>FREE_ACTIVATION</option></select></label>
            <label>Valeur<input name="discount_value" type="number" min="0" step="0.01" required></label>
            <label>Debut<input name="start_date" type="date" required></label>
            <label>Fin<input name="end_date" type="date"></label>
            <label class="check"><input name="active" type="checkbox" checked> Active</label>
            <div class="form-actions"><button class="primary" type="submit">Enregistrer</button></div>
          </form>
        </section>
      </div>
    </section>

    <section class="view" id="addonsView">
      <div class="grid">
        <section class="panel">
          <div class="panel-head"><h2 class="panel-title">Add-ons</h2></div>
          <div class="table-wrap">
            <table>
              <thead><tr><th>Code</th><th>Nom</th><th>Description</th><th>Prix</th><th>Statut</th></tr></thead>
              <tbody id="addonsBody"></tbody>
            </table>
          </div>
        </section>
        <section class="panel">
          <div class="panel-head"><h2 class="panel-title">Nouvel add-on</h2></div>
          <form class="form full" id="addonForm">
            <label>Code<input name="code" required maxlength="80"></label>
            <label>Nom<input name="name" required maxlength="120"></label>
            <label>Description<textarea name="description" required maxlength="500"></textarea></label>
            <label>Prix mensuel<input name="monthly_price" type="number" min="0" step="0.01" required></label>
            <label>Debut<input name="effective_from" type="date"></label>
            <label>Fin<input name="effective_to" type="date"></label>
            <label class="check"><input name="active" type="checkbox" checked> Actif</label>
            <div class="form-actions"><button class="primary" type="submit">Enregistrer</button></div>
          </form>
        </section>
      </div>
    </section>

    <section class="view" id="rulesView">
      <div class="grid">
        <section class="panel">
          <div class="panel-head"><h2 class="panel-title">Regles de compatibilite</h2></div>
          <div class="table-wrap">
            <table>
              <thead><tr><th>Source</th><th>Cible</th><th>Type</th></tr></thead>
              <tbody id="rulesBody"></tbody>
            </table>
          </div>
        </section>
        <section class="panel">
          <div class="panel-head"><h2 class="panel-title">Nouvelle regle</h2></div>
          <form class="form full" id="ruleForm">
            <label>Produit source<input name="source_product" required maxlength="80"></label>
            <label>Produit cible<input name="target_product" required maxlength="80"></label>
            <label>Type<select name="rule_type"><option>REQUIRES</option><option>EXCLUDES</option><option>OPTIONAL</option></select></label>
            <div class="form-actions"><button class="primary" type="submit">Enregistrer</button></div>
          </form>
        </section>
      </div>
    </section>

    <section class="view" id="auditView">
      <section class="panel">
        <div class="panel-head"><h2 class="panel-title">Historique des modifications</h2></div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Date</th><th>Entite</th><th>Action</th><th>Par</th><th>Nouvelle valeur</th></tr></thead>
            <tbody id="auditBody"></tbody>
          </table>
        </div>
      </section>
    </section>
  </main>

  <script>
    const api = "/v1/catalog";
    const message = document.querySelector("#message");
    const planForm = document.querySelector("#planForm");
    const versionForm = document.querySelector("#versionForm");
    const planFields = planForm.elements;
    const versionFields = versionForm.elements;
    const showInactive = document.querySelector("#showInactive");
    let plans = [];
    let selectedPlanId = "";

    function money(value) {
      return new Intl.NumberFormat("fr-CA", { style: "currency", currency: "CAD" }).format(value || 0);
    }

    function dateText(value) {
      return value ? new Intl.DateTimeFormat("fr-CA").format(new Date(`${value}T00:00:00`)) : "-";
    }

    function escapeHtml(value) {
      return String(value ?? "")
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

    function statusClass(status) {
      if (status === "ACTIVE" || status === true) return "active";
      if (status === "DRAFT") return "draft";
      return "inactive";
    }

    function jsonOrEmptyDate(formData, key) {
      return formData.get(key) || null;
    }

    async function request(path, options = {}) {
      const response = await fetch(`${api}${path}`, {
        ...options,
        headers: { "Content-Type": "application/json", "X-User": "catalog-admin-ui", ...(options.headers || {}) }
      });
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || "Operation impossible");
      }
      return response.json();
    }

    function planPayload() {
      return {
        code: planFields.code.value.trim(),
        name: planFields.name.value.trim(),
        description: planFields.description.value.trim(),
        monthly_price: Number(planFields.monthly_price.value),
        data_gb: Number.parseInt(planFields.data_gb.value, 10),
        unlimited_calls: planFields.unlimited_calls.checked,
        effective_from: planFields.effective_from.value,
        effective_to: planFields.effective_to.value || null,
        status: planFields.status.value,
        active: planFields.active.checked
      };
    }

    function versionPayload() {
      return {
        description: versionFields.description.value.trim(),
        monthly_price: Number(versionFields.monthly_price.value),
        data_gb: Number.parseInt(versionFields.data_gb.value, 10),
        unlimited_calls: versionFields.unlimited_calls.checked,
        effective_from: versionFields.effective_from.value,
        effective_to: versionFields.effective_to.value || null,
        status: versionFields.status.value
      };
    }

    function renderPlans() {
      const body = document.querySelector("#plansBody");
      body.innerHTML = "";
      document.querySelector("#plansEmpty").hidden = plans.length > 0;
      plans.forEach((plan) => {
        const version = plan.active_version || {};
        const row = document.createElement("tr");
        row.innerHTML = `
          <td class="code">${escapeHtml(plan.code)}</td>
          <td><strong>${escapeHtml(plan.name)}</strong></td>
          <td>v${version.version_number || "-"}</td>
          <td class="price">${money(version.monthly_price)}</td>
          <td>${version.data_gb ?? "-"} GB</td>
          <td>${dateText(version.effective_from)} - ${dateText(version.effective_to)}</td>
          <td><span class="status ${statusClass(plan.active)}">${plan.active ? "Actif" : "Inactif"}</span></td>
          <td>
            <div class="actions">
              <button class="secondary" type="button" data-action="select" data-id="${plan.id}">Ouvrir</button>
              <button class="danger" type="button" data-action="deactivate" data-id="${plan.id}" ${plan.active ? "" : "disabled"}>Desactiver</button>
            </div>
          </td>
        `;
        body.appendChild(row);
      });
    }

    function renderVersions(plan) {
      const body = document.querySelector("#versionsBody");
      const empty = document.querySelector("#versionsEmpty");
      body.innerHTML = "";
      if (!plan) {
        empty.hidden = false;
        empty.textContent = "Selectionner un plan.";
        return;
      }
      const versions = plan.previous_versions || [];
      empty.hidden = versions.length > 0;
      empty.textContent = "Aucune version precedente.";
      versions.forEach((version) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>v${version.version_number}</td>
          <td class="description">${escapeHtml(version.description)}</td>
          <td class="price">${money(version.monthly_price)}</td>
          <td>${version.data_gb} GB</td>
          <td>${dateText(version.effective_from)} - ${dateText(version.effective_to)}</td>
          <td><span class="status ${statusClass(version.status)}">${escapeHtml(version.status)}</span></td>
        `;
        body.appendChild(row);
      });
    }

    function selectPlan(planId) {
      const plan = plans.find((item) => item.id === planId);
      if (!plan) return;
      selectedPlanId = plan.id;
      const version = plan.active_version || {};
      planFields.planId.value = plan.id;
      planFields.code.value = plan.code;
      planFields.name.value = plan.name;
      planFields.description.value = version.description || "";
      planFields.monthly_price.value = version.monthly_price ?? "";
      planFields.data_gb.value = version.data_gb ?? "";
      planFields.effective_from.value = version.effective_from || "";
      planFields.effective_to.value = version.effective_to || "";
      planFields.status.value = version.status || "ACTIVE";
      planFields.unlimited_calls.checked = Boolean(version.unlimited_calls);
      planFields.active.checked = plan.active;
      document.querySelector("#planFormTitle").textContent = "Metadonnees du plan";

      versionFields.description.value = version.description || "";
      versionFields.monthly_price.value = version.monthly_price ?? "";
      versionFields.data_gb.value = version.data_gb ?? "";
      versionFields.effective_from.value = version.effective_from || "";
      versionFields.effective_to.value = version.effective_to || "";
      versionFields.status.value = "ACTIVE";
      versionFields.unlimited_calls.checked = Boolean(version.unlimited_calls);
      document.querySelector("#saveVersionButton").disabled = false;
      renderVersions(plan);
    }

    function resetPlanForm() {
      selectedPlanId = "";
      planForm.reset();
      versionForm.reset();
      planFields.planId.value = "";
      planFields.unlimited_calls.checked = true;
      planFields.active.checked = true;
      planFields.status.value = "ACTIVE";
      document.querySelector("#planFormTitle").textContent = "Nouveau plan";
      document.querySelector("#saveVersionButton").disabled = true;
      renderVersions(null);
      setMessage("");
    }

    async function loadPlans() {
      const activeOnly = showInactive.checked ? "false" : "true";
      plans = await request(`/plans?active_only=${activeOnly}`, { headers: {} });
      renderPlans();
      if (selectedPlanId) {
        const selected = plans.find((plan) => plan.id === selectedPlanId);
        renderVersions(selected);
      }
    }

    async function loadPromotions() {
      const promotions = await request("/promotions", { headers: {} });
      document.querySelector("#promotionsBody").innerHTML = promotions.map((promotion) => `
        <tr>
          <td><strong>${escapeHtml(promotion.name)}</strong></td>
          <td>${escapeHtml(promotion.discount_type)}</td>
          <td>${promotion.discount_value}</td>
          <td>${dateText(promotion.start_date)} - ${dateText(promotion.end_date)}</td>
          <td><span class="status ${statusClass(promotion.active)}">${promotion.active ? "Active" : "Inactive"}</span></td>
        </tr>
      `).join("");
    }

    async function loadAddons() {
      const addons = await request("/addons", { headers: {} });
      document.querySelector("#addonsBody").innerHTML = addons.map((addon) => `
        <tr>
          <td class="code">${escapeHtml(addon.code)}</td>
          <td><strong>${escapeHtml(addon.name)}</strong></td>
          <td class="description">${escapeHtml(addon.description)}</td>
          <td class="price">${money(addon.monthly_price)}</td>
          <td><span class="status ${statusClass(addon.active)}">${addon.active ? "Actif" : "Inactif"}</span></td>
        </tr>
      `).join("");
    }

    async function loadRules() {
      const rules = await request("/compatibility-rules", { headers: {} });
      document.querySelector("#rulesBody").innerHTML = rules.map((rule) => `
        <tr>
          <td class="code">${escapeHtml(rule.source_product)}</td>
          <td class="code">${escapeHtml(rule.target_product)}</td>
          <td>${escapeHtml(rule.rule_type)}</td>
        </tr>
      `).join("");
    }

    async function loadAudit() {
      const logs = await request("/audit-logs", { headers: {} });
      document.querySelector("#auditBody").innerHTML = logs.slice(0, 80).map((log) => `
        <tr>
          <td>${new Intl.DateTimeFormat("fr-CA", { dateStyle: "short", timeStyle: "short" }).format(new Date(log.timestamp))}</td>
          <td>${escapeHtml(log.entity_type)}<br><span class="code">${escapeHtml(log.entity_id)}</span></td>
          <td>${escapeHtml(log.action)}</td>
          <td>${escapeHtml(log.performed_by)}</td>
          <td class="description"><pre>${escapeHtml(JSON.stringify(log.new_value, null, 2))}</pre></td>
        </tr>
      `).join("");
    }

    async function loadAll() {
      await Promise.all([loadPlans(), loadPromotions(), loadAddons(), loadRules(), loadAudit()]);
    }

    planForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      try {
        if (planFields.planId.value) {
          await request(`/plans/${planFields.planId.value}`, {
            method: "PUT",
            body: JSON.stringify({
              code: planFields.code.value.trim(),
              name: planFields.name.value.trim(),
              active: planFields.active.checked
            })
          });
          setMessage("Metadonnees du plan enregistrees.");
        } else {
          await request("/plans", { method: "POST", body: JSON.stringify(planPayload()) });
          resetPlanForm();
          setMessage("Plan cree.");
        }
        await loadAll();
      } catch (error) {
        setMessage(error.message, true);
      }
    });

    versionForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!selectedPlanId) return;
      try {
        await request(`/plans/${selectedPlanId}/versions`, { method: "POST", body: JSON.stringify(versionPayload()) });
        setMessage("Nouvelle version creee.");
        await loadAll();
        selectPlan(selectedPlanId);
      } catch (error) {
        setMessage(error.message, true);
      }
    });

    document.querySelector("#plansBody").addEventListener("click", async (event) => {
      const button = event.target.closest("button[data-action]");
      if (!button) return;
      try {
        if (button.dataset.action === "select") {
          selectPlan(button.dataset.id);
        }
        if (button.dataset.action === "deactivate") {
          await request(`/plans/${button.dataset.id}`, { method: "DELETE" });
          setMessage("Plan desactive.");
          await loadAll();
        }
      } catch (error) {
        setMessage(error.message, true);
      }
    });

    function simpleFormHandler(selector, path, mapper, reload) {
      document.querySelector(selector).addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        try {
          await request(path, { method: "POST", body: JSON.stringify(mapper(formData)) });
          event.currentTarget.reset();
          setMessage("Enregistrement effectue.");
          await reload();
          await loadAudit();
        } catch (error) {
          setMessage(error.message, true);
        }
      });
    }

    simpleFormHandler("#promotionForm", "/promotions", (data) => ({
      name: data.get("name"),
      description: data.get("description"),
      discount_type: data.get("discount_type"),
      discount_value: Number(data.get("discount_value")),
      start_date: data.get("start_date"),
      end_date: jsonOrEmptyDate(data, "end_date"),
      active: data.get("active") === "on"
    }), loadPromotions);

    simpleFormHandler("#addonForm", "/addons", (data) => ({
      code: data.get("code"),
      name: data.get("name"),
      description: data.get("description"),
      monthly_price: Number(data.get("monthly_price")),
      effective_from: jsonOrEmptyDate(data, "effective_from"),
      effective_to: jsonOrEmptyDate(data, "effective_to"),
      active: data.get("active") === "on"
    }), loadAddons);

    simpleFormHandler("#ruleForm", "/compatibility-rules", (data) => ({
      source_product: data.get("source_product"),
      target_product: data.get("target_product"),
      rule_type: data.get("rule_type")
    }), loadRules);

    document.querySelectorAll(".tab").forEach((button) => {
      button.addEventListener("click", () => {
        document.querySelectorAll(".tab").forEach((item) => item.classList.toggle("active", item === button));
        document.querySelectorAll(".view").forEach((view) => view.classList.toggle("active", view.id === button.dataset.view));
      });
    });

    document.querySelector("#refreshButton").addEventListener("click", () => loadAll().catch((error) => setMessage(error.message, true)));
    document.querySelector("#newPlanButton").addEventListener("click", resetPlanForm);
    document.querySelector("#cancelPlanButton").addEventListener("click", resetPlanForm);
    showInactive.addEventListener("change", loadPlans);

    loadAll().catch((error) => setMessage(error.message, true));
  </script>
</body>
</html>
"""

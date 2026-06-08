const data = {
  evidence: [
    {
      level: "green",
      title: "Suppression protected revenue in high-fatigue users",
      detail: "Holdout users generated 4.1% less revenue than Pulse-suppressed users.",
      value: "$184k protected"
    },
    {
      level: "amber",
      title: "Onboarding step 3 is over-sending",
      detail: "Push plus WhatsApp overlap creates 2.8 contacts in 24h for 31% of new users.",
      value: "$22k leakage"
    },
    {
      level: "red",
      title: "Claim-settlement detractors are receiving acquisition journeys",
      detail: "NPS-negative users are still entering insurance purchase nudges.",
      value: "18k users"
    }
  ],
  journeys: [
    {
      name: "Onboarding step 1",
      segment: "New users, D0",
      sendPressure: 42,
      incrementalValue: 76,
      fatigueLift: 18,
      action: "Keep push. Remove duplicate email for low-intent users."
    },
    {
      name: "Onboarding step 3",
      segment: "Activated, no order",
      sendPressure: 86,
      incrementalValue: 22,
      fatigueLift: 71,
      action: "Suppress WhatsApp if push was ignored in last 12h."
    },
    {
      name: "Cart reminder",
      segment: "High intent",
      sendPressure: 64,
      incrementalValue: 68,
      fatigueLift: 37,
      action: "Send only when trust score is above 0.55."
    },
    {
      name: "Winback offer",
      segment: "Dormant",
      sendPressure: 58,
      incrementalValue: 31,
      fatigueLift: 62,
      action: "Replace discount with content for low receptiveness users."
    }
  ],
  conflicts: [
    {
      user: "U-49321",
      journeys: "Cart reminder, Category promo, Loyalty upsell",
      state: "High intent, high fatigue",
      recommendation: "Suppress all except cart reminder tomorrow 20:30",
      value: "$3.20"
    },
    {
      user: "U-88201",
      journeys: "Insurance purchase, Renewal nudge",
      state: "Low trust after claim settlement",
      recommendation: "Suppress acquisition journey. Route to service recovery.",
      value: "$8.70 protected"
    },
    {
      user: "U-10448",
      journeys: "Welcome, First order, Referral",
      state: "Passive browser",
      recommendation: "Send content. Avoid offer until readiness improves.",
      value: "$0.42"
    }
  ],
  users: [
    {
      id: "A",
      name: "Food delivery new user",
      state: "high_intent_high_fatigue",
      action: "suppress",
      confidence: "0.87",
      rationale: "High purchase readiness but current communication fatigue is too high. Suppression has higher expected value than another product recommendation.",
      counterfactuals: {
        suppress: 18.28,
        send_product_recommendation: 14.22,
        send_content: 5.31
      }
    },
    {
      id: "B",
      name: "Insuretech claim detractor",
      state: "low_trust_high_fatigue",
      action: "service_recovery",
      confidence: "0.82",
      rationale: "Recent poor claim experience lowers trust. Acquisition messaging is likely to damage retention; recovery intervention wins.",
      counterfactuals: {
        service_recovery: 22.40,
        suppress: 17.10,
        send_purchase_nudge: 4.80
      }
    },
    {
      id: "C",
      name: "Low intent loyal user",
      state: "balanced_state",
      action: "send_content",
      confidence: "0.79",
      rationale: "User has high trust but low purchase readiness. Educational content preserves engagement better than a discount.",
      counterfactuals: {
        send_content: 7.82,
        suppress: 5.20,
        send_discount_offer: 4.70
      }
    }
  ],
  holdout: [
    { label: "Pulse", value: 118, max: 130 },
    { label: "Control", value: 100, max: 130 },
    { label: "Static journey", value: 91, max: 130 }
  ]
};

const viewTitles = {
  cockpit: "Decision Cockpit",
  oversend: "Over-send Diagnosis",
  suppression: "Suppression Economics",
  conflicts: "Journey Collision Monitor",
  users: "User Intervention Queue"
};

function initNavigation() {
  document.querySelectorAll(".nav-item").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".nav-item").forEach((item) => item.classList.remove("active"));
      document.querySelectorAll(".view").forEach((view) => view.classList.remove("active"));
      button.classList.add("active");
      document.getElementById(button.dataset.view).classList.add("active");
      document.getElementById("viewTitle").textContent = viewTitles[button.dataset.view];
    });
  });
}

function renderEvidence() {
  const target = document.getElementById("evidenceList");
  target.innerHTML = data.evidence.map((item) => `
    <article class="evidence-item">
      <span class="severity ${item.level}"></span>
      <div>
        <strong>${item.title}</strong>
        <p>${item.detail}</p>
      </div>
      <span class="tag">${item.value}</span>
    </article>
  `).join("");
}

function progressClass(value) {
  if (value > 75) return "red";
  if (value > 55) return "amber";
  return "";
}

function renderJourneys() {
  const target = document.getElementById("journeyTable");
  target.innerHTML = data.journeys.map((row) => `
    <article class="journey-row">
      <div>
        <div class="row-title">${row.name}</div>
        <div class="row-sub">${row.segment}</div>
      </div>
      ${metricBar("Send pressure", row.sendPressure)}
      ${metricBar("Incremental value", row.incrementalValue)}
      ${metricBar("Fatigue lift", row.fatigueLift)}
      <div><span class="pill">Pulse action</span><p>${row.action}</p></div>
    </article>
  `).join("");
}

function metricBar(label, value) {
  return `
    <div>
      <div class="bar-meta"><span>${label}</span><strong>${value}</strong></div>
      <div class="progress ${progressClass(value)}"><span style="width:${value}%"></span></div>
    </div>
  `;
}

function renderSuppression() {
  const fatigue = Number(document.getElementById("fatigueSlider").value) / 100;
  const value = Number(document.getElementById("valueSlider").value) / 100;
  const suppressed = Math.round((fatigue - 0.42) * 870000);
  const saved = Math.round(suppressed * value * 0.18);
  const risk = Math.max(3, Math.round((0.86 - fatigue) * 28));

  document.getElementById("fatigueValue").textContent = fatigue.toFixed(2);
  document.getElementById("valueValue").textContent = `$${value.toFixed(2)}`;
  document.getElementById("simulationOutput").innerHTML = `
    <div class="sim-stat"><span class="muted">Messages suppressed</span><strong>${suppressed.toLocaleString()}</strong></div>
    <div class="sim-stat"><span class="muted">Budget saved</span><strong>$${saved.toLocaleString()}</strong></div>
    <div class="sim-stat"><span class="muted">Revenue risk</span><strong>${risk}%</strong></div>
  `;
}

function renderHoldout() {
  const target = document.getElementById("holdoutBars");
  target.innerHTML = data.holdout.map((row) => `
    <div class="bar-row">
      <div class="bar-meta"><span>${row.label}</span><strong>${row.value}</strong></div>
      <div class="progress"><span style="width:${(row.value / row.max) * 100}%"></span></div>
    </div>
  `).join("");
}

function renderConflicts() {
  const target = document.getElementById("conflictList");
  target.innerHTML = data.conflicts.map((item) => `
    <article class="conflict-item">
      <div><strong>${item.user}</strong><p>${item.journeys}</p></div>
      <div><span class="pill">${item.state}</span></div>
      <div>${item.recommendation}</div>
      <strong>${item.value}</strong>
    </article>
  `).join("");
}

function renderUsers(selectedId = "A") {
  const list = document.getElementById("userList");
  list.innerHTML = data.users.map((user) => `
    <button class="user-item ${user.id === selectedId ? "active" : ""}" data-user="${user.id}">
      <strong>${user.name}</strong>
      <span class="user-meta"><span>${user.state}</span><span>${user.confidence}</span></span>
      <span class="pill">${user.action}</span>
    </button>
  `).join("");
  list.querySelectorAll(".user-item").forEach((button) => {
    button.addEventListener("click", () => renderUsers(button.dataset.user));
  });
  renderDecisionDetail(data.users.find((user) => user.id === selectedId));
}

function renderDecisionDetail(user) {
  const best = user.action;
  const target = document.getElementById("decisionDetail");
  const facts = Object.entries(user.counterfactuals).map(([action, value]) => `
    <div class="counterfactual ${action === best ? "best" : ""}">
      <span class="muted">${action}</span>
      <strong>${value}</strong>
    </div>
  `).join("");

  document.getElementById("decisionTitle").textContent = `Decision Evidence: User ${user.id}`;
  target.innerHTML = `
    <div class="decision-block">
      <span class="pill">Recommended action</span>
      <h2>${user.action}</h2>
      <p>${user.rationale}</p>
    </div>
    <div class="counterfactual-grid">${facts}</div>
  `;
}

function bindControls() {
  document.getElementById("fatigueSlider").addEventListener("input", renderSuppression);
  document.getElementById("valueSlider").addEventListener("input", renderSuppression);
  document.getElementById("goalSelect").addEventListener("change", (event) => {
    const mode = event.target.value;
    const values = {
      revenue: ["$418k", "93%", "$71k", "22%"],
      retention: ["$392k", "96%", "$54k", "28%"],
      roi: ["$447k", "91%", "$83k", "31%"]
    }[mode];
    ["incrementalRevenue", "suppressionSafety", "budgetLeakage", "commsReduction"].forEach((id, index) => {
      document.getElementById(id).textContent = values[index];
    });
  });
}

function init() {
  initNavigation();
  renderEvidence();
  renderJourneys();
  renderSuppression();
  renderHoldout();
  renderConflicts();
  renderUsers();
  bindControls();
}

init();

const loginPanel = document.querySelector("#login");
const loginForm = document.querySelector("#login-form");
const loginError = document.querySelector("#login-error");
const chatForm = document.querySelector("#chat-form");
const messageInput = document.querySelector("#message-input");
const messageList = document.querySelector("#messages");
const sendButton = document.querySelector("#send-button");
const statusText = document.querySelector("#status");
const accessCodeInput = document.querySelector("#access-code");
let token = localStorage.getItem("cofounder-chat-token") || "";
let newestMessageId = 0;
let polling = false;

const personaLabels = {
  orchestrator: "Orchestrator",
  business: "Business",
  cto: "CTO",
  ai_lead: "AI Lead",
  governance: "Governance",
  product: "Product",
  developer: "Developer",
  leads: "Leads & Growth",
  ba_agent: "Business Analyst",
};

function showLogin() {
  loginPanel.hidden = false;
  chatForm.hidden = true;
  messageList.hidden = true;
}

function showChat() {
  loginPanel.hidden = true;
  chatForm.hidden = false;
  messageList.hidden = false;
}

function addMessage(message) {
  const welcome = messageList.querySelector(".welcome");
  if (welcome) welcome.remove();

  const item = document.createElement("article");
  item.className = `message ${message.role}`;

  const label = document.createElement("p");
  label.className = "message-label";
  label.textContent = message.role === "user"
    ? "You"
    : `${personaLabels[message.agent_key] || "Orchestrator"} · Agent`;

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";
  bubble.textContent = message.content;

  const contentUpper = message.content.toUpperCase();
  const needsApproval =
    message.role === "assistant" &&
    (contentUpper.includes("FOUNDER APPROVAL REQUIRED") ||
      contentUpper.includes("TIER 3") ||
      contentUpper.includes("HUMAN APPROVAL REQUIRED"));

  const alreadyApproved =
    message.role === "assistant" &&
    (contentUpper.includes("APPROVED BY FOUNDER") ||
      contentUpper.includes("FOUNDER APPROVAL DECISION RECORDED"));

  if (alreadyApproved) {
    const badge = document.createElement("div");
    badge.className = "approved-badge-card";
    badge.innerHTML = '<span>🛡️</span><span>Verified: Founder Approval Granted &amp; Logged</span>';
    bubble.appendChild(badge);
  } else if (needsApproval) {
    const card = document.createElement("div");
    card.className = "approval-card";
    card.innerHTML = `
      <div class="approval-card-header">
        <span class="warning-badge">🚨 TIER 3 GOVERNANCE GATE</span>
        <span class="approval-status-pill">Pending Founder Sign-off</span>
      </div>
      <p class="approval-card-title">Human-in-the-Loop checkpoint: Requires explicit Founder Approval to proceed.</p>
      <div class="approval-actions">
        <button id="inline-approve-${message.id}" class="btn-inline-approve" type="button">
          ✓ Approve as Founder
        </button>
        <button id="inline-open-gate-${message.id}" class="btn-inline-spec" type="button">
          🛡️ Open Founder Gate
        </button>
      </div>
    `;

    const inlineApproveBtn = card.querySelector(".btn-inline-approve");
    inlineApproveBtn.addEventListener("click", async () => {
      inlineApproveBtn.disabled = true;
      inlineApproveBtn.textContent = "Recording...";
      try {
        await submitFounderApproval("Patient records & AI clinical diagnostics for medical clinics", "approved");
        card.innerHTML = `
          <div class="approved-badge-card" style="margin: 0;">
            <span>🛡️</span><span>✅ Approved by Founder! HITL protocol active.</span>
          </div>
        `;
        await refreshMessages();
      } catch (err) {
        inlineApproveBtn.disabled = false;
        inlineApproveBtn.textContent = "✕ Error (Retry)";
      }
    });

    const openGateBtn = card.querySelector(".btn-inline-spec");
    openGateBtn.addEventListener("click", () => {
      const gateBtn = document.querySelector("#founder-gate-btn");
      if (gateBtn) gateBtn.click();
    });

    bubble.appendChild(card);
  }

  item.append(label, bubble);
  messageList.append(item);
  messageList.scrollTop = messageList.scrollHeight;
  newestMessageId = Math.max(newestMessageId, Number(message.id));
}

async function request(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    if (response.status === 401) {
      token = "";
      localStorage.removeItem("cofounder-chat-token");
      showLogin();
    }
    throw new Error(body.detail || "The request could not be completed.");
  }
  return body;
}

async function refreshMessages() {
  if (!token || polling) return;
  polling = true;
  try {
    const query = newestMessageId ? `?after_id=${newestMessageId}` : "";
    const messages = await request(`/api/messages${query}`);
    messages.forEach(addMessage);
    if (!messageList.children.length) {
      messageList.innerHTML = '<div class="welcome"><div class="welcome-icon" aria-hidden="true">✦</div><h3>Good to see you</h3><p>Ask a question, explore an idea, or pick a co-founder persona. Your messages sync with the other devices using this chat.</p></div>';
    }
    statusText.textContent = "";
  } catch (error) {
    statusText.textContent = error.message;
  } finally {
    polling = false;
  }
}

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  loginError.textContent = "";
  try {
    const result = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ access_code: accessCodeInput.value }),
    });
    const body = await result.json().catch(() => ({}));
    if (!result.ok) throw new Error(body.detail || "Could not log in.");
    token = body.token;
    localStorage.setItem("cofounder-chat-token", token);
    newestMessageId = 0;
    messageList.replaceChildren();
    showChat();
    await refreshMessages();
    messageInput.focus();
  } catch (error) {
    loginError.textContent = error.message;
  }
});

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = messageInput.value.trim();
  if (!message || sendButton.disabled) return;

  sendButton.disabled = true;
  statusText.textContent = "Your co-founder is thinking…";
  try {
    await request("/api/messages", {
      method: "POST",
      body: JSON.stringify({
        message,
        agent_key: document.querySelector("#agent").value,
      }),
    });
    messageInput.value = "";
    await refreshMessages();
  } catch (error) {
    statusText.textContent = error.message;
  } finally {
    sendButton.disabled = false;
    messageInput.focus();
  }
});

// Founder Approval Handlers
const founderGateBtn = document.querySelector("#founder-gate-btn");
const founderModal = document.querySelector("#founder-modal");
const btnCloseModal = document.querySelector("#btn-close-modal");
const btnGrantApproval = document.querySelector("#btn-grant-approval");
const btnRejectApproval = document.querySelector("#btn-reject-approval");
const approvalProjectInput = document.querySelector("#approval-project");
const approvalNotesInput = document.querySelector("#approval-notes");
const founderFeedback = document.querySelector("#founder-feedback");

async function submitFounderApproval(projectName, decision = "approved", notes = "") {
  return await request("/api/approve-founder", {
    method: "POST",
    body: JSON.stringify({
      project_name: projectName,
      decision,
      notes,
    }),
  });
}

if (founderGateBtn && founderModal) {
  founderGateBtn.addEventListener("click", () => {
    if (founderFeedback) {
      founderFeedback.textContent = "";
      founderFeedback.className = "founder-feedback";
    }
    if (typeof founderModal.showModal === "function") {
      founderModal.showModal();
    } else {
      founderModal.setAttribute("open", "");
    }
  });
}

if (btnCloseModal && founderModal) {
  btnCloseModal.addEventListener("click", () => {
    if (typeof founderModal.close === "function") {
      founderModal.close();
    } else {
      founderModal.removeAttribute("open");
    }
  });
}

if (btnGrantApproval) {
  btnGrantApproval.addEventListener("click", async () => {
    const project = (approvalProjectInput && approvalProjectInput.value.trim()) || "Patient records & AI clinical diagnostics for medical clinics";
    const notes = approvalNotesInput ? approvalNotesInput.value.trim() : "";
    btnGrantApproval.disabled = true;
    if (founderFeedback) {
      founderFeedback.textContent = "Recording Founder Approval...";
      founderFeedback.className = "founder-feedback";
    }
    try {
      await submitFounderApproval(project, "approved", notes);
      if (founderFeedback) {
        founderFeedback.textContent = "✓ Founder Approval granted & logged to memory/governance.md!";
      }
      setTimeout(() => {
        if (founderModal && typeof founderModal.close === "function") founderModal.close();
        btnGrantApproval.disabled = false;
        refreshMessages();
      }, 1100);
    } catch (err) {
      if (founderFeedback) {
        founderFeedback.textContent = err.message || "Failed to record approval.";
        founderFeedback.className = "founder-feedback error";
      }
      btnGrantApproval.disabled = false;
    }
  });
}

if (btnRejectApproval) {
  btnRejectApproval.addEventListener("click", async () => {
    const project = (approvalProjectInput && approvalProjectInput.value.trim()) || "Patient records & AI clinical diagnostics for medical clinics";
    const notes = approvalNotesInput ? approvalNotesInput.value.trim() : "";
    btnRejectApproval.disabled = true;
    if (founderFeedback) {
      founderFeedback.textContent = "Recording rejection...";
      founderFeedback.className = "founder-feedback error";
    }
    try {
      await submitFounderApproval(project, "rejected", notes);
      if (founderFeedback) {
        founderFeedback.textContent = "✕ Action marked as Rejected/Hold by Founder.";
      }
      setTimeout(() => {
        if (founderModal && typeof founderModal.close === "function") founderModal.close();
        btnRejectApproval.disabled = false;
        refreshMessages();
      }, 1100);
    } catch (err) {
      if (founderFeedback) {
        founderFeedback.textContent = err.message || "Failed to record decision.";
        founderFeedback.className = "founder-feedback error";
      }
      btnRejectApproval.disabled = false;
    }
  });
}

if (token) {
  showChat();
  refreshMessages();
} else {
  showLogin();
}
window.setInterval(refreshMessages, 2000);

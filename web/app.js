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

if (token) {
  showChat();
  refreshMessages();
} else {
  showLogin();
}
window.setInterval(refreshMessages, 2000);

/**
 * DraftMate AI: Legal Intelligence Studio
 * Harvey.ai Design System — White/Zinc, Newsreader Serif, Inter Sans
 * All classes match the Tailwind config in index.html (harvey.* tokens)
 */

const state = {
  activeModel: "claude-3-5-sonnet",
  activeModelName: "Claude 3.5 Sonnet",
  activeModelBadge: "Advanced",
  activeSkillTag: null,
  activeSkillName: null,
  attachedDocs: [],
  selectedDocsForAttachment: [],
  currentDraftText: "",
  originalComparisonText: "",
  sampleDocs: [],
  higurumaChatHistory: [],
  speechRecognition: null,
  pendingSafetyToken: null,
  isRecordingVoice: false
};

// --- Initialization ---
document.addEventListener("DOMContentLoaded", async () => {
  await loadModels();
  await loadSampleMatters();
  setupSpeechRecognition();
});

// --- API Helpers ---
async function apiPost(endpoint, data) {
  try {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `HTTP Error ${res.status}`);
    }
    return await res.json();
  } catch (error) {
    console.error(`Error in ${endpoint}:`, error);
    showHarveyToast(error.message || "Execution failed", "error");
    throw error;
  }
}

async function apiGet(endpoint) {
  try {
    const res = await fetch(endpoint);
    if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
    return await res.json();
  } catch (error) {
    console.error(`Error in ${endpoint}:`, error);
    throw error;
  }
}

// --- Models ---
async function loadModels() {
  try {
    const models = await apiGet("/api/chat/models");
    const container = document.getElementById("modelOptionsList");
    if (!container) return;

    container.innerHTML = models.map(m => `
      <button onclick="selectModel('${m.id}', '${m.name}', '${m.badge}')"
        class="w-full text-left px-3 py-2.5 rounded-lg text-xs hover:bg-harvey-surface transition-colors flex items-center justify-between group ${state.activeModel === m.id ? 'bg-harvey-surface text-harvey-text font-semibold' : 'text-harvey-muted'}">
        <div>
          <div class="font-medium text-harvey-text text-[13px]">${m.name}</div>
          <div class="text-[11px] text-harvey-subtle leading-tight mt-0.5">${m.description}</div>
        </div>
        <span class="text-[9px] font-mono uppercase tracking-wider text-harvey-subtle border border-harvey-border px-1.5 py-0.5 rounded">${m.badge}</span>
      </button>
    `).join("");
  } catch (e) {
    console.warn("Using default models");
  }
}

function toggleModelDropdown() {
  const dd = document.getElementById("modelDropdown");
  if (dd) dd.classList.toggle("hidden");
}

function selectModel(id, name, badge) {
  state.activeModel = id;
  state.activeModelName = name;
  state.activeModelBadge = badge;

  const label = document.getElementById("activeModelLabel");
  if (label) label.textContent = name;
  toggleModelDropdown();
  showHarveyToast(`Engine switched to ${name}`, "info");
}

document.addEventListener("click", (e) => {
  const btn = document.getElementById("modelSelectBtn");
  const dd = document.getElementById("modelDropdown");
  if (btn && dd && !btn.contains(e.target) && !dd.contains(e.target)) {
    dd.classList.add("hidden");
  }
});

// --- 5 Core Workflows ---
function setWorkflow(tag, name) {
  state.activeSkillTag = tag;
  state.activeSkillName = name;

  const input = document.getElementById("promptInput");
  if (input) {
    if (!input.value.includes(tag)) {
      input.value = `${tag} ${input.value}`.trim() + " ";
    }
    input.focus();
  }

  // Highlight active chip — uses zinc border + black text
  document.querySelectorAll(".workflow-chip").forEach(btn => {
    if (btn.textContent.includes(tag)) {
      btn.classList.add("border-harvey-dark", "text-harvey-dark", "bg-harvey-surface", "font-semibold");
      btn.classList.remove("text-harvey-muted");
    } else {
      btn.classList.remove("border-harvey-dark", "text-harvey-dark", "bg-harvey-surface", "font-semibold");
      btn.classList.add("text-harvey-muted");
    }
  });

  updateAttachedTags();
  showHarveyToast(`Active Workflow: ${name}`, "info");
}

function selectSkill(tag, name) {
  setWorkflow(tag, name);
}

// --- Document Upload & Ingestion (Microsoft MarkItDown) ---
async function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  showHarveyToast(`Parsing ${file.name} via Microsoft MarkItDown...`, "info");
  try {
    const res = await fetch("/api/documents/upload", {
      method: "POST",
      body: formData
    });
    const data = await res.json();
    state.attachedDocs.push({
      filename: data.filename,
      markdown: data.markdown,
      metadata: data.metadata
    });
    updateAttachedTags();
    showHarveyToast(`Structured ${file.name} into legal Markdown.`, "success");
  } catch (e) {
    showHarveyToast(`Ingestion error: ${e.message}`, "error");
  }
}

async function loadSampleMatters() {
  try {
    const docs = await apiGet("/api/documents/samples");
    state.sampleDocs = docs;
  } catch (e) {}
}

function updateAttachedTags() {
  const container = document.getElementById("attachedTagsContainer");
  if (!container) return;

  let html = "";

  // Active skill tag — black pill
  if (state.activeSkillTag) {
    html += `
      <span class="inline-flex items-center gap-1.5 bg-harvey-dark text-white px-2.5 py-1 rounded-lg text-[11px] font-mono font-medium">
        <span>&bull; ${state.activeSkillName}</span>
        <button onclick="clearActiveSkill()" class="hover:opacity-60 ml-0.5 font-bold leading-none">&times;</button>
      </span>
    `;
  }

  // Attached document tags — zinc surface
  state.attachedDocs.forEach((d, i) => {
    html += `
      <span class="inline-flex items-center gap-1.5 bg-harvey-card border border-harvey-border text-harvey-muted px-2.5 py-1 rounded-lg text-[11px] font-mono">
        <span>ATTACHMENT: ${d.filename}</span>
        <button onclick="removeAttachedDoc(${i})" class="hover:text-harvey-dark ml-0.5 font-bold leading-none">&times;</button>
      </span>
    `;
  });

  container.innerHTML = html;
}

function clearActiveSkill() {
  state.activeSkillTag = null;
  state.activeSkillName = null;
  document.querySelectorAll(".workflow-chip").forEach(b => {
    b.classList.remove("border-harvey-dark", "text-harvey-dark", "bg-harvey-surface", "font-semibold");
    b.classList.add("text-harvey-muted");
  });
  updateAttachedTags();
}

function removeAttachedDoc(idx) {
  state.attachedDocs.splice(idx, 1);
  updateAttachedTags();
}

// --- Main Legal Drafting Execution ---
async function executeDrafting() {
  const input = document.getElementById("promptInput");
  const prompt = input.value.trim();
  if (!prompt) {
    showHarveyToast("Please enter drafting instructions or select a workflow.", "warning");
    input.focus();
    return;
  }

  const btn = document.getElementById("sendDraftBtn");
  btn.disabled = true;
  btn.innerHTML = `<span class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin inline-block"></span><span>Drafting...</span>`;

  showHarveyToast("Synthesizing legal instrument with Headroom token conservation...", "info");

  const learnStyle = document.getElementById("learnStyleToggle")?.checked;
  let refStyleText = null;
  if (learnStyle && state.attachedDocs.length > 0) {
    refStyleText = state.attachedDocs[0].markdown;
  }

  try {
    const payload = {
      prompt: prompt,
      model_id: state.activeModel,
      skill_tag: state.activeSkillTag,
      context_docs: state.attachedDocs,
      reference_style_text: refStyleText,
      optimize_tokens: true
    };

    const res = await apiPost("/api/chat/draft", payload);

    state.currentDraftText = res.draft;
    state.originalComparisonText = state.attachedDocs.length > 0 ? state.attachedDocs[0].markdown : res.draft;

    displayDraftingStudio(res);
    showHarveyToast("Instrument synthesized and citations audited.", "success");
  } catch (e) {
    showHarveyToast("Drafting error: " + e.message, "error");
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<span>Draft Instrument</span><i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>`;
    lucide.createIcons();
  }
}

function displayDraftingStudio(res) {
  const container = document.getElementById("studioOutputContainer");
  container.classList.remove("hidden");
  container.scrollIntoView({ behavior: "smooth" });

  // 1. Render Document
  document.getElementById("renderedDraftView").innerHTML = renderMarkdown(res.draft);

  // 2. Headroom Telemetry
  const hBadge = document.getElementById("headroomSavingsBadge");
  const hText = document.getElementById("headroomSavingsText");
  if (res.headroom_metrics && res.headroom_metrics.tokens_saved > 0) {
    hBadge.classList.remove("hidden");
    hBadge.classList.add("inline-flex");
    hText.textContent = `Headroom: ${res.headroom_metrics.reduction_percentage} saved (${res.headroom_metrics.tokens_saved} tokens)`;
  } else {
    hBadge.classList.add("hidden");
  }

  // 3. Citations
  renderCitations(res.citation_audit);

  // 4. Redlines
  renderRedlineDiff();

  switchStudioTab("draft");
}

// --- Markdown Renderer (Harvey light theme) ---
function renderMarkdown(md) {
  if (!md) return "";
  let html = md
    .replace(/^### (.*$)/gim, '<h3 class="font-serif text-base font-semibold text-harvey-dark mt-5 mb-1.5 border-b border-harvey-border pb-1 tracking-tight">$1</h3>')
    .replace(/^## (.*$)/gim, '<h2 class="font-serif text-xl font-normal text-harvey-dark mt-7 mb-2.5 tracking-tight">$1</h2>')
    .replace(/^# (.*$)/gim, '<h1 class="font-serif text-3xl font-normal text-harvey-dark mt-3 mb-5 tracking-tight">$1</h1>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong class="font-semibold text-harvey-dark">$1</strong>')
    .replace(/\*(.*?)\*/gim, '<em class="italic text-harvey-muted">$1</em>')
    .replace(/^> (.*$)/gim, '<blockquote class="border-l-2 border-harvey-dark pl-4 py-2 my-3 text-harvey-dark bg-harvey-surface font-serif italic rounded-r-lg">$1</blockquote>')
    .replace(/\n\n/gim, '</p><p class="my-3 leading-relaxed text-harvey-muted font-normal text-sm">')
    .replace(/\n/gim, '<br>');
  return `<p class="leading-relaxed text-harvey-muted font-normal text-sm">${html}</p>`;
}

// --- Citation Verification Desk ---
function renderCitations(audit) {
  if (!audit) return;

  const countBadge = document.getElementById("citationCountBadge");
  if (countBadge) countBadge.textContent = audit.total_citations;

  const header = document.getElementById("citationSummaryHeader");
  if (header) {
    const scoreColor = audit.integrity_score >= 80 ? "text-harvey-green" : "text-harvey-amber";
    const guardBg = audit.guardrail_status === "SECURE"
      ? "bg-harvey-greenBg text-harvey-green border border-harvey-greenBorder"
      : "bg-harvey-redBg text-harvey-red border border-harvey-redBorder";

    header.innerHTML = `
      <div>
        <div class="flex items-center gap-2">
          <span class="font-serif text-sm font-semibold text-harvey-dark">Authority Audit:</span>
          <span class="font-mono font-bold text-sm ${scoreColor}">${audit.integrity_score}%</span>
          <span class="text-[9px] uppercase font-mono font-semibold px-2 py-0.5 rounded-md ${guardBg}">
            ${audit.guardrail_status}
          </span>
        </div>
        <p class="text-harvey-muted text-[11px] mt-0.5">${audit.summary}</p>
      </div>
      <div class="flex items-center gap-2 text-[10px] font-mono">
        <span class="px-2 py-1 bg-harvey-greenBg text-harvey-green border border-harvey-greenBorder rounded-md">${audit.verified_count} VERIFIED</span>
        <span class="px-2 py-1 bg-harvey-amberBg text-harvey-amber border border-harvey-amberBorder rounded-md">${audit.partially_verified_count} PARTIAL</span>
        <span class="px-2 py-1 bg-harvey-redBg text-harvey-red border border-harvey-redBorder rounded-md">${audit.unverified_count} FLAGGED</span>
      </div>
    `;
  }

  const container = document.getElementById("citationCardsList");
  if (!container) return;

  if (audit.citations.length === 0) {
    container.innerHTML = `<div class="p-8 text-center text-harvey-muted text-sm font-serif italic">No statutory citations or case law precedents detected in this draft.</div>`;
    return;
  }

  container.innerHTML = audit.citations.map(c => {
    const isVerified = c.status === "verified";
    const isPartial = c.status === "partially_verified";

    const badgeClass = isVerified
      ? "bg-harvey-greenBg text-harvey-green border border-harvey-greenBorder"
      : isPartial
        ? "bg-harvey-amberBg text-harvey-amber border border-harvey-amberBorder"
        : "bg-harvey-redBg text-harvey-red border border-harvey-redBorder";

    return `
      <div class="p-5 bg-white rounded-xl border border-harvey-border space-y-3 hover:shadow-sm transition-shadow">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2.5">
            <span class="text-[9px] font-mono font-bold px-2 py-0.5 rounded-md uppercase tracking-wider ${badgeClass}">
              ${c.badge}
            </span>
            <span class="font-serif font-semibold text-sm text-harvey-dark">${c.authority_title}</span>
          </div>
          <span class="text-[11px] text-harvey-subtle font-mono">${c.year || ''}</span>
        </div>

        <div class="text-xs text-harvey-dark font-mono bg-harvey-surface p-2.5 rounded-lg border border-harvey-border">
          &ldquo;${c.citation_text}&rdquo;
        </div>

        <p class="text-xs text-harvey-muted leading-relaxed">${c.summary || c.notes}</p>

        <div class="flex items-center justify-between pt-2 border-t border-harvey-border text-[11px]">
          <span class="text-harvey-muted">Reporter: <strong class="text-harvey-dark">${c.court || 'Official Gazette'}</strong></span>
          ${c.source_url
            ? `<a href="${c.source_url}" target="_blank" rel="noopener noreferrer" class="text-harvey-dark hover:underline flex items-center gap-1 font-semibold text-[11px]"><span>View Official Record</span> &rarr;</a>`
            : `<span class="text-harvey-red font-mono text-[10px] font-semibold">Guardrail Alert: Not in official archive</span>`
          }
        </div>
      </div>
    `;
  }).join("");
}

// --- Redline Diff Viewer ---
async function renderRedlineDiff() {
  const container = document.getElementById("redlineLinesContainer");
  if (!container) return;

  try {
    const res = await apiPost("/api/chat/redline", {
      original_text: state.originalComparisonText || state.currentDraftText,
      revised_text: state.currentDraftText
    });

    if (res.structured_diff.length === 0) {
      container.innerHTML = `<div class="text-center py-6 text-harvey-muted font-serif italic text-sm">No redline variances detected.</div>`;
      return;
    }

    container.innerHTML = res.structured_diff.map(d => {
      if (d.type === "addition") {
        return `<div class="bg-harvey-greenBg text-harvey-green p-2 rounded-lg border-l-2 border-harvey-green text-xs font-mono">+ ${escapeHtml(d.text)}</div>`;
      } else if (d.type === "deletion") {
        return `<div class="bg-harvey-redBg text-harvey-red p-2 rounded-lg border-l-2 border-harvey-red line-through text-xs font-mono">- ${escapeHtml(d.text)}</div>`;
      } else {
        return `<div class="text-harvey-subtle py-0.5 text-xs font-mono">&nbsp;&nbsp;${escapeHtml(d.text)}</div>`;
      }
    }).join("");
  } catch (e) {}
}

function escapeHtml(text) {
  return (text || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function applyRedlinesNotice() {
  showHarveyToast("All redline revisions locked into master instrument.", "success");
}

// --- Studio Tab Switcher ---
function switchStudioTab(tab) {
  ["Draft", "Citations", "Redline"].forEach(t => {
    const btn = document.getElementById(`tab${t}Btn`);
    const content = document.getElementById(`tabContent${t}`);
    if (!btn || !content) return;

    if (t.toLowerCase() === tab) {
      // Active tab: white bg, black text, subtle border, slight shadow
      btn.className = "px-4 py-1.5 rounded-lg text-xs font-semibold bg-white text-harvey-dark border border-harvey-border shadow-sm transition-all";
      content.classList.remove("hidden");
    } else {
      // Inactive tab: muted text, no bg
      btn.className = "px-4 py-1.5 rounded-lg text-xs font-medium text-harvey-muted hover:text-harvey-dark transition-colors";
      content.classList.add("hidden");
    }
  });
}

// --- Hiromi Higuruma Chamber Drawer ---
function toggleHigurumaChamber() {
  const drawer = document.getElementById("higurumaChamberDrawer");
  if (drawer) drawer.classList.toggle("hidden");
}

function askHigurumaQuick(promptText) {
  const input = document.getElementById("higurumaMessageInput");
  if (input) {
    input.value = promptText;
    sendHigurumaMessage(new Event("submit"));
  }
}

async function sendHigurumaMessage(event) {
  if (event) event.preventDefault();
  const input = document.getElementById("higurumaMessageInput");
  const msg = input.value.trim();
  if (!msg) return;

  const thread = document.getElementById("higurumaChatThread");

  // User bubble — right-aligned, zinc surface
  const userBubble = document.createElement("div");
  userBubble.className = "bg-harvey-surface border border-harvey-border rounded-xl p-3 text-right text-harvey-dark text-xs ml-8";
  userBubble.innerHTML = `<span class="font-mono text-harvey-subtle text-[10px] uppercase font-bold block mb-1">INQUIRY:</span>${escapeHtml(msg)}`;
  thread.appendChild(userBubble);
  input.value = "";
  thread.scrollTop = thread.scrollHeight;

  // Typing indicator — white card
  const loadingBubble = document.createElement("div");
  loadingBubble.className = "bg-white border border-harvey-border rounded-xl p-3 text-harvey-muted text-xs mr-8 italic animate-pulse";
  loadingBubble.innerHTML = "Higuruma is weighing the evidentiary burden against statutory provisions...";
  thread.appendChild(loadingBubble);
  thread.scrollTop = thread.scrollHeight;

  try {
    const res = await apiPost("/api/higuruma/chat", {
      message: msg,
      active_draft: state.currentDraftText || null,
      chat_history: state.higurumaChatHistory
    });

    loadingBubble.remove();

    const higurumaBubble = document.createElement("div");
    higurumaBubble.className = "bg-white border border-harvey-border rounded-xl p-4 space-y-3 mr-3 text-xs";
    higurumaBubble.innerHTML = `
      <div class="flex items-center justify-between text-harvey-dark font-serif font-semibold text-sm border-b border-harvey-border pb-2">
        <div class="flex items-center gap-2">
          <span>⚖️</span>
          <span>${res.speaker}</span>
          <span class="text-[9px] font-mono text-harvey-subtle">日車寛見</span>
        </div>
        <span class="text-[9px] bg-harvey-surface text-harvey-dark border border-harvey-border px-1.5 py-0.5 rounded font-mono uppercase font-bold">${res.domain_state}</span>
      </div>
      <div class="text-harvey-dark leading-relaxed space-y-2">
        ${renderMarkdown(res.response)}
      </div>
      ${res.tactical_recommendation ? `
        <div class="mt-3 pt-2.5 border-t border-harvey-border flex items-center justify-between">
          <span class="text-[10px] text-harvey-muted font-serif italic">Remedial clause formulated.</span>
          <button onclick="insertHigurumaRecommendation('${escapeHtml(res.tactical_recommendation)}')"
            class="bg-black hover:bg-zinc-800 text-white font-semibold px-3 py-1 rounded-lg text-[10px] uppercase tracking-wider transition-colors">
            Incorporate into Studio
          </button>
        </div>
      ` : ''}
    `;
    thread.appendChild(higurumaBubble);
    thread.scrollTop = thread.scrollHeight;

    state.higurumaChatHistory.push({ role: "user", content: msg });
    state.higurumaChatHistory.push({ role: "assistant", content: res.response });

  } catch (e) {
    loadingBubble.remove();
    showHarveyToast("Higuruma response error: " + e.message, "error");
  }
}

function insertHigurumaRecommendation(clauseText) {
  const input = document.getElementById("promptInput");
  if (input) {
    input.value += `\n[Higuruma Amendment]: ${clauseText}`;
    input.focus();
    showHarveyToast("Higuruma's clause placed in prompt chamber.", "success");
    document.getElementById("studio")?.scrollIntoView({ behavior: "smooth" });
  }
}

// --- Voice Dictation ---
function openVoiceModal() {
  document.getElementById("voiceModal").classList.remove("hidden");
  startSpeechCapture();
}

function closeVoiceModal() {
  stopSpeechCapture();
  document.getElementById("voiceModal").classList.add("hidden");
}

function setupSpeechRecognition() {
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRec) {
    const recognition = new SpeechRec();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    recognition.onresult = (event) => {
      let interim = "";
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        interim += event.results[i][0].transcript;
      }
      const display = document.getElementById("voiceTranscriptDisplay");
      if (display) display.textContent = `"${interim}"`;
    };

    state.speechRecognition = recognition;
  }
}

function startSpeechCapture() {
  state.isRecordingVoice = true;
  if (state.speechRecognition) {
    try { state.speechRecognition.start(); } catch (e) {}
  }
}

function stopSpeechCapture() {
  state.isRecordingVoice = false;
  if (state.speechRecognition) {
    try { state.speechRecognition.stop(); } catch (e) {}
  }
}

function simulateVoice(phrase) {
  document.getElementById("voiceTranscriptDisplay").textContent = `"${phrase}"`;
  setTimeout(() => {
    closeVoiceModal();
    executeSpokenCommand(phrase);
  }, 400);
}

function processVoiceInput() {
  const display = document.getElementById("voiceTranscriptDisplay");
  const text = display.textContent.replace(/['"]/g, "").trim();
  closeVoiceModal();

  if (text && !text.includes("Listening for spoken")) {
    executeSpokenCommand(text);
  }
}

async function executeSpokenCommand(transcript) {
  showHarveyToast(`Voice Agent: "${transcript}"`, "info");
  try {
    const res = await apiPost("/api/voice/parse", { transcript });

    if (res.status === "confirmation_required") {
      openSafetyModal(res.safety, res.recognized_text);
      return;
    }

    if (res.action === "activate_skill") {
      setWorkflow(res.skill_tag, res.skill_tag.replace("@", ""));
      showHarveyToast(res.feedback, "success");
    } else if (res.action === "verify_citations") {
      switchStudioTab("citations");
      showHarveyToast(res.feedback, "success");
    } else {
      const input = document.getElementById("promptInput");
      input.value = `${input.value} ${res.recognized_text}`.trim();
      showHarveyToast("Dictated speech inserted into prompt dock.", "info");
    }
  } catch (e) {}
}

// --- Consequential Action Safety Modal ---
function openSafetyModal(safety, text) {
  state.pendingSafetyToken = safety.token;
  document.getElementById("safetyTitle").textContent = safety.title;
  document.getElementById("safetyDesc").textContent = safety.description;
  document.getElementById("safetyDetail").textContent = `Command: "${text}"`;
  document.getElementById("safetyModal").classList.remove("hidden");
}

function closeSafetyModal() {
  state.pendingSafetyToken = null;
  document.getElementById("safetyModal").classList.add("hidden");
}

async function confirmSafetyAction() {
  if (!state.pendingSafetyToken) return;
  try {
    const res = await apiPost("/api/voice/safety/confirm", { token: state.pendingSafetyToken });
    closeSafetyModal();
    showHarveyToast(res.message, "success");
  } catch (e) {
    showHarveyToast("Safety authorization error: " + e.message, "error");
  }
}

// --- Exports ---
function exportMarkdown() {
  if (!state.currentDraftText) return;
  downloadBlob(new Blob([state.currentDraftText], { type: "text/markdown" }), "DraftMate_Legal_Instrument.md");
  showHarveyToast("Exported legal instrument as Markdown (.md)", "success");
}

function exportDocx() {
  if (!state.currentDraftText) return;
  downloadBlob(new Blob([state.currentDraftText], { type: "application/msword" }), "DraftMate_Legal_Instrument.doc");
  showHarveyToast("Exported legal instrument as Word (.doc)", "success");
}

function copyDraftText() {
  if (!state.currentDraftText) return;
  navigator.clipboard.writeText(state.currentDraftText);
  showHarveyToast("Instrument copied to clipboard.", "success");
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// --- Toast Notifications (Harvey light theme) ---
function showHarveyToast(message, type = "info") {
  const old = document.getElementById("harveyToast");
  if (old) old.remove();

  const toast = document.createElement("div");
  toast.id = "harveyToast";

  // Color coding: left border accent only, white card background
  const accentClass = type === "success"
    ? "border-l-4 border-l-harvey-green"
    : type === "error"
      ? "border-l-4 border-l-harvey-red"
      : type === "warning"
        ? "border-l-4 border-l-harvey-amber"
        : "border-l-4 border-l-harvey-dark";

  toast.className = `fixed bottom-6 left-6 z-[9999] bg-white border border-harvey-border ${accentClass} px-4 py-3 rounded-xl shadow-lg text-xs font-medium flex items-center gap-2.5 transition-all duration-300 font-sans max-w-sm`;

  const dotColor = type === "success" ? "bg-harvey-green" : type === "error" ? "bg-harvey-red" : type === "warning" ? "bg-harvey-amber" : "bg-harvey-dark";
  toast.innerHTML = `<span class="w-1.5 h-1.5 rounded-full ${dotColor} flex-shrink-0"></span><span class="text-harvey-dark">${message}</span>`;
  document.body.appendChild(toast);

  // Fade out after 4s
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(8px)";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

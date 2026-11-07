/**
 * DraftMate AI — Legal Intelligence Studio
 * Harvey.ai design system: warm off-white #F2F0ED, near-black ink, Newsreader serif
 * All Tailwind tokens match index.html config (harvey.*)
 */

const state = {
  activeModel: "claude-3-5-sonnet",
  activeModelName: "Claude 3.5 Sonnet",
  activeModelBadge: "Advanced",
  activeSkillTag:  null,
  activeSkillName: null,
  attachedDocs: [],
  currentDraftText: "",
  originalComparisonText: "",
  sampleDocs: [],
  higurumaChatHistory: [],
  speechRecognition: null,
  pendingSafetyToken: null,
  isRecordingVoice: false,
  higuramaOpen: false
};

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", async () => {
  await loadModels();
  await loadSampleMatters();
  setupSpeechRecognition();
  lucide.createIcons();
});

// ── API helpers ───────────────────────────────────────────────────────────────
async function apiPost(endpoint, data) {
  try {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }
    return await res.json();
  } catch (error) {
    console.error(`[apiPost] ${endpoint}:`, error);
    showToast(error.message || "Request failed", "error");
    throw error;
  }
}

async function apiGet(endpoint) {
  try {
    const res = await fetch(endpoint);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (error) {
    console.error(`[apiGet] ${endpoint}:`, error);
    throw error;
  }
}

// ── Model selector ────────────────────────────────────────────────────────────
async function loadModels() {
  try {
    const models = await apiGet("/api/chat/models");
    const container = document.getElementById("modelOptionsList");
    if (!container) return;

    container.innerHTML = models.map(m => `
      <button onclick="selectModel('${m.id}', '${m.name}', '${m.badge}')"
        class="w-full text-left px-4 py-2.5 text-[13px] hover:bg-harvey-bg transition-colors flex items-center justify-between ${state.activeModel === m.id ? 'text-harvey-ink font-medium' : 'text-harvey-inkMuted'}">
        <div>
          <div class="font-medium text-harvey-ink">${m.name}</div>
          <div class="text-[11px] text-harvey-muted mt-0.5">${m.description}</div>
        </div>
        <span class="text-[9px] font-mono uppercase tracking-wider text-harvey-subtle border border-harvey-rule px-1.5 py-0.5 rounded-sm ml-3">${m.badge}</span>
      </button>
    `).join("");
  } catch (e) {
    console.warn("Model list unavailable — using defaults");
  }
}

function toggleModelDropdown() {
  document.getElementById("modelDropdown")?.classList.toggle("hidden");
}

function selectModel(id, name, badge) {
  state.activeModel     = id;
  state.activeModelName = name;
  state.activeModelBadge = badge;
  const label = document.getElementById("activeModelLabel");
  if (label) label.textContent = name;
  toggleModelDropdown();
  showToast(`Engine: ${name}`, "info");
}

// Close model dropdown on outside click
document.addEventListener("click", e => {
  const btn = document.getElementById("modelSelectBtn");
  const dd  = document.getElementById("modelDropdown");
  if (btn && dd && !btn.contains(e.target) && !dd.contains(e.target)) {
    dd.classList.add("hidden");
  }
});

// ── Workflow chips ────────────────────────────────────────────────────────────
function setWorkflow(tag, name) {
  state.activeSkillTag  = tag;
  state.activeSkillName = name;

  const input = document.getElementById("promptInput");
  if (input && !input.value.includes(tag)) {
    input.value = `${tag} ${input.value}`.trim() + " ";
    input.focus();
  }

  // Active chip: black border + ink text
  document.querySelectorAll(".workflow-chip").forEach(btn => {
    const isActive = btn.textContent.trim() === name ||
                     btn.getAttribute("onclick")?.includes(tag);
    if (isActive) {
      btn.classList.add("border-harvey-ink", "text-harvey-ink", "bg-harvey-bgAlt");
      btn.classList.remove("text-harvey-inkMuted");
    } else {
      btn.classList.remove("border-harvey-ink", "text-harvey-ink", "bg-harvey-bgAlt");
      btn.classList.add("text-harvey-inkMuted");
    }
  });

  updateAttachedTags();
  showToast(`Workflow: ${name}`, "info");
}

function selectSkill(tag, name) { setWorkflow(tag, name); }

function clearActiveSkill() {
  state.activeSkillTag  = null;
  state.activeSkillName = null;
  document.querySelectorAll(".workflow-chip").forEach(b => {
    b.classList.remove("border-harvey-ink", "text-harvey-ink", "bg-harvey-bgAlt");
    b.classList.add("text-harvey-inkMuted");
  });
  updateAttachedTags();
}

function removeAttachedDoc(idx) {
  state.attachedDocs.splice(idx, 1);
  updateAttachedTags();
}

function updateAttachedTags() {
  const container = document.getElementById("attachedTagsContainer");
  if (!container) return;
  let html = "";

  if (state.activeSkillTag) {
    html += `
      <span class="inline-flex items-center gap-1.5 bg-harvey-ink text-harvey-bg px-2.5 py-1 rounded-sm text-[11px] font-mono font-medium">
        <span>${state.activeSkillName}</span>
        <button onclick="clearActiveSkill()" class="hover:opacity-60 leading-none font-bold">&times;</button>
      </span>`;
  }

  state.attachedDocs.forEach((d, i) => {
    html += `
      <span class="inline-flex items-center gap-1.5 bg-harvey-bg border border-harvey-rule text-harvey-inkMuted px-2.5 py-1 rounded-sm text-[11px] font-mono">
        <i data-lucide="file-text" class="w-3 h-3"></i>
        <span>${d.filename}</span>
        <button onclick="removeAttachedDoc(${i})" class="hover:text-harvey-ink leading-none font-bold">&times;</button>
      </span>`;
  });

  container.innerHTML = html;
  lucide.createIcons();
}

// ── Document upload ───────────────────────────────────────────────────────────
async function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  showToast(`Parsing ${file.name} via MarkItDown…`, "info");
  try {
    const res  = await fetch("/api/documents/upload", { method: "POST", body: formData });
    const data = await res.json();
    state.attachedDocs.push({ filename: data.filename, markdown: data.markdown, metadata: data.metadata });
    updateAttachedTags();
    showToast(`Structured ${file.name} → Markdown`, "success");
  } catch (e) {
    showToast(`Ingestion error: ${e.message}`, "error");
  }
}

async function loadSampleMatters() {
  try {
    state.sampleDocs = await apiGet("/api/documents/samples");
  } catch (e) {}
}

// ── Main drafting ─────────────────────────────────────────────────────────────
async function executeDrafting() {
  const input  = document.getElementById("promptInput");
  const prompt = input.value.trim();
  if (!prompt) {
    showToast("Enter drafting instructions or select a workflow.", "warning");
    input.focus();
    return;
  }

  const btn = document.getElementById("sendDraftBtn");
  btn.disabled = true;
  btn.innerHTML = `
    <span class="w-3.5 h-3.5 border-2 border-harvey-bg border-t-transparent rounded-full animate-spin"></span>
    <span>Drafting…</span>`;

  showToast("Synthesising with Headroom token optimisation…", "info");

  const learnStyle = document.getElementById("learnStyleToggle")?.checked;
  const refStyle   = (learnStyle && state.attachedDocs.length > 0) ? state.attachedDocs[0].markdown : null;

  try {
    const res = await apiPost("/api/chat/draft", {
      prompt:               prompt,
      model_id:             state.activeModel,
      skill_tag:            state.activeSkillTag,
      context_docs:         state.attachedDocs,
      reference_style_text: refStyle,
      optimize_tokens:      true
    });

    state.currentDraftText        = res.draft;
    state.originalComparisonText  = state.attachedDocs.length > 0 ? state.attachedDocs[0].markdown : res.draft;

    displayDraftingStudio(res);
    showToast("Instrument synthesised. Citations audited.", "success");
  } catch (e) {
    // error already shown by apiPost
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<span>Draft Instrument</span><i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>`;
    lucide.createIcons();
  }
}

function displayDraftingStudio(res) {
  const container = document.getElementById("studioOutputContainer");
  container.classList.remove("hidden");
  container.scrollIntoView({ behavior: "smooth", block: "start" });

  document.getElementById("renderedDraftView").innerHTML = renderMarkdown(res.draft);

  const hBadge = document.getElementById("headroomSavingsBadge");
  const hText  = document.getElementById("headroomSavingsText");
  if (res.headroom_metrics?.tokens_saved > 0) {
    hBadge.classList.remove("hidden");
    hBadge.classList.add("inline-flex");
    hText.textContent = `Headroom: ${res.headroom_metrics.reduction_percentage} saved (${res.headroom_metrics.tokens_saved} tk)`;
  } else {
    hBadge.classList.add("hidden");
  }

  renderCitations(res.citation_audit);
  renderRedlineDiff();
  switchStudioTab("draft");
}

// ── Markdown renderer (warm off-white theme) ──────────────────────────────────
function renderMarkdown(md) {
  if (!md) return "";
  const html = md
    .replace(/^### (.*$)/gim, '<h3 class="font-serif text-base font-medium text-harvey-ink mt-5 mb-1.5 border-b border-harvey-rule pb-1 tracking-tight">$1</h3>')
    .replace(/^## (.*$)/gim,  '<h2 class="font-serif text-xl font-light text-harvey-ink mt-7 mb-2.5 tracking-tight">$1</h2>')
    .replace(/^# (.*$)/gim,   '<h1 class="font-serif text-3xl font-light text-harvey-ink mt-3 mb-5 tracking-tight">$1</h1>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong class="font-semibold text-harvey-ink">$1</strong>')
    .replace(/\*(.*?)\*/gim,     '<em class="italic text-harvey-inkMuted">$1</em>')
    .replace(/^> (.*$)/gim,      '<blockquote class="border-l-2 border-harvey-ink pl-4 py-2 my-3 text-harvey-inkMuted bg-harvey-bg font-serif italic rounded-r-sm">$1</blockquote>')
    .replace(/\n\n/gim, '</p><p class="my-3 leading-relaxed text-harvey-inkMuted text-[14px]">')
    .replace(/\n/gim, "<br>");
  return `<p class="leading-relaxed text-harvey-inkMuted text-[14px]">${html}</p>`;
}

// ── Citation rendering ────────────────────────────────────────────────────────
function renderCitations(audit) {
  if (!audit) return;

  const badge = document.getElementById("citationCountBadge");
  if (badge) badge.textContent = audit.total_citations;

  const header = document.getElementById("citationSummaryHeader");
  if (header) {
    const scoreColor = audit.integrity_score >= 80 ? "text-harvey-green" : "text-harvey-amber";
    const guardClass = audit.guardrail_status === "SECURE"
      ? "bg-harvey-greenBg text-harvey-green border-harvey-greenBorder"
      : "bg-harvey-redBg text-harvey-red border-harvey-redBorder";

    header.innerHTML = `
      <div>
        <div class="flex items-center gap-2.5">
          <span class="dm-serif text-sm font-medium text-harvey-ink">Authority Audit</span>
          <span class="font-mono font-bold text-sm ${scoreColor}">${audit.integrity_score}%</span>
          <span class="text-[9px] uppercase font-mono font-semibold px-2 py-0.5 rounded-sm border ${guardClass}">${audit.guardrail_status}</span>
        </div>
        <p class="text-harvey-muted text-[12px] mt-1">${audit.summary}</p>
      </div>
      <div class="flex items-center gap-2 text-[10px] font-mono flex-wrap">
        <span class="px-2 py-1 bg-harvey-greenBg text-harvey-green border border-harvey-greenBorder rounded-sm">${audit.verified_count} VERIFIED</span>
        <span class="px-2 py-1 bg-harvey-amberBg text-harvey-amber border border-harvey-amberBorder rounded-sm">${audit.partially_verified_count} PARTIAL</span>
        <span class="px-2 py-1 bg-harvey-redBg text-harvey-red border border-harvey-redBorder rounded-sm">${audit.unverified_count} FLAGGED</span>
      </div>`;
  }

  const list = document.getElementById("citationCardsList");
  if (!list) return;

  if (!audit.citations.length) {
    list.innerHTML = `<div class="py-8 text-center text-harvey-muted text-sm font-serif italic">No statutory citations or case law precedents detected in this draft.</div>`;
    return;
  }

  list.innerHTML = audit.citations.map(c => {
    const cls = c.status === "verified"
      ? "badge-verified"
      : c.status === "partially_verified"
        ? "badge-partial"
        : "badge-unverified";

    return `
      <div class="p-5 bg-harvey-white rounded-sm border border-harvey-rule space-y-2.5 hover:border-harvey-border transition-colors">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2.5">
            <span class="text-[9px] font-mono font-bold px-2 py-0.5 rounded-sm uppercase tracking-wider border ${cls}">${c.badge}</span>
            <span class="dm-serif font-medium text-sm text-harvey-ink">${c.authority_title}</span>
          </div>
          <span class="text-[11px] text-harvey-subtle font-mono">${c.year || ""}</span>
        </div>
        <div class="text-[12px] text-harvey-inkMuted font-mono bg-harvey-bg p-2.5 rounded-sm border border-harvey-rule">
          &ldquo;${c.citation_text}&rdquo;
        </div>
        <p class="text-[12px] text-harvey-muted leading-relaxed">${c.summary || c.notes}</p>
        <div class="flex items-center justify-between pt-2 border-t border-harvey-rule text-[11px]">
          <span class="text-harvey-muted">Reporter: <strong class="text-harvey-inkMuted">${c.court || "Official Gazette"}</strong></span>
          ${c.source_url
            ? `<a href="${c.source_url}" target="_blank" rel="noopener noreferrer" class="text-harvey-ink hover:underline underline-offset-2 font-medium">View Record &rarr;</a>`
            : `<span class="text-harvey-red font-mono text-[10px]">Not in official archive</span>`}
        </div>
      </div>`;
  }).join("");
}

// ── Redline diff ──────────────────────────────────────────────────────────────
async function renderRedlineDiff() {
  const container = document.getElementById("redlineLinesContainer");
  if (!container) return;

  try {
    const res = await apiPost("/api/chat/redline", {
      original_text: state.originalComparisonText || state.currentDraftText,
      revised_text:  state.currentDraftText
    });

    if (!res.structured_diff?.length) {
      container.innerHTML = `<div class="text-center py-6 text-harvey-muted font-serif italic text-sm">No redline variances detected.</div>`;
      return;
    }

    container.innerHTML = res.structured_diff.map(d => {
      if (d.type === "addition") {
        return `<div class="bg-harvey-greenBg text-harvey-green p-1.5 rounded-sm border-l-2 border-harvey-green">+ ${escHtml(d.text)}</div>`;
      } else if (d.type === "deletion") {
        return `<div class="bg-harvey-redBg text-harvey-red p-1.5 rounded-sm border-l-2 border-harvey-red line-through">- ${escHtml(d.text)}</div>`;
      }
      return `<div class="text-harvey-subtle py-0.5">&nbsp;&nbsp;${escHtml(d.text)}</div>`;
    }).join("");
  } catch (e) {}
}

function escHtml(t) {
  return (t || "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

function applyRedlinesNotice() {
  showToast("All redline revisions locked into master instrument.", "success");
}

// ── Studio tabs ───────────────────────────────────────────────────────────────
function switchStudioTab(tab) {
  ["Draft","Citations","Redline"].forEach(t => {
    const btn     = document.getElementById(`tab${t}Btn`);
    const content = document.getElementById(`tabContent${t}`);
    if (!btn || !content) return;

    if (t.toLowerCase() === tab) {
      btn.className = "px-3.5 py-1.5 rounded-sm text-[12px] font-medium bg-harvey-white text-harvey-ink border border-harvey-rule transition-colors";
      content.classList.remove("hidden");
    } else {
      btn.className = "px-3.5 py-1.5 rounded-sm text-[12px] font-medium text-harvey-muted hover:text-harvey-ink transition-colors";
      content.classList.add("hidden");
    }
  });
}

// ── Higuruma Chamber ──────────────────────────────────────────────────────────
function toggleHigurumaChamber() {
  const drawer = document.getElementById("higurumaChamberDrawer");
  if (!drawer) return;
  state.higuramaOpen = !state.higuramaOpen;
  if (state.higuramaOpen) {
    drawer.classList.add("open");
  } else {
    drawer.classList.remove("open");
  }
}

function askHigurumaQuick(promptText) {
  if (!state.higuramaOpen) toggleHigurumaChamber();
  const input = document.getElementById("higurumaMessageInput");
  if (input) {
    input.value = promptText;
    sendHigurumaMessage(new Event("submit"));
  }
}

async function sendHigurumaMessage(event) {
  if (event) event.preventDefault();
  const input = document.getElementById("higurumaMessageInput");
  const msg   = input?.value.trim();
  if (!msg) return;

  const thread = document.getElementById("higurumaChatThread");

  // User bubble
  const userBubble = document.createElement("div");
  userBubble.className = "bg-harvey-bg border border-harvey-rule rounded-sm p-3 text-right text-harvey-ink text-[12px] ml-10";
  userBubble.innerHTML = `
    <span class="font-mono text-harvey-subtle text-[10px] uppercase block mb-1">Inquiry</span>
    ${escHtml(msg)}`;
  thread.appendChild(userBubble);
  input.value = "";
  thread.scrollTop = thread.scrollHeight;

  // Loading
  const loadBubble = document.createElement("div");
  loadBubble.className = "bg-harvey-white border border-harvey-rule rounded-sm p-3 text-harvey-muted text-[12px] mr-10 italic animate-pulse";
  loadBubble.textContent = "Higuruma is evaluating the evidentiary record…";
  thread.appendChild(loadBubble);
  thread.scrollTop = thread.scrollHeight;

  try {
    const res = await apiPost("/api/higuruma/chat", {
      message:      msg,
      active_draft: state.currentDraftText || null,
      chat_history: state.higurumaChatHistory
    });

    loadBubble.remove();

    const bubble = document.createElement("div");
    bubble.className = "bg-harvey-white border border-harvey-rule rounded-sm p-4 space-y-3 mr-3 text-[12px]";
    bubble.innerHTML = `
      <div class="flex items-center justify-between border-b border-harvey-rule pb-2">
        <div class="flex items-center gap-2">
          <svg class="w-3.5 h-3.5 text-harvey-inkMuted" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18M5 6l7-3 7 3M5 18H2l3-9M19 18h3l-3-9M2 18h20"/></svg>
          <span class="dm-serif text-[13px] font-medium text-harvey-ink">${res.speaker}</span>
          <span class="text-[9px] font-mono text-harvey-muted">日車寛見</span>
        </div>
        <span class="text-[9px] bg-harvey-bg text-harvey-inkMuted border border-harvey-rule px-1.5 py-0.5 rounded-sm font-mono uppercase">${res.domain_state}</span>
      </div>
      <div class="text-harvey-inkMuted leading-relaxed">
        ${renderMarkdown(res.response)}
      </div>
      ${res.tactical_recommendation ? `
        <div class="pt-2.5 border-t border-harvey-rule flex items-center justify-between">
          <span class="text-[11px] text-harvey-muted font-serif italic">Remedial clause ready.</span>
          <button onclick="insertHigurumaRecommendation('${escHtml(res.tactical_recommendation)}')"
            class="bg-harvey-ink hover:bg-harvey-dark text-harvey-bg font-medium px-3 py-1.5 rounded-sm text-[11px] uppercase tracking-wide transition-colors">
            Incorporate
          </button>
        </div>` : ""}`;

    thread.appendChild(bubble);
    thread.scrollTop = thread.scrollHeight;

    state.higurumaChatHistory.push({ role: "user",      content: msg });
    state.higurumaChatHistory.push({ role: "assistant", content: res.response });

  } catch (e) {
    loadBubble.remove();
    showToast("Higuruma response error: " + e.message, "error");
  }
}

function insertHigurumaRecommendation(clauseText) {
  const input = document.getElementById("promptInput");
  if (input) {
    input.value += `\n[Higuruma Amendment]: ${clauseText}`;
    input.focus();
    showToast("Clause inserted into prompt dock.", "success");
    document.getElementById("studio")?.scrollIntoView({ behavior: "smooth" });
  }
}

// ── Voice ─────────────────────────────────────────────────────────────────────
function openVoiceModal() {
  document.getElementById("voiceModal")?.classList.remove("hidden");
  startSpeechCapture();
}

function closeVoiceModal() {
  stopSpeechCapture();
  document.getElementById("voiceModal")?.classList.add("hidden");
}

function setupSpeechRecognition() {
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRec) return;
  const rec = new SpeechRec();
  rec.continuous = true;
  rec.interimResults = true;
  rec.lang = "en-US";
  rec.onresult = e => {
    let interim = "";
    for (let i = e.resultIndex; i < e.results.length; ++i) interim += e.results[i][0].transcript;
    const disp = document.getElementById("voiceTranscriptDisplay");
    if (disp) disp.textContent = `"${interim}"`;
  };
  state.speechRecognition = rec;
}

function startSpeechCapture() {
  state.isRecordingVoice = true;
  try { state.speechRecognition?.start(); } catch (e) {}
}

function stopSpeechCapture() {
  state.isRecordingVoice = false;
  try { state.speechRecognition?.stop(); } catch (e) {}
}

function simulateVoice(phrase) {
  const disp = document.getElementById("voiceTranscriptDisplay");
  if (disp) disp.textContent = `"${phrase}"`;
  setTimeout(() => { closeVoiceModal(); executeSpokenCommand(phrase); }, 400);
}

function processVoiceInput() {
  const text = (document.getElementById("voiceTranscriptDisplay")?.textContent || "").replace(/['"]/g,"").trim();
  closeVoiceModal();
  if (text && !text.includes("Listening")) executeSpokenCommand(text);
}

async function executeSpokenCommand(transcript) {
  showToast(`Voice: "${transcript}"`, "info");
  try {
    const res = await apiPost("/api/voice/parse", { transcript });
    if (res.status === "confirmation_required") { openSafetyModal(res.safety, res.recognized_text); return; }
    if (res.action === "activate_skill") {
      setWorkflow(res.skill_tag, res.skill_tag.replace("@",""));
      showToast(res.feedback, "success");
    } else if (res.action === "verify_citations") {
      switchStudioTab("citations");
      showToast(res.feedback, "success");
    } else {
      const input = document.getElementById("promptInput");
      if (input) input.value = `${input.value} ${res.recognized_text}`.trim();
      showToast("Dictated text inserted.", "info");
    }
  } catch (e) {}
}

// ── Safety modal ──────────────────────────────────────────────────────────────
function openSafetyModal(safety, text) {
  state.pendingSafetyToken = safety.token;
  document.getElementById("safetyTitle").textContent  = safety.title;
  document.getElementById("safetyDesc").textContent   = safety.description;
  document.getElementById("safetyDetail").textContent = `Command: "${text}"`;
  document.getElementById("safetyModal")?.classList.remove("hidden");
}

function closeSafetyModal() {
  state.pendingSafetyToken = null;
  document.getElementById("safetyModal")?.classList.add("hidden");
}

async function confirmSafetyAction() {
  if (!state.pendingSafetyToken) return;
  try {
    const res = await apiPost("/api/voice/safety/confirm", { token: state.pendingSafetyToken });
    closeSafetyModal();
    showToast(res.message, "success");
  } catch (e) {
    showToast("Safety error: " + e.message, "error");
  }
}

// ── Exports ───────────────────────────────────────────────────────────────────
function exportMarkdown() {
  if (!state.currentDraftText) return;
  downloadBlob(new Blob([state.currentDraftText], { type: "text/markdown" }), "DraftMate_Legal_Instrument.md");
  showToast("Exported as Markdown (.md)", "success");
}

function exportDocx() {
  if (!state.currentDraftText) return;
  downloadBlob(new Blob([state.currentDraftText], { type: "application/msword" }), "DraftMate_Legal_Instrument.doc");
  showToast("Exported as Word (.doc)", "success");
}

function copyDraftText() {
  if (!state.currentDraftText) return;
  navigator.clipboard.writeText(state.currentDraftText);
  showToast("Copied to clipboard.", "success");
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a   = document.createElement("a");
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click();
  document.body.removeChild(a); URL.revokeObjectURL(url);
}

// ── Toast notifications (Harvey warm light theme) ─────────────────────────────
function showToast(message, type = "info") {
  document.getElementById("dmToast")?.remove();

  const toast = document.createElement("div");
  toast.id = "dmToast";

  // Left border accent — the only color indicator
  const accent = {
    success: "border-l-harvey-green",
    error:   "border-l-harvey-red",
    warning: "border-l-harvey-amber",
    info:    "border-l-harvey-inkMuted"
  }[type] || "border-l-harvey-inkMuted";

  const dot = {
    success: "bg-harvey-green",
    error:   "bg-harvey-red",
    warning: "bg-harvey-amber",
    info:    "bg-harvey-inkMuted"
  }[type] || "bg-harvey-inkMuted";

  toast.className = `fixed bottom-6 left-6 z-[9999] bg-harvey-white border border-harvey-rule border-l-4 ${accent} px-4 py-3 rounded-sm shadow-lg text-[12px] font-medium flex items-center gap-2.5 max-w-xs transition-all duration-300 font-sans`;
  toast.innerHTML = `<span class="w-1.5 h-1.5 rounded-full ${dot} flex-shrink-0"></span><span class="text-harvey-inkMuted">${message}</span>`;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(6px)";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Legacy alias (called from old inline handlers if any remain)
function showHarveyToast(msg, type) { showToast(msg, type); }

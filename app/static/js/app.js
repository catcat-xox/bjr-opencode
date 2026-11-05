const state = {
  items: [],
  historyStudentId: null,
};

let toastTimer;

const elements = {
  itemsBody: document.getElementById("items-body"),
  itemsEmpty: document.getElementById("items-empty"),
  loanItem: document.getElementById("loan-item"),
  historyBody: document.getElementById("history-body"),
  historyEmpty: document.getElementById("history-empty"),
  toast: document.getElementById("toast"),
  serverStatus: document.getElementById("server-status"),
  stats: {
    items: document.getElementById("stat-items"),
    total: document.getElementById("stat-total"),
    available: document.getElementById("stat-available"),
    borrowed: document.getElementById("stat-borrowed"),
  },
};

function setConnectionStatus(online) {
  elements.serverStatus.textContent = online
    ? "Terhubung ke API"
    : "Koneksi bermasalah";
  elements.serverStatus.classList.toggle("connection-status--error", !online);
}

function showToast(message, type = "success") {
  elements.toast.textContent = message;
  elements.toast.className = `toast toast--${type} toast--visible`;
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => {
    elements.toast.className = "toast";
  }, 3500);
}

async function api(path, options = {}) {
  const config = {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  };

  let response;
  try {
    response = await fetch(path, config);
  } catch (error) {
    setConnectionStatus(false);
    throw new Error("Tidak dapat terhubung ke server.");
  }

  setConnectionStatus(true);

  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("application/json")
    ? await response.json()
    : null;

  if (!response.ok) {
    throw new Error(
      (data && data.error) || `Request gagal (${response.status}).`
    );
  }

  return data;
}

function escapeHtml(value) {
  const element = document.createElement("div");
  element.textContent = value ?? "";
  return element.innerHTML;
}

function formatDate(value) {
  if (!value) return "-";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("id-ID", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

function statusLabel(status) {
  const labels = {
    BORROWED: "Dipinjam",
    RETURNED: "Dikembalikan",
    CANCELLED: "Dibatalkan",
  };
  return labels[status] || status;
}

function renderStats(items) {
  elements.stats.items.textContent = items.length;
  elements.stats.total.textContent = items.reduce(
    (total, item) => total + item.total_stock,
    0
  );
  elements.stats.available.textContent = items.reduce(
    (total, item) => total + item.available_stock,
    0
  );
  elements.stats.borrowed.textContent = items.reduce(
    (total, item) => total + (item.total_stock - item.available_stock),
    0
  );
}

function renderItems(items) {
  elements.itemsBody.innerHTML = "";
  elements.itemsEmpty.hidden = items.length > 0;

  items.forEach((item) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${item.id}</td>
      <td>${escapeHtml(item.name)}</td>
      <td>${item.total_stock}</td>
      <td><span class="${item.available_stock > 0 ? "stock-ok" : "stock-empty"}">${item.available_stock}</span></td>
      <td>
        <button class="btn btn--tiny" type="button" data-loan-item="${item.id}" ${item.available_stock === 0 ? "disabled" : ""}>
          Pinjam
        </button>
      </td>
    `;
    elements.itemsBody.appendChild(row);
  });

  const previousValue = elements.loanItem.value;
  elements.loanItem.innerHTML = "";

  if (items.length === 0) {
    const option = document.createElement("option");
    option.value = "";
    option.textContent = "Belum ada alat";
    elements.loanItem.appendChild(option);
    elements.loanItem.disabled = true;
    return;
  }

  elements.loanItem.disabled = false;
  items.forEach((item) => {
    const option = document.createElement("option");
    option.value = item.id;
    option.textContent = `${item.name} (tersedia: ${item.available_stock})`;
    elements.loanItem.appendChild(option);
  });

  if (
    previousValue &&
    items.some((item) => String(item.id) === previousValue)
  ) {
    elements.loanItem.value = previousValue;
  }
}

function itemName(itemId) {
  const item = state.items.find((entry) => entry.id === itemId);
  return item ? item.name : `Alat #${itemId}`;
}

function renderHistory(loans) {
  elements.historyBody.innerHTML = "";
  elements.historyEmpty.hidden = loans.length > 0;

  loans.forEach((loan) => {
    const row = document.createElement("tr");
    const canReturn = loan.status === "BORROWED";
    row.innerHTML = `
      <td>${loan.id}</td>
      <td>${escapeHtml(loan.student_id)}</td>
      <td>${escapeHtml(itemName(loan.item_id))}</td>
      <td>${loan.quantity}</td>
      <td><span class="badge badge--${loan.status.toLowerCase()}">${statusLabel(loan.status)}</span></td>
      <td>${formatDate(loan.created_at)}</td>
      <td>
        ${
          canReturn
            ? `<button class="btn btn--tiny" type="button" data-return="${loan.id}">Kembalikan</button>`
            : "-"
        }
      </td>
    `;
    elements.historyBody.appendChild(row);
  });
}

async function loadItems() {
  try {
    const items = await api("/items");
    state.items = items;
    renderStats(items);
    renderItems(items);
  } catch (error) {
    showToast(error.message, "error");
  }
}

async function loadHistory(studentId, silent = false) {
  try {
    const loans = await api(
      `/loans/student/${encodeURIComponent(studentId)}`
    );
    state.historyStudentId = studentId;
    renderHistory(loans);
    if (!silent) {
      showToast(`Riwayat ${studentId} dimuat.`);
    }
  } catch (error) {
    showToast(error.message, "error");
  }
}

document.getElementById("refresh-items").addEventListener("click", loadItems);

elements.itemsBody.addEventListener("click", (event) => {
  const button = event.target.closest("[data-loan-item]");
  if (!button) return;

  elements.loanItem.value = button.dataset.loanItem;
  document
    .getElementById("loan-form")
    .scrollIntoView({ behavior: "smooth", block: "center" });
  document.querySelector("#loan-form input[name='quantity']").focus();
});

document.getElementById("item-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const submitButton = form.querySelector("button[type='submit']");
  const payload = {
    name: form.elements.name.value,
    total_stock: Number(form.elements.total_stock.value),
  };

  submitButton.disabled = true;
  try {
    const item = await api("/items", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    form.reset();
    await loadItems();
    showToast(`Alat "${item.name}" berhasil ditambahkan.`);
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    submitButton.disabled = false;
  }
});

document.getElementById("loan-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const submitButton = form.querySelector("button[type='submit']");
  const payload = {
    student_id: form.elements.student_id.value,
    item_id: Number(form.elements.item_id.value),
    quantity: Number(form.elements.quantity.value),
  };

  submitButton.disabled = true;
  try {
    const loan = await api("/loans", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    form.elements.quantity.value = "1";
    await loadItems();
    if (state.historyStudentId === loan.student_id) {
      await loadHistory(loan.student_id, true);
    }
    showToast(`Peminjaman #${loan.id} berhasil dicatat.`);
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    submitButton.disabled = false;
  }
});

document
  .getElementById("history-form")
  .addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const submitButton = form.querySelector("button[type='submit']");
    const studentId = form.elements.student_id.value.trim();

    if (!studentId) return;

    submitButton.disabled = true;
    try {
      await loadHistory(studentId);
    } finally {
      submitButton.disabled = false;
    }
  });

elements.historyBody.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-return]");
  if (!button) return;

  const loanId = button.dataset.return;
  button.disabled = true;

  try {
    await api(`/loans/${loanId}/return`, { method: "PUT" });
    await loadItems();
    if (state.historyStudentId) {
      await loadHistory(state.historyStudentId, true);
    }
    showToast(`Transaksi #${loanId} berhasil dikembalikan.`);
  } catch (error) {
    button.disabled = false;
    showToast(error.message, "error");
  }
});

loadItems();

const pages = [
  { key: "home", label: "Home", file: "Home.html", icon: "home" },
  { key: "bills", label: "Bills", file: "Bills.html", icon: "fileText" },
  { key: "schedule", label: "Schedule", file: "Schedule.html", icon: "calendar" },
  { key: "profile", label: "Profile", file: "Profile.html", icon: "user" },
  { key: "settings", label: "Settings", file: "Settings.html", icon: "settings" },
];

const currencies = {
  USD: { label: "USD", symbol: "$", rate: 1 },
  ILS: { label: "ILS", symbol: "₪", rate: 3.70 },
  JOD: { label: "JOD", symbol: "JD", rate: 0.71 },
  SAR: { label: "SAR", symbol: "SR", rate: 3.75 },
  EUR: { label: "EUR", symbol: "€", rate: 0.92 },
  EGP: { label: "EGP", symbol: "E£", rate: 47.50 },
};

const billCategories = {
  rent: { key: "rent", icon: "home", label: "rent", color: "#7c3aed", bg: "#ede7ff", hover: "#f5f1ff" },
  water: { key: "water", icon: "droplet", label: "water", color: "#0b3d91", bg: "#dce9ff", hover: "#eef5ff" },
  gas: { key: "gas", icon: "flame", label: "gas", color: "#e02424", bg: "#ffe2e2", hover: "#fff0f0" },
  wifi: { key: "wifi", icon: "wifi", label: "wifi", color: "#0097a7", bg: "#d6fbff", hover: "#e9fdff" },
  electricity: { key: "electricity", icon: "zap", label: "electricity", color: "#d49a00", bg: "#fff4bf", hover: "#fff9de" },
  other: { key: "other", icon: "fileText", label: "other", color: "#64748b", bg: "#e9eef5", hover: "#f5f7fa" },
};

const translations = {
  en: {
    home: "Home",
    bills: "Bills",
    schedule: "Schedule",
    profile: "Profile",
    settings: "Settings",
    logout: "Logout",
    household: "Household expenses",
  },
  ar: {
    home: "الرئيسية",
    bills: "الفواتير",
    schedule: "الجدول",
    profile: "الملف الشخصي",
    settings: "الإعدادات",
    logout: "تسجيل الخروج",
    household: "مصاريف المنزل",
  },
};

const iconPaths = {
  home: '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M9 21v-7h6v7"/>',
  fileText: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M8 13h8"/><path d="M8 17h8"/><path d="M8 9h2"/>',
  calendar: '<path d="M8 2v4"/><path d="M16 2v4"/><path d="M3 10h18"/><rect x="3" y="4" width="18" height="18" rx="2"/>',
  user: '<path d="M20 21a8 8 0 0 0-16 0"/><circle cx="12" cy="7" r="4"/>',
  settings: '<path d="M12 15.5A3.5 3.5 0 1 0 12 8a3.5 3.5 0 0 0 0 7.5z"/><path d="M19.4 15a1.7 1.7 0 0 0 .34 1.88l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06A1.7 1.7 0 0 0 15 19.4a1.7 1.7 0 0 0-1 .56V20a2 2 0 1 1-4 0v-.09a1.7 1.7 0 0 0-1-.56 1.7 1.7 0 0 0-1.88.34l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-.56-1H4a2 2 0 1 1 0-4h.09a1.7 1.7 0 0 0 .56-1 1.7 1.7 0 0 0-.34-1.88l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-.56V4a2 2 0 1 1 4 0v.09a1.7 1.7 0 0 0 1 .56 1.7 1.7 0 0 0 1.88-.34l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.7 1.7 0 0 0 19.4 9c.19.34.37.68.56 1H20a2 2 0 1 1 0 4h-.09a1.7 1.7 0 0 0-.56 1z"/>',
  logOut: '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5"/><path d="M21 12H9"/>',
  plus: '<path d="M12 5v14"/><path d="M5 12h14"/>',
  edit: '<path d="M12 20h9"/><path d="m16.5 3.5 4 4L8 20H4v-4z"/>',
  trash: '<path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/>',
  dollar: '<path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7H14a3.5 3.5 0 0 1 0 7H6"/>',
  alert: '<circle cx="12" cy="12" r="10"/><path d="M12 8v4"/><path d="M12 16h.01"/>',
  check: '<path d="M20 6 9 17l-5-5"/><circle cx="12" cy="12" r="10"/>',
  trend: '<path d="m22 7-8.5 8.5-5-5L2 17"/><path d="M16 7h6v6"/>',
  zap: '<path d="M13 2 3 14h8l-2 8 10-12h-8z"/>',
  droplet: '<path d="M12 2s6 6.2 6 11a6 6 0 0 1-12 0c0-4.8 6-11 6-11z"/>',
  wifi: '<path d="M5 13a10 10 0 0 1 14 0"/><path d="M8.5 16.5a5 5 0 0 1 7 0"/><path d="M12 20h.01"/>',
  flame: '<path d="M8.5 14a3.5 3.5 0 1 0 7 0c0-4-3.5-5-2.5-10-3 1.5-5 4-5 7 0 0-1.5-.5-2-2.5C4 12 5.5 17.5 12 20"/>',
  search: '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
  phone: '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.3 1.8.7 2.6a2 2 0 0 1-.4 2.1L8.1 9.7a16 16 0 0 0 6.2 6.2l1.3-1.3a2 2 0 0 1 2.1-.4c.8.3 1.7.6 2.6.7a2 2 0 0 1 1.7 2z"/>',
  mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
  mapPin: '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
  bell: '<path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 7h18s-3 0-3-7"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>',
  moon: '<path d="M21 12.8A8.5 8.5 0 1 1 11.2 3 6.5 6.5 0 0 0 21 12.8z"/>',
};

function currentLanguage() {
  return localStorage.getItem("myhome:language") || "en";
}

function t(key) {
  const language = currentLanguage();
  return translations[language]?.[key] || translations.en[key] || key;
}

function icon(name, className = "") {
  return `<svg class="${className}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${iconPaths[name] || ""}</svg>`;
}

function preferredCurrency() {
  return localStorage.getItem("myhome:currency") || "USD";
}

function convertAmount(amount, fromCurrency = "USD", toCurrency = preferredCurrency()) {
  const source = currencies[fromCurrency] || currencies.USD;
  const target = currencies[toCurrency] || currencies.USD;
  return (Number(amount || 0) / source.rate) * target.rate;
}

function formatCurrency(value, fromCurrency = "USD", toCurrency = preferredCurrency()) {
  const converted = convertAmount(value, fromCurrency, toCurrency);
  return new Intl.NumberFormat(currentLanguage() === "ar" ? "ar" : "en-US", {
    style: "currency",
    currency: toCurrency,
    maximumFractionDigits: 2,
  }).format(converted);
}

function parseDate(value) {
  const [year, month, day] = String(value).split("-").map(Number);
  return new Date(year, month - 1, day);
}

function formatDate(value) {
  return parseDate(value).toLocaleDateString("en-US", { month: "numeric", day: "numeric", year: "numeric" });
}

function categoryForBill(bill) {
  if (bill?.category && billCategories[bill.category]) return billCategories[bill.category];

  const text = String(bill?.name || bill || "").toLowerCase();
  if (text.includes("rent")) return billCategories.rent;
  if (text.includes("water")) return billCategories.water;
  if (text.includes("internet") || text.includes("wifi")) return billCategories.wifi;
  if (text.includes("gas")) return billCategories.gas;
  if (text.includes("electric")) return billCategories.electricity;
  return billCategories.other;
}

function billDescription(bill) {
  const category = categoryForBill(bill).key;
  const descriptions = {
    electricity: "Main house electricity",
    water: "Household water service",
    wifi: "Home internet plan",
    gas: "Natural gas service",
  };
  return descriptions[category] || "Household expense";
}

function isOverdue(bill) {
  return bill.status === "unpaid" && parseDate(bill.due_date) < new Date(new Date().toDateString());
}

function daysOverdue(bill) {
  const msPerDay = 24 * 60 * 60 * 1000;
  return Math.max(0, Math.ceil((new Date(new Date().toDateString()) - parseDate(bill.due_date)) / msPerDay));
}

function setToast(message) {
  let toast = document.querySelector(".toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.className = "toast";
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.classList.add("show");
  window.setTimeout(() => toast.classList.remove("show"), 2800);
}

function pagePath(file) {
  return file;
}

function renderShell(activePage, content) {
  document.body.classList.toggle("dark", localStorage.getItem("myhome:dark") === "true");
  document.documentElement.lang = currentLanguage();
  document.documentElement.dir = currentLanguage() === "ar" ? "rtl" : "ltr";
  const nav = pages.map((page) => `
    <a class="nav-link ${page.key === activePage ? "active" : ""}" href="${pagePath(page.file)}">
      ${icon(page.icon)}
      <span>${t(page.key)}</span>
    </a>
  `).join("");

  document.body.innerHTML = `
    <div class="app-shell">
      <aside class="sidebar">
        <div class="sidebar-brand">
          <strong>${icon("home")} MyHome</strong>
          <small>${t("household")}</small>
        </div>
        <nav class="nav">${nav}</nav>
        <div class="logout-wrap">
          <button class="logout-button" type="button" data-action="logout">${icon("logOut")} ${t("logout")}</button>
        </div>
      </aside>
      <main class="main-content">${content}</main>
    </div>
    <div class="toast"></div>
  `;

  document.querySelector("[data-action='logout']")?.addEventListener("click", async () => {
    try {
      await api.logout();
    } finally {
      clearStoredUser();
      window.location.href = "Login.html";
    }
  });
}

function renderTopbar(title, subtitle, actionHtml = "") {
  return `
    <header class="topbar">
      <div>
        <h1 class="page-title">${title}</h1>
        <p class="page-subtitle">${subtitle}</p>
      </div>
      ${actionHtml}
    </header>
  `;
}

function billCard(bill) {
  const category = categoryForBill(bill);
  return `
    <article class="bill-card" data-category="${category.key}" style="--category-hover:${category.hover};--category-color:${category.color}" data-bill-id="${bill.id}">
      <div class="category-icon" style="background:${category.bg};color:${category.color}">${icon(category.icon)}</div>
      <div class="bill-main">
        <h3>
          ${bill.name}
          <span class="badge category">${l(category.key)}</span>
          <span class="badge ${bill.status}">${bill.status}</span>
          <span class="badge recurring">${bill.frequency === "once" ? "One time" : "Recurring"}</span>
        </h3>
        <div class="bill-meta">Due: ${formatDate(bill.due_date)} <span class="bill-amount">${formatCurrency(bill.amount, bill.currency)}</span></div>
        <div class="bill-description">${billDescription(bill)}</div>
      </div>
      <div class="bill-actions">
        ${bill.status === "unpaid" ? `<button class="icon-button" type="button" title="Mark paid" data-action="pay-bill" data-id="${bill.id}">${icon("check")}</button>` : ""}
        <button class="icon-button" type="button" title="Edit bill" data-action="edit-bill" data-id="${bill.id}">${icon("edit")}</button>
        <button class="icon-button danger-icon" type="button" title="Delete bill" data-action="delete-bill" data-id="${bill.id}">${icon("trash")}</button>
      </div>
    </article>
  `;
}

function createBillModal(bill = null) {
  const isEdit = Boolean(bill);
  const modal = document.createElement("div");
  modal.className = "modal-backdrop open";
  modal.innerHTML = `
    <form class="modal" data-bill-form>
      <div class="modal-header">
        <h2>${isEdit ? "Edit Bill" : "Add Bill"}</h2>
        <button class="icon-button" type="button" data-action="close-modal">×</button>
      </div>
      <label class="field">Bill Name<input name="name" required value="${bill?.name || ""}" placeholder="Electricity Bill"></label>
      <label class="field">${l("billType") || "Bill Type"}
        <select name="category">
          ${Object.keys(billCategories).map((item) => `<option value="${item}" ${bill?.category === item ? "selected" : ""}>${l(item)}</option>`).join("")}
        </select>
      </label>
      <label class="field">Amount<input name="amount" type="text" inputmode="decimal" required value="${bill?.amount || ""}" placeholder="125.50"></label>
      <label class="field">Currency
        <select name="currency">
          ${Object.keys(currencies).map((item) => `<option value="${item}" ${bill?.currency === item ? "selected" : ""}>${currencies[item].label}</option>`).join("")}
        </select>
      </label>
      <label class="field">Due Date<input name="due_date" type="date" required value="${bill?.due_date || ""}"></label>
      <label class="field">Frequency
        <select name="frequency">
          ${["weekly", "monthly", "yearly", "once"].map((item) => `<option value="${item}" ${bill?.frequency === item ? "selected" : ""}>${item}</option>`).join("")}
        </select>
      </label>
      <div class="modal-actions">
        <button class="ghost-button" type="button" data-action="close-modal">Cancel</button>
        <button class="secondary-button" type="submit">${isEdit ? "Save Bill" : "Add Bill"}</button>
      </div>
    </form>
  `;
  document.body.appendChild(modal);
  modal.querySelectorAll("[data-action='close-modal']").forEach((button) => {
    button.addEventListener("click", () => modal.remove());
  });
  return modal;
}

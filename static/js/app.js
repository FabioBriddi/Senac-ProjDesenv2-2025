let token = null;

function showSection(id) {
    document.querySelectorAll(".section").forEach(sec => {
        sec.classList.remove("active");
    });
    document.getElementById(id).classList.add("active");
}

// ---- LOGIN ----
async function doLogin() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const res = await fetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const statusEl = document.getElementById("login-status");

    if (!res.ok) {
        statusEl.textContent = "Falha no login";
        token = null;
        return;
    }

    const data = await res.json();
    token = data.access_token;
    statusEl.textContent = "Login OK, token: " + token;
}

// ---- FONTES ----
async function loadSources() {
    const res = await fetch("/sources/");
    const data = await res.json();

    const tbody = document.getElementById("sources-table-body");
    tbody.innerHTML = "";

    data.forEach(src => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${src.id}</td>
            <td>${src.name}</td>
            <td>${src.type}</td>
            <td>${src.active ? "Sim" : "Não"}</td>
        `;
        tbody.appendChild(tr);
    });
}

async function createSource() {
    const name = document.getElementById("source-name").value;
    const type = document.getElementById("source-type").value;

    if (!name || !type) {
        alert("Preencha nome e tipo.");
        return;
    }

    const res = await fetch("/sources/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, type, active: true })
    });

    if (!res.ok) {
        alert("Erro ao criar fonte");
        return;
    }

    document.getElementById("source-name").value = "";
    document.getElementById("source-type").value = "";
    loadSources();
}

// ---- RELATÓRIOS ----
async function loadSummary() {
    const res = await fetch("/reports/summary");
    const data = await res.json();

    const rows = data.rows || [];
    const tbody = document.getElementById("summary-table-body");
    tbody.innerHTML = "";

    rows.forEach(row => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${row.artist}</td>
            <td>${row.platform}</td>
            <td>${row.plays}</td>
            <td>${row.revenue.toFixed(2)}</td>
        `;
        tbody.appendChild(tr);
    });
}

// Carrega fontes e resumo ao iniciar
window.addEventListener("load", () => {
    loadSources();
    loadSummary();
});

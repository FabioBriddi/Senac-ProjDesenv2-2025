function openUploader(type) {
    document.getElementById("dashboard").innerHTML = `
        <h4>Upload CSV (${type})</h4>
        <input type="file" id="csvFile" class="form-control mb-3">
        <button class="btn btn-primary" onclick="sendCSV('${type}')">Enviar</button>
    `;
}

async function sendCSV(type) {
    const fileInput = document.getElementById("csvFile");
    if (!fileInput.files.length) {
        alert("Selecione um arquivo CSV");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const endpoint = type === "artists"
        ? "/upload/artists"
        : "/upload/devices";

    const res = await fetch(endpoint, { method: "POST", body: formData });

    const data = await res.json();

    document.getElementById("dashboard").innerHTML =
        `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

async function loadSummary() {
    const res = await fetch("/reports/summary");
    const data = await res.json();

    document.getElementById("dashboard").innerHTML =
        `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

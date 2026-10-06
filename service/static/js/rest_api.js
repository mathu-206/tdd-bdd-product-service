"use strict";
const $ = (id) => document.getElementById(id);
const FIELDS = ["product_id", "product_name", "product_description", "product_price"];

function flash(message) {
  $("flash_message").textContent = message;
}

function clearForm() {
  FIELDS.forEach((f) => ($(f).value = ""));
  $("product_available").value = "";
  $("product_category").value = "";
}

function fillForm(p) {
  $("product_id").value = p.id;
  $("product_name").value = p.name;
  $("product_description").value = p.description;
  $("product_price").value = p.price;
  $("product_available").value = String(p.available);
  $("product_category").value = p.category;
}

function formData() {
  return {
    name: $("product_name").value,
    description: $("product_description").value,
    price: $("product_price").value,
    available: $("product_available").value !== "false",
    category: $("product_category").value || "UNKNOWN",
  };
}

function pretty(name) {
  return name.charAt(0) + name.slice(1).toLowerCase();
}

function renderResults(list) {
  const holder = $("search_results");
  holder.textContent = "";
  const table = document.createElement("table");
  const head = table.insertRow();
  ["Id", "Name", "Category", "Available", "Price"].forEach((t) => {
    const th = document.createElement("th");
    th.textContent = t;
    head.appendChild(th);
  });
  list.forEach((p) => {
    const row = table.insertRow();
    [p.id, p.name, pretty(p.category), p.available, p.price].forEach((v) => {
      row.insertCell().textContent = v;
    });
  });
  holder.appendChild(table);
}

async function call(method, url, body) {
  const options = { method, headers: {} };
  if (body) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }
  const resp = await fetch(url, options);
  let data = null;
  if (resp.status !== 204) {
    try { data = await resp.json(); } catch (e) { data = null; }
  }
  return { ok: resp.ok, data };
}

const errorText = (r) => (r.data && r.data.message) || "Server error!";

$("create-btn").addEventListener("click", async () => {
  flash("");
  const r = await call("POST", "/products", formData());
  if (r.ok) { fillForm(r.data); flash("Success"); } else { flash(errorText(r)); }
});

$("retrieve-btn").addEventListener("click", async () => {
  flash("");
  const id = $("product_id").value;
  const r = await call("GET", `/products/${id}`);
  if (r.ok) { fillForm(r.data); flash("Success"); } else { flash(errorText(r)); }
});

$("update-btn").addEventListener("click", async () => {
  flash("");
  const id = $("product_id").value;
  const r = await call("PUT", `/products/${id}`, formData());
  if (r.ok) { fillForm(r.data); flash("Success"); } else { flash(errorText(r)); }
});

$("delete-btn").addEventListener("click", async () => {
  flash("");
  const id = $("product_id").value;
  const r = await call("DELETE", `/products/${id}`);
  if (r.ok) { clearForm(); flash("Product has been Deleted!"); } else { flash(errorText(r)); }
});

$("clear-btn").addEventListener("click", () => {
  clearForm();
  $("search_results").textContent = "";
  flash("");
});

$("search-btn").addEventListener("click", async () => {
  flash("");
  const params = new URLSearchParams();
  if ($("product_name").value) params.set("name", $("product_name").value);
  if ($("product_category").value) params.set("category", $("product_category").value);
  if ($("product_available").value) params.set("available", $("product_available").value);
  const r = await call("GET", `/products?${params.toString()}`);
  if (r.ok) {
    renderResults(r.data);
    if (r.data.length === 1) fillForm(r.data[0]);
    flash("Success");
  } else {
    flash(errorText(r));
  }
});

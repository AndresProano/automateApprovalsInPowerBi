<template>
  <main class="container">
    <h1>Actualización Power BI</h1>
    <button @click="onProcess" :disabled="loading">
      {{ loading ? "Procesando..." : "Actualizar y abrir reporte" }}
    </button>
  </main>
</template>

<script setup>
import { ref } from "vue";
import { loginAndGetIdToken } from "./msal";

const loading = ref(false);

async function onProcess() {
  loading.value = true;
  try {
    const { idToken } = await loginAndGetIdToken();
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/approvals/process`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id_token: idToken }),
    });
    const data = await res.json();
    if (!res.ok || !data.ok) throw new Error(data.detail || "Error");
    // Abre el reporte (solo usuarios de la organización con acceso podrán verlo)
    window.open(data.powerBiUrl || import.meta.env.VITE_POWERBI_REPORT_URL, "_blank", "noopener,noreferrer");
  } catch (e) {
    console.error(e);
    alert("Fallo en el proceso.");
  } finally {
    loading.value = false;
  }
}
</script>

<style>
.container{max-width:640px;margin:0 auto;padding:2rem;text-align:center;font-family:system-ui,sans-serif}
button{background:#0078d4;color:#fff;padding:.8rem 1.4rem;border:none;border-radius:8px;cursor:pointer}
button:disabled{background:#888}
</style>
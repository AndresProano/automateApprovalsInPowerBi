<script setup>
  import { ref, onMounted } from "vue";
  import { PublicClientApplication } from "@azure/msal-browser";
  import { msalConfig, loginRequest } from "./authConfig";
  import logoUsfq from "./logo-usfq.svg";
  
  const loading = ref(false);
  const isMsalReady = ref(false);

  const urlToShow = ref("https://app.powerbi.com/reportEmbed?reportId=84f5e2e7-cafb-474f-8e04-63a5183d4256&autoAuth=true&ctid=9f119962-8c62-431c-a8ef-e7e0a42d11fc");

  const msalInstance = new PublicClientApplication(msalConfig);
  const userList = ref([]);
  const isAuthenticated = ref(false);
  const tokenGuardado = ref("");

  const delay = ms => new Promise(res => setTimeout(res, ms));

  onMounted(async ()=>{
    try{
      await msalInstance.initialize();
      isMsalReady.value = true;

      const accounts = msalInstance.getAllAccounts();
      if (accounts.length > 0) {
        msalInstance.setActiveAccount(accounts[0]);
        isAuthenticated.value = true;
      }
    } catch (error) {
      console.error("Error inicializando MSAL:", error);
    }
  });

  const loginAndFetch = async () => {
    try {

      const loginResponse = await msalInstance.loginPopup(loginRequest);

      msalInstance.setActiveAccount(loginResponse.account);
      isAuthenticated.value = true;

      const accessToken = loginResponse.accessToken;
      tokenGuardado.value = accessToken;

      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/users`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${accessToken}`, //llave hacia el back
            'Content-Type': 'application/json'
        }
      });

        if (response.ok){
          const data = await response.json();
          userList.value = data.value || [];
        } else {
          console.error("Error al obtener datos del usuario");
        }
      } catch (error) {
          console.error("Login Error", error);
        }
    };
  

  async function ejecutarAccionBackend() {
    if (!tokenGuardado.value) {
      alert("Por favor inicie sesión primero.");
      return;
    }
    loading.value = true;
    try {
      const response = await fetch("http://localhost:8000/api/approvals", {
        method: "GET",
        headers: { 
          "Authorization": `Bearer ${tokenGuardado.value}`,
        }
      });
      
      if (!response.ok) {
        console.error("Error en backend");
        alert("Hubo un error al procesar");
        loading.value = false;
      } else {
        const data = await response.json();
        console.log("Proceso completado", data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      loading.value = false;
    }
  }

  async function abrirPestana() {
    window.open(urlToShow.value, "_blank");
  }
  
  function cerrarPestana() {
    showPowerBI.value = false;
  }

  async function ejecutarTodo() {
    await ejecutarAccionBackend();
    await abrirPestana();
  }
</script>

<template>
  <div class="app-container">
    
    <transition name="fade" mode="out-in">
      <div v-if="!isAuthenticated" class="login-view" key="login">
        <div class="login-card">
          <div class="icon-header"><img :src="logoUsfq" alt="Logo USFQ" class="logo-img"></div>
          <h1>Bienvenido</h1>
          <p class="subtitle">Sistema de Aprobaciones</p>
          
          <button @click="loginAndFetch" class="btn-primary">
            Iniciar Sesión con Microsoft
          </button>
        </div>
      </div>

      <main v-else class="dashboard-view" key="dashboard">
        <header class="top-bar">
          <div class="brand">
            <span class="logo-icon">📊</span>
            <h1>Approvals App <span class="badge">Admin</span></h1>
          </div>
          <div class="user-actions">
            <span class="user-status">Conectado</span>
          </div>
        </header>

        <div class="content-wrapper">
          
          <section class="control-panel">
            <div class="panel-header">
              <h2>Panel de Control</h2>
              <p>Generación de reportes y visualización de métricas</p>
            </div>
            
            <button class="btn-primary large" @click="ejecutarTodo" :disabled="loading">
              <span v-if="loading" class="spinner"></span>
              {{ loading ? 'Procesando datos...' : 'Generar Reporte y Actualizar' }}
            </button>
          </section>

          <section v-if="userList.length > 0" class="users-section">
            <h3>👥 Usuarios Sincronizados</h3>
            <div class="user-grid">
              <div v-for="user in userList" :key="user.id" class="user-card">
                <div class="avatar">{{ getInitials(user.displayName) }}</div>
                <div class="user-info">
                  <span class="name">{{ user.displayName }}</span>
                  <span class="email">{{ user.mail }}</span>
                </div>
              </div>
            </div>
          </section>

          <section v-if="showPowerBI" class="report-section">
            <div class="tab-header">
              <span>📈 Visualización Power BI</span>
              <button class="close-btn" @click="showPowerBI = false">✕ Cerrar</button>
            </div>
            <div class="pbi-wrapper">
              <iframe title="Tablero_Approvals (1)" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=1939beeb-2abb-4001-9941-f7f609c19e99&autoAuth=true&ctid=9f119962-8c62-431c-a8ef-e7e0a42d11fc" frameborder="0" allowFullScreen="true"></iframe>
            </div>
          </section>

        </div>
      </main>
    </transition>
  </div>
</template>

<style scoped>
  /* ===== VARIABLES & RESET ===== */
  :root {
    --primary: #8a1c1c; /* Tu rojo oscuro original */
    --primary-hover: #a02525;
    --bg-body: #f4f6f8;
    --bg-card: #ffffff;
    --text-main: #2c3e50;
    --text-muted: #6c757d;
    --shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    --radius: 12px;
  }

  .app-container {
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--bg-body);
    min-height: 100vh;
    color: var(--text-main);
  }

  /* ===== VISTA LOGIN ===== */
  .login-view {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
  }

  .login-card {
    background: white;
    padding: 3rem;
    border-radius: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    text-align: center;
    max-width: 400px;
    width: 100%;
  }

  .icon-header { 
    margin-bottom: 1rem;
    display: flex;
    justify-content: center;
  }

.logo-img {
    width: 80px;
    height: auto;
  }

  .subtitle { color: var(--text-muted); margin-bottom: 2rem; }

  /* ===== VISTA DASHBOARD ===== */
  .dashboard-view {
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  .top-bar {
    background: white;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  }

  .brand h1 { font-size: 1.2rem; margin: 0; font-weight: 700; color: var(--text-main); display: flex; align-items: center; gap: 10px;}
  .badge { background: #eee; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; color: #555; text-transform: uppercase; }
  
  .content-wrapper {
    max-width: 1200px;
    margin: 2rem auto;
    width: 95%;
    padding-bottom: 3rem;
  }

  /* ===== BOTONES ===== */
  .btn-primary {
    background: var(--primary);
    color: black;
    border: 1px solid black;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
  }

  .btn-primary:hover:not(:disabled) {
    background: var(--primary-hover);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(138, 28, 28, 0.3);
  }

  .btn-primary:disabled {
    background: #ccc;
    cursor: not-allowed;
  }

  .btn-primary.large {
    width: 100%;
    max-width: 300px;
    padding: 15px;
    font-size: 1.1rem;
  }

  /* ===== CARDS DE USUARIOS ===== */
  .users-section { margin-top: 2rem; }
  .users-section h3 { margin-bottom: 1rem; color: var(--text-muted); font-size: 1rem; text-transform: uppercase; letter-spacing: 1px; }

  .user-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
  }

  .user-card {
    background: white;
    padding: 1rem;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    display: flex;
    align-items: center;
    gap: 1rem;
    border: 1px solid #eee;
  }

  .avatar {
    background: #f0e2d4;
    color: var(--primary);
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    font-size: 0.9rem;
  }

  .user-info { display: flex; flex-direction: column; overflow: hidden; }
  .user-info .name { font-weight: 600; font-size: 0.95rem; }
  .user-info .email { font-size: 0.8rem; color: var(--text-muted); text-overflow: ellipsis; overflow: hidden; white-space: nowrap; }

  /* ===== POWER BI & PANEL ===== */
  .control-panel {
    background: white;
    padding: 2rem;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    text-align: center;
    margin-bottom: 2rem;
  }
  .panel-header { margin-bottom: 1.5rem; }
  .panel-header h2 { margin: 0; font-size: 1.5rem; }
  .panel-header p { margin: 5px 0 0; color: var(--text-muted); }

  .report-section {
    background: white;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    overflow: hidden;
    margin-top: 2rem;
  }

  .tab-header {
    background: #f8f9fa;
    padding: 15px 20px;
    border-bottom: 1px solid #eee;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 600;
  }

  .close-btn {
    background: transparent;
    border: 1px solid #ddd;
    padding: 5px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.8rem;
    transition: 0.2s;
  }
  .close-btn:hover { background: #fee; color: red; border-color: red; }

  .pbi-wrapper iframe {
    width: 100%;
    height: 75vh;
    border: none;
    display: block;
  }

  /* ===== ANIMACIONES ===== */
  .fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
  .fade-enter, .fade-leave-to { opacity: 0; }

  /* Spinner simple */
  .spinner {
    border: 3px solid rgba(255,255,255,0.3);
    border-radius: 50%;
    border-top: 3px solid white;
    width: 16px;
    height: 16px;
    animation: spin 1s linear infinite;
    display: inline-block;
  }
  @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>
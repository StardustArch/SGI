<!-- Ficheiro: frontend/app/pages/dashboard.vue (ATUALIZADO) -->
<template>
  <div class="flex">

    <!-- ************************************ -->
    <!-- **** 1. SIDEBAR (PARA DESKTOP) **** -->
    <!-- ************************************ -->
    <aside
      class="fixed z-20 hidden md:flex flex-col min-h-screen bg-white p-4 shadow-lg dark:bg-gray-800 transition-all duration-300 ease-in-out"
      :class="isSidebarOpen ? 'w-64' : 'w-20'">
      <!-- ... (Logo e Botão de Encolher) ... -->
      <div class="flex items-center" :class="isSidebarOpen ? 'justify-between' : 'justify-center'">
        <h2 v-if="isSidebarOpen" class="text-lg font-bold dark:text-white">SGI</h2>
        <button @click="toggleSidebar" class="p-2 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700">
          <BootstrapIcon name="list" class="w-6 h-6 dark:text-white" />
        </button>
      </div>

      <!-- ... (A carregar...) ... -->
      <div v-if="pending" class="text-gray-500 dark:text-gray-400 mt-4">A carregar...</div>

      <!-- **** MUDANÇA AQUI (Menus Principais) **** -->
      <!-- A navegação principal (sem o "Meu Perfil") -->
      <nav class="flex-1 mt-6 space-y-2">

        <!-- Menu do Administrador -->
        <ul v-if="userData?.perfil === 1">
          <li>
            <NuxtLink to="/dashboard/admin" class="nav-link">
              <BootstrapIcon name="house-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Visão Geral</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/admin/reports" class="nav-link">
              <BootstrapIcon name="bar-chart-line-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Relatórios</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/admin/estudantes" class="nav-link">
              <BootstrapIcon name="people-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Gerir Estudantes</span>
            </NuxtLink>
          </li>
        </ul>

        <!-- Menu do Estudante (REMOVEMOS O "Meu Perfil" daqui) -->
        <ul v-else-if="userData?.perfil === 2">
          <li>
            <NuxtLink to="/dashboard/student" class="nav-link">
              <BootstrapIcon name="house-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Visão Geral</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/student/financas" class="nav-link">
              <BootstrapIcon name="cash-coin" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Hist. Financeiro</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/student/disciplina" class="nav-link">
              <BootstrapIcon name="info-circle-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Hist. Disciplinar</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/student/presencas" class="nav-link">
              <BootstrapIcon name="calendar-check-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Hist. Presenças</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/student/pedidos" class="nav-link">
              <BootstrapIcon name="arrow-up-circle-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Pedidos de Saída</span>
            </NuxtLink>
          </li>
        </ul>

        <!-- Menu do Encarregado -->
        <ul v-else-if="userData?.perfil === 3">
          <li>
            <NuxtLink to="/dashboard/foreman" class="nav-link">
              <BootstrapIcon name="house-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Visão Geral</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/foreman/students" class="nav-link">
              <BootstrapIcon name="people-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Meus Educandos</span>
            </NuxtLink>
          </li>
          <li>
                    <NuxtLink to="/dashboard/foreman/financas" class="nav-link">
          <BootstrapIcon name="cash-coin" class="nav-icon" />
                        <span v-if="isSidebarOpen" class="nav-text">Hist. Financeiro</span>
        </NuxtLink>
          </li>

                    <li>
        <NuxtLink to="/dashboard/foreman/pedidos" class="nav-link">

          <BootstrapIcon name="arrow-up-circle-fill" class="nav-icon" />
                        <span v-if="isSidebarOpen" class="nav-text">Pedidos de Saída</span>
        </NuxtLink>
          </li>

                             <li>
        <NuxtLink to="/dashboard/foreman/presencas" class="nav-link">

          <BootstrapIcon name="calendar-check-fill" class="nav-icon" />
                        <span v-if="isSidebarOpen" class="nav-text">Hist. Presenças</span>
        </NuxtLink>
          </li>
        </ul>
      </nav>

      <!-- **** MUDANÇA AQUI (Menus Inferiores) **** -->
      <!-- Links de rodapé da Sidebar -->
      <div class="mt-4 border-t pt-4 border-gray-200 dark:border-gray-700 space-y-2">

        <!-- O seu NOVO link "Meu Perfil" Padronizado -->
        <NuxtLink v-if="profileLink" :to="profileLink" class="nav-link">
          <BootstrapIcon name="person-circle" class="nav-icon" />
          <span v-if="isSidebarOpen" class="nav-text">Meu Perfil</span>
        </NuxtLink>

        <!-- Botão de Tema -->
        <div class="py-2" :class="isSidebarOpen ? 'flex justify-end' : 'flex justify-center'">
          <ThemeToggle />
        </div>

        <!-- Botão de Sair (Logout) (Baixo) -->
        <button @click="logout" class="nav-link w-full bg-red-100 dark:bg-red-800 text-red-700 dark:text-red-300">
          <BootstrapIcon name="box-arrow-right" class="nav-icon" />
          <span v-if="isSidebarOpen" class="nav-text">Sair (Logout)</span>
        </button>
      </div>

    </aside>

    <!-- ************************************ -->
    <!-- **** 2. SIDEBAR (PARA MOBILE) **** -->
    <!-- ************************************ -->

    <div class="md:hidden p-2 fixed top-2 left-2 z-30">
      <button @click="toggleSidebar" class="p-2 rounded-md bg-white dark:bg-gray-800 shadow">
        <BootstrapIcon name="list" class="w-6 h-6 dark:text-white" />
      </button>
    </div>

    <div v-if="isSidebarOpen" class="md:hidden fixed inset-0 z-20 bg-black/50" @click="isSidebarOpen = false">
    </div>
    <aside
      class="md:hidden fixed z-30 top-0 left-0 min-h-screen bg-white p-4 shadow-lg dark:bg-gray-800 transition-all duration-300 ease-in-out w-64"
      :class="isSidebarOpen ? 'translate-x-0' : '-translate-x-full'">
      <!-- ... (Header e Botão de Tema) ... -->
      <div v-if="pending" class="text-gray-500 dark:text-gray-400 mt-4">A carregar...</div>

      <!-- **** MUDANÇA AQUI (Menu Mobile do Estudante) **** -->
      <nav class="flex-1 mt-6 space-y-2">
        <!-- ... (Menu Admin) ... -->
        <ul v-if="userData?.perfil === 1">
          <li>
            <NuxtLink to="/dashboard/admin" class="nav-link">
              <BootstrapIcon name="house-fill" class="nav-icon" />
              <span class="nav-text">Visão Geral</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/admin/reports" class="nav-link">
              <BootstrapIcon name="bar-chart-line-fill" class="nav-icon" />
              <span class="nav-text">Relatórios</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/admin/students" class="nav-link">
              <BootstrapIcon name="people-fill" class="nav-icon" />
              <span class="nav-text">Gerir Estudantes</span>
            </NuxtLink>
          </li>
        </ul>

        <!-- Menu Mobile do Estudante (REMOVEMOS O "Meu Perfil" daqui) -->
        <ul v-else-if="userData?.perfil === 2">
          <li>
            <NuxtLink to="/dashboard/student" class="nav-link">
              <BootstrapIcon name="house-fill" class="nav-icon" />
              <span class="nav-text">Visão Geral</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/student/me" class="nav-link">
              <BootstrapIcon name="person-fill" class="nav-icon" />
              <span class="nav-text">Meu Perfil</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/student/financas" class="nav-link">
              <BootstrapIcon name="cash-coin" class="nav-icon" />
              <span class="nav-text">Hist. Financeiro</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/student/disciplina" class="nav-link">
              <BootstrapIcon name="info-circle-fill" class="nav-icon" />
              <span class="nav-text">Hist. Disciplinar</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/student/presencas" class="nav-link">
              <BootstrapIcon name="calendar-check-fill" class="nav-icon" />
              <span class="nav-text">Hist. Presenças</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/student/pedidos" class="nav-link">
              <BootstrapIcon name="arrow-up-circle-fill" class="nav-icon" />
              <span class="nav-text">Pedidos de Saída</span>
            </NuxtLink>
          </li>
        </ul>

        <!-- ... (Menu Encarregado) ... -->
        <ul v-else-if="userData?.perfil === 3">
          <li>
            <NuxtLink to="/dashboard/foreman" class="nav-link">
              <BootstrapIcon name="house-fill" class="nav-icon" />
              <span class="nav-text">Home</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/foreman/students" class="nav-link">
              <BootstrapIcon name="people-fill" class="nav-icon" />
              <span class="nav-text">Meus Educandos</span>
            </NuxtLink>
          </li>
        </ul>
      </nav>

      <!-- **** MUDANÇA AQUI (Menus Inferiores Mobile) **** -->
      <div class="mt-4 border-t pt-4 border-gray-200 dark:border-gray-700 space-y-2">
        <NuxtLink v-if="profileLink" :to="profileLink" class="nav-link">
          <BootstrapIcon name="person-circle" class="nav-icon" />
          <span class="nav-text">Meu Perfil</span>
        </NuxtLink>
        <button @click="logout" class="nav-link w-full bg-red-100 dark:bg-red-800 text-red-700 dark:text-red-300">
          <BootstrapIcon name="box-arrow-right" class="nav-icon" />
          <span class="nav-text">Sair (Logout)</span>
        </button>
      </div>
    </aside>

    <!-- ... (Área de Conteúdo - sem alterações) ... -->
    <div class="flex-1 transition-all duration-300 ease-in-out" :class="isSidebarOpen ? 'md:ml-64' : 'md:ml-20'">
      <div class="container mx-auto p-8">
        <NuxtPage />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, provide, watch, computed } from 'vue' // <-- ADICIONE 'computed'

// Estado para controlar a sidebar (aberta ou encolhida/fechada)
const isSidebarOpen = ref(false)
function toggleSidebar() {
  isSidebarOpen.value = !isSidebarOpen.value
}

onMounted(() => {
  // Isto só corre no CLIENTE.
  // Assim que o cliente "acorda", ele abre a sidebar.
  // Isto evita o "mismatch" porque o servidor e o cliente
  // agora concordam no estado inicial (sidebar fechada).
  isSidebarOpen.value = true
})
definePageMeta({
  layout: 'default'
})

const { api } = useApi()
const { clearTokens } = useAuth()
const router = useRouter()

// 1. Buscar os dados do utilizador
const { data: userData, pending, error } = await useAsyncData(
  'userData',
  () => api<any>('/users/me/'),
  { lazy: true }
)

// 2. Fornecer os dados aos filhos
provide('userData', userData)
provide('pendingData', pending)

// 3. Observar por erros
watch(error, (newError) => {
  if (newError) {
    console.error('Erro ao buscar dados do dashboard:', newError)
  }
})

// 4. Função de Logout
async function logout() {
  clearTokens()
  await router.push('/')
}

// 5. ---- A SUA NOVA LÓGICA DE LINK DINÂMICO ----
// 'computed' reage a 'userData' quando ele carregar
const profileLink = computed(() => {
  if (!userData.value) return null

  const perfil = userData.value.perfil

  if (perfil === 1) {
    return '/dashboard/admin/me'
  } else if (perfil === 2) {
    return '/dashboard/student/me'
  } else if (perfil === 3) {
    return '/dashboard/foreman/me'
  }
  return null
})
</script>

<style scoped>
/* (Estilos existentes - não precisam de alterações) */
.nav-link {
  @apply flex items-center p-2 rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700;
}

.nav-icon {
  @apply w-6 h-6 flex-shrink-0;
}

.nav-text {
  @apply ml-3 whitespace-nowrap;
}

.router-link-exact-active {
  @apply bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 font-bold;
}
</style>

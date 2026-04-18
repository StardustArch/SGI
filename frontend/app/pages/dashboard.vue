<template>
  <div class="flex">
    <!-- Sidebar Desktop -->
    <aside
      class="fixed z-20 hidden md:flex flex-col min-h-screen bg-white dark:bg-slate-900 p-4 border-r border-slate-200 dark:border-slate-800 shadow-sm transition-all duration-300 ease-in-out"
      :class="[
        isSidebarOpen ? 'w-64' : 'w-20',
        { 'opacity-50 pointer-events-none select-none': userData?.precisa_mudar_senha }
      ]"
    >
      <div class="flex items-center" :class="isSidebarOpen ? 'justify-between' : 'justify-center'">
        <h2 v-if="isSidebarOpen" class="text-lg font-bold text-slate-900 dark:text-white">SGI</h2>
        <button @click="toggleSidebar" class="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
          <BootstrapIcon name="list" class="w-5 h-5 text-slate-600 dark:text-slate-400" />
        </button>
      </div>

      <div v-if="pending" class="text-slate-500 dark:text-slate-400 mt-4 text-sm">A carregar...</div>

      <nav class="flex-1 mt-6 space-y-1">
        <!-- Menu para GESTOR -->
        <ul v-if="perfilNome === 'Gestor'">
          <li><NuxtLink to="/dashboard/admin" class="nav-link"><BootstrapIcon name="house-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Visão Geral</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/students" class="nav-link"><BootstrapIcon name="people-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Gerir Estudantes</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/rooms" class="nav-link"><BootstrapIcon name="door-closed-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Gestão de Quartos</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/exits" class="nav-link"><BootstrapIcon name="door-open-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Triagem de Saídas</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/reports" class="nav-link"><BootstrapIcon name="bar-chart-line-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Relatórios</span></NuxtLink></li>
        </ul>

        <!-- Menu para FINANCEIRO -->
        <ul v-else-if="perfilNome === 'Financeiro'">
          <li><NuxtLink to="/dashboard/admin" class="nav-link"><BootstrapIcon name="house-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Visão Geral</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/finance" class="nav-link"><BootstrapIcon name="wallet-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Finanças</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/reports" class="nav-link"><BootstrapIcon name="bar-chart-line-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Relatórios Financeiros</span></NuxtLink></li>
        </ul>

        <!-- Menu para DISCIPLINAR -->
        <ul v-else-if="perfilNome === 'Disciplinar'">
          <li><NuxtLink to="/dashboard/admin" class="nav-link"><BootstrapIcon name="house-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Visão Geral</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/attendance" class="nav-link"><BootstrapIcon name="calendar-check-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Presenças</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/discipline" class="nav-link"><BootstrapIcon name="shield-exclamation" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Disciplina</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/reports" class="nav-link"><BootstrapIcon name="bar-chart-line-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Relatórios Disciplinares</span></NuxtLink></li>
        </ul>

        <!-- Menu para SUPORTE (acesso total) -->
        <ul v-else-if="perfilNome === 'Suporte'">
          <li><NuxtLink to="/dashboard/admin" class="nav-link"><BootstrapIcon name="house-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Visão Geral</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/students" class="nav-link"><BootstrapIcon name="people-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Gerir Estudantes</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/rooms" class="nav-link"><BootstrapIcon name="door-closed-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Gestão de Quartos</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/finance" class="nav-link"><BootstrapIcon name="wallet-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Finanças</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/attendance" class="nav-link"><BootstrapIcon name="calendar-check-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Presenças</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/exits" class="nav-link"><BootstrapIcon name="door-open-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Triagem de Saídas</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/discipline" class="nav-link"><BootstrapIcon name="shield-exclamation" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Disciplina</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/reports" class="nav-link"><BootstrapIcon name="bar-chart-line-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Relatórios</span></NuxtLink></li>
        </ul>

        <!-- Menu para ESTUDANTE -->
        <ul v-else-if="perfilNome === 'Estudante'">
          <li><NuxtLink to="/dashboard/student" class="nav-link"><BootstrapIcon name="house-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Visão Geral</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/student/me" class="nav-link"><BootstrapIcon name="cash-coin" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Hist. Financeiro</span></NuxtLink></li>
        </ul>

        <!-- Menu para ENCARREGADO -->
        <ul v-else-if="perfilNome === 'Encarregado'">
          <li><NuxtLink to="/dashboard/guardian" class="nav-link"><BootstrapIcon name="house-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Visão Geral</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/guardian/exits" class="nav-link"><BootstrapIcon name="arrow-up-circle-fill" class="nav-icon" /><span v-if="isSidebarOpen" class="nav-text">Pedidos de Saída</span></NuxtLink></li>
        </ul>
      </nav>

      <div class="mt-4 border-t border-slate-200 dark:border-slate-800 pt-4 space-y-1">
        <NuxtLink v-if="profileLink" :to="profileLink" class="nav-link">
          <BootstrapIcon name="person-circle" class="nav-icon" />
          <span v-if="isSidebarOpen" class="nav-text">Meu Perfil</span>
        </NuxtLink>

        <div class="py-1" :class="isSidebarOpen ? 'flex justify-end' : 'flex justify-center'">
          <ThemeToggle />
        </div>

        <button @click="logout" class="nav-link w-full !text-rose-600 dark:!text-rose-400 hover:!bg-rose-50 dark:hover:!bg-rose-900/20">
          <BootstrapIcon name="box-arrow-right" class="nav-icon" />
          <span v-if="isSidebarOpen" class="nav-text">Sair (Logout)</span>
        </button>
      </div>
    </aside>

    <!-- Versão Mobile Header -->
    <div class="md:hidden fixed top-0 left-0 right-0 z-10 bg-white/90 dark:bg-slate-900/90 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 h-16 px-4 flex items-center justify-between shadow-sm">
      <div class="flex items-center gap-3">
        <button @click="toggleSidebar" class="p-2 -ml-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 transition-colors">
          <BootstrapIcon name="list" class="w-6 h-6" />
        </button>
        <span class="font-semibold text-lg text-slate-900 dark:text-white">SGI Portal</span>
      </div>
    </div>

    <!-- Overlay Mobile -->
    <div v-if="isSidebarOpen" class="md:hidden fixed inset-0 z-20 bg-black/50" @click="isSidebarOpen = false"></div>

    <!-- Sidebar Mobile -->
    <aside
      class="md:hidden fixed z-30 top-0 left-0 min-h-screen bg-white dark:bg-slate-900 p-4 border-r border-slate-200 dark:border-slate-800 shadow-sm transition-all duration-300 ease-in-out w-64"
      :class="[
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full',
        { 'opacity-50 pointer-events-none select-none': userData?.precisa_mudar_senha }
      ]"
    >
      <div v-if="pending" class="text-slate-500 dark:text-slate-400 mt-4 text-sm">A carregar...</div>
      <nav class="flex-1 mt-6 space-y-1">
        <!-- Mesma estrutura condicional sem v-if="isSidebarOpen" -->
        <ul v-if="perfilNome === 'Gestor'">
          <li><NuxtLink to="/dashboard/admin" class="nav-link"><BootstrapIcon name="house-fill" class="nav-icon" /><span class="nav-text">Visão Geral</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/students" class="nav-link"><BootstrapIcon name="people-fill" class="nav-icon" /><span class="nav-text">Gerir Estudantes</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/rooms" class="nav-link"><BootstrapIcon name="door-closed-fill" class="nav-icon" /><span class="nav-text">Gestão de Quartos</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/exits" class="nav-link"><BootstrapIcon name="door-open-fill" class="nav-icon" /><span class="nav-text">Triagem de Saídas</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/reports" class="nav-link"><BootstrapIcon name="bar-chart-line-fill" class="nav-icon" /><span class="nav-text">Relatórios</span></NuxtLink></li>
        </ul>
        <ul v-else-if="perfilNome === 'Financeiro'">
          <li><NuxtLink to="/dashboard/admin" class="nav-link"><BootstrapIcon name="house-fill" class="nav-icon" /><span class="nav-text">Visão Geral</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/finance" class="nav-link"><BootstrapIcon name="wallet-fill" class="nav-icon" /><span class="nav-text">Finanças</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/reports" class="nav-link"><BootstrapIcon name="bar-chart-line-fill" class="nav-icon" /><span class="nav-text">Relatórios Financeiros</span></NuxtLink></li>
        </ul>
        <ul v-else-if="perfilNome === 'Disciplinar'">
          <li><NuxtLink to="/dashboard/admin" class="nav-link"><BootstrapIcon name="house-fill" class="nav-icon" /><span class="nav-text">Visão Geral</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/attendance" class="nav-link"><BootstrapIcon name="calendar-check-fill" class="nav-icon" /><span class="nav-text">Presenças</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/discipline" class="nav-link"><BootstrapIcon name="shield-exclamation" class="nav-icon" /><span class="nav-text">Disciplina</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/reports" class="nav-link"><BootstrapIcon name="bar-chart-line-fill" class="nav-icon" /><span class="nav-text">Relatórios Disciplinares</span></NuxtLink></li>
        </ul>
        <ul v-else-if="perfilNome === 'Suporte'">
          <li><NuxtLink to="/dashboard/admin" class="nav-link"><BootstrapIcon name="house-fill" class="nav-icon" /><span class="nav-text">Visão Geral</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/students" class="nav-link"><BootstrapIcon name="people-fill" class="nav-icon" /><span class="nav-text">Gerir Estudantes</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/rooms" class="nav-link"><BootstrapIcon name="door-closed-fill" class="nav-icon" /><span class="nav-text">Gestão de Quartos</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/finance" class="nav-link"><BootstrapIcon name="wallet-fill" class="nav-icon" /><span class="nav-text">Finanças</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/attendance" class="nav-link"><BootstrapIcon name="calendar-check-fill" class="nav-icon" /><span class="nav-text">Presenças</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/exits" class="nav-link"><BootstrapIcon name="door-open-fill" class="nav-icon" /><span class="nav-text">Triagem de Saídas</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/discipline" class="nav-link"><BootstrapIcon name="shield-exclamation" class="nav-icon" /><span class="nav-text">Disciplina</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/admin/reports" class="nav-link"><BootstrapIcon name="bar-chart-line-fill" class="nav-icon" /><span class="nav-text">Relatórios</span></NuxtLink></li>
        </ul>
        <ul v-else-if="perfilNome === 'Estudante'">
          <li><NuxtLink to="/dashboard/student" class="nav-link"><BootstrapIcon name="house-fill" class="nav-icon" /><span class="nav-text">Visão Geral</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/student/me" class="nav-link"><BootstrapIcon name="cash-coin" class="nav-icon" /><span class="nav-text">Hist. Financeiro</span></NuxtLink></li>
        </ul>
        <ul v-else-if="perfilNome === 'Encarregado'">
          <li><NuxtLink to="/dashboard/guardian" class="nav-link"><BootstrapIcon name="house-fill" class="nav-icon" /><span class="nav-text">Visão Geral</span></NuxtLink></li>
          <li><NuxtLink to="/dashboard/guardian/exits" class="nav-link"><BootstrapIcon name="arrow-up-circle-fill" class="nav-icon" /><span class="nav-text">Pedidos de Saída</span></NuxtLink></li>
        </ul>
      </nav>

      <div class="mt-4 border-t border-slate-200 dark:border-slate-800 pt-4 space-y-1">
        <NuxtLink v-if="profileLink" :to="profileLink" class="nav-link">
          <BootstrapIcon name="person-circle" class="nav-icon" />
          <span class="nav-text">Meu Perfil</span>
        </NuxtLink>
        <button @click="logout" class="nav-link w-full !text-rose-600 dark:!text-rose-400 hover:!bg-rose-50 dark:hover:!bg-rose-900/20">
          <BootstrapIcon name="box-arrow-right" class="nav-icon" />
          <span class="nav-text">Sair (Logout)</span>
        </button>
      </div>
    </aside>

    <!-- Conteúdo principal -->
    <div class="flex-1 ml-0 w-full overflow-x-hidden transition-all duration-300 ease-in-out" :class="isSidebarOpen ? 'md:ml-64' : 'md:ml-20'">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8 pt-24 md:pt-8">
        <NuxtPage />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, provide, watch, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const isSidebarOpen = ref(false)

function toggleSidebar() {
  isSidebarOpen.value = !isSidebarOpen.value
}

onMounted(() => {
  isSidebarOpen.value = true
})

definePageMeta({
  layout: 'default'
})

const { api } = useApi()
const { clearTokens } = useAuth()

const { data: userData, pending, error } = await useAsyncData(
  'userData',
  () => api<any>('/users/me/'),
  { lazy: true }
)

provide('userData', userData)
provide('pendingData', pending)

watch(error, (newError) => {
  if (newError) {
    console.error('Erro ao buscar dados do dashboard:', newError)
  }
})

async function logout() {
  clearTokens()
  await router.push('/')
}

const perfilNome = computed(() => userData.value?.perfil_nome)

const profileLink = computed(() => {
  if (!userData.value) return null
  const perfil = perfilNome.value
  if (perfil === 'Gestor' || perfil === 'Financeiro' || perfil === 'Disciplinar' || perfil === 'Suporte') {
    return '/dashboard/admin/me'
  } else if (perfil === 'Estudante') {
    return '/dashboard/student/me/security'
  } else if (perfil === 'Encarregado') {
    return '/dashboard/guardian/me'
  }
  return null
})

// Redireciona para página de perfil se a senha for a padrão
watch([userData, () => route.path], ([newUser, newPath]) => {
  if (!newUser) return

  if (newUser.precisa_mudar_senha) {
    let perfilDestino = ''
    const perfil = perfilNome.value
    if (perfil === 'Gestor' || perfil === 'Financeiro' || perfil === 'Disciplinar' || perfil === 'Suporte') {
      perfilDestino = '/dashboard/admin/me'
    } else if (perfil === 'Estudante') {
      perfilDestino = '/dashboard/student/me'
    } else if (perfil === 'Encarregado') {
      perfilDestino = '/dashboard/guardian/me'
    }

    if (perfilDestino && newPath !== perfilDestino) {
      console.warn("⚠️ Segurança: Mudança de senha obrigatória.")
      router.replace(perfilDestino)
    }
  }
}, { immediate: true })
</script>

<style scoped>
.nav-link {
  @apply flex items-center p-2.5 rounded-lg text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors;
}
.nav-icon {
  @apply w-5 h-5 flex-shrink-0;
}
.nav-text {
  @apply ml-3 text-sm font-medium whitespace-nowrap;
}
.router-link-exact-active {
  @apply bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 border-l-2 border-blue-600 dark:border-blue-400;
}
</style>
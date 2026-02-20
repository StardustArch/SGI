<template>
  <div class="flex">

<aside
  class="fixed z-20 hidden md:flex flex-col min-h-screen bg-white p-4 shadow-lg dark:bg-gray-800 transition-all duration-300 ease-in-out"
  :class="[
    isSidebarOpen ? 'w-64' : 'w-20',
    { 'opacity-50 pointer-events-none select-none': userData?.precisa_mudar_senha }
  ]"
>
      
      <div class="flex items-center" :class="isSidebarOpen ? 'justify-between' : 'justify-center'">
        <h2 v-if="isSidebarOpen" class="text-lg font-bold dark:text-white">SGI</h2>
        <button @click="toggleSidebar" class="p-2 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700">
          <BootstrapIcon name="list" class="w-6 h-6 dark:text-white" />
        </button>
      </div>

      <div v-if="pending" class="text-gray-500 dark:text-gray-400 mt-4">A carregar...</div>

      <nav class="flex-1 mt-6 space-y-2">

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
            <NuxtLink to="/dashboard/admin/students" class="nav-link">
              <BootstrapIcon name="people-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Gerir Estudantes</span>
            </NuxtLink>
          </li>
        </ul>

        <ul v-else-if="userData?.perfil === 2">
          <li>
            <NuxtLink to="/dashboard/student" class="nav-link">
              <BootstrapIcon name="house-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Visão Geral</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/student/finance" class="nav-link">
              <BootstrapIcon name="cash-coin" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Hist. Financeiro</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/student/discipline" class="nav-link">
              <BootstrapIcon name="info-circle-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Hist. Disciplinar</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/student/attendance" class="nav-link">
              <BootstrapIcon name="calendar-check-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Hist. Presenças</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/student/exits" class="nav-link">
              <BootstrapIcon name="arrow-up-circle-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Pedidos de Saída</span>
            </NuxtLink>
          </li>
        </ul>

        <ul v-else-if="userData?.perfil === 3">
          <li>
            <NuxtLink to="/dashboard/guardian" class="nav-link">
              <BootstrapIcon name="house-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Visão Geral</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/guardian/finance" class="nav-link">
              <BootstrapIcon name="cash-coin" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Hist. Financeiro</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/guardian/discipline" class="nav-link">
              <BootstrapIcon name="info-circle-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Hist. Disciplinar</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/guardian/attendance" class="nav-link">
              <BootstrapIcon name="calendar-check-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Hist. Presenças</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/guardian/exits" class="nav-link">
              <BootstrapIcon name="arrow-up-circle-fill" class="nav-icon" />
              <span v-if="isSidebarOpen" class="nav-text">Pedidos de Saída</span>
            </NuxtLink>
          </li>
        </ul>

      </nav>

      <div class="mt-4 border-t pt-4 border-gray-200 dark:border-gray-700 space-y-2">
        <NuxtLink v-if="profileLink" :to="profileLink" class="nav-link">
          <BootstrapIcon name="person-circle" class="nav-icon" />
          <span v-if="isSidebarOpen" class="nav-text">Meu Perfil</span>
        </NuxtLink>

        <div class="py-2" :class="isSidebarOpen ? 'flex justify-end' : 'flex justify-center'">
          <ThemeToggle />
        </div>

        <button @click="logout" class="nav-link w-full bg-red-100 dark:bg-red-800 text-red-700 dark:text-red-300">
          <BootstrapIcon name="box-arrow-right" class="nav-icon" />
          <span v-if="isSidebarOpen" class="nav-text">Sair (Logout)</span>
        </button>
      </div>

    </aside>

<div class="md:hidden fixed top-0 left-0 right-0 z-10 bg-white/90 dark:bg-gray-900/90 backdrop-blur-md border-b border-gray-200 dark:border-gray-800 h-16 px-4 flex items-center justify-between shadow-sm">
      <div class="flex items-center gap-3">
        <button @click="toggleSidebar" class="p-2 -ml-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-white transition-colors">
          <BootstrapIcon name="list" class="w-7 h-7" />
        </button>
        <span class="font-bold text-lg text-gray-800 dark:text-white tracking-tight">SGI Portal</span>
      </div>
      </div>

    <div v-if="isSidebarOpen" class="md:hidden fixed inset-0 z-20 bg-black/50" @click="isSidebarOpen = false"></div>
    
<aside
  class="md:hidden fixed z-30 top-0 left-0 min-h-screen bg-white p-4 shadow-lg dark:bg-gray-800 transition-all duration-300 ease-in-out w-64"
  :class="[
    isSidebarOpen ? 'translate-x-0' : '-translate-x-full',
    { 'opacity-50 pointer-events-none select-none': userData?.precisa_mudar_senha }
  ]"
>
      
      <div v-if="pending" class="text-gray-500 dark:text-gray-400 mt-4">A carregar...</div>

      <nav class="flex-1 mt-6 space-y-2">
        
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

        <ul v-else-if="userData?.perfil === 2">
          <li>
            <NuxtLink to="/dashboard/student" class="nav-link">
              <BootstrapIcon name="house-fill" class="nav-icon" />
              <span class="nav-text">Visão Geral</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/student/finance" class="nav-link">
              <BootstrapIcon name="cash-coin" class="nav-icon" />
              <span class="nav-text">Hist. Financeiro</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/student/discipline" class="nav-link">
              <BootstrapIcon name="info-circle-fill" class="nav-icon" />
              <span class="nav-text">Hist. Disciplinar</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/student/attendance" class="nav-link">
              <BootstrapIcon name="calendar-check-fill" class="nav-icon" />
              <span class="nav-text">Hist. Presenças</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/student/exits" class="nav-link">
              <BootstrapIcon name="arrow-up-circle-fill" class="nav-icon" />
              <span class="nav-text">Pedidos de Saída</span>
            </NuxtLink>
          </li>
        </ul>

        <ul v-else-if="userData?.perfil === 3">
          <li>
            <NuxtLink to="/dashboard/guardian" class="nav-link">
              <BootstrapIcon name="house-fill" class="nav-icon" />
              <span class="nav-text">Visão Geral</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/guardian/finance" class="nav-link">
              <BootstrapIcon name="cash-coin" class="nav-icon" />
              <span class="nav-text">Hist. Financeiro</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/guardian/discipline" class="nav-link">
              <BootstrapIcon name="info-circle-fill" class="nav-icon" />
              <span class="nav-text">Hist. Disciplinar</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/guardian/attendance" class="nav-link">
              <BootstrapIcon name="calendar-check-fill" class="nav-icon" />
              <span class="nav-text">Hist. Presenças</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/dashboard/guardian/exits" class="nav-link">
              <BootstrapIcon name="arrow-up-circle-fill" class="nav-icon" />
              <span class="nav-text">Pedidos de Saída</span>
            </NuxtLink>
          </li>
        </ul>

      </nav>

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

<div class="flex-1 ml-0 w-full overflow-x-hidden transition-all duration-300 ease-in-out" :class="isSidebarOpen ? 'md:ml-64' : 'md:ml-20'">
  <div class="container mx-auto p-4 pt-24 md:p-8 md:pt-8"> <NuxtPage />
  </div>
</div>
  </div>
</template>

<script setup lang="ts">
import { ref, provide, watch, computed } from 'vue'




// 1. Obter rota atual para verificar onde estamos
const route = useRoute()

// 2. O Watcher de Segurança (Adiciona isto logo após o provide)

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
const router = useRouter()

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

const profileLink = computed(() => {
  if (!userData.value) return null

  const perfil = userData.value.perfil

  if (perfil === 1) {
    return '/dashboard/admin/me'
  } else if (perfil === 2) {
    return '/dashboard/student/me'
  } else if (perfil === 3) {
    // CORRIGIDO: Aponta para 'profile.vue' que criámos para o encarregado
    return '/dashboard/guardian/me'
  }
  return null
})

watch([userData, () => route.path], ([newUser, newPath]) => {
  if (!newUser) return

  // SE a senha for a padrão E não estivermos já na página de perfil...
  if (newUser.precisa_mudar_senha) {
    
    // Define qual é a página de perfil correta baseada no tipo de utilizador
    let perfilDestino = ''
    if (newUser.perfil === 1) perfilDestino = '/dashboard/admin/me'
    else if (newUser.perfil === 2) perfilDestino = '/dashboard/student/me'
    else if (newUser.perfil === 3) perfilDestino = '/dashboard/guardian/me' // A nossa nova página
    
    // Se não estivermos lá, força o redirecionamento
    if (newPath !== perfilDestino) {
      console.warn("⚠️ Segurança: Mudança de senha obrigatória.")
      router.replace(perfilDestino)
      
      // Opcional: Mostrar um alerta/toast ao utilizador
      // alert("Por motivos de segurança, deve alterar a sua senha inicial antes de continuar.")
    }
  }
}, { immediate: true })


</script>

<style scoped>
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
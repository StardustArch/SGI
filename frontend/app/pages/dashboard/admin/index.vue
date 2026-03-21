<template>
  <div class="space-y-8 dark:text-white max-w-8xl mx-auto p-4 md:p-8">
    <div>
      <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">
        Dashboard {{ perfil }}
      </h1>
      <p class="text-stone-500 dark:text-gray-400 mt-1">
        Visão geral {{ getDescription() }}
      </p>
    </div>

    <!-- Seção Administrativa (Gestor e Suporte) -->
    <div v-if="dashboard?.administrative" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-blue-50 dark:bg-blue-900/30 rounded-2xl text-blue-600">
            <BootstrapIcon name="people" class="w-8 h-8" />
          </div>
          <div>
            <p class="text-stone-500 text-xs font-bold uppercase tracking-wider">Alunos Activos</p>
            <h3 class="text-2xl font-bold">{{ dashboard.administrative.total_estudantes_ativos }}</h3>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-emerald-50 dark:bg-emerald-900/30 rounded-2xl text-emerald-600">
            <BootstrapIcon name="door-closed" class="w-8 h-8" />
          </div>
          <div>
            <p class="text-stone-500 text-xs font-bold uppercase tracking-wider">Ocupação de Quartos</p>
            <h3 class="text-2xl font-bold">{{ dashboard.administrative.total_ocupadas }} / {{ dashboard.administrative.total_vagas }}</h3>
            <p class="text-xs text-stone-400">{{ dashboard.administrative.vagas_disponiveis }} vagas livres</p>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-amber-50 dark:bg-amber-900/30 rounded-2xl text-amber-600">
            <BootstrapIcon name="clock-history" class="w-8 h-8" />
          </div>
          <div>
            <p class="text-stone-500 text-xs font-bold uppercase tracking-wider">Pedidos de Saída</p>
            <h3 class="text-2xl font-bold text-amber-600">{{ dashboard.administrative.pedidos_saida_pendentes }}</h3>
            <p class="text-xs">pendentes</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Seção Financeira (Financeiro e Suporte) -->
    <div v-if="dashboard?.finance" class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-emerald-50 dark:bg-emerald-900/30 rounded-2xl text-emerald-600">
            <BootstrapIcon name="cash-coin" class="w-8 h-8" />
          </div>
          <div>
            <p class="text-stone-500 text-xs font-bold uppercase tracking-wider">Arrecadado (Mês)</p>
            <h3 class="text-2xl font-bold">{{ formatMoeda(dashboard.finance.total_arrecadado_mes) }}</h3>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-amber-50 dark:bg-amber-900/30 rounded-2xl text-amber-600">
            <BootstrapIcon name="hourglass-split" class="w-8 h-8" />
          </div>
          <div>
            <p class="text-stone-500 text-xs font-bold uppercase tracking-wider">Pendentes</p>
            <h3 class="text-2xl font-bold">{{ dashboard.finance.total_estudantes_pendentes }} <span class="text-sm font-normal text-stone-400">Alunos</span></h3>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-rose-50 dark:bg-rose-900/30 rounded-2xl text-rose-600">
            <BootstrapIcon name="exclamation-circle" class="w-8 h-8" />
          </div>
          <div>
            <p class="text-stone-500 text-xs font-bold uppercase tracking-wider">Em Atraso</p>
            <h3 class="text-2xl font-bold text-rose-500">{{ dashboard.finance.total_estudantes_atraso || 0 }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- Seção Disciplinar (Disciplinar e Suporte) -->
    <div v-if="dashboard?.discipline" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white dark:bg-gray-800 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm p-6">
        <h3 class="font-bold text-lg mb-4 flex items-center gap-2">
          <BootstrapIcon name="exclamation-triangle" class="text-rose-500" />
          Top Infratores (mês)
        </h3>
        <div v-if="dashboard.discipline.top_infratores?.length" class="space-y-3">
          <div v-for="item in dashboard.discipline.top_infratores" :key="item.estudante_id" class="flex justify-between items-center border-b dark:border-gray-700 pb-2">
            <span class="font-medium">{{ item.estudante__nome_completo }}</span>
            <span class="text-rose-500 font-bold">{{ item.total }} sanção(ões)</span>
          </div>
        </div>
        <p v-else class="text-stone-400 text-sm">Nenhuma sanção registada este mês.</p>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm p-6">
        <h3 class="font-bold text-lg mb-4 flex items-center gap-2">
          <BootstrapIcon name="person-dash" class="text-amber-500" />
          Maiores Ausências (mês)
        </h3>
        <div v-if="dashboard.discipline.top_ausentes?.length" class="space-y-3">
          <div v-for="item in dashboard.discipline.top_ausentes" :key="item.estudante_id" class="flex justify-between items-center border-b dark:border-gray-700 pb-2">
            <span class="font-medium">{{ item.estudante__nome_completo }}</span>
            <span class="text-amber-500 font-bold">{{ item.total }} ausência(s)</span>
          </div>
        </div>
        <p v-else class="text-stone-400 text-sm">Nenhuma ausência registada este mês.</p>
      </div>
    </div>

    <!-- Gráfico de sanções por tipo (apenas disciplinares) -->
    <div v-if="dashboard?.discipline?.sancao_por_tipo?.length" class="bg-white dark:bg-gray-800 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm p-6">
      <h3 class="font-bold text-lg mb-4">Sanções por Tipo (mês)</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div v-for="tipo in dashboard.discipline.sancao_por_tipo" :key="tipo.tipo_sancao" class="bg-stone-50 dark:bg-gray-700 p-3 rounded-xl text-center">
          <p class="font-bold text-2xl text-rose-500">{{ tipo.total }}</p>
          <p class="text-xs">{{ tipo.tipo_sancao }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
const { api } = useApi()
const { accessToken, isLoggedIn } = useAuth()

// 1. Buscar dados do utilizador logado
const { data: user, pending: userPending } = await useAsyncData(
  'user-profile',
  () => api<any>('/users/me/'),
  { server: false }
)

const perfil = computed(() => user.value?.perfil_nome || null)
console.log(perfil)
// 2. Buscar dashboard (só executar se perfil for administrativo)
//    Mas se não for, dashboard fica undefined e o template usa optional chaining.
const { data: dashboard, pending: dashboardPending, error } = await useAsyncData(
  'admin-dashboard',
  () => api<any>('/admin/dashboard/'),
  {
    // só executar se o utilizador tiver perfil administrativo
    immediate: !!perfil.value && ['Gestor', 'Financeiro', 'Disciplinar', 'Suporte'].includes(perfil.value)
  }
)
console.log(dashboard.value)

// Helper para descrição (já trata undefined)
const getDescription = () => {
  const d = dashboard.value
  if (!d) return ''
  if (d.administrative) return 'dos dados administrativos (ocupação, alunos, pedidos).'
  if (d.finance) return 'do fluxo financeiro (receitas, pendências, atrasos).'
  if (d.discipline) return 'do comportamento (sanções, ausências).'
  return ''
}

const formatMoeda = (valor: any) => new Intl.NumberFormat('pt-MZ', { style: 'currency', currency: 'MZN' }).format(Number(valor))
</script>
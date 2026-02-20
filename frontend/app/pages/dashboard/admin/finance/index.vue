<template>
  <div class="space-y-8 dark:text-white max-w-8xl mx-auto p-4 md:p-8">
    
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Gestão Financeira</h1>
        <p class="text-stone-500 dark:text-gray-400 mt-1 text-lg">Controlo de mensalidades e fluxos de caixa.</p>
      </div>

      <div class="flex gap-3 w-full md:w-auto">
        <NuxtLink to="/dashboard/admin/finance/generate" class="flex-1 md:flex-none px-6 py-3 rounded-xl bg-gray-900 dark:bg-white text-white dark:text-gray-900 font-bold text-sm hover:opacity-90 transition-all flex items-center justify-center gap-2 shadow-lg">
          <BootstrapIcon name="plus-circle" /> Gerar Lote
        </NuxtLink>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-emerald-50 dark:bg-emerald-900/30 rounded-2xl text-emerald-600">
            <BootstrapIcon name="cash-coin" class="w-8 h-8" />
          </div>
          <div>
            <p class="text-stone-500 text-xs font-bold uppercase tracking-wider">Arrecadado (Mês)</p>
            <h3 class="text-2xl font-bold">{{ formatMoeda(stats?.total_arrecadado || 0) }}</h3>
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
            <h3 class="text-2xl font-bold">{{ stats?.total_pendentes || 0 }} <span class="text-sm font-normal text-stone-400">Alunos</span></h3>
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
            <h3 class="text-2xl font-bold text-rose-500">{{ stats?.total_atraso || 0 }}</h3>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-stone-50 dark:bg-gray-800/50 p-4 rounded-[1.5rem] border border-stone-100 dark:border-gray-700 flex flex-col md:flex-row gap-4">
      <div class="flex-1 relative">
        <BootstrapIcon name="search" class="absolute left-4 top-1/2 -translate-y-1/2 text-stone-400" />
        <input 
          v-model="pesquisa" 
          type="text" 
          placeholder="Pesquisar por aluno ou número..." 
          class="w-full pl-12 pr-4 py-3 bg-white dark:bg-gray-800 border border-stone-200 dark:border-gray-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-rose-200"
        />
      </div>
      <select v-model="filtroEstado" class="bg-white dark:bg-gray-800 border border-stone-200 dark:border-gray-700 rounded-xl px-4 py-3 outline-none">
        <option :value="null">Todos os Estados</option>
        <option value="Pendente">Pendentes</option>
        <option value="Pago">Pagos</option>
        <option value="Atraso">Em Atraso</option>
      </select>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-[2rem] border border-stone-100 dark:border-gray-700 overflow-hidden shadow-sm">
      <table class="w-full text-left border-collapse">
        <thead class="bg-stone-50 dark:bg-gray-700/50">
          <tr>
            <th class="p-5 text-xs font-bold text-stone-400 uppercase">Estudante</th>
            <th class="p-5 text-xs font-bold text-stone-400 uppercase">Mês Ref.</th>
            <th class="p-5 text-xs font-bold text-stone-400 uppercase">Estado</th>
            <th class="p-5 text-xs font-bold text-stone-400 uppercase">Ação</th>
          </tr>
        </thead>
        <tbody class="divide-y dark:divide-gray-700">
          <tr v-for="item in mensalidades" :key="item.id" class="hover:bg-stone-50/50 dark:hover:bg-gray-700/30 transition-colors">
            <td class="p-5 font-bold text-gray-800 dark:text-white">
               {{ item.nome_estudante }}
               <p class="text-[10px] text-stone-400 font-normal">Nº: {{ item.num_estudante }}</p>
            </td>
            <td class="p-5 text-sm text-stone-500 capitalize">{{ formatMes(item.mes_referencia) }}</td>
            <td class="p-5">
              <span :class="['px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border', getStatusBadge(item.estado)]">
                {{ item.estado }}
              </span>
            </td>
            <td class="p-5">
              <NuxtLink 
                :to="`/dashboard/admin/financas/confirmar/${item.id}`"
                class="text-xs font-bold text-rose-500 hover:text-rose-700 underline"
              >
                Detalhes / Confirmar
              </NuxtLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
const { api } = useApi()

// Estados Reativos
const pesquisa = ref('')
const filtroEstado = ref<string | null>(null)

// 1. Buscar Resumo (Stats)
const { data: stats } = await useAsyncData('admin-fin-stats', () => api<any>('/admin/financeiro/sumario/'))

// 2. Buscar Mensalidades (Paginado e Filtrado)
const { data: mensalidades } = await useAsyncData(
  'admin-fin-list', 
  () => api<any[]>('/admin/financeiro/mensalidades/'), // Endpoint que o Admin usa para ver tudo
  { watch: [pesquisa, filtroEstado] }
)

// Helpers Visuais
const getStatusBadge = (estado: string) => {
  if (estado === 'Pago') return 'bg-emerald-50 text-emerald-700 border-emerald-100 dark:bg-emerald-900/30 dark:text-emerald-300'
  if (estado === 'Atraso') return 'bg-rose-50 text-rose-700 border-rose-100'
  return 'bg-amber-50 text-amber-700 border-amber-100'
}

const formatMoeda = (valor: any) => new Intl.NumberFormat('pt-MZ', { style: 'currency', currency: 'MZN' }).format(Number(valor))
const formatMes = (data: string) => new Date(data).toLocaleDateString('pt-PT', { month: 'long', year: 'numeric' })
</script>
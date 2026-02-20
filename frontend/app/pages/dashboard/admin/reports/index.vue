<template>
  <div class="space-y-8 dark:text-white max-w-8xl mx-auto p-4 md:p-8">
    
    <div>
      <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Relatórios & Insights</h1>
      <p class="text-stone-500 dark:text-gray-400 mt-1 text-lg">Visão global da saúde financeira e disciplinar do internato.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="stat-card bg-emerald-50 dark:bg-emerald-900/10 border-emerald-100">
        <p class="stat-label text-emerald-600">Receita Estimada (Mês)</p>
        <h3 class="stat-value">{{ formatMoeda(financeiro?.total_arrecadado_mes || 0) }}</h3>
        <div class="mt-2 text-[10px] font-bold text-emerald-500 uppercase">↑ 12% vs mês anterior</div>
      </div>

      <div class="stat-card bg-rose-50 dark:bg-rose-900/10 border-rose-100">
        <p class="stat-label text-rose-600">Saídas Ativas</p>
        <h3 class="stat-value">{{ saidas?.total_aprovados || 0 }}</h3>
        <div class="mt-2 text-[10px] font-bold text-rose-400 uppercase">Alunos fora do recinto</div>
      </div>

      <div class="stat-card bg-amber-50 dark:bg-amber-900/10 border-amber-100">
        <p class="stat-label text-amber-600">Taxa de Inadimplência</p>
        <h3 class="stat-value">{{ financeiro?.total_estudantes_pendentes || 0 }}</h3>
        <div class="mt-2 text-[10px] font-bold text-amber-500 uppercase">Mensalidades em falta</div>
      </div>

      <div class="stat-card bg-violet-50 dark:bg-violet-900/10 border-violet-100">
        <p class="stat-label text-violet-600">Média de Assiduidade</p>
        <h3 class="stat-value">94%</h3>
        <div class="mt-2 text-[10px] font-bold text-violet-400 uppercase">Presença nos estudos</div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      
      <div class="bg-white dark:bg-gray-800 rounded-[2rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm">
        <h3 class="text-lg font-bold mb-6 flex items-center gap-2">
          <BootstrapIcon name="shield-lock-fill" class="text-rose-500" />
          Top 5 Infratores (Mês)
        </h3>
        <div class="space-y-4">
          <div v-for="(inf, index) in infratores" :key="index" class="flex items-center gap-4">
            <span class="text-sm font-bold text-stone-300">#{{ index + 1 }}</span>
            <div class="flex-1">
              <div class="flex justify-between mb-1">
                <span class="text-sm font-bold">{{ inf.nome_completo }}</span>
                <span class="text-xs font-bold text-rose-500">{{ inf.total_sancoes }} sanções</span>
              </div>
              <div class="w-full bg-stone-100 dark:bg-gray-700 h-2 rounded-full overflow-hidden">
                <div class="bg-rose-500 h-full" :style="{ width: (inf.total_sancoes * 20) + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-[2rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm">
        <h3 class="text-lg font-bold mb-6 flex items-center gap-2">
          <BootstrapIcon name="calendar-x-fill" class="text-amber-500" />
          Maiores Ausências (Estudo)
        </h3>
        <div class="space-y-4">
          <div v-for="(aus, index) in ausentes" :key="index" class="flex items-center gap-4">
            <span class="text-sm font-bold text-stone-300">#{{ index + 1 }}</span>
            <div class="flex-1">
              <div class="flex justify-between mb-1">
                <span class="text-sm font-bold">{{ aus.nome_completo }}</span>
                <span class="text-xs font-bold text-amber-500">{{ aus.total_ausencias }} faltas</span>
              </div>
              <div class="w-full bg-stone-100 dark:bg-gray-700 h-2 rounded-full overflow-hidden">
                <div class="bg-amber-500 h-full" :style="{ width: (aus.total_ausencias * 10) + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
const { api } = useApi()

// Fetch de múltiplos relatórios em paralelo
const { data: stats } = await useAsyncData('admin-global-stats', async () => {
  const [financeiro, infratores, ausentes, saidas] = await Promise.all([
    api<any>('/admin/financeiro/sumario/'),
    api<any[]>('/admin/relatorios/top-infratores/'),
    api<any[]>('/admin/relatorios/top-ausentes/'),
    api<any>('/admin/relatorios/saidas-sumario/')
  ])
  return { financeiro, infratores, ausentes, saidas }
})

const financeiro = computed(() => stats.value?.financeiro)
const infratores = computed(() => stats.value?.infratores || [])
const ausentes = computed(() => stats.value?.ausentes || [])
const saidas = computed(() => stats.value?.saidas)

const formatMoeda = (v: any) => new Intl.NumberFormat('pt-MZ', { style: 'currency', currency: 'MZN' }).format(Number(v))
</script>

<style scoped>
.stat-card {
  @apply p-6 rounded-[2rem] border shadow-sm relative overflow-hidden;
}
.stat-label {
  @apply text-[10px] font-black uppercase tracking-widest mb-1 opacity-70;
}
.stat-value {
  @apply text-3xl font-black text-gray-900 dark:text-white;
}
</style>
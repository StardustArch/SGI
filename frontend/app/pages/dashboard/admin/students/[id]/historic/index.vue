<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
      <div class="flex items-center gap-3">
        <NuxtLink 
          :to="`/dashboard/admin/students/${route.params.id}`" 
          class="p-2 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-700 dark:hover:text-slate-300 transition shadow-sm"
        >
          <BootstrapIcon name="arrow-left" class="w-5 h-5" />
        </NuxtLink>
        <div>
          <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">{{ estudante?.nome_completo }}</h1>
          <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400 uppercase tracking-wide mt-0.5">Dossiê Completo de Interno</p>
        </div>
      </div>

      <span :class="[
        'px-3 py-1.5 rounded-lg text-xs font-medium border',
        estudante?.estado === 'Activo' 
          ? 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30' 
          : 'bg-red-50 text-red-700 border-red-200 dark:bg-red-900/20 dark:text-red-400 dark:border-red-800/30'
      ]">
        Status: {{ estudante?.estado }}
      </span>
    </div>

    <!-- Abas -->
    <div class="flex p-1 bg-slate-100 dark:bg-slate-800 rounded-xl overflow-x-auto max-w-full no-scrollbar mb-6">
      <button 
        v-for="tab in ['Financeiro', 'Disciplina', 'Presenças', 'Saídas']" 
        :key="tab"
        @click="activeTab = tab"
        :class="[
          'px-5 sm:px-6 py-2.5 rounded-lg text-sm font-medium transition-all whitespace-nowrap',
          activeTab === tab 
            ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-white shadow-sm' 
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
        ]"
      >
        {{ tab }}
      </button>
    </div>

    <!-- Loading -->
    <div v-if="pending" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="i in 6" :key="i" class="h-32 bg-slate-100 dark:bg-slate-800 animate-pulse rounded-xl"></div>
    </div>

    <!-- Conteúdo das abas -->
    <div v-else class="mt-6">
      
      <!-- Aba Financeiro -->
      <div v-if="activeTab === 'Financeiro'" class="space-y-4">
        <div v-if="mensalidades.length === 0" class="text-center py-16 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800">
          <BootstrapIcon name="cash-coin" class="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-3" />
          <p class="text-slate-500 dark:text-slate-400">Nenhuma mensalidade encontrada.</p>
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div 
            v-for="pag in mensalidades" 
            :key="pag.id" 
            class="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow"
          >
            <p class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase mb-2">
              {{ formatMes(pag.mes_referencia) }} • {{ pag.tipo || 'Mensalidade' }}
            </p>
            <h4 class="text-xl font-bold text-slate-900 dark:text-white mb-3">{{ formatMoeda(pag.valor_pago || 25000) }}</h4>
            <span :class="[
              'px-2.5 py-0.5 rounded-md text-xs font-medium border',
              pag.estado === 'Pago' 
                ? 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30' 
                : 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-900/20 dark:text-amber-400 dark:border-amber-800/30'
            ]">
              {{ pag.estado }}
            </span>
          </div>
        </div>
      </div>

      <!-- Aba Disciplina -->
      <div v-if="activeTab === 'Disciplina'" class="space-y-3">
        <div v-if="sancoes.length === 0" class="text-center py-16 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800">
          <BootstrapIcon name="emoji-smile" class="w-12 h-12 text-emerald-400 dark:text-emerald-500 mx-auto mb-3" />
          <p class="text-slate-500 dark:text-slate-400">Sem registos disciplinares. Comportamento exemplar.</p>
        </div>
        <div 
          v-for="s in sancoes" 
          :key="s.id" 
          class="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col sm:flex-row gap-4"
        >
          <div class="sm:border-r border-slate-200 dark:border-slate-700 sm:pr-5 shrink-0 text-center sm:text-left">
            <span class="block text-2xl font-bold text-rose-600 dark:text-rose-400">{{ formatDia(s.data_ocorrencia) }}</span>
            <span class="block text-xs font-medium text-slate-400 uppercase">{{ formatMesCurto(s.data_ocorrencia) }}</span>
          </div>
          <div class="flex-1">
            <h4 class="font-semibold text-slate-900 dark:text-white mb-1">{{ s.tipo_sancao }}</h4>
            <p class="text-sm text-slate-600 dark:text-slate-300 italic">"{{ s.descricao }}"</p>
          </div>
        </div>
      </div>

      <!-- Aba Presenças (substituindo tabela por cards) -->
      <div v-if="activeTab === 'Presenças'" class="space-y-3">
        <div v-if="presencas.length === 0" class="text-center py-16 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800">
          <BootstrapIcon name="calendar-check" class="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-3" />
          <p class="text-slate-500 dark:text-slate-400">Nenhum registo de presença.</p>
        </div>
        <div 
          v-for="p in presencas" 
          :key="p.id" 
          class="bg-white dark:bg-slate-900 rounded-lg p-4 border border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between gap-3"
        >
          <div class="flex items-center gap-3">
            <div :class="[
              'w-2 h-2 rounded-full',
              p.estado === 'Presente' ? 'bg-emerald-500' : 'bg-rose-500'
            ]"></div>
            <span class="text-sm font-medium text-slate-700 dark:text-slate-300">
              {{ formatDate(p.data_presenca) }} <span class="text-slate-400 text-xs">({{ p.periodo }})</span>
            </span>
          </div>
          <div class="flex items-center gap-4">
            <span :class="[
              'text-sm font-medium',
              p.estado === 'Presente' ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'
            ]">
              {{ p.estado }}
            </span>
            <span class="text-xs text-slate-400">Admin ID: {{ p.admin_id_registo || '---' }}</span>
          </div>
        </div>
      </div>

      <!-- Aba Saídas -->
      <div v-if="activeTab === 'Saídas'" class="space-y-3">
        <div v-if="saidas.length === 0" class="text-center py-16 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800">
          <BootstrapIcon name="door-open" class="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-3" />
          <p class="text-slate-500 dark:text-slate-400">Nenhum pedido de saída registado.</p>
        </div>
        <div 
          v-for="sd in saidas" 
          :key="sd.id" 
          class="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm"
        >
          <div class="flex flex-wrap justify-between items-start gap-3 mb-3">
            <p class="text-sm font-semibold text-slate-900 dark:text-white">
              {{ formatDate(sd.data_saida_pretendida) }} → {{ formatDate(sd.data_retorno_pretendida) }}
            </p>
            <span :class="[
              'px-2.5 py-0.5 rounded-md text-xs font-medium border',
              getStatusSaidaBadge(sd.estado)
            ]">
              {{ sd.estado }}
            </span>
          </div>
          <p class="text-sm text-slate-600 dark:text-slate-300 mb-1">Motivo: {{ sd.motivo }}</p>
          <p class="text-xs text-slate-500 dark:text-slate-400 mb-2">
            Destino: {{ sd.cidade_destino || '—' }} • Transporte: {{ sd.meio_transporte || '—' }}
          </p>
          <p v-if="sd.motivo_rejeicao" class="text-xs text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-900/20 p-2 rounded-md border border-rose-200 dark:border-rose-800/30">
            Rejeição: {{ sd.motivo_rejeicao }}
          </p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const { api } = useApi()
const route = useRoute()
const activeTab = ref('Financeiro')

const { data, pending } = await useAsyncData(`student-full-history-${route.params.id}`, async () => {
  const estudante = await api<any>(`/admin/estudantes/${route.params.id}/`)
  const mensalidadesResp = await api<any>(`/admin/estudantes/${route.params.id}/mensalidades/`)
  const mensalidades = mensalidadesResp.results ?? mensalidadesResp
  const sancoesResp = await api<any>(`/admin/estudantes/${route.params.id}/sancoes/`)
  const sancoes = sancoesResp.results ?? sancoesResp
  const presencasResp = await api<any>(`/admin/estudantes/${route.params.id}/presencas/`)
  const presencas = presencasResp.results ?? presencasResp
  const saidasResp = await api<any>(`/admin/pedidos-saida/?estudante=${route.params.id}`)
  const saidas = saidasResp.results ?? saidasResp
  return { estudante, mensalidades, sancoes, presencas, saidas }
})

const estudante = computed(() => data.value?.estudante)
const mensalidades = computed(() => data.value?.mensalidades || [])
const sancoes = computed(() => data.value?.sancoes || [])
const presencas = computed(() => data.value?.presencas || [])
const saidas = computed(() => data.value?.saidas || [])

// Helpers
const formatMoeda = (v: any) => new Intl.NumberFormat('pt-MZ', { style: 'currency', currency: 'MZN' }).format(Number(v))
const formatMes = (d: string) => new Date(d).toLocaleDateString('pt-PT', { month: 'long', year: 'numeric' })
const formatMesCurto = (d: string) => new Date(d).toLocaleDateString('pt-PT', { month: 'short' }).toUpperCase()
const formatDia = (d: string) => new Date(d).getDate()
const formatDate = (d: string) => new Date(d).toLocaleDateString('pt-PT')

const getStatusSaidaBadge = (estado: string) => {
  const map: Record<string, string> = {
    'Autorizado': 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30',
    'Rejeitado': 'bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-900/20 dark:text-rose-400 dark:border-rose-800/30',
    'Aguardando_Encarregado': 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-900/20 dark:text-amber-400 dark:border-amber-800/30',
  }
  return map[estado] || 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-slate-800 dark:text-slate-400'
}
</script>

<style scoped>
/* Esconder scrollbar */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
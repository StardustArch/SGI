<template>
  <div class="space-y-8 dark:text-white max-w-7xl mx-auto p-4 md:p-8">
    
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
      <div class="flex items-center gap-4">
        <NuxtLink :to="`/dashboard/admin/students/${route.params.id}`" class="p-2 hover:bg-stone-100 rounded-full transition">
          <BootstrapIcon name="arrow-left" class="w-6 h-6" />
        </NuxtLink>
        <div>
          <h1 class="text-3xl font-bold tracking-tight">{{ estudante?.nome_completo }}</h1>
          <p class="text-stone-500 text-sm font-medium uppercase tracking-widest">Dossiê Completo de Interno</p>
        </div>
      </div>

      <span :class="['px-4 py-2 rounded-2xl text-xs font-black uppercase tracking-widest border', estudante?.estado === 'Activo' ? 'bg-emerald-50 text-emerald-600 border-emerald-100' : 'bg-rose-50 text-rose-600 border-rose-100']">
        Status: {{ estudante?.estado }}
      </span>
    </div>

    <div class="flex p-1.5 bg-stone-100 dark:bg-gray-800 rounded-2xl w-fit overflow-x-auto max-w-full">
      <button 
        v-for="tab in ['Financeiro', 'Disciplina', 'Presenças', 'Saídas']" 
        :key="tab"
        @click="activeTab = tab"
        :class="['px-6 py-2.5 rounded-xl text-sm font-bold transition-all', activeTab === tab ? 'bg-white shadow-md text-rose-500 dark:bg-gray-700 dark:text-white' : 'text-stone-500 hover:text-stone-700']"
      >
        {{ tab }}
      </button>
    </div>

    <div class="mt-8">
      
      <div v-if="activeTab === 'Financeiro'" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="pag in mensalidades" :key="pag.id" class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm relative">
            <div :class="['absolute left-0 top-8 bottom-8 w-1 rounded-r-full', pag.estado === 'Pago' ? 'bg-emerald-400' : 'bg-amber-400']"></div>
            <p class="text-[10px] font-black text-stone-400 uppercase mb-1">{{ formatMes(pag.mes_referencia) }}</p>
            <h4 class="text-xl font-bold">{{ formatMoeda(pag.valor_pago || 25000) }}</h4>
            <span :class="['mt-3 inline-block px-2 py-0.5 rounded text-[10px] font-bold uppercase', pag.estado === 'Pago' ? 'bg-emerald-50 text-emerald-600' : 'bg-amber-50 text-amber-600']">
              {{ pag.estado }}
            </span>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'Disciplina'" class="space-y-4">
        <div v-if="sancoes.length === 0" class="text-center py-20 bg-stone-50 dark:bg-gray-800/50 rounded-[2rem] border-2 border-dashed border-stone-200">
           <BootstrapIcon name="emoji-smile" class="text-4xl text-emerald-400 mb-2" />
           <p class="text-stone-500 font-bold">Sem registos disciplinares. Comportamento exemplar.</p>
        </div>
        <div v-for="s in sancoes" :key="s.id" class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm flex flex-col md:flex-row gap-6">
           <div class="shrink-0 text-center md:border-r md:pr-6 border-stone-100">
              <span class="block text-2xl font-black text-rose-500">{{ formatDia(s.data_ocorrencia) }}</span>
              <span class="block text-[10px] font-bold text-stone-400 uppercase">{{ formatMesCurto(s.data_ocorrencia) }}</span>
           </div>
           <div class="flex-1">
              <h4 class="font-bold text-gray-800 dark:text-white mb-1">{{ s.tipo_sancao }}</h4>
              <p class="text-sm text-stone-500 dark:text-gray-400 italic">"{{ s.descricao }}"</p>
           </div>
        </div>
      </div>

      <div v-if="activeTab === 'Presenças'" class="bg-white dark:bg-gray-800 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm overflow-hidden">
        <table class="w-full text-left">
          <thead class="bg-stone-50 dark:bg-gray-700">
            <tr>
              <th class="p-5 text-[10px] font-bold uppercase text-stone-400">Data</th>
              <th class="p-5 text-[10px] font-bold uppercase text-stone-400">Estado</th>
              <th class="p-5 text-[10px] font-bold uppercase text-stone-400">Registado por</th>
            </tr>
          </thead>
          <tbody class="divide-y dark:divide-gray-700">
            <tr v-for="p in presencas" :key="p.id">
              <td class="p-5 text-sm font-bold">{{ formatDate(p.data_presenca) }}</td>
              <td class="p-5">
                <span :class="['px-2 py-0.5 rounded text-[10px] font-bold uppercase', p.estado === 'Presente' ? 'text-emerald-500' : 'text-rose-500']">
                  ● {{ p.estado }}
                </span>
              </td>
              <td class="p-5 text-xs text-stone-400">Admin ID: {{ p.admin_id_registo || '---' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="activeTab === 'Saídas'" class="space-y-4">
        <div v-for="sd in saidas" :key="sd.id" class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm flex justify-between items-center">
          <div>
            <p class="text-sm font-bold">{{ formatDate(sd.data_saida_pretendida) }} → {{ formatDate(sd.data_retorno_pretendida) }}</p>
            <p class="text-xs text-stone-400 mt-1">Motivo: {{ sd.motivo }}</p>
          </div>
          <span class="px-3 py-1 rounded-full bg-stone-100 text-[10px] font-bold uppercase text-stone-500">
            {{ sd.estado }}
          </span>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
const { api } = useApi()
const route = useRoute()
const activeTab = ref('Financeiro')

// Chamada de dados em paralelo para popular o Dossiê
const { data, pending } = await useAsyncData(`student-full-history-${route.params.id}`, async () => {
  const [estudante, mensalidades, sancoes, presencas, saidas] = await Promise.all([
    api<any>(`/admin/estudantes/${route.params.id}/`),
    api<any[]>(`/admin/mensalidades/`, { params: { estudante: route.params.id } }),
    api<any[]>(`/admin/sancoes/`, { params: { estudante: route.params.id } }),
    api<any[]>(`/admin/presencas/`, { params: { estudante: route.params.id } }),
    api<any[]>(`/admin/pedidos-saida/`, { params: { estudante: route.params.id } })
  ])
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
</script>
<template>
  <div class="space-y-8 dark:text-white max-w-8xl mx-auto p-4 md:p-8">
    
    <div>
      <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Registo de Presenças</h1>
      <p class="text-stone-500 dark:text-gray-400 mt-1 text-lg">Histórico de assiduidade nos estudos obrigatórios.</p>
    </div>

    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-stone-50 dark:bg-gray-800/50 p-4 rounded-[1.5rem] border border-stone-100 dark:border-gray-700">
      
      <div class="flex gap-2 overflow-x-auto max-w-full pb-1 md:pb-0">
          <button 
              v-for="estado in ['Todos', 'Presente', 'Ausente', 'Justificado']"
              :key="estado"
              @click="filtros.estado = estado === 'Todos' ? null : estado; page = 1"
              :class="[
                  'px-4 py-2 text-xs font-bold rounded-xl transition-all whitespace-nowrap border',
                  (filtros.estado === estado || (estado === 'Todos' && !filtros.estado))
                    ? 'bg-white text-gray-800 border-stone-200 shadow-sm dark:bg-gray-700 dark:text-white dark:border-gray-600' 
                    : 'bg-transparent border-transparent text-stone-500 hover:text-stone-700 dark:text-stone-400'
              ]"
          >
              <span v-if="estado === 'Presente'" class="w-2 h-2 rounded-full bg-emerald-400 inline-block mr-1"></span>
              <span v-else-if="estado === 'Ausente'" class="w-2 h-2 rounded-full bg-rose-400 inline-block mr-1"></span>
              <span v-else-if="estado === 'Justificado'" class="w-2 h-2 rounded-full bg-amber-400 inline-block mr-1"></span>
              {{ estado }}
          </button>
      </div>

      <div class="w-full md:w-64">
        <div class="relative">
          <select 
            v-model="filtros.estudante" 
            @change="page = 1"
            class="w-full appearance-none bg-white dark:bg-gray-800 border border-stone-200 dark:border-gray-600 text-gray-700 dark:text-gray-200 py-2.5 px-4 pr-8 rounded-xl focus:outline-none focus:ring-2 focus:ring-rose-200 font-medium text-sm shadow-sm cursor-pointer"
          >
            <option :value="null">Todos os Educandos</option>
            <option v-for="filho in educandos" :key="filho.utilizador_id" :value="filho.utilizador_id">
              {{ filho.nome_completo }}
            </option>
          </select>
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-gray-500">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </div>
        </div>
      </div>
    </div>

    <div>
      
      <div v-if="pending" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        <div v-for="n in 6" :key="n" class="bg-white dark:bg-gray-800 rounded-3xl p-4 shadow-sm border border-stone-100 dark:border-gray-700 animate-pulse h-24 flex items-center gap-4">
           <div class="w-16 h-16 bg-stone-100 rounded-2xl"></div>
           <div class="flex-1 space-y-2">
             <div class="h-4 bg-stone-100 rounded w-3/4"></div>
             <div class="h-3 bg-stone-100 rounded w-1/2"></div>
           </div>
        </div>
      </div>

      <div v-else-if="presencasComNome.length === 0" class="flex flex-col items-center justify-center py-20 bg-stone-50/50 dark:bg-gray-800/50 rounded-[2rem] border border-stone-100 dark:border-gray-700 text-center">
        <div class="bg-white p-4 rounded-full shadow-sm mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-stone-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <p class="text-stone-500 font-medium">Nenhum registo encontrado com estes filtros.</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
        
        <div 
          v-for="item in presencasComNome" 
          :key="item.id"
          class="group bg-white dark:bg-gray-800 rounded-[1.5rem] p-4 shadow-sm hover:shadow-md transition-all duration-300 border border-stone-100 dark:border-gray-700 flex items-center gap-4 relative overflow-hidden"
        >
          <div :class="[
            'absolute left-0 top-0 bottom-0 w-1.5',
            item.estado === 'Presente' ? 'bg-emerald-400' : (item.estado === 'Ausente' ? 'bg-rose-400' : 'bg-amber-400')
          ]"></div>

          <div class="flex flex-col items-center justify-center h-16 w-16 bg-stone-50 dark:bg-gray-700/50 rounded-2xl border border-stone-100 dark:border-gray-600 ml-2 shrink-0">
            <span class="text-[10px] font-bold text-stone-400 uppercase tracking-wider">
              {{ formatMes(item.data_presenca) }}
            </span>
            <span class="text-2xl font-bold text-gray-800 dark:text-white leading-none mt-0.5">
              {{ formatDia(item.data_presenca) }}
            </span>
          </div>

          <div class="flex-1 min-w-0">
            <h3 class="font-bold text-gray-800 dark:text-white truncate text-base mb-1">
              {{ item.nome_estudante }}
            </h3>
            
            <div class="flex items-center gap-2">
                <span :class="[
                  'inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wide border',
                  item.estado === 'Presente' 
                    ? 'bg-emerald-50 text-emerald-700 border-emerald-100 dark:bg-emerald-900/20 dark:text-emerald-300' 
                    : (item.estado === 'Ausente' ? 'bg-rose-50 text-rose-700 border-rose-100' : 'bg-amber-50 text-amber-700 border-amber-100')
                ]">
                  <span :class="[
                    'w-1.5 h-1.5 rounded-full',
                    item.estado === 'Presente' ? 'bg-emerald-500' : (item.estado === 'Ausente' ? 'bg-rose-500' : 'bg-amber-500')
                  ]"></span>
                  {{ item.estado }}
                </span>
            </div>
          </div>

          <div class="pr-2 opacity-0 group-hover:opacity-100 transition-opacity">
             <div class="h-8 w-8 rounded-full bg-stone-50 dark:bg-gray-700 flex items-center justify-center text-stone-400">
               <svg v-if="item.estado === 'Presente'" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-500" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
               <svg v-else-if="item.estado === 'Ausente'" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-rose-500" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
               <span v-else class="text-xs font-bold text-amber-500">?</span>
             </div>
          </div>

        </div>
      </div>

      <div v-if="presencasComNome.length > 0" class="flex justify-center items-center gap-4 mt-8 pb-8">
        <button 
          @click="page--" 
          :disabled="!data?.presencas?.previous"
          class="h-10 w-10 rounded-full border border-stone-200 dark:border-gray-600 flex items-center justify-center text-stone-500 hover:bg-stone-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
        </button>
        <span class="text-sm font-medium text-stone-600 dark:text-gray-400">Página {{ page }}</span>
        <button 
          @click="page++" 
          :disabled="!data?.presencas?.next"
          class="h-10 w-10 rounded-full border border-stone-200 dark:border-gray-600 flex items-center justify-center text-stone-500 hover:bg-stone-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
        </button>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
const { api } = useApi()
const route = useRoute() 

// Estados
const page = ref(1)
const filtros = reactive({
  // Se houver ID no URL usa-o, senão null
  estudante: route.query.student ? Number(route.query.student) : null as number | null,
  
  // AQUI ESTÁ O TRUQUE: 'as string | null'
  estado: null as string | null 
})

// 1. Educandos (Dropdown)
const { data: educandos } = await useAsyncData(
  'filtros-educandos', 
  () => api<any[]>('/perfil-encarregado/meus-educandos/')
)

// 2. Presenças (Lista Paginada)
const { data, pending } = await useAsyncData(
  'encarregado-presencas-full',
  async () => {
    const params: any = { page: page.value }
    if (filtros.estudante) params.estudante = filtros.estudante
    if (filtros.estado) params.estado = filtros.estado

    // Apenas precisamos da lista e da paginação
    const presencas = await api<any>('/perfil-encarregado/presencas/', { params })
    return { presencas }
  },
  { 
    watch: [page, filtros]
  }
)

// Mapper: Associar Nomes
const presencasComNome = computed(() => {
  if (!data.value?.presencas?.results || !educandos.value) return []
  
  const lista = data.value.presencas.results
  const mapaNomes = new Map(educandos.value.map((e: any) => [e.utilizador_id, e.nome_completo]))
  
  return lista.map((item: any) => ({
    ...item,
    nome_estudante: mapaNomes.get(item.estudante) || 'Desconhecido'
  }))
})

// Helpers de Data
const formatDia = (dataStr: string) => {
  if (!dataStr) return '--';
  return new Date(dataStr).getDate();
}

const formatMes = (dataStr: string) => {
  if (!dataStr) return '---';
  return new Date(dataStr).toLocaleString('pt-PT', { month: 'short' }).toUpperCase().replace('.', ''); 
}
</script>
<template>
  <div class="space-y-6 md:space-y-8 dark:text-white max-w-8xl mx-auto p-4 md:p-8">
    
    <div>
      <h1 class="text-2xl md:text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Registo Disciplinar</h1>
      <p class="text-stone-500 dark:text-gray-400 mt-1 text-base md:text-lg">Histórico de ocorrências e sanções aplicadas.</p>
    </div>

    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-stone-50 dark:bg-gray-800/50 p-3 md:p-4 rounded-[1.5rem] border border-stone-100 dark:border-gray-700">
      
      <div class="w-full md:w-auto overflow-x-auto pb-2 md:pb-0 scrollbar-hide">
        <div class="flex gap-2 min-w-max">
            <button 
                v-for="tipo in ['Todos', 'Advertência Verbal', 'Trabalho Comunitário', 'Suspensão de Saída']"
                :key="tipo"
                @click="filtros.tipo = tipo === 'Todos' ? null : tipo; page = 1"
                :class="[
                    'px-3 md:px-4 py-2 text-xs font-bold rounded-xl transition-all whitespace-nowrap border',
                    (filtros.tipo === tipo || (tipo === 'Todos' && !filtros.tipo))
                      ? 'bg-white text-gray-800 border-stone-200 shadow-sm dark:bg-gray-700 dark:text-white dark:border-gray-600' 
                      : 'bg-transparent border-transparent text-stone-500 hover:text-stone-700 dark:text-stone-400'
                ]"
            >
                {{ tipo }}
            </button>
        </div>
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
      
      <div v-if="pending" class="space-y-4">
        <div v-for="n in 3" :key="n" class="bg-white dark:bg-gray-800 rounded-[1.5rem] p-6 shadow-sm border border-stone-100 dark:border-gray-700 animate-pulse h-40"></div>
      </div>

      <div v-else-if="sancoesComNome.length === 0" class="flex flex-col items-center justify-center py-16 md:py-20 bg-stone-50/50 dark:bg-gray-800/50 rounded-[2rem] border border-stone-100 dark:border-gray-700 text-center px-4">
        <div class="bg-white p-4 rounded-full shadow-sm mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-emerald-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 class="text-lg font-bold text-gray-800 dark:text-white">Comportamento Exemplar</h3>
        <p class="text-stone-500 dark:text-gray-400 text-sm mt-1">Nenhuma ocorrência disciplinar encontrada.</p>
      </div>

      <div v-else class="grid grid-cols-1 gap-6 mb-8">
        
        <div 
          v-for="item in sancoesComNome" 
          :key="item.id"
          class="group bg-white dark:bg-gray-800 rounded-[1.5rem] p-0 shadow-sm hover:shadow-lg transition-all duration-300 border border-stone-100 dark:border-gray-700 relative overflow-hidden flex flex-col md:flex-row"
        >
          <div :class="[
            'w-full md:w-2 h-2 md:h-auto',
            getSeverityColor(item.tipo_sancao)
          ]"></div>

          <div class="flex-1 p-5 md:p-8 flex flex-col md:flex-row gap-5 md:gap-6">
            
            <div class="w-full md:w-48 shrink-0 flex flex-row md:flex-col items-center md:items-start justify-start gap-4 md:gap-2">
               
               <div class="bg-stone-50 dark:bg-gray-700/50 px-4 py-2 rounded-xl border border-stone-100 dark:border-gray-600 text-center w-fit shrink-0">
                  <span class="block text-xs font-bold text-stone-400 uppercase tracking-wider">{{ formatMes(item.data_ocorrencia) }}</span>
                  <span class="block text-2xl font-bold text-gray-800 dark:text-white">{{ formatDia(item.data_ocorrencia) }}</span>
               </div>
               
               <div class="text-left flex-1 md:text-left overflow-hidden">
                  <p class="text-[10px] md:text-xs font-bold text-stone-400 uppercase tracking-wider mb-0.5">Educando</p>
                  <div class="flex items-center gap-2">
                    <div class="h-6 w-6 rounded-full bg-stone-100 dark:bg-gray-600 flex items-center justify-center text-[10px] font-bold text-stone-500 shrink-0">
                        {{ getIniciais(item.nome_estudante) }}
                    </div>
                    <p class="text-sm font-bold text-gray-800 dark:text-white truncate w-full md:max-w-[120px]">
                        {{ item.nome_estudante.split(' ')[0] }}
                    </p>
                  </div>
               </div>
            </div>

            <div class="hidden md:block w-px bg-stone-100 dark:bg-gray-700"></div>

            <div class="flex-1 min-w-0"> <div class="flex flex-wrap items-center gap-2 md:gap-3 mb-3">
                 <span :class="[
                   'px-3 py-1 rounded-lg text-xs font-bold uppercase tracking-wide border whitespace-normal text-center',
                   getSeverityBadge(item.tipo_sancao)
                 ]">
                   {{ item.tipo_sancao }}
                 </span>
                 
                 <span v-if="item.notificado_encarregado" class="flex items-center gap-1 text-[10px] font-bold text-stone-400 bg-stone-50 dark:bg-gray-700 px-2 py-1 rounded-md border border-stone-100 dark:border-gray-600">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" /></svg>
                    Notificado
                 </span>
              </div>

              <h3 class="text-xs font-bold text-stone-400 uppercase tracking-wider mb-2">Descrição da Ocorrência</h3>
              <div class="p-3 md:p-4 bg-stone-50 dark:bg-gray-700/30 rounded-2xl border border-stone-100 dark:border-gray-700">
                <p class="text-sm text-stone-600 dark:text-gray-300 italic leading-relaxed break-words">
                  "{{ item.descricao }}"
                </p>
              </div>
            </div>

          </div>
        </div>

      </div>

      <div v-if="sancoesComNome.length > 0" class="flex justify-center items-center gap-4 mt-8 pb-8">
        <button 
          @click="page--" 
          :disabled="!data?.sancoes?.previous"
          class="h-10 w-10 rounded-full border border-stone-200 dark:border-gray-600 flex items-center justify-center text-stone-500 hover:bg-stone-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
        </button>
        <span class="text-sm font-medium text-stone-600 dark:text-gray-400">Página {{ page }}</span>
        <button 
          @click="page++" 
          :disabled="!data?.sancoes?.next"
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
  estudante: route.query.student ? Number(route.query.student) : null,
  tipo: null as string | null 
})
// 1. Educandos (Dropdown)
const { data: educandos } = await useAsyncData(
  'filtros-educandos', 
  () => api<any[]>('/perfil-encarregado/meus-educandos/')
)

// 2. Sanções (Lista)
const { data, pending } = await useAsyncData(
  'encarregado-sancoes-full',
  async () => {
    const params: any = { page: page.value }
    if (filtros.estudante) params.estudante = filtros.estudante
    if (filtros.tipo) params.tipo_sancao = filtros.tipo 

    const sancoes = await api<any>('/perfil-encarregado/sancoes/', { params })
    return { sancoes }
  },
  { 
    watch: [page, filtros]
  }
)

// Mapper
const sancoesComNome = computed(() => {
  if (!data.value?.sancoes?.results || !educandos.value) return []
  
  const lista = data.value.sancoes.results
  const mapaNomes = new Map(educandos.value.map((e: any) => [e.utilizador_id, e.nome_completo]))
  
  return lista.map((item: any) => ({
    ...item,
    nome_estudante: mapaNomes.get(item.estudante) || 'Desconhecido'
  }))
})

// --- Cores e Estilos ---
const getSeverityColor = (tipo: string) => {
  if (tipo.includes('Suspensão')) return 'bg-rose-500'
  if (tipo.includes('Trabalho')) return 'bg-orange-400'
  return 'bg-amber-400' // Advertência
}

const getSeverityBadge = (tipo: string) => {
  if (tipo.includes('Suspensão')) return 'bg-rose-50 text-rose-700 border-rose-100 dark:bg-rose-900/20 dark:text-rose-300'
  if (tipo.includes('Trabalho')) return 'bg-orange-50 text-orange-700 border-orange-100 dark:bg-orange-900/20 dark:text-orange-300'
  return 'bg-amber-50 text-amber-700 border-amber-100 dark:bg-amber-900/20 dark:text-amber-300'
}

// Helpers Data
const formatDia = (dataStr: string) => new Date(dataStr).getDate()
const formatMes = (dataStr: string) => new Date(dataStr).toLocaleString('pt-PT', { month: 'short' }).toUpperCase().replace('.', '')
const getIniciais = (nome: string) => {
  const limpo = (nome || '').trim();
  if (!limpo) return '??';
  const partes = limpo.split(/\s+/);
  const primeira = partes[0]?.[0] || '';
  const ultima = partes.length > 1 ? partes[partes.length - 1]?.[0] || '' : '';
  return (primeira + ultima).toUpperCase();
}
</script>
<template>
  <div class="space-y-8 dark:text-white max-w-7xl mx-auto p-4 md:p-8">
    
    <div>
      <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Registo Disciplinar</h1>
      <p class="text-stone-500 dark:text-gray-400 mt-1 text-lg">O meu histórico de ocorrências e sanções.</p>
    </div>

    <div class="bg-stone-50 dark:bg-gray-800/50 p-4 rounded-[1.5rem] border border-stone-100 dark:border-gray-700 overflow-x-auto">
      <div class="flex gap-2 min-w-max">
          <button 
              v-for="tipo in ['Todos', 'Advertência Verbal', 'Trabalho Comunitário', 'Suspensão de Saída']"
              :key="tipo"
              @click="filtroTipo = tipo === 'Todos' ? null : tipo"
              :class="[
                  'px-4 py-2 text-xs font-bold rounded-xl transition-all whitespace-nowrap border',
                  (filtroTipo === tipo || (tipo === 'Todos' && !filtroTipo))
                    ? 'bg-white text-gray-800 border-stone-200 shadow-sm dark:bg-gray-700 dark:text-white dark:border-gray-600' 
                    : 'bg-transparent border-transparent text-stone-500 hover:text-stone-700 dark:text-stone-400'
              ]"
          >
              {{ tipo }}
          </button>
      </div>
    </div>

    <div>
      
      <div v-if="pending" class="space-y-4">
        <div v-for="n in 3" :key="n" class="bg-white dark:bg-gray-800 rounded-[1.5rem] p-6 shadow-sm border border-stone-100 dark:border-gray-700 animate-pulse h-40"></div>
      </div>

      <div v-else-if="sancoesFiltradas.length === 0" class="flex flex-col items-center justify-center py-20 bg-stone-50/50 dark:bg-gray-800/50 rounded-[2rem] border border-stone-100 dark:border-gray-700 text-center">
        <div class="bg-white p-4 rounded-full shadow-sm mb-4">
          <BootstrapIcon name="award" class="w-10 h-10 text-emerald-300" />
        </div>
        <h3 class="text-lg font-bold text-gray-800 dark:text-white">Comportamento Exemplar</h3>
        <p class="text-stone-500 dark:text-gray-400 text-sm mt-1">Nenhuma ocorrência encontrada.</p>
      </div>

      <div v-else class="grid grid-cols-1 gap-6 mb-8">
        
        <div 
          v-for="item in sancoesFiltradas" 
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
               
               <div class="hidden md:block text-stone-400 text-xs italic mt-2">
                 Ocorrência registada nesta data.
               </div>
            </div>

            <div class="hidden md:block w-px bg-stone-100 dark:bg-gray-700"></div>

            <div class="flex-1 min-w-0">
              
              <div class="flex flex-wrap items-center gap-2 md:gap-3 mb-3">
                 <span :class="[
                   'px-3 py-1 rounded-lg text-xs font-bold uppercase tracking-wide border whitespace-normal text-center',
                   getSeverityBadge(item.tipo_sancao)
                 ]">
                   {{ item.tipo_sancao }}
                 </span>
                 
                 <span v-if="item.notificado_encarregado" class="flex items-center gap-1 text-[10px] font-bold text-stone-400 bg-stone-50 dark:bg-gray-700 px-2 py-1 rounded-md border border-stone-100 dark:border-gray-600">
                    <BootstrapIcon name="bell-fill" class="w-3 h-3" />
                    Encarregado Notificado
                 </span>
              </div>

              <h3 class="text-xs font-bold text-stone-400 uppercase tracking-wider mb-2">Descrição</h3>
              <div class="p-4 bg-stone-50 dark:bg-gray-700/30 rounded-2xl border border-stone-100 dark:border-gray-700">
                <p class="text-sm text-stone-600 dark:text-gray-300 italic leading-relaxed break-words">
                  "{{ item.descricao }}"
                </p>
              </div>
            </div>

          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const { api } = useApi()

// Filtro Local
const filtroTipo = ref<string | null>(null)

// Buscar os dados (Apenas os meus)
const { data: sancoes, pending } = await useAsyncData(
  'student-discipline',
  () => api<any[]>('/student/discipline/'),
  { lazy: true, default: () => [] }
)

// Filtragem Local
const sancoesFiltradas = computed(() => {
  if (!sancoes.value) return []
  if (!filtroTipo.value) return sancoes.value
  
  return sancoes.value.filter(s => s.tipo_sancao === filtroTipo.value)
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
const formatDia = (dataStr: string) => {
  if (!dataStr) return '--';
  return new Date(dataStr).getDate();
}

const formatMes = (dataStr: string) => {
  if (!dataStr) return '---';
  return new Date(dataStr).toLocaleString('pt-PT', { month: 'short' }).toUpperCase().replace('.', ''); 
}
</script>
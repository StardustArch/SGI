<template>
  <div class="space-y-8 dark:text-white max-w-7xl mx-auto p-4 md:p-8">
    
    <div>
      <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Registo de Presenças</h1>
      <p class="text-stone-500 dark:text-gray-400 mt-1 text-lg">O meu histórico de assiduidade nos estudos obrigatórios.</p>
    </div>

    <div class="bg-stone-50 dark:bg-gray-800/50 p-4 rounded-[1.5rem] border border-stone-100 dark:border-gray-700 overflow-x-auto">
      <div class="flex gap-2 min-w-max">
          <button 
              v-for="estado in ['Todos', 'Presente', 'Ausente', 'Justificado']"
              :key="estado"
              @click="filtroEstado = estado === 'Todos' ? null : estado"
              :class="[
                  'px-4 py-2 text-xs font-bold rounded-xl transition-all whitespace-nowrap border',
                  (filtroEstado === estado || (estado === 'Todos' && !filtroEstado))
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

      <div v-else-if="presencasFiltradas.length === 0" class="flex flex-col items-center justify-center py-20 bg-stone-50/50 dark:bg-gray-800/50 rounded-[2rem] border border-stone-100 dark:border-gray-700 text-center">
        <div class="bg-white p-4 rounded-full shadow-sm mb-4">
          <BootstrapIcon name="calendar-x" class="w-10 h-10 text-stone-300" />
        </div>
        <p class="text-stone-500 font-medium">Nenhum registo encontrado.</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
        
        <div 
          v-for="item in presencasFiltradas" 
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
            <div class="flex items-center gap-2">
                <span :class="[
                  'inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-bold uppercase tracking-wide border',
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
            
            <p class="text-xs text-stone-400 mt-2 font-medium">Estudo Obrigatório</p>
          </div>

          <div class="pr-2 opacity-0 group-hover:opacity-100 transition-opacity">
             <div class="h-8 w-8 rounded-full bg-stone-50 dark:bg-gray-700 flex items-center justify-center text-stone-400 shadow-sm">
               <BootstrapIcon v-if="item.estado === 'Presente'" name="check-lg" class="w-4 h-4 text-emerald-500" />
               <BootstrapIcon v-else-if="item.estado === 'Ausente'" name="x-lg" class="w-4 h-4 text-rose-500" />
               <BootstrapIcon v-else name="question-lg" class="w-4 h-4 text-amber-500" />
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
const filtroEstado = ref<string | null>(null)

// Buscar os dados do endpoint /student/attendance/
// Nota: Aqui não precisamos de paginação no servidor por enquanto,
// a lista do estudante não costuma ser gigante como a do admin.
const { data: presencas, pending } = await useAsyncData(
  'student-attendance',
  () => api<any[]>('/student/attendance/'),
  { lazy: true, default: () => [] }
)

// Filtragem Local (Computed)
const presencasFiltradas = computed(() => {
  if (!presencas.value) return []
  if (!filtroEstado.value) return presencas.value
  
  return presencas.value.filter(p => p.estado === filtroEstado.value)
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
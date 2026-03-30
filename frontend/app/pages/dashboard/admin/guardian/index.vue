<template>
  <div class="space-y-8 dark:text-white max-w-7xl mx-auto p-4 md:p-8">
    
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Gestão de Encarregados</h1>
        <p class="text-stone-500 dark:text-gray-400 mt-1">Diretório de contactos de emergência e responsáveis dos internos.</p>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-800 p-4 rounded-[1.5rem] border border-stone-100 dark:border-gray-700 shadow-sm">
      <div class="relative">
        <BootstrapIcon name="search" class="absolute left-4 top-1/2 -translate-y-1/2 text-stone-400" />
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Pesquisar por nome, telefone ou email..." 
          class="w-full pl-12 pr-4 py-3 bg-stone-50 dark:bg-gray-700 border-none rounded-xl focus:ring-2 focus:ring-rose-200 outline-none transition-all"
        />
      </div>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-[2rem] border border-stone-100 dark:border-gray-700 overflow-hidden shadow-sm">
      <table class="w-full text-left border-collapse">
        <thead class="bg-stone-50 dark:bg-gray-700/50">
          <tr>
            <th class="p-5 text-xs font-bold text-stone-400 uppercase tracking-wider">Responsável</th>
            <th class="p-5 text-xs font-bold text-stone-400 uppercase tracking-wider">Contactos</th>
            <th class="p-5 text-xs font-bold text-stone-400 uppercase tracking-wider">Educando(s)</th>
            <th class="p-5 text-xs font-bold text-stone-400 uppercase tracking-wider text-right">Ação</th>
          </tr>
        </thead>
        <tbody class="divide-y dark:divide-gray-700">
          <tr v-if="pending" v-for="n in 3" :key="n">
            <td colspan="4" class="p-5 animate-pulse bg-stone-50/50 dark:bg-gray-800/50 h-20"></td>
          </tr>
          <tr v-else-if="encarregadosFiltrados.length === 0">
            <td colspan="4" class="p-10 text-center text-stone-500">Nenhum encarregado encontrado.</td>
          </tr>
          <tr v-else v-for="enc in encarregadosFiltrados" :key="enc.utilizador_id" class="hover:bg-stone-50/50 dark:hover:bg-gray-700/30 transition-colors">
            
            <td class="p-5">
              <div class="flex items-center gap-4">
                <div class="h-10 w-10 rounded-xl bg-stone-100 dark:bg-gray-700 text-stone-500 flex items-center justify-center font-bold border border-stone-200 dark:border-gray-600">
                  {{ enc.nome_completo?.charAt(0) }}
                </div>
                <p class="font-bold text-gray-800 dark:text-white text-base">{{ enc.nome_completo }}</p>
              </div>
            </td>

            <td class="p-5 space-y-1">
              <div class="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                <BootstrapIcon name="telephone-fill" class="text-emerald-500 w-3 h-3" />
                {{ enc.telefone_principal }}
              </div>
              <div class="flex items-center gap-2 text-xs text-stone-500 dark:text-gray-400">
                <BootstrapIcon name="envelope-fill" class="w-3 h-3" />
                {{ enc.email_contacto || 'Sem email' }}
              </div>
            </td>

            <td class="p-5">
              <div class="flex flex-wrap gap-1">
                <span v-for="(aluno, idx) in enc.educandos" :key="idx" class="px-2.5 py-1 rounded-lg bg-rose-50 dark:bg-rose-900/20 text-rose-600 dark:text-rose-400 text-[10px] font-bold uppercase border border-rose-100 dark:border-rose-800/30">
                  {{ aluno.split(' ')[0] }} </span>
              </div>
            </td>

            <td class="p-5 text-right">
              <NuxtLink :to="`/dashboard/admin/guardian/${enc.utilizador_id}`" class="p-2 hover:bg-stone-100 dark:hover:bg-gray-700 rounded-lg inline-block text-stone-400 hover:text-rose-500 transition-colors" title="Editar Contactos">
                <BootstrapIcon name="pencil-square" class="w-5 h-5" />
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
const searchQuery = ref('')

// Buscar a lista de encarregados
const { data: encarregadosData, pending } = await useAsyncData('admin-encarregados', () => api<any>('/admin/encarregados/'))

const encarregados = computed(() => {
  if (!encarregadosData.value) return []
  return encarregadosData.value.results ?? encarregadosData.value
})
// Filtragem local baseada na pesquisa
const encarregadosFiltrados = computed(() => {
  if (!encarregados.value) return []
  const query = searchQuery.value.toLowerCase()
  if (!query) return encarregados.value
  
  return encarregados.value.filter((e: { nome_completo: string; telefone_principal: string | string[]; email_contacto: string }) => 
    e.nome_completo.toLowerCase().includes(query) || 
    e.telefone_principal.includes(query) ||
    (e.email_contacto && e.email_contacto.toLowerCase().includes(query))
  )
})


</script>
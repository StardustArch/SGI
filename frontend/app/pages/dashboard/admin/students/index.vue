<template>
  <div class="space-y-8 dark:text-white max-w-7xl mx-auto p-4 md:p-8">
    
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Gestão de Internos</h1>
        <p class="text-stone-500 dark:text-gray-400 mt-1">Administre todos os estudantes registados no internato.</p>
      </div>

      <NuxtLink to="/dashboard/admin/registo-completo" class="px-6 py-3 rounded-xl bg-gray-900 dark:bg-white text-white dark:text-gray-900 font-bold text-sm shadow-lg hover:opacity-90 transition-all flex items-center gap-2">
        <BootstrapIcon name="person-plus-fill" /> Novo Estudante
      </NuxtLink>
    </div>

    <div class="bg-white dark:bg-gray-800 p-4 rounded-[1.5rem] border border-stone-100 dark:border-gray-700 shadow-sm flex flex-col md:flex-row gap-4">
      <div class="flex-1 relative">
        <BootstrapIcon name="search" class="absolute left-4 top-1/2 -translate-y-1/2 text-stone-400" />
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Pesquisar por nome ou nº de estudante..." 
          class="w-full pl-12 pr-4 py-3 bg-stone-50 dark:bg-gray-700 border-none rounded-xl focus:ring-2 focus:ring-rose-200 outline-none"
        />
      </div>
      <div class="flex gap-2">
         <button @click="filtroEstado = 'Activo'" :class="['px-4 py-2 rounded-xl text-xs font-bold border transition-all', filtroEstado === 'Activo' ? 'bg-emerald-500 text-white border-emerald-500' : 'bg-white text-stone-500 border-stone-200']">Activos</button>
         <button @click="filtroEstado = 'Inactivo'" :class="['px-4 py-2 rounded-xl text-xs font-bold border transition-all', filtroEstado === 'Inactivo' ? 'bg-rose-500 text-white border-rose-500' : 'bg-white text-stone-500 border-stone-200']">Inactivos</button>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-[2rem] border border-stone-100 dark:border-gray-700 overflow-hidden shadow-sm">
      <table class="w-full text-left border-collapse">
        <thead class="bg-stone-50 dark:bg-gray-700/50">
          <tr>
            <th class="p-5 text-xs font-bold text-stone-400 uppercase">Estudante</th>
            <th class="p-5 text-xs font-bold text-stone-400 uppercase">Quarto / Curso</th>
            <th class="p-5 text-xs font-bold text-stone-400 uppercase">Encarregado</th>
            <th class="p-5 text-xs font-bold text-stone-400 uppercase">Estado</th>
            <th class="p-5 text-xs font-bold text-stone-400 uppercase">Ação</th>
          </tr>
        </thead>
        <tbody class="divide-y dark:divide-gray-700">
          <tr v-if="pending" v-for="n in 3" :key="n">
            <td colspan="5" class="p-5 animate-pulse bg-stone-50/50 h-16"></td>
          </tr>
          <tr v-else v-for="aluno in estudantesFiltrados" :key="aluno.utilizador_id" class="hover:bg-stone-50/50 transition-colors">
            <td class="p-5">
              <div class="flex items-center gap-3">
                <div class="h-10 w-10 rounded-xl bg-rose-50 text-rose-500 flex items-center justify-center font-bold border border-rose-100">
                  {{ aluno.nome_completo?.charAt(0) }}
                </div>
                <div>
                  <p class="font-bold text-gray-800 dark:text-white">{{ aluno.nome_completo }}</p>
                  <p class="text-[10px] text-stone-400 font-bold">ID: {{ aluno.num_estudante }}</p>
                </div>
              </div>
            </td>
            <td class="p-5">
              <p class="text-sm font-bold text-gray-700 dark:text-stone-300">Quarto {{ aluno.quarto }}</p>
              <p class="text-xs text-stone-400">{{ aluno.curso }}</p>
            </td>
            <td class="p-5">
               <p class="text-sm font-medium">{{ aluno.encarregado_nome }}</p>
            </td>
            <td class="p-5">
              <span :class="['px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border', aluno.estado === 'Activo' ? 'bg-emerald-50 text-emerald-700 border-emerald-100' : 'bg-rose-50 text-rose-700 border-rose-100']">
                {{ aluno.estado }}
              </span>
            </td>
<td class="p-5 text-right flex justify-end gap-2">
  <NuxtLink 
    :to="`/dashboard/admin/students/${aluno.utilizador_id}/historic`" 
    class="p-2 hover:bg-rose-50 rounded-lg text-stone-400 hover:text-rose-500 transition-colors"
    title="Ver Dossiê Completo"
  >
    <BootstrapIcon name="journal-richtext" class="w-5 h-5" />
  </NuxtLink>

  <NuxtLink 
    :to="`/dashboard/admin/students/${aluno.utilizador_id}`" 
    class="p-2 hover:bg-stone-100 rounded-lg text-stone-400 hover:text-gray-800 transition-colors"
    title="Editar Dados"
  >
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
const filtroEstado = ref('Activo')

// Buscar a lista do Admin
const { data: estudantes, pending } = await useAsyncData('admin-students', () => api<any[]>('/admin/estudantes/'))

// Filtragem local baseada na pesquisa
const estudantesFiltrados = computed(() => {
  if (!estudantes.value) return []
  return estudantes.value.filter(a => {
    const matchesSearch = a.nome_completo.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                          a.num_estudante.includes(searchQuery.value)
    const matchesEstado = a.estado === filtroEstado.value
    return matchesSearch && matchesEstado
  })
})
</script>
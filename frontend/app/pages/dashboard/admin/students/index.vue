<template>
  <div class="space-y-8 dark:text-white max-w-7xl mx-auto p-4 md:p-8">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Gestão de Internos</h1>
        <p class="text-stone-500 dark:text-gray-400 mt-1">Administre todos os estudantes registados no internato.</p>
      </div>
      <NuxtLink to="/dashboard/admin/students/register" class="px-6 py-3 rounded-xl bg-gray-900 dark:bg-white text-white dark:text-gray-900 font-bold text-sm shadow-lg hover:opacity-90 transition-all flex items-center gap-2">
        <BootstrapIcon name="person-plus-fill" /> Novo Estudante
      </NuxtLink>
    </div>

    <div class="bg-white dark:bg-gray-800 p-4 rounded-[1.5rem] border border-stone-100 dark:border-gray-700 shadow-sm flex flex-col md:flex-row gap-4">
      <div class="flex-1 relative">
        <BootstrapIcon name="search" class="absolute left-4 top-1/2 -translate-y-1/2 text-stone-400" />
        <input v-model="searchQuery" type="text" placeholder="Pesquisar por nome, curso, BI..." class="w-full pl-12 pr-4 py-3 bg-stone-50 dark:bg-gray-700 border-none rounded-xl focus:ring-2 focus:ring-rose-200 outline-none transition-all" />
      </div>
      <select v-model="filtroEstado" class="px-4 py-3 bg-stone-50 dark:bg-gray-700 border-none rounded-xl focus:ring-2 focus:ring-rose-200 outline-none font-medium">
        <option value="Todos">Todos os Estados</option>
        <option value="Activo">Activos</option>
        <option value="Inactivo">Inactivos</option>
      </select>
    </div>

    <div v-if="pending" class="grid grid-cols-1 gap-4">
      <div v-for="i in 5" :key="i" class="h-16 bg-stone-100 dark:bg-gray-800 animate-pulse rounded-xl"></div>
    </div>

    <div v-else-if="error" class="p-10 text-center bg-rose-50 rounded-[2rem] border border-rose-100">
      <BootstrapIcon name="exclamation-circle" class="text-rose-500 w-12 h-12 mx-auto mb-4" />
      <p class="text-rose-800 font-bold">Erro ao carregar a lista de alunos.</p>
      <button @click="refresh()" class="mt-4 px-6 py-2 bg-rose-500 text-white rounded-lg">Tentar novamente</button>
    </div>

    <div v-else class="bg-white dark:bg-gray-800 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="border-b border-stone-100 dark:border-gray-700">
            <th class="p-5 text-xs font-black uppercase tracking-widest text-stone-400">Estudante</th>
            <th class="p-5 text-xs font-black uppercase tracking-widest text-stone-400">Curso / Quarto</th>
            <th class="p-5 text-xs font-black uppercase tracking-widest text-stone-400">Contacto</th>
            <th class="p-5 text-xs font-black uppercase tracking-widest text-stone-400">Estado</th>
            <th class="p-5 text-right text-xs font-black uppercase tracking-widest text-stone-400">Acções</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-stone-50 dark:divide-gray-700">
          <tr v-for="aluno in estudantesFiltrados" :key="aluno.utilizador_id" class="hover:bg-stone-50/50 dark:hover:bg-gray-700/30 transition-colors">
            <td class="p-5">
              <div class="flex items-center gap-3">
                <div class="h-10 w-10 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center font-bold">
                  {{ aluno.nome_completo.charAt(0) }}
                </div>
                <div>
                  <p class="font-bold text-gray-900 dark:text-white">{{ aluno.nome_completo }}</p>
                  <p class="text-xs text-stone-500">{{ aluno.bi || 'Sem BI' }}</p>
                </div>
              </div>
            </td>
            <td class="p-5">
              <p class="text-sm font-medium">{{ aluno.curso }}</p>
              <p class="text-xs text-stone-400">Quarto: {{ aluno.quarto_numero || 'Não alocado' }}</p>
            </td>
            <td class="p-5 text-sm">
              {{ aluno.telefone_pessoal || '—' }}
            </td>
            <td class="p-5">
              <span :class="['px-3 py-1 rounded-full text-[10px] font-black uppercase border', getEstadoColor(aluno.estado)]">
                {{ aluno.estado }}
              </span>
            </td>
            <td class="p-5 text-right flex justify-end gap-2">
              <NuxtLink :to="`/dashboard/admin/students/${aluno.utilizador_id}/historic`" class="p-2 hover:bg-rose-50 rounded-lg text-stone-400 hover:text-rose-500 transition-colors" title="Dossiê">
                <BootstrapIcon name="journal-richtext" class="w-5 h-5" />
              </NuxtLink>
              <NuxtLink :to="`/dashboard/admin/students/${aluno.utilizador_id}`" class="p-2 hover:bg-stone-100 rounded-lg text-stone-400 hover:text-gray-800 transition-colors" title="Editar">
                <BootstrapIcon name="pencil-square" class="w-5 h-5" />
              </NuxtLink>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="estudantesFiltrados.length === 0" class="p-20 text-center text-stone-400 font-medium">
        Nenhum estudante encontrado com estes filtros.
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Estudante } from '~/types/types'

const { api } = useApi()
const searchQuery = ref('')
const filtroEstado = ref('Activo')

const { data: estudantes, pending, error, refresh } = await useAsyncData<Estudante[]>(
  'admin-students-list', 
  () => api<Estudante[]>('/admin/estudantes/'),
  { server: false }
)

const estudantesFiltrados = computed(() => {
  if (!estudantes.value) return []
  const lista = Array.isArray(estudantes.value) ? estudantes.value : (estudantes.value.results || [])
  return lista.filter((aluno: any) => {
    const busca = searchQuery.value.toLowerCase()
    const matchesSearch = 
      aluno.nome_completo?.toLowerCase().includes(busca) ||
      aluno.curso?.toLowerCase().includes(busca) ||
      aluno.bi?.includes(busca)
    const matchesEstado = filtroEstado.value === 'Todos' || aluno.estado === filtroEstado.value
    return matchesSearch && matchesEstado
  })
})

const getEstadoColor = (estado: string) => {
  const colors: Record<string, string> = {
    'Activo': 'bg-emerald-50 text-emerald-600 border-emerald-100',
    'Inactivo': 'bg-stone-50 text-stone-600 border-stone-100',
  }
  return colors[estado] || 'bg-gray-50 text-gray-600 border-gray-100'
}
</script>
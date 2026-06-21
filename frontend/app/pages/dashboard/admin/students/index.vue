<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 md:mb-8">
      <div>
        <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">Gestão de Internos</h1>
        <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">Administre todos os estudantes registados no internato.</p>
      </div>
      <NuxtLink 
        to="/dashboard/admin/students/register" 
        class="px-5 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors flex items-center gap-2 min-h-[44px]"
      >
        <BootstrapIcon name="person-plus-fill" class="w-4 h-4" />
        Novo Estudante
      </NuxtLink>
    </div>

    <!-- Barra de pesquisa e filtros -->
    <div class="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col gap-3 mb-6">
      <!-- Linha 1: pesquisa + estado -->
      <div class="flex flex-col md:flex-row gap-3">
        <div class="flex-1 relative">
          <BootstrapIcon name="search" class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Pesquisar por nome, BI..." 
            class="w-full pl-10 pr-4 py-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors" 
          />
        </div>
        <select 
          v-model="filtroEstado" 
          class="px-4 py-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-medium cursor-pointer md:w-48"
        >
          <option value="Todos">Todos os Estados</option>
          <option value="Activo">Activos</option>
          <option value="Inactivo">Inactivos</option>
        </select>
      </div>

      <!-- Linha 2: curso + género + toggle de visualização -->
      <div class="flex flex-col sm:flex-row gap-3 items-start sm:items-center">
        <select 
          v-model="filtroCurso" 
          class="w-full sm:w-48 px-4 py-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-medium cursor-pointer"
        >
          <option value="">Todos os Cursos</option>
          <option v-for="curso in cursosUnicos" :key="curso" :value="curso">{{ curso }}</option>
        </select>

        <select 
          v-model="filtroGenero" 
          class="w-full sm:w-40 px-4 py-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-medium cursor-pointer"
        >
          <option value="">Todos os Géneros</option>
          <option value="M">Masculino</option>
          <option value="F">Feminino</option>
        </select>

        <!-- Toggle de visualização -->
        <div class="flex items-center gap-2 ml-auto">
          <button 
            @click="modoVisualizacao = 'cards'" 
            class="p-2 rounded-lg transition-colors"
            :class="modoVisualizacao === 'cards' ? 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400' : 'text-slate-400 hover:text-slate-600 dark:hover:text-slate-300'"
            title="Visualização em cards"
          >
            <BootstrapIcon name="grid-3x3-gap-fill" class="w-5 h-5" />
          </button>
          <button 
            @click="modoVisualizacao = 'tabela'" 
            class="p-2 rounded-lg transition-colors"
            :class="modoVisualizacao === 'tabela' ? 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400' : 'text-slate-400 hover:text-slate-600 dark:hover:text-slate-300'"
            title="Visualização em tabela"
          >
            <BootstrapIcon name="table" class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="pending" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="i in 6" :key="i" class="h-32 bg-slate-100 dark:bg-slate-800 animate-pulse rounded-xl"></div>
    </div>

    <!-- Erro -->
    <div v-else-if="error" class="p-10 text-center bg-red-50 dark:bg-red-900/20 rounded-xl border border-red-200 dark:border-red-800/30">
      <BootstrapIcon name="exclamation-circle" class="text-red-500 dark:text-red-400 w-12 h-12 mx-auto mb-4" />
      <p class="text-red-800 dark:text-red-300 font-semibold">Erro ao carregar a lista de alunos.</p>
      <button @click="refresh()" class="mt-4 px-5 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg text-sm font-medium transition-colors">Tentar novamente</button>
    </div>

    <!-- Lista de estudantes -->
    <div v-else>
      <!-- Modo Cards -->
      <div v-if="modoVisualizacao === 'cards'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-5">
        <div 
          v-for="aluno in estudantesFiltrados" 
          :key="aluno.utilizador_id"
          class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow p-5 flex flex-col"
        >
          <!-- Cabeçalho do card -->
          <div class="flex items-start gap-3 mb-3">
            <div class="h-12 w-12 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center text-lg font-bold border border-blue-100 dark:border-blue-800 shrink-0">
              {{ aluno.nome_completo?.charAt(0).toUpperCase() }}
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="font-semibold text-slate-900 dark:text-white truncate">{{ aluno.nome_completo }}</h3>
              <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{{ aluno.bi || 'Sem BI' }}</p>
            </div>
            <span :class="['px-2 py-0.5 rounded-md text-xs font-medium border shrink-0', getEstadoColor(aluno.estado)]">
              {{ aluno.estado }}
            </span>
          </div>

          <!-- Detalhes -->
          <div class="space-y-2 mb-4 flex-1">
            <div class="flex items-center gap-2 text-sm">
              <BootstrapIcon name="mortarboard" class="w-4 h-4 text-slate-400 shrink-0" />
              <span class="text-slate-700 dark:text-slate-300 truncate">{{ aluno.curso }}</span>
            </div>
            <div class="flex items-center gap-2 text-sm">
              <BootstrapIcon name="door-closed" class="w-4 h-4 text-slate-400 shrink-0" />
              <span class="text-slate-700 dark:text-slate-300">
                Bloco {{ aluno.bloco || 'Não alocado' }}
              </span>
            </div>
            <div class="flex items-center gap-2 text-sm">
              <BootstrapIcon name="telephone" class="w-4 h-4 text-slate-400 shrink-0" />
              <span class="text-slate-700 dark:text-slate-300">{{ aluno.telefone_pessoal || '—' }}</span>
            </div>
            <div class="flex items-center gap-2 text-sm">
              <BootstrapIcon name="calendar" class="w-4 h-4 text-slate-400 shrink-0" />
              <span class="text-slate-700 dark:text-slate-300">{{ aluno.data_entrada || 'S/D' }}</span>
            </div>
          </div>

          <!-- Ações -->
          <div class="flex justify-end gap-1 pt-2 border-t border-slate-100 dark:border-slate-800">
            <NuxtLink 
              :to="`/dashboard/admin/students/${aluno.utilizador_id}/historic`" 
              class="p-2 rounded-lg text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
              title="Dossiê"
            >
              <BootstrapIcon name="journal-richtext" class="w-5 h-5" />
            </NuxtLink>
            <NuxtLink 
              :to="`/dashboard/admin/students/${aluno.utilizador_id}`" 
              class="p-2 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              title="Editar"
            >
              <BootstrapIcon name="pencil-square" class="w-5 h-5" />
            </NuxtLink>
          </div>
        </div>
      </div>

      <!-- Modo Tabela -->
      <div v-else class="overflow-x-auto rounded-xl border border-slate-200 dark:border-slate-800">
        <table class="min-w-full divide-y divide-slate-200 dark:divide-slate-800 text-sm">
          <thead class="bg-slate-50 dark:bg-slate-800/50">
            <tr>
              <th class="px-4 py-3 text-left font-semibold text-slate-600 dark:text-slate-300">Nome</th>
              <th class="px-4 py-3 text-left font-semibold text-slate-600 dark:text-slate-300">Curso</th>
              <th class="px-4 py-3 text-left font-semibold text-slate-600 dark:text-slate-300">Bloco</th>
              <th class="px-4 py-3 text-left font-semibold text-slate-600 dark:text-slate-300">Género</th>
              <th class="px-4 py-3 text-left font-semibold text-slate-600 dark:text-slate-300">Estado</th>
              <th class="px-4 py-3 text-left font-semibold text-slate-600 dark:text-slate-300">BI</th>
              <th class="px-4 py-3 text-right font-semibold text-slate-600 dark:text-slate-300">Ações</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-200 dark:divide-slate-800 bg-white dark:bg-slate-900">
            <tr v-for="aluno in estudantesFiltrados" :key="aluno.utilizador_id" class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
              <td class="px-4 py-3 font-medium text-slate-900 dark:text-white">{{ aluno.nome_completo }}</td>
              <td class="px-4 py-3 text-slate-700 dark:text-slate-300">{{ aluno.curso }}</td>
              <td class="px-4 py-3 text-slate-700 dark:text-slate-300">{{ aluno.bloco || '—' }}</td>
              <td class="px-4 py-3 text-slate-700 dark:text-slate-300">{{ aluno.genero === 'M' ? 'Masculino' : 'Feminino' }}</td>
              <td class="px-4 py-3">
                <span :class="['px-2 py-0.5 rounded-md text-xs font-medium border', getEstadoColor(aluno.estado)]">
                  {{ aluno.estado }}
                </span>
              </td>
              <td class="px-4 py-3 text-slate-700 dark:text-slate-300">{{ aluno.bi || '—' }}</td>
              <td class="px-4 py-3 text-right">
                <NuxtLink 
                  :to="`/dashboard/admin/students/${aluno.utilizador_id}/historic`" 
                  class="p-1.5 rounded-lg text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors inline-block"
                  title="Dossiê"
                >
                  <BootstrapIcon name="journal-richtext" class="w-4 h-4" />
                </NuxtLink>
                <NuxtLink 
                  :to="`/dashboard/admin/students/${aluno.utilizador_id}`" 
                  class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors inline-block ml-1"
                  title="Editar"
                >
                  <BootstrapIcon name="pencil-square" class="w-4 h-4" />
                </NuxtLink>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Mensagem quando não há resultados -->
      <div v-if="estudantesFiltrados.length === 0" class="p-16 text-center bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800">
        <BootstrapIcon name="people" class="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-3" />
        <p class="text-slate-500 dark:text-slate-400 font-medium">Nenhum estudante encontrado com estes filtros.</p>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import type { Estudante } from '~/types/types'

const { api } = useApi()
const searchQuery = ref('')
const filtroEstado = ref('Activo')
const filtroCurso = ref('')
const filtroGenero = ref('')
const modoVisualizacao = ref<'cards' | 'tabela'>('cards') // padrão cards

const { data: estudantes, pending, error, refresh } = await useAsyncData<Estudante[]>(
  'admin-students-list', 
  () => api<Estudante[]>('/admin/estudantes/'),
  { server: false }
)
console.log(estudantes)
// Extrair cursos únicos para o dropdown
const cursosUnicos = computed(() => {
  if (!estudantes.value) return []
  const lista = Array.isArray(estudantes.value) ? estudantes.value : (estudantes.value.results || [])
  const cursos = lista.map(aluno => aluno.curso).filter(Boolean)
  return [...new Set(cursos)].sort()
})

const estudantesFiltrados = computed(() => {
  if (!estudantes.value) return []
  const lista = Array.isArray(estudantes.value) ? estudantes.value : (estudantes.value.results || [])
  return lista.filter((aluno: any) => {
    const busca = searchQuery.value.toLowerCase()
    const matchesSearch = 
      aluno.nome_completo?.toLowerCase().includes(busca) ||
      aluno.curso?.toLowerCase().includes(busca) ||
      aluno.bi?.includes(busca) ||
      aluno.nuit?.includes(busca)
    
    const matchesEstado = filtroEstado.value === 'Todos' || aluno.estado === filtroEstado.value
    const matchesCurso = !filtroCurso.value || aluno.curso === filtroCurso.value
    const matchesGenero = !filtroGenero.value || aluno.genero === filtroGenero.value

    return matchesSearch && matchesEstado && matchesCurso && matchesGenero
  })
})

const getEstadoColor = (estado: string) => {
  const colors: Record<string, string> = {
    'Activo': 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30',
    'Inactivo': 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-slate-800 dark:text-slate-400 dark:border-slate-700',
  }
  return colors[estado] || 'bg-gray-50 text-gray-600 border-gray-100'
}
</script>
<template>
  <div class="space-y-6 dark:text-white max-w-4xl">
    <h1 class="text-3xl font-bold">Histórico de Presenças (Meus Educandos)</h1>

    <div class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow">
      <table class="w-full">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th class="table-header">Educando</th>
            <th class="table-header">Data</th>
            <th class="table-header">Estado</th>
          </tr>
        </thead>
        <tbody class="divide-y dark:divide-gray-700">
          <tr v-if="pending" class="text-center">
            <td colspan="3" class="table-cell text-gray-500">A carregar histórico...</td>
          </tr>
          <tr v-else-if="presencasComNome.length === 0">
            <td colspan="3" class="table-cell text-center text-gray-500">Nenhum registo de presença encontrado.</td>
          </tr>
          <tr v-for="item in presencasComNome" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td class="table-cell font-medium">{{ item.nome_estudante }}</td>
            <td class="table-cell">{{ item.data_presenca }}</td>
            <td class="table-cell">
              <span :class="getStatusClass(item.estado)">
                {{ item.estado }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const { api } = useApi()

// 1. Buscar TODOS os dados necessários (em paralelo)
const { data, pending } = await useAsyncData(
  'encarregado-presencas',
  async () => {
    const [presencas, educandos] = await Promise.all([
      api<any[]>('/perfil-encarregado/presencas/'),
      api<any[]>('/perfil-encarregado/meus-educandos/'),
    ])
    return { presencas, educandos }
  },
  { lazy: true, default: () => ({ presencas: [], educandos: [] }) }
)

// 2. Criar um 'computed' para "juntar" os nomes
const presencasComNome = computed(() => {
  if (!data.value?.presencas || !data.value?.educandos) return []
  
  const mapaNomes = new Map(
    data.value.educandos.map(e => [e.utilizador_id, e.nome_completo])
  )
  
  return data.value.presencas.map(item => ({
    ...item,
    nome_estudante: mapaNomes.get(item.estudante) || 'Desconhecido'
  }))
})

// Helper de Estilo
function getStatusClass(estado: string) {
  if (estado === 'Presente') return 'status-green'
  if (estado === 'Ausente') return 'status-red'
  if (estado === 'Justificado') return 'status-yellow'
  return ''
}
</script>

<style scoped>
.table-header { @apply px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase; }
.table-cell { @apply px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white; }
.status-green { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100; }
.status-yellow { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100; }
.status-red { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100; }
</style>
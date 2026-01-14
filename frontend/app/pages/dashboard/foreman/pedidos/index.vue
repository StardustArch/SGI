<template>
  <div class="space-y-6 dark:text-white max-w-6xl">
    <h1 class="text-3xl font-bold">Histórico de Pedidos de Saída (Meus Educandos)</h1>

    <div class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow">
      <table class="w-full">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th class="table-header">Educando</th>
            <th class="table-header">Data Submissão</th>
            <th class="table-header">Saída</th>
            <th class="table-header">Retorno</th>
            <th class="table-header">Estado</th>
            <th class="table-header">Observação (Admin)</th>
          </tr>
        </thead>
        <tbody class="divide-y dark:divide-gray-700">
          <tr v-if="pending" class="text-center">
            <td colspan="6" class="table-cell text-gray-500">A carregar histórico...</td>
          </tr>
          <tr v-else-if="pedidos.length === 0">
            <td colspan="6" class="table-cell text-center text-gray-500">Nenhum pedido de saída encontrado.</td>
          </tr>
          <tr v-for="item in pedidos" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td class="table-cell font-medium">{{ item.estudante_nome }}</td>
            <td class="table-cell">{{ new Date(item.data_submissao).toLocaleString() }}</td>
            <td class="table-cell">{{ item.data_saida_pretendida }}</td>
            <td class="table-cell">{{ item.data_retorno_pretendida }}</td>
            <td class="table-cell">
              <span :class="getStatusClass(item.estado)">
                {{ getEstadoLegivel(item.estado) }}
              </span>
            </td>
            <td class="table-cell">{{ item.observacao_admin || 'N/A' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">

const { api } = useApi()

// Buscar os dados do endpoint /perfil-encarregado/pedidos-saida/
// Este endpoint já inclui o 'estudante_nome' (graças ao PedidoSaidaListAdminSerializer)
const { data: pedidos, pending } = await useAsyncData(
  'encarregado-pedidos',
  () => api<any[]>('/perfil-encarregado/pedidos-saida/'),
  { lazy: true, default: () => [] } // Inicia como array vazio
)

// --- Funções Helper (Estilo) ---
function getEstadoLegivel(estado: string) {
  if (estado === 'Aprovado_Admin') return 'Aprovado'
  if (estado === 'Rejeitado') return 'Rejeitado'
  return 'Pendente'
}

function getStatusClass(estado: string) {
  if (estado === 'Aprovado_Admin') return 'status-green'
  if (estado === 'Rejeitado') return 'status-red'
  return 'status-yellow'
}
</script>

<style scoped>
.table-header { @apply px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase; }
.table-cell { @apply px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white; }
.status-green { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100; }
.status-yellow { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100; }
.status-red { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100; }
</style>
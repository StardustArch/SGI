<template>
  <div class="space-y-6 dark:text-white max-w-4xl">
    <h1 class="text-3xl font-bold">Meu Histórico Financeiro</h1>

    <div class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow">
      <table class="w-full">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th class="table-header">Mês</th>
            <th class="table-header">Estado</th>
            <th class="table-header">Valor Pago</th>
            <th class="table-header">Método</th>
            <th class="table-header">Data Conf.</th>
          </tr>
        </thead>
        <tbody class="divide-y dark:divide-gray-700">
          <tr v-if="pending" class="text-center">
            <td colspan="5" class="table-cell text-gray-500">A carregar histórico...</td>
          </tr>
          <tr v-else-if="financas.length === 0">
            <td colspan="5" class="table-cell text-center text-gray-500">Nenhum registo financeiro encontrado.</td>
          </tr>
          <tr v-for="item in financas" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td class="table-cell">{{ item.mes_referencia }}</td>
            <td class="table-cell">
              <span :class="item.estado === 'Pago' ? 'status-green' : 'status-yellow'">
                {{ item.estado }}
              </span>
            </td>
            <td class="table-cell">{{ item.valor_pago }}</td>
            <td class="table-cell">{{ item.metodo_pagamento || 'N/A' }}</td>
            <td class="table-cell">{{ item.data_pagamento_confirmado || 'N/A' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">

const { api } = useApi()

// Buscar os dados do endpoint /perfil/mensalidades/
const { data: financas, pending } = await useAsyncData(
  'estudante-financas',
  () => api<any[]>('/perfil/mensalidades/'),
  { lazy: true, default: () => [] } // Inicia como array vazio
)
</script>

<style scoped>
/* Estilos comuns para tabelas e status */
.table-header { @apply px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase; }
.table-cell { @apply px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white; }
.status-green { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100; }
.status-yellow { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100; }
</style>
<template>
  <div class="space-y-6 dark:text-white max-w-4xl">
    <h1 class="text-3xl font-bold">Meu Histórico Disciplinar</h1>

    <div class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow">
      <table class="w-full">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th class="table-header">Data</th>
            <th class="table-header">Tipo</th>
            <th class="table-header">Descrição</th>
          </tr>
        </thead>
        <tbody class="divide-y dark:divide-gray-700">
          <tr v-if="pending" class="text-center">
            <td colspan="3" class="table-cell text-gray-500">A carregar histórico...</td>
          </tr>
          <tr v-else-if="sancoes.length === 0">
            <td colspan="3" class="table-cell text-center text-gray-500">Nenhum registo disciplinar encontrado.</td>
          </tr>
          <tr v-for="item in sancoes" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td class="table-cell">{{ item.data_ocorrencia }}</td>
            <td class="table-cell">{{ item.tipo_sancao }}</td>
            <td class="table-cell min-w-[300px] whitespace-normal">{{ item.descricao }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">

const { api } = useApi()

// Buscar os dados do endpoint /perfil/sancoes/
const { data: sancoes, pending } = await useAsyncData(
  'estudante-sancoes',
  () => api<any[]>('/perfil/sancoes/'),
  { lazy: true, default: () => [] } // Inicia como array vazio
)
</script>

<style scoped>
.table-header { @apply px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase; }
.table-cell { @apply px-6 py-4 text-sm text-gray-900 dark:text-white; }
</style>
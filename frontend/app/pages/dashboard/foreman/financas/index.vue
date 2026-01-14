<template>
    <div class="space-y-6 dark:text-white max-w-6xl">
        <h1 class="text-3xl font-bold">Histórico Financeiro (Meus Educandos)</h1>

        <div class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow">
            <table class="w-full">
                <thead class="bg-gray-50 dark:bg-gray-700">
                    <tr>
                        <th class="table-header">Educando</th>
                        <th class="table-header">Mês</th>
                        <th class="table-header">Estado</th>
                        <th class="table-header">Valor Pago</th>
                        <th class="table-header">Método</th>
                        <th class="table-header">Data Conf.</th>
                    </tr>
                </thead>
                <tbody class="divide-y dark:divide-gray-700">
                    <tr v-if="pending" class="text-center">
                        <td colspan="6" class="table-cell text-gray-500">A carregar histórico...</td>
                    </tr>
                    <tr v-else-if="financasComNome.length === 0">
                        <td colspan="6" class="table-cell text-center text-gray-500">Nenhum registo financeiro
                            encontrado.</td>
                    </tr>
                    <tr v-for="item in financasComNome" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                        <td class="table-cell font-medium">{{ item.nome_estudante }}</td>
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
import { computed } from 'vue'

const { api } = useApi()

// 1. Buscar TODOS os dados necessários (em paralelo)
const { data, pending } = await useAsyncData(
    'encarregado-financas',
    async () => {
        // Precisamos da lista de mensalidades E da lista de educandos (para saber os nomes)
        const [financas, educandos] = await Promise.all([
            api<any[]>('/perfil-encarregado/mensalidades/'),
            api<any[]>('/perfil-encarregado/meus-educandos/'),
        ])
        return { financas, educandos }
    },
    { lazy: true, default: () => ({ financas: [], educandos: [] }) }
)

// 2. Criar um 'computed' para "juntar" os nomes às finanças
const financasComNome = computed(() => {
    if (!data.value?.financas || !data.value?.educandos) return []

    // Criar um mapa (ID -> Nome) para consulta rápida
    const mapaNomes = new Map(
        data.value.educandos.map(e => [e.utilizador_id, e.nome_completo])
    )

    // Adicionar o 'nome_estudante' a cada objecto de finança
    return data.value.financas.map(item => ({
        ...item,
        nome_estudante: mapaNomes.get(item.estudante) || 'Desconhecido'
    }))
})
</script>

<style scoped>
/* Estilos comuns para tabelas e status */
.table-header {
    @apply px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase;
}

.table-cell {
    @apply px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white;
}

.status-green {
    @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100;
}

.status-yellow {
    @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100;
}
</style>
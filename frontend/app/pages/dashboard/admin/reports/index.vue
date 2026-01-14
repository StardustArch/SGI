<template>
  <div>
    <h1 class="text-3xl font-bold dark:text-white">
      Relatórios do Administrador
    </h1>

    <div v-if="pending" class="dark:text-white mt-4">A carregar relatórios...</div>

    <!-- Grelha de Relatórios -->
    <div v-if="!pending && relatorios" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
      
      <!-- Card: Relatório Financeiro -->
      <div class="p-4 bg-white dark:bg-gray-800 rounded-lg shadow">
        <h2 class="text-lg font-semibold dark:text-white">Finanças (Mês)</h2>
        <div v-if="relatorios.financeiro" class="mt-2 space-y-1">
          <p class="dark:text-gray-300">Total Arrecadado: <span class="font-bold text-green-600 dark:text-green-400">{{ relatorios.financeiro.total_arrecadado_mes }}</span></p>
          <p class="dark:text-gray-300">Pendentes: <span class="font-bold text-red-600 dark:text-red-400">{{ relatorios.financeiro.total_estudantes_pendentes }}</span></p>
        </div>
      </div>
      
      <!-- Card: Top Infratores -->
      <div class="p-4 bg-white dark:bg-gray-800 rounded-lg shadow">
        <h2 class="text-lg font-semibold dark:text-white">Top Infratores (Mês)</h2>
        <ul v-if="relatorios.topInfratores?.length" class="mt-2 space-y-1">
          <li v-for="item in relatorios.topInfratores" :key="item.estudante_id" class="dark:text-gray-300">
            {{ item.nome_completo }}: <span class="font-bold">{{ item.total_sancoes }}</span>
          </li>
        </ul>
        <p v-else class="dark:text-gray-400 text-sm">Nenhuma sanção este mês.</p>
      </div>

      <!-- Card: Pedidos de Saída -->
      <div class="p-4 bg-white dark:bg-gray-800 rounded-lg shadow">
        <h2 class="text-lg font-semibold dark:text-white">Pedidos de Saída (Mês)</h2>
        <div v-if="relatorios.pedidosSaida" class="mt-2 space-y-1">
          <p class="dark:text-gray-300">Pendentes: <span class="font-bold text-yellow-600 dark:text-yellow-400">{{ relatorios.pedidosSaida.total_pendentes }}</span></p>
          <p class="dark:text-gray-300">Aprovados: <span class="font-bold text-green-600 dark:text-green-400">{{ relatorios.pedidosSaida.total_aprovados }}</span></p>
        </div>
      </div>
      
      <!-- TODO: Adicionar os outros relatórios (Top Ausentes, Tipo de Sanção) -->

    </div>
  </div>
</template>

<script setup lang="ts">
// 1. Importar o seu novo composable 'useApi'

// 2. Obter a função 'api' do composable
const { api } = useApi()

// 3. 'accessToken' e 'authHeaders' foram REMOVIDOS
//    (O 'useApi' trata disto agora)

// 4. Usar useAsyncData, e chamar 'api' dentro dele
const { data: relatorios, pending } = await useAsyncData(
  'admin-dashboard-reports', // Chave única
  async () => {
    
    // 5. Usar 'api' e remover '/api/v1' e 'headers'
    const financeiro = api<any>('/relatorios/financeiro/')
    const topInfratores = api<any>('/relatorios/disciplina/top-10/') // Nota: O seu URL era top-10, mas a API é top-5
    const pedidosSaida = api<any>('/relatorios/pedidos-saida/sumario/')
    
    // 6. Adicionar os relatórios que faltavam
    const topAusentes = api<any>('/relatorios/assiduidade/top-ausentes/')
    const porTipo = api<any>('/relatorios/disciplina/por-tipo/')

    // 7. Espera que todos os pedidos terminem
    const [fin, infratores, saida, ausentes, tipo] = await Promise.all([
      financeiro,
      topInfratores,
      pedidosSaida,
      topAusentes,
      porTipo
    ])

    // 8. Retorna o objecto completo para o 'relatorios'
    return {
      financeiro: fin,
      topInfratores: infratores,
      pedidosSaida: saida,
      topAusentes: ausentes,
      porTipo: tipo
    }
  },
  { lazy: true } // Não bloquear a navegação
)
</script>
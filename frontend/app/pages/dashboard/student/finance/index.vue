<template>
  <div class="space-y-8 dark:text-white max-w-7xl mx-auto p-4 md:p-8">
    
    <div>
      <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Minhas Finanças</h1>
      <p class="text-stone-500 dark:text-gray-400 mt-1 text-lg">Histórico de mensalidades e pagamentos.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      
      <div class="bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-900/20 dark:to-teal-900/20 p-6 rounded-[2rem] border border-emerald-100 dark:border-emerald-800 flex items-center gap-4 relative overflow-hidden">
        <div class="absolute right-0 top-0 w-32 h-32 bg-emerald-400/10 rounded-full blur-3xl -mr-10 -mt-10"></div>
        <div class="p-3 bg-white dark:bg-emerald-900 rounded-2xl shadow-sm text-emerald-600 z-10">
          <BootstrapIcon name="cash-stack" class="w-8 h-8" />
        </div>
        <div class="z-10">
          <p class="text-stone-500 dark:text-gray-400 text-xs font-bold uppercase tracking-wider">Total Pago</p>
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white">
            {{ formatMoeda(stats.total_pago) }}
          </h3>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 flex items-center gap-4 shadow-sm">
        <div class="p-3 bg-amber-50 dark:bg-amber-900/30 rounded-2xl text-amber-600">
          <BootstrapIcon name="clock-history" class="w-8 h-8" />
        </div>
        <div>
          <p class="text-stone-500 dark:text-gray-400 text-xs font-bold uppercase tracking-wider">Por Pagar</p>
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white">
            {{ stats.pendentes }} <span class="text-sm font-normal text-stone-400">Mensalidades</span>
          </h3>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 flex items-center gap-4 shadow-sm lg:col-span-1 md:col-span-2">
         <div class="p-3 bg-indigo-50 dark:bg-indigo-900/30 rounded-2xl text-indigo-600">
          <BootstrapIcon name="calendar-event" class="w-8 h-8" />
        </div>
        <div>
           <p class="text-stone-500 dark:text-gray-400 text-xs font-bold uppercase tracking-wider">Valor Mensal</p>
           <h3 class="text-2xl font-bold text-indigo-600">25,000.00 MT</h3>
        </div>
      </div>
    </div>

    <div>
      
      <div v-if="pending" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="n in 3" :key="n" class="bg-white dark:bg-gray-800 rounded-[1.5rem] p-6 shadow-sm border border-stone-100 dark:border-gray-700 animate-pulse h-48"></div>
      </div>

      <div v-else-if="pagamentos.length === 0" class="flex flex-col items-center justify-center py-20 bg-stone-50/50 dark:bg-gray-800/50 rounded-[2rem] border border-stone-100 dark:border-gray-700 text-center">
        <div class="bg-white p-4 rounded-full shadow-sm mb-4">
           <BootstrapIcon name="receipt" class="w-10 h-10 text-stone-300" />
        </div>
        <p class="text-stone-500 font-medium">Nenhum registo financeiro encontrado.</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        
        <div 
          v-for="item in pagamentos" 
          :key="item.id"
          class="group bg-white dark:bg-gray-800 rounded-[1.5rem] p-6 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 border border-stone-100 dark:border-gray-700 flex flex-col relative overflow-hidden"
        >
          <div :class="[
            'absolute left-0 top-0 bottom-0 w-1.5',
            item.estado === 'Pago' ? 'bg-emerald-400' : (item.estado === 'Atraso' ? 'bg-rose-400' : 'bg-amber-400')
          ]"></div>

          <div class="flex justify-between items-start mb-4 pl-3">
            <div>
              <p class="text-[10px] text-stone-400 uppercase font-bold tracking-wider mb-1">Mês de Referência</p>
              <h3 class="text-lg font-bold text-gray-800 dark:text-white capitalize">
                {{ formatMes(item.mes_referencia) }}
              </h3>
            </div>
            
            <span :class="[
              'px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border',
              item.estado === 'Pago' 
                ? 'bg-emerald-50 text-emerald-700 border-emerald-100 dark:bg-emerald-900/30 dark:text-emerald-300' 
                : (item.estado === 'Atraso' ? 'bg-rose-50 text-rose-700 border-rose-100' : 'bg-amber-50 text-amber-700 border-amber-100')
            ]">
              {{ item.estado }}
            </span>
          </div>

          <div class="border-t-2 border-dashed border-stone-100 dark:border-gray-700 my-2 mx-[-1.5rem]"></div>

          <div class="pl-3 py-2 space-y-3">
              <div>
                 <p class="text-[10px] text-stone-400 uppercase font-bold tracking-wider mb-1">Valor</p>
                 <div class="flex items-baseline gap-1">
                    <span class="text-sm text-stone-500 font-medium">MZN</span>
                    <span class="text-2xl font-bold text-gray-900 dark:text-white">
                      {{ item.valor_pago > 0 ? formatMoeda(item.valor_pago).replace('MT', '') : '25,000.00' }}
                    </span>
                 </div>
              </div>

              <div v-if="item.estado === 'Pago'">
                 <p class="text-[10px] text-stone-400 uppercase font-bold tracking-wider mb-1">Método</p>
                 <p class="text-sm font-medium text-gray-700 dark:text-gray-300 flex items-center gap-2">
                    <BootstrapIcon name="credit-card" class="w-4 h-4 text-stone-400" />
                    {{ item.metodo_pagamento || 'Depósito Bancário' }}
                 </p>
              </div>

              <div v-if="item.data_pagamento_confirmado">
                 <p class="text-[10px] text-stone-400 uppercase font-bold tracking-wider mb-1">Data Confirmação</p>
                 <p class="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {{ formatDate(item.data_pagamento_confirmado) }}
                 </p>
              </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { api } = useApi()

// Carregar Dados
const { data: pagamentos, pending } = await useAsyncData('student-fin', () => api<any[]>('/student/financial/'), { default: () => [] })

// Calcular Estatísticas Locais (já que a API do aluno só devolve a lista)
const stats = computed(() => {
  if (!pagamentos.value) return { total_pago: 0, pendentes: 0 }
  
  const pagos = pagamentos.value.filter((p: any) => p.estado === 'Pago')
  const pendentes = pagamentos.value.filter((p: any) => p.estado !== 'Pago')
  
  const total = pagos.reduce((acc: number, curr: any) => acc + Number(curr.valor_pago), 0)
  
  return {
    total_pago: total,
    pendentes: pendentes.length
  }
})

// Helpers
const formatMoeda = (valor: any) => {
  return new Intl.NumberFormat('pt-MZ', { style: 'currency', currency: 'MZN' }).format(Number(valor))
}
const formatMes = (dataStr: string) => {
    if (!dataStr) return '---'
    return new Date(dataStr).toLocaleDateString('pt-PT', { month: 'long', year: 'numeric' })
}
const formatDate = (dataStr: string) => {
    return new Date(dataStr).toLocaleDateString('pt-PT')
}
</script>
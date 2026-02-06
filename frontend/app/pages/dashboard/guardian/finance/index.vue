<template>
  <div class="space-y-8 dark:text-white max-w-8xl mx-auto p-4 md:p-8">
    
    <div>
      <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Extrato Financeiro</h1>
      <p class="text-stone-500 dark:text-gray-400 mt-1 text-lg">Histórico consolidado de pagamentos e mensalidades.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      
      <div class="bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-900/20 dark:to-teal-900/20 p-6 rounded-[2rem] border border-emerald-100 dark:border-emerald-800 flex items-center gap-4 relative overflow-hidden">
        <div class="absolute right-0 top-0 w-32 h-32 bg-emerald-400/10 rounded-full blur-3xl -mr-10 -mt-10"></div>
        <div class="p-3 bg-white dark:bg-emerald-900 rounded-2xl shadow-sm text-emerald-600 z-10">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        </div>
        <div class="z-10">
          <p class="text-stone-500 dark:text-gray-400 text-xs font-bold uppercase tracking-wider">Total Investido</p>
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white">
            {{ formatMoeda(stats?.total_pago || 0) }}
          </h3>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 flex items-center gap-4 shadow-sm hover:shadow-md transition-shadow">
        <div class="p-3 bg-amber-50 dark:bg-amber-900/30 rounded-2xl text-amber-600">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        </div>
        <div>
          <p class="text-stone-500 dark:text-gray-400 text-xs font-bold uppercase tracking-wider">Por Pagar</p>
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats?.faturas_pendentes || 0 }} <span class="text-sm font-normal text-stone-400">Mensalidades</span></h3>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 flex items-center gap-4 shadow-sm hover:shadow-md transition-shadow">
        <div class="p-3 bg-rose-50 dark:bg-rose-900/30 rounded-2xl text-rose-600">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
        </div>
        <div>
          <p class="text-stone-500 dark:text-gray-400 text-xs font-bold uppercase tracking-wider">Em Atraso</p>
          <h3 class="text-2xl font-bold text-rose-600">{{ stats?.faturas_atraso || 0 }} <span class="text-sm font-normal text-stone-400">Faturas</span></h3>
        </div>
      </div>
    </div>

    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 pt-4 border-t border-stone-100 dark:border-gray-700">
      
      <div class="flex p-1 bg-stone-100 dark:bg-gray-800 rounded-xl overflow-x-auto max-w-full">
          <button 
              v-for="estado in ['Todos', 'Pendente', 'Pago', 'Atraso']"
              :key="estado"
              @click="filtros.estado = estado === 'Todos' ? null : estado; page = 1"
              :class="[
                  'px-4 py-2 text-xs font-bold rounded-lg transition-all whitespace-nowrap',
                  (filtros.estado === estado || (estado === 'Todos' && !filtros.estado))
                    ? 'bg-white text-gray-800 shadow-sm dark:bg-gray-700 dark:text-white' 
                    : 'text-stone-500 hover:text-stone-700 dark:text-stone-400'
              ]"
          >
              {{ estado }}
          </button>
      </div>

      <div class="w-full md:w-64">
        <select 
          v-model="filtros.estudante" 
          @change="page = 1"
          class="w-full appearance-none bg-white dark:bg-gray-800 border border-stone-200 dark:border-gray-700 text-gray-700 dark:text-gray-200 py-2.5 px-4 rounded-xl focus:outline-none focus:ring-2 focus:ring-rose-200 font-medium text-sm shadow-sm cursor-pointer"
        >
          <option :value="null">Todos os Educandos</option>
          <option v-for="filho in educandos" :key="filho.utilizador_id" :value="filho.utilizador_id">
            {{ filho.nome_completo }}
          </option>
        </select>
      </div>
    </div>

    <div>
      
      <div v-if="pending" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="n in 3" :key="n" class="bg-white dark:bg-gray-800 rounded-[1.5rem] p-6 shadow-sm border border-stone-100 dark:border-gray-700 animate-pulse h-48"></div>
      </div>

      <div v-else-if="financasComNome.length === 0" class="flex flex-col items-center justify-center py-20 bg-stone-50/50 dark:bg-gray-800/50 rounded-[2rem] border border-stone-100 dark:border-gray-700 text-center">
        <div class="bg-white p-4 rounded-full shadow-sm mb-4">
           <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-stone-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
        </div>
        <p class="text-stone-500 font-medium">Nenhum registo encontrado com estes filtros.</p>
        <button v-if="filtros.estado || filtros.estudante" @click="limparFiltros" class="mt-2 text-rose-500 text-sm font-bold hover:underline">Limpar Filtros</button>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        
        <div 
          v-for="item in financasComNome" 
          :key="item.id"
          class="group bg-white dark:bg-gray-800 rounded-[1.5rem] p-6 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 border border-stone-100 dark:border-gray-700 flex flex-col relative overflow-hidden"
        >
          <div :class="[
            'absolute left-0 top-0 bottom-0 w-1.5',
            item.estado === 'Pago' ? 'bg-emerald-400' : (item.estado === 'Atraso' ? 'bg-rose-400' : 'bg-amber-400')
          ]"></div>

          <div class="flex justify-between items-start mb-4 pl-3">
            <div>
              <p class="text-[10px] text-stone-400 uppercase font-bold tracking-wider mb-1">Referência</p>
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

          <div class="pl-3 py-2">
              <div class="flex items-baseline gap-1 mb-1">
                  <span class="text-sm text-stone-500 font-medium">MZN</span>
                  <span class="text-2xl font-bold text-gray-900 dark:text-white">
                    {{ item.estado === 'Pago' ? item.valor_pago : (item.valor_devido || '25,000') }}
                  </span>
              </div>
              <p class="text-xs text-stone-400 mt-1">
                 Vencimento: {{ item.data_vencimento || '---' }}
              </p>
          </div>

          <div class="mt-auto pt-4 pl-3 flex items-center justify-between">
             <div class="flex items-center gap-2">
                <div class="h-6 w-6 rounded-full bg-stone-100 dark:bg-gray-700 flex items-center justify-center text-[10px] font-bold text-stone-600 dark:text-stone-300">
                  {{ getIniciais(item.nome_estudante) }}
                </div>
                <span class="text-xs font-bold text-stone-600 dark:text-gray-300 truncate max-w-[100px]">
                    {{ item.nome_estudante.split(' ')[0] }}
                </span>
             </div>

             <button 
                v-if="item.estado !== 'Pago'"
                @click="abrirModalPagamento(item)"
                class="text-xs font-bold text-rose-500 hover:text-rose-700 underline"
             >
               Pagar
             </button>
             <span v-else class="text-xs font-bold text-emerald-500 flex items-center gap-1">
               <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
               Pago
             </span>
          </div>

        </div>
      </div>

      <div v-if="financasComNome.length > 0" class="flex justify-center items-center gap-4 mt-8">
        <button 
          @click="page--" 
          :disabled="!data?.financas?.previous"
          class="h-10 w-10 rounded-full border border-stone-200 dark:border-gray-600 flex items-center justify-center text-stone-500 hover:bg-stone-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
        </button>
        <span class="text-sm font-medium text-stone-600 dark:text-gray-400">Página {{ page }}</span>
        <button 
          @click="page++" 
          :disabled="!data?.financas?.next"
          class="h-10 w-10 rounded-full border border-stone-200 dark:border-gray-600 flex items-center justify-center text-stone-500 hover:bg-stone-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
        </button>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
const { api } = useApi()
const route = useRoute() // <--- Importante: Precisamos ler a rota
// Estados Reativos
const page = ref(1)
const filtros = reactive({
  estudante: route.query.student ? Number(route.query.student) : null as number | null,
  estado: null as string | null
})
// 1. Carregar lista de filhos (para o Dropdown)
const { data: educandos } = await useAsyncData(
  'filtros-educandos', 
  () => api<any[]>('/perfil-encarregado/meus-educandos/')
)

// 2. Carregar Dados (Stats + Lista Paginada e Filtrada)
const { data, pending, refresh } = await useAsyncData(
  'encarregado-financas-full',
  async () => {
    // Construir query params
    const params: any = { page: page.value }
    if (filtros.estudante) params.estudante = filtros.estudante
    if (filtros.estado) params.estado = filtros.estado

    const [financas, stats] = await Promise.all([
       api<any>('/perfil-encarregado/mensalidades/', { params }),
       api<any>('/perfil-encarregado/financas-resumo/') // Stats globais
    ])
    return { financas, stats }
  },
  { 
    watch: [page, filtros] // Recarrega se filtros mudarem
  }
)

const stats = computed(() => data.value?.stats)

// Mapper: Juntar nomes (como a lista vem misturada, precisamos de saber quem é quem)
const financasComNome = computed(() => {
    if (!data.value?.financas?.results || !educandos.value) return []
    
    const lista = data.value.financas.results
    const mapaNomes = new Map(educandos.value.map((e: any) => [e.utilizador_id, e.nome_completo]))

    return lista.map((item: any) => ({
        ...item,
        nome_estudante: mapaNomes.get(item.estudante) || 'Desconhecido'
    }))
})

// Ações
const limparFiltros = () => {
  filtros.estudante = null
  filtros.estado = null
  page.value = 1
}

const abrirModalPagamento = (item: any) => {
  // FUTURO: Aqui abrirá o modal para upload do comprovativo (PATCH)
  // navigateTo(`/dashboard/guardian/finance/pay/${item.id}`)
  alert(`Funcionalidade de Upload para: ${item.mes_referencia} - ${item.nome_estudante}`)
}

// Utilitários
const getIniciais = (nome: string) => {
  const limpo = (nome || '').trim();
  if (!limpo) return '??';
  
  const partes = limpo.split(/\s+/);
  
  // Usamos '?.' para aceder com segurança e '|| ""' caso falhe
  const primeira = partes[0]?.[0] || '';
  const ultima = partes.length > 1 ? partes[partes.length - 1]?.[0] || '' : '';

  return (primeira + ultima).toUpperCase();
}
const formatMoeda = (valor: any) => {
  return new Intl.NumberFormat('pt-MZ', { style: 'currency', currency: 'MZN' }).format(Number(valor))
}
const formatMes = (dataStr: string) => {
    if (!dataStr) return '---'
    // Formatar data (ex: Fevereiro 2026)
    return new Date(dataStr).toLocaleDateString('pt-PT', { month: 'long', year: 'numeric' })
}
</script>
<template>
  <div class="space-y-8 dark:text-white max-w-8xl mx-auto p-4 md:p-8">
    
    <div class="flex items-center gap-4">
      <button 
        @click="router.back()" 
        class="p-2 rounded-full bg-white border border-stone-200 text-stone-500 hover:bg-stone-50 hover:text-stone-800 transition dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400 shadow-sm"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
      </button>
      <h1 class="text-xl font-bold text-gray-800 dark:text-white">Perfil do Educando</h1>
    </div>

    <div v-if="pending" class="flex flex-col items-center justify-center py-12">
      <div class="animate-spin h-10 w-10 border-4 border-rose-500 border-t-transparent rounded-full mb-4"></div>
      <p class="text-stone-400">A carregar perfil de {{ estudante?.nome_completo }}...</p>
    </div>

    <div v-else class="space-y-8">
      
      <div class="relative bg-white dark:bg-gray-800 rounded-[2.5rem] p-8 shadow-lg shadow-stone-200/50 dark:shadow-none border border-stone-100 dark:border-gray-700 overflow-hidden">
        <div class="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-rose-100/50 to-orange-100/50 dark:from-rose-900/10 dark:to-orange-900/10 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none"></div>

        <div class="relative z-10 flex flex-col md:flex-row items-center md:items-start gap-8">
          
          <div class="h-28 w-28 rounded-[2rem] bg-gradient-to-br from-rose-50 to-white dark:from-gray-700 dark:to-gray-600 flex items-center justify-center text-3xl font-bold text-rose-500 shadow-inner border border-stone-100 dark:border-gray-600">
            {{ getIniciais(estudante?.nome_completo || '') }}
          </div>

          <div class="text-center md:text-left flex-1">
            <h2 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight mb-2">
              {{ estudante?.nome_completo }}
            </h2>
            
            <div class="flex flex-wrap justify-center md:justify-start gap-3 mb-6">
              <span class="px-3 py-1 bg-stone-100 dark:bg-gray-700 text-stone-600 dark:text-gray-300 rounded-lg text-xs font-bold uppercase tracking-wide">
                {{ estudante?.curso }}
              </span>
              <span class="px-3 py-1 bg-stone-100 dark:bg-gray-700 text-stone-600 dark:text-gray-300 rounded-lg text-xs font-bold uppercase tracking-wide">
                Quarto {{ estudante?.quarto }}
              </span>
              <span :class="[
                'px-3 py-1 rounded-lg text-xs font-bold uppercase tracking-wide border',
                estudante?.estado === 'Activo' ? 'bg-emerald-50 text-emerald-700 border-emerald-100' : 'bg-stone-50 text-stone-500'
              ]">
                {{ estudante?.estado }}
              </span>
            </div>

            <div class="flex flex-col md:flex-row gap-6 text-sm text-stone-500 dark:text-gray-400">
               <div>
                 <span class="block text-xs font-bold uppercase text-stone-400 mb-0.5">Nº Estudante</span>
                 #{{ estudante?.num_estudante }}
               </div>
               <div>
                 <span class="block text-xs font-bold uppercase text-stone-400 mb-0.5">Encarregado</span>
                 {{ estudante?.encarregado_nome }}
               </div>
            </div>
          </div>

        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        <div 

            @click="navigateTo({ path: '/dashboard/guardian/finance', query: { student: studentId } })"
          class="bg-white dark:bg-gray-800 rounded-3xl p-6 border border-stone-100 dark:border-gray-700 hover:shadow-lg hover:-translate-y-1 transition-all cursor-pointer group relative overflow-hidden"
        >
          <div :class="[
            'absolute top-0 left-0 w-full h-1',
            dividaTotal > 0 ? 'bg-amber-400' : 'bg-emerald-400'
          ]"></div>
          
          <div class="flex justify-between items-start mb-4">
            <div class="p-3 rounded-2xl bg-stone-50 dark:bg-gray-700 text-stone-500 group-hover:text-emerald-600 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            </div>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-stone-300 group-hover:text-stone-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
          </div>
          
          <h3 class="text-stone-500 text-xs font-bold uppercase tracking-wider mb-1">Situação Financeira</h3>
          <div v-if="dividaTotal > 0">
            <p class="text-2xl font-bold text-amber-600">{{ formatMoeda(dividaTotal) }}</p>
            <p class="text-xs text-stone-400 mt-1">Em Dívida/Pendente</p>
          </div>
          <div v-else>
            <p class="text-2xl font-bold text-emerald-600">Em Dia</p>
            <p class="text-xs text-stone-400 mt-1">Nenhum valor pendente</p>
          </div>
        </div>

        <div 
@click="navigateTo({ path: '/dashboard/guardian/attendance', query: { student: studentId } })"
           class="bg-white dark:bg-gray-800 rounded-3xl p-6 border border-stone-100 dark:border-gray-700 hover:shadow-lg hover:-translate-y-1 transition-all cursor-pointer group relative overflow-hidden"
        >
          <div :class="[
            'absolute top-0 left-0 w-full h-1',
            ultimaPresenca?.estado === 'Presente' ? 'bg-emerald-400' : (ultimaPresenca ? 'bg-rose-400' : 'bg-gray-300')
          ]"></div>

          <div class="flex justify-between items-start mb-4">
             <div class="p-3 rounded-2xl bg-stone-50 dark:bg-gray-700 text-stone-500 group-hover:text-blue-600 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
            </div>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-stone-300 group-hover:text-stone-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
          </div>

          <h3 class="text-stone-500 text-xs font-bold uppercase tracking-wider mb-1">Última Presença</h3>
          <div v-if="ultimaPresenca">
             <p :class="[
               'text-xl font-bold',
               ultimaPresenca.estado === 'Presente' ? 'text-emerald-600' : 'text-rose-600'
             ]">
               {{ ultimaPresenca.estado }}
             </p>
             <p class="text-xs text-stone-400 mt-1 capitalize">{{ formatDataRecente(ultimaPresenca.data_presenca) }}</p>
          </div>
          <div v-else>
            <p class="text-xl font-bold text-stone-400">Sem registos</p>
            <p class="text-xs text-stone-400 mt-1">Ainda sem dados</p>
          </div>
        </div>

        <div 
@click="navigateTo({ path: '/dashboard/guardian/discipline', query: { student: studentId } })"
           class="bg-white dark:bg-gray-800 rounded-3xl p-6 border border-stone-100 dark:border-gray-700 hover:shadow-lg hover:-translate-y-1 transition-all cursor-pointer group relative overflow-hidden"
        >
          <div :class="[
            'absolute top-0 left-0 w-full h-1',
             totalSancoes > 0 ? 'bg-rose-400' : 'bg-emerald-400'
          ]"></div>

          <div class="flex justify-between items-start mb-4">
             <div class="p-3 rounded-2xl bg-stone-50 dark:bg-gray-700 text-stone-500 group-hover:text-rose-600 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
            </div>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-stone-300 group-hover:text-stone-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
          </div>

          <h3 class="text-stone-500 text-xs font-bold uppercase tracking-wider mb-1">Comportamento</h3>
          <div v-if="totalSancoes === 0">
             <p class="text-2xl font-bold text-emerald-600">Exemplar</p>
             <p class="text-xs text-stone-400 mt-1">0 Ocorrências registadas</p>
          </div>
          <div v-else>
            <p class="text-2xl font-bold text-rose-600">{{ totalSancoes }} Sanções</p>
             <p class="text-xs text-stone-400 mt-1">Ver histórico completo</p>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const router = useRouter()
const { api } = useApi()

const studentId = route.params.id

// Fetch Completo: Perfil + Pequenos resumos dos outros endpoints para montar o dashboard
const { data, pending } = await useAsyncData(
  `student-dashboard-${studentId}`,
  async () => {
    // Usamos Promise.all para ser rápido
    const [perfil, finStats, presencas, sancoes] = await Promise.all([
      // 1. Dados do Aluno
      api<any>(`/perfil-encarregado/meus-educandos/${studentId}/`),
      
      // 2. Resumo Financeiro (reusamos o endpoint de stats filtrado)
      api<any>(`/perfil-encarregado/financas-resumo/?estudante=${studentId}`),
      
      // 3. Última presença (pedimos page_size=1)
      api<any>(`/perfil-encarregado/presencas/?estudante=${studentId}&page_size=1`),

      // 4. Sanções (apenas count)
      api<any>(`/perfil-encarregado/sancoes/?estudante=${studentId}&page_size=1`)
    ])

    return { 
      estudante: perfil, 
      finStats: finStats, 
      ultimaPresenca: presencas.results?.[0] || null,
      totalSancoes: sancoes.count || 0
    }
  }
)

const estudante = computed(() => data.value?.estudante)
const dividaTotal = computed(() => (data.value?.finStats?.faturas_pendentes || 0) + (data.value?.finStats?.faturas_atraso || 0)) // Valor aproximado ou contagem
const ultimaPresenca = computed(() => data.value?.ultimaPresenca)
const totalSancoes = computed(() => data.value?.totalSancoes)

// Helpers
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
  // Nota: Aqui estamos a mostrar nº de faturas em dívida ou valor se o backend retornasse valor. 
  // Se o backend retornar contagem, mudamos o texto.
  // Assumindo que o endpoint de stats retorna contagem de faturas pendentes, vamos adaptar.
  if (typeof valor === 'number' && valor < 100) return `${valor} Faturas`; 
  return new Intl.NumberFormat('pt-MZ', { style: 'currency', currency: 'MZN' }).format(Number(valor))
}

const formatDataRecente = (dataStr: string) => {
  if (!dataStr) return ''
  const hoje = new Date().toISOString().split('T')[0]
  if (dataStr === hoje) return 'Hoje'
  return new Date(dataStr).toLocaleDateString('pt-PT', { day: 'numeric', month: 'long' })
}
</script>
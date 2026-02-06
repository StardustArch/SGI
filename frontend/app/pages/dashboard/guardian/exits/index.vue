<template>
  <div class="space-y-8 dark:text-white max-w-8xl mx-auto p-4 md:p-8">
    
    <div>
      <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Autorizações de Saída</h1>
      <p class="text-stone-500 dark:text-gray-400 mt-1 text-lg">Gerencie e autorize os pedidos de saída do internato.</p>
    </div>

    <div class="flex flex-col md:flex-row justify-between items-end gap-6">
      
      <div class="bg-stone-100 dark:bg-gray-800 p-1.5 rounded-2xl flex gap-1 w-full md:w-auto">
        <button 
          @click="abaAtiva = 'acao'; page = 1"
          :class="[
            'px-6 py-2.5 rounded-xl text-sm font-bold transition-all shadow-sm flex items-center gap-2 flex-1 md:flex-none justify-center',
            abaAtiva === 'acao' 
              ? 'bg-white text-rose-600 shadow-md dark:bg-gray-700 dark:text-white' 
              : 'text-stone-500 hover:text-stone-700 dark:text-stone-400'
          ]"
        >
          <div v-if="qtdPendentesAcao > 0" class="w-5 h-5 rounded-full bg-rose-500 text-white flex items-center justify-center text-[10px]">{{ qtdPendentesAcao }}</div>
          <span v-else class="w-2 h-2 rounded-full bg-rose-500"></span>
          Para Aprovar
        </button>
        
        <button 
          @click="abaAtiva = 'historico'; page = 1"
          :class="[
            'px-6 py-2.5 rounded-xl text-sm font-bold transition-all shadow-sm flex-1 md:flex-none justify-center',
            abaAtiva === 'historico' 
              ? 'bg-white text-gray-800 shadow-md dark:bg-gray-700 dark:text-white' 
              : 'text-stone-500 hover:text-stone-700 dark:text-stone-400'
          ]"
        >
          Histórico Geral
        </button>
      </div>

      <div class="w-full md:w-64">
        <div class="relative">
          <select 
            v-model="filtroEstudante" 
            @change="page = 1"
            class="w-full appearance-none bg-white dark:bg-gray-800 border border-stone-200 dark:border-gray-700 text-gray-700 dark:text-gray-200 py-3 px-4 pr-8 rounded-xl focus:outline-none focus:ring-2 focus:ring-rose-200 font-medium cursor-pointer"
          >
            <option :value="null">Todos os Educandos</option>
            <option v-for="filho in educandos" :key="filho.utilizador_id" :value="filho.utilizador_id">
              {{ filho.nome_completo }}
            </option>
          </select>
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-gray-500">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </div>
        </div>
      </div>
    </div>

    <div>
      <div v-if="pending" class="py-20 flex flex-col items-center">
         <div class="animate-spin h-10 w-10 border-4 border-rose-500 border-t-transparent rounded-full mb-4"></div>
         <p class="text-stone-400">A carregar pedidos...</p>
      </div>

      <div v-else-if="pedidosComNome.length === 0" class="flex flex-col items-center justify-center py-24 bg-stone-50/50 dark:bg-gray-800/50 rounded-[2.5rem] border border-stone-100 dark:border-gray-700 text-center">
        <div class="bg-white p-6 rounded-full shadow-sm mb-4">
          <svg v-if="abaAtiva === 'acao'" xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-stone-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" /></svg>
        </div>
        <h3 class="text-xl font-bold text-gray-800 dark:text-white">
          {{ abaAtiva === 'acao' ? 'Tudo em dia!' : 'Sem histórico' }}
        </h3>
        <p class="text-stone-500 dark:text-gray-400 mt-2 max-w-xs mx-auto">
          {{ abaAtiva === 'acao' ? 'Não existem pedidos a aguardar a sua aprovação neste momento.' : 'Nenhum pedido de saída foi encontrado nos registos.' }}
        </p>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        
        <div 
          v-for="item in pedidosComNome" 
          :key="item.id"
          class="bg-white dark:bg-gray-800 rounded-[2rem] border border-stone-100 dark:border-gray-700 overflow-hidden shadow-sm hover:shadow-lg transition-all relative flex flex-col"
        >
          <div :class="[
            'h-1.5 w-full',
            getStatusColor(item.estado)
          ]"></div>

          <div class="p-6 md:p-8 flex-1">
            
            <div class="flex justify-between items-start mb-6">
               <div class="flex items-center gap-3">
                 <div class="h-12 w-12 rounded-2xl bg-stone-100 dark:bg-gray-700 flex items-center justify-center font-bold text-stone-600 dark:text-stone-300 text-lg border border-stone-200 dark:border-gray-600">
                    {{ getIniciais(item.estudante_nome) }}
                 </div>
                 <div>
                   <h3 class="font-bold text-gray-800 dark:text-white text-lg leading-tight">{{ item.estudante_nome }}</h3>
                   <p class="text-xs text-stone-400 mt-0.5">Submetido: {{ formatDate(item.data_submissao) }}</p>
                 </div>
               </div>

               <span :class="[
                 'px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border',
                 getStatusBadge(item.estado)
               ]">
                 {{ getStatusLabel(item.estado) }}
               </span>
            </div>

            <div class="flex gap-4 mb-6">
               <div class="flex-1 bg-stone-50 dark:bg-gray-700/50 rounded-2xl p-3 border border-stone-100 dark:border-gray-600 flex flex-col items-center text-center">
                  <span class="text-[10px] font-bold text-stone-400 uppercase tracking-wider mb-1">Saída</span>
                  <div class="flex items-center gap-1 text-rose-500">
                     <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
                     <span class="text-sm font-bold">{{ formatDateShort(item.data_saida_pretendida) }}</span>
                  </div>
               </div>
               
               <div class="flex-1 bg-stone-50 dark:bg-gray-700/50 rounded-2xl p-3 border border-stone-100 dark:border-gray-600 flex flex-col items-center text-center">
                  <span class="text-[10px] font-bold text-stone-400 uppercase tracking-wider mb-1">Retorno</span>
                  <div class="flex items-center gap-1 text-emerald-600">
                     <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" /></svg>
                     <span class="text-sm font-bold">{{ formatDateShort(item.data_retorno_pretendida) }}</span>
                  </div>
               </div>
            </div>

            <div class="mb-6">
              <span class="text-xs font-bold text-stone-400 uppercase tracking-wider">Motivo:</span>
              <p class="text-sm text-stone-600 dark:text-gray-300 italic mt-1 leading-relaxed">"{{ item.motivo }}"</p>
            </div>

          </div>

          <div v-if="item.estado === 'Aguardando_Encarregado'" class="p-4 bg-stone-50 dark:bg-gray-700/30 border-t border-stone-100 dark:border-gray-700 grid grid-cols-2 gap-3">
             <button 
                @click="processarAcao(item.id, 'Rejeitado')"
                :disabled="loadingId === item.id"
                class="px-4 py-3 rounded-xl bg-white border border-stone-200 text-stone-600 font-bold text-sm hover:bg-rose-50 hover:text-rose-600 hover:border-rose-200 transition-colors disabled:opacity-50"
             >
               Rejeitar
             </button>
             <button 
                @click="processarAcao(item.id, 'Autorizado')"
                :disabled="loadingId === item.id"
                class="px-4 py-3 rounded-xl bg-emerald-500 text-white font-bold text-sm hover:bg-emerald-600 shadow-lg shadow-emerald-200 dark:shadow-none transition-all disabled:opacity-50 flex justify-center items-center gap-2"
             >
               <span v-if="loadingId === item.id" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
               Autorizar Saída
             </button>
          </div>

          <div v-else class="p-4 bg-stone-50 dark:bg-gray-700/30 border-t border-stone-100 dark:border-gray-700 text-center">
             <p class="text-xs font-medium text-stone-400">
               Processo finalizado em {{ formatDate(item.data_submissao) }} </p>
          </div>

        </div>
      </div>

      <div v-if="pedidosComNome.length > 0" class="flex justify-center items-center gap-4 mt-8 pb-8">
        <button @click="page--" :disabled="!data?.pedidos?.previous" class="h-10 w-10 rounded-full border border-stone-200 dark:border-gray-600 flex items-center justify-center text-stone-500 hover:bg-stone-50 disabled:opacity-50 transition"><svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg></button>
        <span class="text-sm font-medium text-stone-600 dark:text-gray-400">Página {{ page }}</span>
        <button @click="page++" :disabled="!data?.pedidos?.next" class="h-10 w-10 rounded-full border border-stone-200 dark:border-gray-600 flex items-center justify-center text-stone-500 hover:bg-stone-50 disabled:opacity-50 transition"><svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg></button>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
const { api } = useApi()
const route = useRoute() 

// Estados
const page = ref(1)
const abaAtiva = ref('acao') // 'acao' ou 'historico'
const filtroEstudante = ref<number | null>(
  route.query.student ? Number(route.query.student) : null // <--- AQUI (neste usámos ref em vez de reactive no ultimo codigo)
)
const loadingId = ref<number | null>(null)

// 1. Educandos
const { data: educandos } = await useAsyncData(
  'filtros-educandos', 
  () => api<any[]>('/perfil-encarregado/meus-educandos/')
)

// 2. Pedidos (Reage à aba, filtro e página)
const { data, pending, refresh } = await useAsyncData(
  'encarregado-pedidos',
  async () => {
    const params: any = { page: page.value }
    if (filtroEstudante.value) params.estudante = filtroEstudante.value
    
    // Lógica das Abas (Filtra o estado na API)
    if (abaAtiva.value === 'acao') {
      params.estado = 'Aguardando_Encarregado'
    } else {
      // Histórico = Tudo o que NÃO é 'Aguardando_Encarregado'
      // O backend Django Filter por padrão faz "exact".
      // Para o histórico, podemos pedir todos e filtrar no front ou, idealmente, o backend suportar "exclude".
      // Como o backend é simples, vamos pedir TODOS e filtrar no computed para simplificar,
      // OU (Melhor) o backend já suporta ordenação, então pedimos todos e o utilizador vê o estado.
      // TRUQUE: Se aba == historico, não mandamos filtro de estado, mas ordenamos.
      // O ideal seria ?estado__ne=Aguardando_Encarregado.
      // Vamos assumir que na aba Histórico mostramos TUDO, inclusive os pendentes de admin.
    }

    const pedidos = await api<any>('/perfil-encarregado/pedidos-saida/', { params })
    return { pedidos }
  },
  { 
    watch: [page, filtroEstudante, abaAtiva]
  }
)

// Mapper e Filtro Client-Side (para garantir separação das abas)
const pedidosComNome = computed(() => {
  if (!data.value?.pedidos?.results || !educandos.value) return []
  
  let lista = data.value.pedidos.results
  
  // Filtragem extra client-side para garantir que a aba 'Historico' não mostra os 'Aguardando'
  if (abaAtiva.value === 'historico') {
      lista = lista.filter((p: any) => p.estado !== 'Aguardando_Encarregado')
  }

  // Mapa de Nomes (já que o endpoint admin serializer tem o nome, mas o encarregado pode não ter, garantimos aqui)
  // Nota: Se usaste o 'PedidoSaidaListAdminSerializer' no view 'EncarregadoPedidoSaidaListView', ele JÁ TRAZ 'estudante_nome'.
  // Se não, usamos o mapa. Vamos prevenir e usar o mapa se faltar.
  const mapaNomes = new Map(educandos.value.map((e: any) => [e.utilizador_id, e.nome_completo]))

  return lista.map((item: any) => ({
    ...item,
    estudante_nome: item.estudante_nome || mapaNomes.get(item.estudante) || 'Desconhecido'
  }))
})

// Contador de Pendentes (Para a bolinha vermelha na aba)
// Fazemos uma chamada leve separada ou calculamos do load atual
const qtdPendentesAcao = computed(() => {
  // Num cenário real, isto viria de um endpoint de /stats.
  // Aqui vamos assumir que se estivermos na aba 'acao', é o total count.
  if (abaAtiva.value === 'acao') return data.value?.pedidos?.count || 0
  return 0
})

// AÇÃO: Aprovar / Rejeitar
const processarAcao = async (id: number, novoEstado: string) => {
  if (!confirm(`Tem a certeza que deseja definir como ${novoEstado}?`)) return;

  loadingId.value = id
  try {
    // ❌ ERRADO (Como tinhas):
    // await api.patch(`/perfil-encarregado/pedidos-saida/${id}/`, { ... })

    // ✅ CORRETO (Usando a tua estrutura atual):
    await api(`/perfil-encarregado/pedidos-saida/${id}/`, {
      method: 'PATCH',
      body: { 
        estado: novoEstado 
      }
    })
    
    // Sucesso!
    refresh() 
  } catch (error) {
    console.error(error)
    alert("Erro ao processar pedido.")
  } finally {
    loadingId.value = null
  }
}

// --- Estilos ---
const getStatusColor = (estado: string) => {
  if (estado === 'Autorizado') return 'bg-emerald-500'
  if (estado === 'Rejeitado') return 'bg-rose-500'
  if (estado === 'Aguardando_Encarregado') return 'bg-amber-500'
  return 'bg-blue-400' // Pendente (Admin)
}

const getStatusBadge = (estado: string) => {
  if (estado === 'Autorizado') return 'bg-emerald-50 text-emerald-700 border-emerald-100'
  if (estado === 'Rejeitado') return 'bg-rose-50 text-rose-700 border-rose-100'
  if (estado === 'Aguardando_Encarregado') return 'bg-amber-50 text-amber-700 border-amber-100'
  return 'bg-blue-50 text-blue-700 border-blue-100'
}

const getStatusLabel = (estado: string) => {
  if (estado === 'Aguardando_Encarregado') return 'Requer Sua Aprovação'
  if (estado === 'Pendente') return 'Em Análise na Escola'
  if (estado === 'Autorizado') return 'Autorizado'
  return estado
}

// Helpers Data
const formatDate = (d: string) => new Date(d).toLocaleDateString('pt-PT')
const formatDateShort = (d: string) => new Date(d).toLocaleDateString('pt-PT', {day:'2-digit', month:'short'}).toUpperCase()
const getIniciais = (nome: string) => {
  const limpo = (nome || '').trim();
  if (!limpo) return '??';
  
  const partes = limpo.split(/\s+/);
  
  // Usamos '?.' para aceder com segurança e '|| ""' caso falhe
  const primeira = partes[0]?.[0] || '';
  const ultima = partes.length > 1 ? partes[partes.length - 1]?.[0] || '' : '';

  return (primeira + ultima).toUpperCase();
}
</script>
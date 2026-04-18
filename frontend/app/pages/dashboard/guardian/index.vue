<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <div v-if="pending" class="flex flex-col items-center justify-center py-20 space-y-4">
      <div class="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full"></div>
      <p class="text-sm text-slate-500 dark:text-slate-400 font-medium">A carregar o seu painel...</p>
    </div>
    
    <div v-else class="space-y-8">
      
      <!-- Cabeçalho -->
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">
            Olá, {{ userData?.first_name || 'Encarregado' }}!
          </h1>
          <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">
            Aqui está o resumo dos seus educandos.
          </p>
        </div>
        <span class="px-3 py-1.5 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 rounded-lg text-xs font-medium border border-blue-100 dark:border-blue-800/30">
          {{ educandosList?.length || 0 }} Educandos Matriculados
        </span>
      </div>

      <!-- Cards dos educandos -->
      <section>
        <h2 class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-5 border-b border-slate-100 dark:border-slate-800 pb-3">
          <BootstrapIcon name="people" class="w-5 h-5 text-slate-400" />
          Acesso Rápido aos Educandos
        </h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          <div 
            v-for="aluno in educandosList" 
            :key="aluno.utilizador_id"
            @click="navigateTo(`/dashboard/guardian/students/${aluno.utilizador_id}`)"
            class="group bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm hover:border-blue-200 dark:hover:border-blue-800 hover:shadow-md transition-all cursor-pointer"
          >
            <div class="flex items-start gap-4">
              <div class="h-14 w-14 sm:h-16 sm:w-16 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center text-lg sm:text-xl font-bold border border-blue-100 dark:border-blue-800 shrink-0 group-hover:scale-105 transition-transform">
                {{ getIniciais(aluno.nome_completo) }}
              </div>
              
              <div class="flex-1 min-w-0">
                <h3 class="text-base sm:text-lg font-bold text-slate-900 dark:text-white truncate group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                  {{ aluno.nome_completo }}
                </h3>
                <p class="text-sm text-slate-500 dark:text-slate-400 mb-1.5">{{ aluno.curso }}</p>
                <span :class="[
                  'px-2 py-0.5 rounded-md text-xs font-medium border',
                  aluno.estado === 'Activo' 
                    ? 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30' 
                    : 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-slate-800 dark:text-slate-400'
                ]">
                  {{ aluno.estado }}
                </span>
              </div>
            </div>

            <div class="mt-5 flex items-center justify-end">
              <span class="text-sm font-medium text-slate-400 group-hover:text-blue-600 dark:group-hover:text-blue-400 flex items-center gap-1 transition-colors">
                Ver Painel do Aluno
                <BootstrapIcon name="arrow-right" class="w-4 h-4" />
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Menus Rápidos -->
      <section>
        <h2 class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-5 border-b border-slate-100 dark:border-slate-800 pb-3">
          <BootstrapIcon name="grid" class="w-5 h-5 text-slate-400" />
          Menus Rápidos
        </h2>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          
          <NuxtLink to="/dashboard/guardian/exits" class="group bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm hover:border-blue-200 dark:hover:border-blue-800 hover:shadow-md transition-all flex flex-col items-center text-center relative">
            <div class="h-12 w-12 rounded-lg bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
              <BootstrapIcon name="door-open" class="w-6 h-6" />
            </div>
            <span class="font-semibold text-slate-900 dark:text-white">Pedidos de Saída</span>
            <span v-if="pendentesCount > 0" class="absolute -top-2 -right-2 bg-rose-500 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center shadow-sm">
              {{ pendentesCount }}
            </span>
            <span class="text-xs text-slate-500 dark:text-slate-400 mt-1">Aprovar ou rejeitar saídas</span>
          </NuxtLink>

          <div class="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col items-center text-center opacity-80">
            <div class="h-12 w-12 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 flex items-center justify-center mb-3">
              <BootstrapIcon name="person" class="w-6 h-6" />
            </div>
            <span class="font-semibold text-slate-700 dark:text-slate-300">Outras funções</span>
            <span class="text-xs text-slate-500 dark:text-slate-400 mt-1">Disponíveis no perfil do educando</span>
          </div>

        </div>
        <p class="text-xs text-slate-400 dark:text-slate-500 mt-3 text-center sm:text-left">
          💡 Financeiro, Presenças e Disciplina estão disponíveis dentro do perfil de cada educando.
        </p>
      </section>

    </div>
  </div>
</template>

<script setup lang="ts">
import { inject, type Ref } from 'vue'

const { api } = useApi()
const userData = inject<Ref<any>>('userData')

const { data, pending } = await useAsyncData(
  'guardian-home',
  async () => {
    const [alunos, pedidos] = await Promise.all([
      api<any[]>('/guardian/students/'),
      api<any>('/guardian/exits/?estado=Aguardando_Encarregado')
    ])
    return { alunos, pendentesCount: pedidos.count || 0 }
  },
  { lazy: true, default: () => ({ alunos: [], pendentesCount: 0 }) }
)

const educandosList = computed(() => {
  const alunosRaw = data.value?.alunos
  if (!alunosRaw) return []
  
  const list = Array.isArray(alunosRaw) ? alunosRaw : (alunosRaw.results || [])
  return list.filter(item => item && typeof item === 'object' && item.utilizador_id)
})

const pendentesCount = computed(() => data.value?.pendentesCount || 0)

const getIniciais = (nome: string) => {
  const limpo = (nome || '').trim()
  if (!limpo) return '??'
  const partes = limpo.split(/\s+/)
  return ((partes[0]?.[0] || '') + (partes.length > 1 ? partes[partes.length - 1]?.[0] || '' : '')).toUpperCase()
}
</script>
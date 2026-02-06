<template>
  <div class="space-y-10 dark:text-white max-w-8xl mx-auto p-4 md:p-8">
    
    <div v-if="pending" class="flex flex-col items-center justify-center py-20">
      <div class="animate-spin h-10 w-10 border-4 border-rose-500 border-t-transparent rounded-full mb-4"></div>
      <p class="text-stone-400">A carregar o seu painel...</p>
    </div>
    
    <div v-else class="space-y-10">
      
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">
            Olá, {{ userData?.first_name || 'Encarregado' }}! 👋
          </h1>
          <p class="text-stone-500 dark:text-gray-400 mt-1 text-lg">
            Aqui está o resumo dos seus educandos.
          </p>
        </div>
        <span class="px-4 py-2 bg-rose-50 text-rose-700 rounded-full text-xs font-bold uppercase tracking-wider border border-rose-100 dark:bg-rose-900/20 dark:border-rose-800 dark:text-rose-300">
          {{ educandos.length }} Educandos Matriculados
        </span>
      </div>

      <section>
        <h2 class="text-xl font-bold text-gray-800 dark:text-white mb-6 flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-rose-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
          Acesso Rápido aos Educandos
        </h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="aluno in educandos" 
            :key="aluno.utilizador_id"
            @click="navigateTo(`/dashboard/guardian/students/${aluno.utilizador_id}`)"
            class="group bg-white dark:bg-gray-800 rounded-[2rem] p-6 border border-stone-100 dark:border-gray-700 hover:border-rose-200 dark:hover:border-rose-900 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 cursor-pointer relative overflow-hidden"
          >
            <div class="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-rose-400 to-orange-300 opacity-0 group-hover:opacity-100 transition-opacity"></div>

            <div class="flex items-start gap-4">
              <div class="h-16 w-16 rounded-2xl bg-stone-50 dark:bg-gray-700 text-stone-600 dark:text-stone-300 flex items-center justify-center text-xl font-bold border border-stone-100 dark:border-gray-600 group-hover:bg-rose-50 group-hover:text-rose-600 group-hover:border-rose-100 transition-colors shadow-sm">
                {{ getIniciais(aluno.nome_completo) }}
              </div>
              
              <div class="flex-1 min-w-0">
                <h3 class="text-lg font-bold text-gray-800 dark:text-white truncate group-hover:text-rose-600 transition-colors">
                  {{ aluno.nome_completo }}
                </h3>
                <p class="text-sm text-stone-500 dark:text-gray-400 mb-2">{{ aluno.curso }}</p>
                <span :class="[
                  'px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wide border',
                  aluno.estado === 'Activo' ? 'bg-emerald-50 text-emerald-700 border-emerald-100 dark:bg-emerald-900/20' : 'bg-stone-100 text-stone-500'
                ]">
                  {{ aluno.estado }}
                </span>
              </div>
            </div>

            <div class="mt-6 flex items-center justify-end">
              <span class="text-sm font-medium text-stone-400 group-hover:text-rose-600 flex items-center gap-1 transition-colors">
                Ver Painel do Aluno
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
              </span>
            </div>
          </div>
        </div>
      </section>

      <hr class="border-stone-100 dark:border-gray-700" />

      <section>
        <h2 class="text-xl font-bold text-gray-800 dark:text-white mb-6 flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-stone-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
          Menus Gerais
        </h2>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          
          <NuxtLink to="/dashboard/guardian/finance" class="menu-card group">
            <div class="icon-box bg-emerald-50 text-emerald-600 dark:bg-emerald-900/20 dark:text-emerald-400 group-hover:scale-110 transition-transform">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            </div>
            <span class="font-bold text-gray-700 dark:text-gray-200">Extrato Financeiro</span>
          </NuxtLink>
          
          <NuxtLink to="/dashboard/guardian/exits" class="menu-card group">
            <div class="icon-box bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400 group-hover:scale-110 transition-transform">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
            </div>
            <span class="font-bold text-gray-700 dark:text-gray-200">Pedidos de Saída</span>
          </NuxtLink>

          <NuxtLink to="/dashboard/guardian/attendance" class="menu-card group">
            <div class="icon-box bg-amber-50 text-amber-600 dark:bg-amber-900/20 dark:text-amber-400 group-hover:scale-110 transition-transform">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
            </div>
            <span class="font-bold text-gray-700 dark:text-gray-200">Assiduidade</span>
          </NuxtLink>

          <NuxtLink to="/dashboard/guardian/discipline" class="menu-card group">
            <div class="icon-box bg-rose-50 text-rose-600 dark:bg-rose-900/20 dark:text-rose-400 group-hover:scale-110 transition-transform">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
            </div>
            <span class="font-bold text-gray-700 dark:text-gray-200">Disciplina</span>
          </NuxtLink>

        </div>
      </section>

    </div>
  </div>
</template>

<script setup lang="ts">
import { inject, type Ref } from 'vue'
const { api } = useApi()

// Dados do Usuário (Injectados do Layout ou Dashboard)
const userData = inject<Ref<any>>('userData')

// Fetch da Lista de Educandos (Endpoint do Encarregado)
const { data: educandos, pending } = await useAsyncData(
  'encarregado-home-educandos',
  () => api<any[]>('/perfil-encarregado/meus-educandos/'),
  { lazy: true, default: () => [] }
)

// Helper para Iniciais
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

<style scoped>
/* Classes utilitárias para limpar o template */
.menu-card {
  @apply bg-white dark:bg-gray-800 rounded-3xl p-6 border border-stone-100 dark:border-gray-700 hover:shadow-lg hover:-translate-y-1 transition-all duration-300 flex flex-col items-center justify-center gap-3 text-center cursor-pointer;
}

.icon-box {
  @apply h-14 w-14 rounded-2xl flex items-center justify-center mb-1 shadow-sm;
}
</style>
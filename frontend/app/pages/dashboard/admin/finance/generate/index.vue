<template>
  <div class="space-y-8 dark:text-white max-w-4xl mx-auto p-4 md:p-8">
    
    <div class="flex items-center gap-4">
      <NuxtLink to="/dashboard/admin/finance" class="p-2 hover:bg-stone-100 dark:hover:bg-gray-700 rounded-full transition">
        <BootstrapIcon name="arrow-left" class="w-6 h-6" />
      </NuxtLink>
      <div>
        <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Geração de Mensalidades</h1>
        <p class="text-stone-500 dark:text-gray-400 mt-1">Crie cobranças em lote para todos os alunos ativos.</p>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-[2.5rem] border border-stone-100 dark:border-gray-700 shadow-xl p-8 md:p-12 relative overflow-hidden">
      
      <div class="absolute top-0 right-0 w-64 h-64 bg-rose-50 dark:bg-rose-900/10 rounded-full -mr-20 -mt-20 blur-3xl opacity-50"></div>

      <div class="relative z-10 max-w-md mx-auto text-center space-y-8">
        <div class="bg-rose-50 dark:bg-gray-700 w-20 h-20 rounded-3xl flex items-center justify-center mx-auto text-rose-500 shadow-inner">
          <BootstrapIcon name="stack" class="w-10 h-10" />
        </div>

        <div class="space-y-2">
          <h2 class="text-xl font-bold">Configurar Novo Mês</h2>
          <p class="text-stone-500 dark:text-gray-400 text-sm">
            O sistema irá verificar todos os estudantes com estado <span class="text-emerald-500 font-bold">Activo</span> e criar um registo pendente de 25,000 MT.
          </p>
        </div>

        <div class="space-y-6 text-left">
          <div class="space-y-1">
            <label class="text-xs font-bold text-stone-400 uppercase ml-1">Mês de Referência</label>
            <input 
              v-model="mesReferencia" 
              type="date" 
              class="w-full bg-stone-50 dark:bg-gray-700 border border-stone-200 dark:border-gray-600 rounded-2xl py-4 px-6 focus:outline-none focus:ring-4 focus:ring-rose-100 dark:focus:ring-rose-900/20 transition-all font-bold text-lg"
            />
          </div>

          <button 
            @click="gerarLote"
            :disabled="loading || !mesReferencia"
            class="w-full bg-gray-900 dark:bg-white text-white dark:text-gray-900 py-4 rounded-2xl font-bold text-lg shadow-lg hover:opacity-90 transition-all disabled:opacity-50 flex items-center justify-center gap-3"
          >
            <span v-if="loading" class="animate-spin h-5 w-5 border-2 border-current border-t-transparent rounded-full"></span>
            {{ loading ? 'A processar alunos...' : 'Gerar Mensalidades Agora' }}
          </button>
        </div>

        <div v-if="resultado" class="mt-6 p-6 rounded-2xl bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-100 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300 text-sm animate-bounce-short">
          <p class="font-bold mb-1">✓ {{ resultado.mensagem }}</p>
          <div class="flex justify-center gap-4 mt-2 opacity-80">
            <span>Novas: <b>{{ resultado.novas_mensalidades }}</b></span>
            <span>Ignoradas: <b>{{ resultado.registos_existentes_ignorados }}</b></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { api } = useApi()
const loading = ref(false)
const mesReferencia = ref('')
const resultado = ref<any>(null)

// Definir o dia 1 por defeito ao escolher o mês
watch(mesReferencia, (val) => {
  if (val) {
    const d = new Date(val)
    if (d.getDate() !== 1) {
      const year = d.getFullYear()
      const month = String(d.getMonth() + 1).padStart(2, '0')
      mesReferencia.value = `${year}-${month}-01`
    }
  }
})

async function gerarLote() {
  if (!confirm(`Confirmar a geração de mensalidades para o mês de ${mesReferencia.value}?`)) return
  
  loading.value = true
  resultado.value = null
  
  try {
    const res = await api('/admin/financeiro/gerar-lote/', {
      method: 'POST',
      body: { mes_referencia: mesReferencia.value }
    })
    resultado.value = res
  } catch (e: any) {
    alert(e.data?.erro || "Erro ao processar lote.")
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.animate-bounce-short {
  animation: bounce 0.5s ease-out;
}
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}
</style>
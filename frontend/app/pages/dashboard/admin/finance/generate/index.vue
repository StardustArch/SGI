<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho -->
    <div class="flex items-center gap-3 mb-6 md:mb-8">
      <NuxtLink 
        to="/dashboard/admin/finance" 
        class="p-2 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-700 dark:hover:text-slate-300 transition shadow-sm"
      >
        <BootstrapIcon name="arrow-left" class="w-5 h-5" />
      </NuxtLink>
      <div>
        <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">Geração de Mensalidades</h1>
        <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">Crie todas as mensalidades do ano para todos os alunos activos.</p>
      </div>
    </div>

    <!-- Card Principal -->
    <div class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-6 md:p-8">
      
      <div class="max-w-md mx-auto text-center space-y-6">
        <!-- Ícone -->
        <div class="h-16 w-16 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center mx-auto">
          <BootstrapIcon name="calendar2-month" class="w-8 h-8" />
        </div>

        <!-- Texto explicativo -->
        <div class="space-y-2">
          <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Gerar Ano Lectivo</h2>
          <p class="text-sm text-slate-500 dark:text-slate-400">
            O sistema irá gerar 12 mensalidades (Janeiro a Dezembro) para todos os estudantes com estado 
            <span class="text-emerald-600 dark:text-emerald-400 font-medium">Activo</span>, 
            respeitando a data de entrada de cada um.
          </p>
        </div>

        <!-- Formulário -->
        <div class="space-y-5 text-left">
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Ano *</label>
            <input 
              v-model.number="anoSelecionado"
              type="number"
              min="2020"
              max="2100"
              step="1"
              class="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg py-2.5 px-3 text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              placeholder="Ex: 2026"
            />
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Informe o ano (ex: 2026) para gerar todas as mensalidades.</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Valor Padrão (MZN)</label>
            <input 
              v-model.number="valorPadrao"
              type="number"
              step="0.01"
              min="0"
              class="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg py-2.5 px-3 text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              placeholder="2.500"
            />
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Deixe em branco para usar o valor padrão (2.500 MT).</p>
          </div>

          <button 
            @click="gerarLote"
            :disabled="loading || !anoSelecionado"
            class="w-full py-3 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center gap-2 min-h-[44px]"
          >
            <span v-if="loading" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
            {{ loading ? 'A processar...' : 'Gerar Mensalidades do Ano' }}
          </button>
        </div>

        <!-- Mensagem de Sucesso -->
        <div v-if="resultado" class="mt-4 p-4 rounded-lg bg-emerald-50 dark:bg-emerald-900/20 text-emerald-800 dark:text-emerald-300 text-sm border border-emerald-200 dark:border-emerald-800/30 flex flex-col items-center">
          <BootstrapIcon name="check-circle-fill" class="w-6 h-6 mb-2" />
          <p class="font-medium">{{ resultado.mensagem }}</p>
          <div class="flex justify-center gap-4 mt-2 text-xs">
            <span>Novas: <strong>{{ resultado.novas_mensalidades }}</strong></span>
            <span>Ignoradas: <strong>{{ resultado.ja_existiam }}</strong></span>
          </div>
        </div>

        <!-- Mensagem de Erro -->
        <div v-if="erroMsg" class="mt-4 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-300 text-sm border border-red-200 dark:border-red-800/30 flex items-start gap-2">
          <BootstrapIcon name="exclamation-triangle-fill" class="w-5 h-5 shrink-0 mt-0.5" />
          <span>{{ erroMsg }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { api } = useApi()
const loading = ref(false)
const anoSelecionado = ref<number | null>(null)
const valorPadrao = ref<number | null>(null)
const resultado = ref<any>(null)
const erroMsg = ref<string | null>(null)

async function gerarLote() {
  if (!anoSelecionado.value) {
    alert('Informe o ano.')
    return
  }

  if (!confirm(`Confirmar a geração de todas as mensalidades para o ano ${anoSelecionado.value}?`)) return

  loading.value = true
  resultado.value = null
  erroMsg.value = null

  try {
    const payload: any = { ano: anoSelecionado.value }
    if (valorPadrao.value) payload.valor_padrao = valorPadrao.value

    const res = <any> await api('/admin/financeiro/gerar-lote/', {
      method: 'POST',
      body: payload
    })
    resultado.value = {
      mensagem: res.mensagem,
      novas_mensalidades: res.mensalidades_criadas,
      ja_existiam: res.ja_existiam
    }
  } catch (err: any) {
    const msg = err.response?._data?.erro || 'Erro ao processar lote.'
    erroMsg.value = msg
    console.error('Erro ao gerar lote:', err)
  } finally {
    loading.value = false
  }
}
</script>
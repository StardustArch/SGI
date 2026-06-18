<template>
  <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho simplificado -->
    <div class="flex items-center gap-3 mb-6 md:mb-8">
      <NuxtLink 
        to="/dashboard/admin/finance" 
        class="p-2 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-700 dark:hover:text-slate-300 transition shadow-sm"
      >
        <BootstrapIcon name="arrow-left" class="w-5 h-5" />
      </NuxtLink>
      <div>
        <h1 class="text-xl md:text-2xl font-bold text-slate-900 dark:text-white">Confirmar Pagamento</h1>
        <p class="text-sm text-slate-500 dark:text-slate-400">Registe o recebimento em numerário.</p>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="pending" class="animate-pulse space-y-4">
      <div class="h-32 bg-slate-100 dark:bg-slate-800 rounded-xl"></div>
      <div class="h-48 bg-slate-100 dark:bg-slate-800 rounded-xl"></div>
    </div>

    <!-- Conteúdo -->
    <div v-else-if="mensalidade" class="space-y-5">
      
      <!-- Resumo da mensalidade -->
      <section class="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
          <div>
            <p class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase">
              {{ mensalidade.tipo || 'Mensalidade' }} • {{ formatMes(mensalidade.mes_referencia) }}
            </p>
            <h2 class="text-lg font-bold text-slate-900 dark:text-white mt-1">
              {{ mensalidade.nome_estudante || `ID: ${mensalidade.estudante}` }}
            </h2>
            <span :class="[
              'px-2.5 py-0.5 rounded-md text-xs font-medium border mt-2 inline-block',
              mensalidade.estado === 'Pago' 
                ? 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30' 
                : 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-900/20 dark:text-amber-400 dark:border-amber-800/30'
            ]">
              {{ mensalidade.estado === 'Pago' ? 'Paga' : 'Pendente' }}
            </span>
          </div>

          <div class="text-left md:text-right">
            <p class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase">Valor</p>
            <h3 class="text-2xl font-bold text-slate-900 dark:text-white">
              {{ formatMoeda(mensalidade.valor_pago || 2500) }}
            </h3>
          </div>
        </div>
      </section>

      <!-- Formulário de confirmação (apenas se pendente) -->
      <section v-if="mensalidade.estado !== 'Pago'" class="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm">
        <form @submit.prevent="confirmarPagamento" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
              Data do Pagamento *
            </label>
            <input 
              v-model="form.data_pagamento_confirmado" 
              type="date" 
              required 
              class="w-full px-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
              Nº do Talão / Referência (opcional)
            </label>
            <input 
              v-model="form.referencia_comprovativo" 
              type="text" 
              placeholder="Ex: Talão 123 ou 'Entregue em mão'"
              class="w-full px-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div class="flex justify-end pt-2">
            <button 
              type="submit" 
              :disabled="saving"
              class="px-6 py-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-sm transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <span v-if="saving" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
              <BootstrapIcon v-else name="check-circle" class="w-4 h-4" />
              {{ saving ? 'A registar...' : 'Confirmar Recebimento' }}
            </button>
          </div>
        </form>
      </section>

      <!-- Mensagem de sucesso (já paga) -->
      <section v-else class="bg-emerald-50 dark:bg-emerald-900/20 rounded-xl p-6 border border-emerald-200 dark:border-emerald-800/30 text-center">
        <div class="w-16 h-16 bg-emerald-100 dark:bg-emerald-800 text-emerald-600 dark:text-emerald-300 rounded-full flex items-center justify-center mx-auto mb-4">
          <BootstrapIcon name="check-circle-fill" class="w-8 h-8" />
        </div>
        <h3 class="text-lg font-semibold text-emerald-800 dark:text-emerald-300">Pagamento Confirmado</h3>
        <p class="text-emerald-700 dark:text-emerald-400 mt-2 text-sm">
          Registado em <strong>{{ formatDate(mensalidade.data_pagamento_confirmado) }}</strong>
        </p>
        <p v-if="mensalidade.referencia_comprovativo" class="text-emerald-600 dark:text-emerald-500 text-xs mt-1">
          Ref: {{ mensalidade.referencia_comprovativo }}
        </p>

        <button 
          @click="downloadRecibo"
          class="mt-6 px-5 py-2.5 rounded-lg bg-white dark:bg-slate-800 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-700 font-medium text-sm hover:bg-emerald-50 dark:hover:bg-slate-700 transition-colors flex items-center justify-center gap-2 mx-auto"
        >
          <BootstrapIcon name="file-pdf" class="w-4 h-4" />
          Baixar Recibo PDF
        </button>
      </section>

    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'

const { api } = useApi()
const route = useRoute()
const saving = ref(false)

// Formulário com apenas data e referência (método fixo = Numerário)
const form = reactive({
  estado: 'Pago',
  valor_pago: 2500, // será sobrescrito pelo valor real se existir
  metodo_pagamento: 'Numerário', // fixo
  data_pagamento_confirmado: new Date().toISOString().substr(0, 10),
  referencia_comprovativo: ''
})

// Buscar dados da mensalidade
const { data: mensalidade, pending, refresh } = await useAsyncData(
  `admin-mensalidade-${route.params.id}`, 
  () => api<any>(`/admin/mensalidades/${route.params.id}/`)
)
console.log(mensalidade.value)

// Confirmar pagamento
async function confirmarPagamento() {
  if (!confirm('Tem a certeza que deseja dar esta mensalidade como PAGA?')) return

  saving.value = true
  try {
    // Envia o valor real da mensalidade (se existir, senão 2500)
    const payload = {
      ...form,
      valor_pago: mensalidade.value?.valor_pago || 2500
    }
    await api(`/admin/mensalidades/${route.params.id}/`, {
      method: 'PATCH',
      body: payload
    })
    alert('Pagamento registado com sucesso!')
    await refresh()
  } catch (error) {
    alert('Erro ao registar o pagamento. Verifique os dados.')
  } finally {
    saving.value = false
  }
}

// Baixar recibo
async function downloadRecibo() {
  try {
    const blob = await api<Blob>(`/admin/mensalidades/${route.params.id}/recibo/`, {
      method: 'GET',
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `recibo_${route.params.id}.pdf`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (error: any) {
    const message = error?.data?.erro || 'Não foi possível gerar o recibo.'
    alert(message)
  }
}

// Helpers
const formatMoeda = (valor: any) => 
  new Intl.NumberFormat('pt-MZ', { style: 'currency', currency: 'MZN' }).format(Number(valor))

const formatMes = (data: string) => 
  new Date(data).toLocaleDateString('pt-PT', { month: 'long', year: 'numeric' })

const formatDate = (data: string) => 
  new Date(data).toLocaleDateString('pt-PT')
</script>
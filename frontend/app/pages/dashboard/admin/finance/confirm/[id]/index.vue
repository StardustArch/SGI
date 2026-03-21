<template>
  <div class="space-y-8 dark:text-white max-w-4xl mx-auto p-4 md:p-8">
    
    <div class="flex items-center gap-4">
      <NuxtLink to="/dashboard/admin/finance" class="p-2 hover:bg-stone-100 dark:hover:bg-gray-700 rounded-full transition">
        <BootstrapIcon name="arrow-left" class="w-6 h-6" />
      </NuxtLink>
      <div>
        <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Confirmar Pagamento</h1>
        <p class="text-stone-500 dark:text-gray-400 mt-1">Registe a entrada do valor da mensalidade.</p>
      </div>
    </div>

    <div v-if="pending" class="animate-pulse h-64 bg-stone-100 dark:bg-gray-800 rounded-[2.5rem]"></div>

    <div v-else-if="mensalidade" class="space-y-6">
      
      <div class="bg-white dark:bg-gray-800 rounded-[2.5rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm relative overflow-hidden">
        <div class="absolute top-0 right-0 w-32 h-32 bg-stone-50 dark:bg-gray-700/50 rounded-full -mr-10 -mt-10 opacity-50"></div>
        
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 relative z-10">
          <div>
            <p class="text-[10px] font-bold text-stone-400 uppercase tracking-widest mb-1">
              Mês de Referência: {{ formatMes(mensalidade.mes_referencia) }}
            </p>
            <h2 class="text-2xl font-black text-gray-800 dark:text-white mb-2">
              Estudante ID: {{ mensalidade.estudante }}
            </h2>
            <span :class="['px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide border', mensalidade.estado === 'Pago' ? 'bg-emerald-50 text-emerald-700 border-emerald-100' : 'bg-amber-50 text-amber-700 border-amber-100']">
              Estado Atual: {{ mensalidade.estado }}
            </span>
          </div>

          <div class="text-left md:text-right">
            <p class="text-[10px] font-bold text-stone-400 uppercase tracking-widest mb-1">Valor a Cobrar</p>
            <h3 class="text-4xl font-black text-gray-900 dark:text-white">
              {{ formatMoeda(mensalidade.valor_pago > 0 ? mensalidade.valor_pago : 25000) }}
            </h3>
          </div>
        </div>
      </div>

      <div v-if="mensalidade.estado !== 'Pago'" class="bg-white dark:bg-gray-800 rounded-[2.5rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm">
        <h3 class="text-lg font-bold mb-6 flex items-center gap-2">
          <BootstrapIcon name="receipt-cutoff" class="text-rose-500" />
          Detalhes do Recibo
        </h3>

        <form @submit.prevent="confirmarPagamento" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            <div class="space-y-1">
              <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Método de Pagamento</label>
              <select v-model="form.metodo_pagamento" required class="admin-input appearance-none">
                <option value="Depósito">Depósito Bancário</option>
                <option value="Numerário">Numerário (Dinheiro Vivo)</option>
              </select>
            </div>

            <div class="space-y-1">
              <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Data do Pagamento</label>
              <input v-model="form.data_pagamento_confirmado" type="date" required class="admin-input" />
            </div>

            <div class="space-y-1 md:col-span-2">
              <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Nº do Comprovativo / Referência</label>
              <input 
                v-model="form.referencia_comprovativo" 
                type="text" 
                placeholder="Ex: Talão nº 123456 ou 'Entregue em mão'" 
                class="admin-input" 
              />
            </div>

          </div>

          <div class="pt-4 flex justify-end">
            <button 
              type="submit" 
              :disabled="saving"
              class="px-8 py-4 rounded-2xl bg-emerald-500 text-white font-bold text-sm shadow-lg hover:bg-emerald-600 transition-all disabled:opacity-50 flex items-center gap-2"
            >
              <span v-if="saving" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
              <BootstrapIcon v-else name="check-circle-fill" />
              {{ saving ? 'A registar...' : 'Confirmar Recebimento' }}
            </button>
          </div>
        </form>
      </div>

<div v-else class="bg-emerald-50 dark:bg-emerald-900/20 rounded-[2rem] p-8 border border-emerald-100 dark:border-emerald-800 text-center">
  <div class="w-16 h-16 bg-emerald-100 dark:bg-emerald-800 text-emerald-500 dark:text-emerald-300 rounded-full flex items-center justify-center mx-auto mb-4">
    <BootstrapIcon name="check2-all" class="w-8 h-8" />
  </div>
  <h3 class="text-xl font-bold text-emerald-700 dark:text-emerald-400">Mensalidade Paga</h3>
  <p class="text-emerald-600 dark:text-emerald-500 mt-2 text-sm">
    Este pagamento foi confirmado em <b>{{ formatDate(mensalidade.data_pagamento_confirmado) }}</b> 
    via <b>{{ mensalidade.metodo_pagamento }}</b>.
  </p>
  <p v-if="mensalidade.referencia_comprovativo" class="text-emerald-600 dark:text-emerald-500 text-xs mt-1">
    Ref: {{ mensalidade.referencia_comprovativo }}
  </p>

  <!-- NOVO BOTÃO PARA DOWNLOAD DO RECIBO -->
  <button 
    @click="downloadRecibo"
    class="mt-6 px-6 py-3 rounded-xl bg-white dark:bg-gray-800 text-emerald-600 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800 font-bold text-sm hover:bg-emerald-50 dark:hover:bg-gray-700 transition-all flex items-center justify-center gap-2 mx-auto"
  >
    <BootstrapIcon name="file-pdf-fill" />
    Baixar Recibo (PDF)
  </button>
</div>

    </div>
  </div>
</template>

<script setup lang="ts">
const { api } = useApi()
const route = useRoute()

const saving = ref(false)

// Formulário começa com a data de hoje por padrão
const form = reactive({
  estado: 'Pago',
  valor_pago: 25000, // Valor padrão da mensalidade
  metodo_pagamento: 'Depósito',
  data_pagamento_confirmado: new Date().toISOString().substr(0, 10),
  referencia_comprovativo: ''
})

// Buscar a mensalidade específica
const { data: mensalidade, pending, refresh } = await useAsyncData(
  `admin-mensalidade-${route.params.id}`, 
  () => api<any>(`/admin/mensalidades/${route.params.id}/`)
)

async function confirmarPagamento() {
  if (!confirm('Tem a certeza que deseja dar esta mensalidade como PAGA?')) return

  saving.value = true
  try {
    await api(`/admin/mensalidades/${route.params.id}/`, {
      method: 'PATCH',
      body: form
    })
    alert('Pagamento registado com sucesso!')
    refresh() // Recarrega a página para mostrar a mensagem verde de sucesso
  } catch (error) {
    alert('Erro ao registar o pagamento. Verifique os dados.')
  } finally {
    saving.value = false
  }
}

// Helpers
const formatMoeda = (valor: any) => new Intl.NumberFormat('pt-MZ', { style: 'currency', currency: 'MZN' }).format(Number(valor))
const formatMes = (data: string) => new Date(data).toLocaleDateString('pt-PT', { month: 'long', year: 'numeric' }).toUpperCase()
const formatDate = (data: string) => new Date(data).toLocaleDateString('pt-PT')

async function downloadRecibo() {
  try {
    // Chamada para o endpoint de recibo
    const blob = await api<Blob>(`/admin/mensalidades/${route.params.id}/recibo/`, {
      method: 'GET',
      responseType: 'blob'
    })

    // Criar link de download
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `recibo_${route.params.id}.pdf`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (error: any) {
    console.error('Erro ao baixar recibo:', error)
    // Trata mensagem de erro amigável
    const message = error?.data?.erro || 'Não foi possível gerar o recibo. Verifique se o pagamento está confirmado.'
    alert(message)
  }
}
</script>

<style scoped>
.admin-input {
  @apply w-full bg-stone-50 dark:bg-gray-900 border border-stone-200 dark:border-gray-700 rounded-xl py-3 px-4 focus:outline-none focus:ring-2 focus:ring-rose-200 dark:focus:ring-rose-900 transition-all font-medium text-gray-800 dark:text-white;
}
</style>
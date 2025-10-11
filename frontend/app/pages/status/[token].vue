<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
    <div class="container mx-auto px-4 max-w-4xl">
      <!-- Header -->
      <header class="text-center mb-12">
        <div class="flex justify-center items-center mb-4">
          <div class="w-16 h-16 bg-indigo-600 rounded-full flex items-center justify-center">
            <span class="text-2xl text-white">📋</span>
          </div>
        </div>
        <h1 class="text-4xl font-bold text-gray-800 mb-4">
          Acompanhar Denúncia
        </h1>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          Consulte o status da sua denúncia usando o token de acompanhamento
        </p>
      </header>

      <!-- Main Content -->
      <div class="max-w-2xl mx-auto">
        <div class="bg-white rounded-xl shadow-lg p-6 mb-8">
          <!-- Token Input -->
          <div class="mb-6">
            <label for="token" class="block text-sm font-medium text-gray-700 mb-2">
              Token de Acompanhamento
            </label>
            <div class="flex gap-2">
              <input
                id="token"
                v-model="inputToken"
                type="text"
                placeholder="Digite seu token (ex: DC123456789ABC)"
                class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 font-mono"
                @keyup.enter="fetchStatus"
              />
              <button
                @click="fetchStatus"
                :disabled="isLoading || !inputToken.trim()"
                class="bg-indigo-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span v-if="isLoading">
                  <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white inline mr-2"></div>
                  Consultando...
                </span>
                <span v-else>Consultar</span>
              </button>
            </div>
          </div>

          <!-- Resultado -->
          <div v-if="statusResult" class="mt-6">
            <div class="border-t pt-6">
              <h3 class="text-lg font-semibold text-gray-800 mb-4">Status da Denúncia</h3>
              
              <!-- Card de Status -->
              <div class="bg-gray-50 rounded-lg p-4 mb-4">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm text-gray-500">Token</p>
                    <p class="font-mono font-bold text-lg">{{ statusResult.token }}</p>
                  </div>
                  <div :class="statusBadgeClass" class="px-3 py-1 rounded-full text-sm font-medium">
                    {{ getStatusText(statusResult.status) }}
                  </div>
                </div>
              </div>

              <!-- Detalhes -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p class="text-sm text-gray-500">Data de Recebimento</p>
                  <p class="font-medium">{{ formatDate(statusResult.createdAt) }}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-500">Última Atualização</p>
                  <p class="font-medium">{{ formatDate(statusResult.updatedAt) }}</p>
                </div>
              </div>

              <!-- Mensagem -->
              <div class="mt-4 p-3 bg-blue-50 rounded-lg">
                <p class="text-sm text-blue-700">{{ statusResult.message }}</p>
              </div>
            </div>
          </div>

          <!-- Erro -->
          <div v-if="error" class="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div class="flex items-center">
              <span class="text-red-500 mr-2">⚠️</span>
              <p class="text-red-700">{{ error }}</p>
            </div>
          </div>
        </div>

        <!-- Ações -->
        <div class="text-center">
          <NuxtLink 
            to="/" 
            class="inline-flex items-center text-indigo-600 hover:text-indigo-700 font-medium"
          >
            ← Voltar para fazer nova denúncia
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Configuração da API
const config = useRuntimeConfig()

// Estado
const inputToken = ref('')
const statusResult = ref(null)
const isLoading = ref(false)
const error = ref('')

// Buscar status da denúncia
const fetchStatus = async () => {
  if (!inputToken.value.trim()) {
    error.value = 'Por favor, digite um token válido'
    return
  }

  isLoading.value = true
  error.value = ''
  statusResult.value = null

  try {
    console.log('🔍 Consultando status para token:', inputToken.value)
    
    const response = await $fetch(`/v1/reports/status/${inputToken.value}`, {
      baseURL: config.public.apiBase
    })

    statusResult.value = {
      ...response,
      updatedAt: new Date().toISOString() // Simular atualização
    }

    console.log('✅ Status encontrado:', response.status)
    
  } catch (err) {
    console.error('❌ Erro ao consultar status:', err)
    
    if (err.status === 404) {
      error.value = 'Token não encontrado. Verifique se o token está correto.'
    } else {
      error.value = 'Erro ao consultar status. Tente novamente.'
    }
  } finally {
    isLoading.value = false
  }
}

// Helper functions
const getStatusText = (status) => {
  const statusMap = {
    'RECEIVED': 'Recebida',
    'ANALYZED': 'Analisada',
    'IN_PROGRESS': 'Em Andamento',
    'RESOLVED': 'Resolvida',
    'CLOSED': 'Encerrada'
  }
  return statusMap[status] || status
}

const statusBadgeClass = computed(() => {
  const status = statusResult.value?.status
  const classes = {
    'RECEIVED': 'bg-blue-100 text-blue-800',
    'ANALYZED': 'bg-yellow-100 text-yellow-800',
    'IN_PROGRESS': 'bg-purple-100 text-purple-800',
    'RESOLVED': 'bg-green-100 text-green-800',
    'CLOSED': 'bg-gray-100 text-gray-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
})

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleString('pt-BR')
}

// Se tiver token na URL, preencher automaticamente
const route = useRoute()
onMounted(() => {
  if (route.params.token) {
    inputToken.value = route.params.token
    // Auto-consultar se token veio na URL
    setTimeout(() => {
      fetchStatus()
    }, 500)
  }
})

// Meta tags
useSeoMeta({
  title: 'Acompanhar Denúncia - Sistema de Denúncias Anônimas',
  description: 'Consulte o status da sua denúncia usando o token de acompanhamento'
})
</script>
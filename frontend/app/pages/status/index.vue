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
          Consultar Denúncia
        </h1>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          Digite seu token de acompanhamento para consultar o status da denúncia
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
                @keyup.enter="goToStatus"
              />
              <button
                @click="goToStatus"
                :disabled="!inputToken.trim()"
                class="bg-indigo-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Consultar
              </button>
            </div>
            <p class="text-xs text-gray-500 mt-2">
              O token foi enviado para você quando a denúncia foi submetida
            </p>
          </div>

          <!-- Exemplo -->
          <div class="bg-gray-50 rounded-lg p-4">
            <h4 class="text-sm font-medium text-gray-700 mb-2">Exemplo de token:</h4>
            <p class="font-mono text-sm text-gray-600">DC536493F09415</p>
          </div>
        </div>

        <!-- Ações -->
        <div class="text-center space-y-4">
          <NuxtLink 
            to="/" 
            class="inline-flex items-center text-indigo-600 hover:text-indigo-700 font-medium"
          >
            ← Voltar para fazer nova denúncia
          </NuxtLink>
          
          <div class="text-sm text-gray-500">
            Problemas com seu token? <a href="mailto:suporte@denuncias.local" class="text-indigo-600 hover:text-indigo-700">Entre em contato com o suporte</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const inputToken = ref('')

const goToStatus = () => {
  if (inputToken.value.trim()) {
    // Navegar para a página dinâmica com o token
    navigateTo(`/status/${inputToken.value.trim()}`)
  }
}

// Meta tags
useSeoMeta({
  title: 'Consultar Denúncia - Sistema de Denúncias Anônimas',
  description: 'Consulte o status da sua denúncia usando o token de acompanhamento'
})
</script>
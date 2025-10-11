<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
    <div class="container mx-auto px-4 max-w-4xl">
      <!-- Header -->
      <header class="text-center mb-12">
        <div class="flex justify-center items-center mb-4">
          <div class="w-16 h-16 bg-indigo-600 rounded-full flex items-center justify-center">
            <span class="text-2xl text-white">🛡️</span>
          </div>
        </div>
        <h1 class="text-4xl font-bold text-gray-800 mb-4">
          Sistema de Denúncias Anônimas
        </h1>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          Denuncie de forma 100% anônima e segura. Sua identidade será preservada.
        </p>
      </header>

      <!-- Main Content -->
      <div class="grid md:grid-cols-3 gap-8">
        <!-- Form Section -->
        <div class="md:col-span-2">
          <div class="bg-white rounded-xl shadow-lg p-6">
            <SubmissionForm />
          </div>
        </div>

        <!-- Info Section -->
        <div class="space-y-6">
          <!-- Security Info -->
          <div class="bg-white rounded-xl shadow-lg p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-3 flex items-center">
              <span class="text-green-500 mr-2">✓</span>
              Segurança Garantida
            </h3>
            <ul class="text-sm text-gray-600 space-y-2">
              <li class="flex items-start">
                <span class="text-green-500 mr-2 mt-0.5">•</span>
                <span>Criptografia ponta a ponta</span>
              </li>
              <li class="flex items-start">
                <span class="text-green-500 mr-2 mt-0.5">•</span>
                <span>Nenhum dado pessoal coletado</span>
              </li>
              <li class="flex items-start">
                <span class="text-green-500 mr-2 mt-0.5">•</span>
                <span>Token único de acompanhamento</span>
              </li>
            </ul>
          </div>

          <!-- Status Check -->
          <div class="bg-white rounded-xl shadow-lg p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-3">
              Consultar Denúncia
            </h3>
            <p class="text-sm text-gray-600 mb-4">
              Já fez uma denúncia? Consulte o status usando seu token.
            </p>
            <NuxtLink 
              to="/status" 
              class="w-full bg-indigo-100 text-indigo-700 hover:bg-indigo-200 transition-colors py-2 px-4 rounded-lg text-sm font-medium text-center block"
            >
              Consultar Status
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Meta tags para SEO
useSeoMeta({
  title: 'Sistema de Denúncias Anônimas',
  description: 'Denuncie de forma 100% anônima e segura. Criptografia ponta a ponta garantida.'
})
</script>
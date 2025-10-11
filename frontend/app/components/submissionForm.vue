<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Fazer Denúncia Anônima</h2>
    
    <form @submit.prevent="submitReport" class="space-y-6">
      <!-- Categoria -->
      <div>
        <label for="category" class="block text-sm font-medium text-gray-700 mb-2">
          Tipo de Denúncia *
        </label>
        <select
          id="category"
          v-model="form.category"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          <option value="">Selecione uma categoria</option>
          <option value="ASSEDIO">Assédio Moral/Sexual</option>
          <option value="DISCRIMINACAO">Discriminação</option>
          <option value="CORRUPCAO">Corrupção</option>
          <option value="ASSEDIO_MORAL">Assédio Moral</option>
          <option value="OUTROS">Outros</option>
        </select>
      </div>

      <!-- Descrição -->
      <div>
        <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
          Descrição da Denúncia *
        </label>
        <textarea
          id="description"
          v-model="form.description"
          required
          rows="6"
          placeholder="Descreva os fatos de forma clara e objetiva. Evite incluir informações pessoais suas ou de outras pessoas."
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
          maxlength="5000"
        ></textarea>
        <p class="text-xs text-gray-500 mt-1">
          {{ form.description.length }}/5000 caracteres
        </p>
      </div>

      <!-- Status de Segurança -->
      <div v-if="isLoadingKey" class="p-3 bg-blue-50 rounded-lg">
        <div class="flex items-center">
          <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
          <span class="text-sm text-blue-700">Carregando sistema de segurança...</span>
        </div>
      </div>

      <div v-else-if="publicKey" class="p-3 bg-green-50 rounded-lg">
        <div class="flex items-center">
          <span class="text-green-500 mr-2">✓</span>
          <span class="text-sm text-green-700">Sistema de segurança ativo e criptografia garantida</span>
        </div>
      </div>

      <!-- Botão de Envio -->
      <div class="pt-4">
        <button
          type="submit"
          :disabled="isSubmitting || !publicKey"
          class="w-full bg-indigo-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="isSubmitting">
            <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-white inline mr-2"></div>
            Enviando denúncia...
          </span>
          <span v-else>
            🛡️ Enviar Denúncia Anonimamente
          </span>
        </button>
        
        <p class="text-xs text-gray-500 text-center mt-3">
          Ao enviar, você receberá um token único para acompanhar sua denúncia.
        </p>
      </div>
    </form>

    <!-- Modal de Sucesso -->
    <div v-if="showSuccessModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-xl shadow-lg p-6 max-w-md w-full">
        <div class="text-center">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <span class="text-2xl text-green-600">✓</span>
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Denúncia Enviada!</h3>
          <p class="text-gray-600 mb-4">
            Sua denúncia foi recebida com sucesso e está protegida por criptografia.
          </p>
          <div class="bg-gray-50 p-3 rounded-lg mb-4">
            <p class="text-sm text-gray-500">Seu token de acompanhamento:</p>
            <p class="text-lg font-mono font-bold text-indigo-600">{{ submissionToken }}</p>
          </div>
          <p class="text-xs text-gray-500 mb-4">
            Guarde este token em local seguro. Ele é a única forma de acompanhar sua denúncia.
          </p>
          <button
            @click="showSuccessModal = false"
            class="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-indigo-700"
          >
            Entendido
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const { encryptText } = useEncryption();
// Estado do formulário
const form = ref({
  category: '',
  description: ''
})

const isSubmitting = ref(false)
const showSuccessModal = ref(false)
const submissionToken = ref('')
const publicKey = ref(null)
const isLoadingKey = ref(false)

// Configuração da API
const config = useRuntimeConfig()

// Buscar chave pública do servidor
const fetchPublicKey = async () => {
  try {
    isLoadingKey.value = true
    const response = await $fetch('/v1/keys/public', {
      baseURL: config.public.apiBase
    })
    publicKey.value = response.publicKeyPem
    console.log('🔑 Chave pública carregada:', response.keyId)
  } catch (error) {
    console.error('❌ Erro ao carregar chave pública:', error)
    alert('Erro ao carregar sistema de segurança. Tente novamente.')
  } finally {
    isLoadingKey.value = false
  }
}

// Carregar chave pública ao montar o componente
onMounted(() => {
  fetchPublicKey()
})

// Enviar denúncia
const submitReport = async () => {
  if (!publicKey.value) {
    alert('Sistema de segurança não carregado. Aguarde...');
    return;
  }

  if (!form.value.description.trim()) {
    alert('Por favor, descreva a denúncia.');
    return;
  }

  isSubmitting.value = true;
  
  try {
    console.log('🚀 Iniciando envio de denúncia criptografada...');
    
    // 1. Criptografar o texto
    const encryptedData = await encryptText(form.value.description, publicKey.value);
    
    console.log('📤 Enviando dados criptografados para API...');

    // 2. Enviar para API
    const response = await $fetch('/v1/reports', {
      baseURL: config.public.apiBase,
      method: 'POST',
      body: {
        encryptedBlob: encryptedData.encryptedBlob,
        wrappedKey: encryptedData.wrappedKey
      }
    });

    console.log('✅ Resposta da API:', response);
    
    submissionToken.value = response.token;
    showSuccessModal.value = true;
    
    // Reset form
    form.value = { category: '', description: '' };
    
  } catch (error) {
    console.error('❌ Erro ao enviar denúncia:', error);
    
    if (error.message?.includes('Failed to fetch')) {
      alert('Erro de conexão com o servidor. Verifique se o backend está rodando.');
    } else if (error.message?.includes('criptografia')) {
      alert('Erro no sistema de criptografia. Tente novamente.');
    } else {
      alert('Erro ao enviar denúncia. Tente novamente.');
    }
  } finally {
    isSubmitting.value = false;
  }
};
</script>
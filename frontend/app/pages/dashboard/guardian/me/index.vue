<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho -->
    <div class="mb-6 md:mb-8">
      <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">O Meu Perfil</h1>
      <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">Gerencie os seus dados de contacto e segurança.</p>
    </div>

    <!-- Loading -->
    <div v-if="userPending || loadingProfile" class="flex flex-col items-center justify-center py-20 space-y-4">
      <div class="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full"></div>
      <p class="text-sm text-slate-500 dark:text-slate-400 font-medium">A carregar informações...</p>
    </div>

    <!-- Conteúdo principal -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6 md:gap-8">
      
      <!-- Coluna da esquerda -->
      <div class="lg:col-span-2 space-y-5 md:space-y-6">
        
        <!-- Card de identificação -->
        <section class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm flex items-start gap-4 sm:gap-6">
          <div class="h-16 w-16 sm:h-20 sm:w-20 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center text-xl sm:text-2xl font-bold border border-blue-100 dark:border-blue-800 shrink-0">
            {{ getIniciais(userData?.first_name || '') }}
          </div>

          <div class="min-w-0">
            <h2 class="text-lg sm:text-xl font-bold text-slate-900 dark:text-white break-words">
              {{ userData?.first_name }} {{ userData?.last_name }}
            </h2>
            <div class="mt-1">
              <span class="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-xs font-medium border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300">
                Encarregado
              </span>
            </div>

          </div>
        </section>

        <!-- Card de contactos -->
        <section class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
          <div class="flex items-center justify-between mb-5 border-b border-slate-100 dark:border-slate-800 pb-3">
            <h3 class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2">
              <BootstrapIcon name="telephone" class="w-5 h-5 text-slate-400" />
              Meus Contactos
            </h3>
            <span class="text-xs text-slate-400 dark:text-slate-500 bg-slate-50 dark:bg-slate-800 px-2.5 py-0.5 rounded-md">Editável</span>
          </div>

          <!-- Mensagem de feedback -->
          <div v-if="msgProfile.text" :class="[
            'mb-5 p-3 rounded-lg flex items-start gap-2 text-sm border',
            msgProfile.type === 'success' 
              ? 'bg-emerald-50 text-emerald-800 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30' 
              : 'bg-red-50 text-red-800 border-red-200 dark:bg-red-900/20 dark:text-red-400 dark:border-red-800/30'
          ]">
            <BootstrapIcon v-if="msgProfile.type === 'success'" name="check-circle-fill" class="w-4 h-4 shrink-0 mt-0.5" />
            <BootstrapIcon v-else name="exclamation-triangle-fill" class="w-4 h-4 shrink-0 mt-0.5" />
            <span>{{ msgProfile.text }}</span>
          </div>

          <form @submit.prevent="handleUpdateProfile" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Telefone Principal</label>
                <input 
                  v-model="formProfile.telefone_principal" 
                  type="text" 
                  class="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg py-2.5 px-3 text-sm text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                  placeholder="Ex: 841234567"
                  required
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Email de Contacto</label>
                <input 
                  v-model="formProfile.email_contacto" 
                  type="email" 
                  class="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg py-2.5 px-3 text-sm text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                  placeholder="email@exemplo.com"
                  required
                />
              </div>
            </div>

            <div class="flex justify-end pt-2">
              <button 
                type="submit" 
                :disabled="pendingProfileUpdate"
                class="px-5 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-2 min-h-[44px]"
              >
                <span v-if="pendingProfileUpdate" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
                {{ pendingProfileUpdate ? 'A guardar...' : 'Atualizar Contactos' }}
              </button>
            </div>
          </form>
        </section>

      </div>

      <!-- Coluna da direita - Segurança -->
      <div class="space-y-5 md:space-y-6">
        
        <section class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
          <h3 class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-5 border-b border-slate-100 dark:border-slate-800 pb-3">
            <BootstrapIcon name="shield-lock" class="w-5 h-5 text-slate-400" />
            Segurança
          </h3>

          <!-- Mensagem de feedback da senha -->
          <div v-if="msgPassword.text" :class="[
            'mb-5 p-3 rounded-lg flex items-start gap-2 text-sm border',
            msgPassword.type === 'success' 
              ? 'bg-emerald-50 text-emerald-800 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30' 
              : 'bg-red-50 text-red-800 border-red-200 dark:bg-red-900/20 dark:text-red-400 dark:border-red-800/30'
          ]">
            <BootstrapIcon v-if="msgPassword.type === 'success'" name="check-circle-fill" class="w-4 h-4 shrink-0 mt-0.5" />
            <BootstrapIcon v-else name="exclamation-triangle-fill" class="w-4 h-4 shrink-0 mt-0.5" />
            <span>{{ msgPassword.text }}</span>
          </div>

          <form @submit.prevent="handleChangePassword" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Senha Atual</label>
              <input 
                v-model="formSenha.old_password" 
                type="password" 
                required 
                placeholder="••••••••"
                class="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg py-2.5 px-3 text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors" 
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Nova Senha</label>
              <input 
                v-model="formSenha.new_password" 
                type="password" 
                required 
                placeholder="••••••••"
                class="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg py-2.5 px-3 text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors" 
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Confirmar Nova Senha</label>
              <input 
                v-model="formSenha.confirm_password" 
                type="password" 
                required 
                placeholder="••••••••"
                class="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg py-2.5 px-3 text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors" 
              />
            </div>

            <button 
              type="submit" 
              :disabled="pendingSenha"
              class="w-full mt-6 py-3 sm:py-2.5 px-4 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex justify-center items-center gap-2 min-h-[44px]"
            >
              <span v-if="pendingSenha" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
              {{ pendingSenha ? 'A processar...' : 'Alterar Senha' }}
            </button>
          </form>

        </section>

      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { inject, type Ref, ref, reactive, onMounted } from 'vue'
const { api } = useApi()
// Dados Injetados (Layout/Dashboard)
interface UserData {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  perfil: number;
}
const userData = inject<Ref<UserData | null>>('userData')
const userPending = inject<Ref<boolean>>('pendingData')

// --- LÓGICA 1: DADOS DE CONTACTO DO ENCARREGADO ---
const loadingProfile = ref(true)
const pendingProfileUpdate = ref(false)
const msgProfile = reactive({ text: '', type: '' })
const formProfile = reactive({
  telefone_principal: '',
  email_contacto: ''
})

// Fetch Dados Iniciais
onMounted(async () => {
  try {
    const res = await api<any>('/perfil-encarregado/meus-dados/')
    formProfile.telefone_principal = res.telefone_principal
    formProfile.email_contacto = res.email_contacto
  } catch (e) {
    console.error("Erro ao carregar perfil encarregado", e)
  } finally {
    loadingProfile.value = false
  }
})

// Update Dados
const handleUpdateProfile = async () => {
  pendingProfileUpdate.value = true
  msgProfile.text = ''
  
  try {
    await api('/perfil-encarregado/meus-dados/', {
      method: 'PATCH',
      body: { ...formProfile }
    })
    msgProfile.type = 'success'
    msgProfile.text = 'Contactos atualizados com sucesso!'
  } catch (err) {
    msgProfile.type = 'error'
    msgProfile.text = 'Erro ao atualizar. Verifique os dados.'
  } finally {
    pendingProfileUpdate.value = false
  }
}

// --- LÓGICA 2: ALTERAR SENHA ---
const pendingSenha = ref(false)
const msgPassword = reactive({ text: '', type: '' })
const formSenha = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const handleChangePassword = async () => {
  pendingSenha.value = true
  msgPassword.text = ''

  if (formSenha.new_password !== formSenha.confirm_password) {
    msgPassword.type = 'error'
    msgPassword.text = "As novas senhas não coincidem."
    pendingSenha.value = false
    return
  }

  try {
    await api('/users/change-password/', {
      method: 'PATCH',
      body: {
        old_password: formSenha.old_password,
        new_password: formSenha.new_password
      }
    })
    msgPassword.type = 'success'
    msgPassword.text = "Senha alterada com sucesso!"
    
    // Limpar campos
    formSenha.old_password = ''
    formSenha.new_password = ''
    formSenha.confirm_password = ''
  } catch (err: any) {
    msgPassword.type = 'error'
    if (err.data?.old_password) msgPassword.text = "Senha antiga incorreta."
    else if (err.data?.new_password) msgPassword.text = err.data.new_password[0]
    else msgPassword.text = "Erro ao alterar a senha."
  } finally {
    pendingSenha.value = false
  }
}

// Helper Iniciais
const getIniciais = (nome: string) => {
  const limpo = (nome || '').trim();
  if (!limpo) return '??';
  
  const partes = limpo.split(/\s+/);
  const primeira = partes[0]?.[0] || '';
  const ultima = partes.length > 1 ? partes[partes.length - 1]?.[0] || '' : '';

  return (primeira + ultima).toUpperCase();
}
</script>
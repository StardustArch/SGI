<template>
  <div class="space-y-8 dark:text-white max-w-8xl mx-auto p-4 md:p-8">
    
    <div>
      <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">O Meu Perfil</h1>
      <p class="text-stone-500 dark:text-gray-400 mt-1 text-lg">Gerencie os seus dados de contacto e segurança.</p>
    </div>

    <div v-if="userPending || loadingProfile" class="flex flex-col items-center justify-center py-20">
      <div class="animate-spin h-10 w-10 border-4 border-rose-500 border-t-transparent rounded-full mb-4"></div>
      <p class="text-stone-400">A carregar informações...</p>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <div class="lg:col-span-2 space-y-8">
        
        <div class="bg-white dark:bg-gray-800 rounded-[2rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm flex items-start gap-6 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-32 h-32 bg-stone-100 rounded-full -mr-10 -mt-10 dark:bg-gray-700 opacity-50"></div>

          <div class="h-20 w-20 rounded-2xl bg-rose-50 dark:bg-gray-700 text-rose-500 flex items-center justify-center text-2xl font-bold border border-rose-100 dark:border-gray-600 shrink-0 z-10">
            {{ getIniciais(userData?.first_name || '') }}
          </div>

          <div class="z-10">
            <h2 class="text-2xl font-bold text-gray-800 dark:text-white">
              {{ userData?.first_name }} {{ userData?.last_name }}
            </h2>
            <p class="text-stone-500 dark:text-gray-400 mt-1 flex items-center gap-2">
              <span class="px-2 py-0.5 rounded bg-stone-100 dark:bg-gray-700 text-xs font-bold uppercase tracking-wide border border-stone-200 dark:border-gray-600">
                Encarregado
              </span>
            </p>
            <p class="text-sm text-stone-400 mt-4">
              <span class="font-bold uppercase text-[10px] tracking-wider">Email de Login:</span><br>
              {{ userData?.email }}
            </p>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-[2rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-bold text-gray-800 dark:text-white flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-rose-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>
              Meus Contactos
            </h3>
            <span class="text-xs text-stone-400 bg-stone-50 dark:bg-gray-700 px-2 py-1 rounded">Editável</span>
          </div>

          <div v-if="msgProfile.text" :class="['mb-6 p-4 rounded-xl flex items-center gap-3 text-sm font-medium', msgProfile.type === 'success' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-200' : 'bg-rose-50 text-rose-700 dark:bg-rose-900/30 dark:text-rose-200']">
             <div :class="['w-2 h-2 rounded-full', msgProfile.type === 'success' ? 'bg-emerald-500' : 'bg-rose-500']"></div>
             {{ msgProfile.text }}
          </div>

          <form @submit.prevent="handleUpdateProfile" class="space-y-5">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div class="space-y-1">
                <label class="text-xs font-bold text-stone-500 uppercase ml-1">Telefone Principal</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-stone-400">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>
                  </div>
                  <input 
                    v-model="formProfile.telefone_principal" 
                    type="text" 
                    class="w-full bg-stone-50 dark:bg-gray-700 border border-stone-200 dark:border-gray-600 text-gray-800 dark:text-white rounded-xl py-3 pl-10 pr-4 focus:outline-none focus:ring-2 focus:ring-rose-200 transition-all font-medium"
                    placeholder="Ex: 841234567"
                    required
                  />
                </div>
              </div>

              <div class="space-y-1">
                <label class="text-xs font-bold text-stone-500 uppercase ml-1">Email de Contacto</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-stone-400">
                     <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
                  </div>
                  <input 
                    v-model="formProfile.email_contacto" 
                    type="email" 
                    class="w-full bg-stone-50 dark:bg-gray-700 border border-stone-200 dark:border-gray-600 text-gray-800 dark:text-white rounded-xl py-3 pl-10 pr-4 focus:outline-none focus:ring-2 focus:ring-rose-200 transition-all font-medium"
                    placeholder="email@exemplo.com"
                    required
                  />
                </div>
              </div>
            </div>

            <div class="flex justify-end pt-2">
              <button 
                type="submit" 
                :disabled="pendingProfileUpdate"
                class="px-6 py-3 rounded-xl bg-gray-900 dark:bg-white text-white dark:text-gray-900 font-bold text-sm hover:opacity-90 transition-opacity disabled:opacity-50 flex items-center gap-2"
              >
                <span v-if="pendingProfileUpdate" class="animate-spin h-4 w-4 border-2 border-current border-t-transparent rounded-full"></span>
                {{ pendingProfileUpdate ? 'A guardar...' : 'Atualizar Contactos' }}
              </button>
            </div>
          </form>
        </div>

      </div>

      <div class="space-y-8">
        
        <div class="bg-white dark:bg-gray-800 rounded-[2rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm relative overflow-hidden">
          
          <div class="flex items-center gap-2 mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-rose-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
            <h3 class="text-lg font-bold text-gray-800 dark:text-white">Segurança</h3>
          </div>

          <div v-if="msgPassword.text" :class="['mb-6 p-4 rounded-xl flex items-center gap-3 text-sm font-medium', msgPassword.type === 'success' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-200' : 'bg-rose-50 text-rose-700 dark:bg-rose-900/30 dark:text-rose-200']">
             {{ msgPassword.text }}
          </div>

          <form @submit.prevent="handleChangePassword" class="space-y-4">
            <div>
              <label class="text-xs font-bold text-stone-500 uppercase ml-1 block mb-1">Senha Atual</label>
              <input v-model="formSenha.old_password" type="password" required class="w-full bg-stone-50 dark:bg-gray-700 border border-stone-200 dark:border-gray-600 rounded-xl py-3 px-4 focus:outline-none focus:ring-2 focus:ring-rose-200 transition-all font-medium" />
            </div>
            
            <div>
              <label class="text-xs font-bold text-stone-500 uppercase ml-1 block mb-1">Nova Senha</label>
              <input v-model="formSenha.new_password" type="password" required class="w-full bg-stone-50 dark:bg-gray-700 border border-stone-200 dark:border-gray-600 rounded-xl py-3 px-4 focus:outline-none focus:ring-2 focus:ring-rose-200 transition-all font-medium" />
            </div>

            <div>
              <label class="text-xs font-bold text-stone-500 uppercase ml-1 block mb-1">Confirmar Nova Senha</label>
              <input v-model="formSenha.confirm_password" type="password" required class="w-full bg-stone-50 dark:bg-gray-700 border border-stone-200 dark:border-gray-600 rounded-xl py-3 px-4 focus:outline-none focus:ring-2 focus:ring-rose-200 transition-all font-medium" />
            </div>

            <button 
              type="submit" 
              :disabled="pendingSenha"
              class="w-full py-3 rounded-xl bg-rose-500 text-white font-bold text-sm hover:bg-rose-600 shadow-lg shadow-rose-200 dark:shadow-none transition-all disabled:opacity-50 mt-2"
            >
              {{ pendingSenha ? 'A processar...' : 'Alterar Senha' }}
            </button>
          </form>

        </div>

      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { inject, type Ref } from 'vue'
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
  
  // Usamos '?.' para aceder com segurança e '|| ""' caso falhe
  const primeira = partes[0]?.[0] || '';
  const ultima = partes.length > 1 ? partes[partes.length - 1]?.[0] || '' : '';

  return (primeira + ultima).toUpperCase();
}
</script>
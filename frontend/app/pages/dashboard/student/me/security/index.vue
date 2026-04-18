<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-12">
    
    <header class="mb-6 md:mb-8 border-b border-slate-200 dark:border-slate-800 pb-4 md:pb-6">
      <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">Dossiê Pessoal</h1>
      <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">
        Consulte os seus dados académicos e faça a gestão da sua segurança.
      </p>
    </header>

    <div v-if="pending" class="flex flex-col items-center justify-center py-20 space-y-4">
      <div class="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full"></div>
      <p class="text-sm text-slate-500 dark:text-slate-400 font-medium">A sincronizar dados...</p>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6 md:gap-8">
      
      <div class="lg:col-span-2 space-y-5 md:space-y-6">
        
        <section class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col sm:flex-row items-start sm:items-center gap-4 sm:gap-6">
          <div class="h-16 w-16 sm:h-20 sm:w-20 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center text-xl sm:text-2xl font-bold border border-blue-100 dark:border-blue-800 shrink-0">
            {{ getIniciais(perfil?.nome_completo || '') }}
          </div>

          <div class="flex-grow min-w-0">
            <h2 class="text-lg sm:text-xl font-bold text-slate-900 dark:text-white mb-1 break-words">
              {{ perfil?.nome_completo }}
            </h2>
            <div class="flex flex-wrap items-center gap-2 mb-2 sm:mb-3">
              <span class="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-xs font-medium border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300">
                Residente
              </span>
              <span :class="['px-2.5 py-0.5 rounded-md text-xs font-medium border', perfil?.estado === 'Activo' ? 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30' : 'bg-red-50 text-red-700 border-red-200 dark:bg-red-900/20 dark:text-red-400 dark:border-red-800/30']">
                {{ perfil?.estado }}
              </span>
            </div>
            <p class="text-sm text-slate-500 dark:text-slate-400 flex items-center gap-2 break-all">
              <BootstrapIcon name="envelope" class="w-4 h-4 shrink-0" />
              <span class="truncate">{{ perfil?.email }}</span>
            </p>
          </div>
        </section>

        <section class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
          <h3 class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-5 md:mb-6 border-b border-slate-100 dark:border-slate-800 pb-3">
            <BootstrapIcon name="mortarboard" class="w-5 h-5 text-slate-400 shrink-0" />
            Dados Institucionais
          </h3>

          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-6">
             <div>
                <p class="text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">Nº Estudante</p>
                <p class="text-sm font-semibold text-slate-900 dark:text-white">{{ perfil?.num_estudante }}</p>
             </div>
             <div>
                <p class="text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">Curso</p>
                <p class="text-sm font-semibold text-slate-900 dark:text-white truncate" :title="perfil?.curso">{{ perfil?.curso }}</p>
             </div>
             <div>
                <p class="text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">Alojamento</p>
                <div class="flex items-center gap-1.5">
                   <BootstrapIcon name="door-closed" class="w-4 h-4 text-slate-400 shrink-0" />
                   <p class="text-sm font-semibold text-slate-900 dark:text-white">Quarto {{ perfil?.quarto }}</p>
                </div>
             </div>
          </div>
        </section>

        <section class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
          <h3 class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-5 md:mb-6 border-b border-slate-100 dark:border-slate-800 pb-3">
            <BootstrapIcon name="person-heart" class="w-5 h-5 text-slate-400 shrink-0" />
            Encarregado de Educação
          </h3>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
             <div>
                <p class="text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">Nome Completo</p>
                <p class="text-sm font-semibold text-slate-900 dark:text-white break-words">{{ perfil?.encarregado_nome }}</p>
             </div>
             <div>
                <p class="text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">Contacto Principal</p>
                <p class="text-sm font-semibold text-slate-900 dark:text-white flex items-center gap-1.5">
                   <BootstrapIcon name="telephone" class="w-4 h-4 text-slate-400 shrink-0" />
                   {{ perfil?.encarregado_telefone }}
                </p>
             </div>
          </div>
        </section>

      </div>

      <div class="space-y-5 md:space-y-6">
        
        <section class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
          
          <h3 class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-5 md:mb-6 border-b border-slate-100 dark:border-slate-800 pb-3">
            <BootstrapIcon name="shield-lock" class="w-5 h-5 text-slate-400 shrink-0" />
            Credenciais de Acesso
          </h3>

          <div v-if="msgPassword.text" :class="['mb-5 md:mb-6 p-4 rounded-lg flex gap-3 text-sm font-medium border', msgPassword.type === 'success' ? 'bg-emerald-50 text-emerald-800 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30' : 'bg-red-50 text-red-800 border-red-200 dark:bg-red-900/20 dark:text-red-400 dark:border-red-800/30']">
             <BootstrapIcon v-if="msgPassword.type === 'success'" name="check-circle-fill" class="w-5 h-5 shrink-0" />
             <BootstrapIcon v-else name="exclamation-triangle-fill" class="w-5 h-5 shrink-0" />
             <p class="break-words">{{ msgPassword.text }}</p>
          </div>

          <form @submit.prevent="handleChangePassword" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Senha Atual</label>
              <input 
                v-model="formSenha.old_password" 
                type="password" 
                required 
                placeholder="••••••••"
                class="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg py-2.5 sm:py-2 px-3 text-base sm:text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors" 
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Nova Senha</label>
              <input 
                v-model="formSenha.new_password" 
                type="password" 
                required 
                placeholder="••••••••"
                class="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg py-2.5 sm:py-2 px-3 text-base sm:text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors" 
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Confirmar Nova Senha</label>
              <input 
                v-model="formSenha.confirm_password" 
                type="password" 
                required 
                placeholder="••••••••"
                class="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg py-2.5 sm:py-2 px-3 text-base sm:text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors" 
              />
            </div>

            <button 
              type="submit" 
              :disabled="pendingSenha"
              class="w-full mt-6 py-3 sm:py-2.5 px-4 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex justify-center items-center gap-2 min-h-[44px]"
            >
              <span v-if="pendingSenha" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
              {{ pendingSenha ? 'A processar...' : 'Atualizar Senha' }}
            </button>
          </form>

        </section>

      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'

const { api } = useApi()

// Buscar os dados do perfil (Estudante)
const { data: perfil, pending } = await useAsyncData(
  'student-profile',
  () => api<any>('/student/me/'),
  { lazy: true }
)

// --- LÓGICA: ALTERAR SENHA ---
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
    msgPassword.text = "Senha alterada com sucesso."
    
    // Limpar campos
    formSenha.old_password = ''
    formSenha.new_password = ''
    formSenha.confirm_password = ''
  } catch (err: any) {
    msgPassword.type = 'error'
    // Tenta ler a mensagem de erro específica do backend
    if (err.response?._data?.old_password) msgPassword.text = "A senha atual está incorreta."
    else if (err.response?._data?.new_password) msgPassword.text = err.response._data.new_password[0]
    else msgPassword.text = "Ocorreu um erro ao atualizar a senha."
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
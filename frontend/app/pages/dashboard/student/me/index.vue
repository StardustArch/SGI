<template>
  <div class="space-y-8 dark:text-white max-w-7xl mx-auto p-4 md:p-8">
    
    <div>
      <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">O Meu Perfil</h1>
      <p class="text-stone-500 dark:text-gray-400 mt-1 text-lg">Os seus dados pessoais e académicos.</p>
    </div>

    <div v-if="pending" class="flex flex-col items-center justify-center py-20">
      <div class="animate-spin h-10 w-10 border-4 border-rose-500 border-t-transparent rounded-full mb-4"></div>
      <p class="text-stone-400">A carregar informações...</p>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <div class="lg:col-span-2 space-y-8">
        
        <div class="bg-white dark:bg-gray-800 rounded-[2rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm flex items-start gap-6 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-32 h-32 bg-stone-100 rounded-full -mr-10 -mt-10 dark:bg-gray-700 opacity-50"></div>

          <div class="h-20 w-20 rounded-2xl bg-rose-50 dark:bg-gray-700 text-rose-500 flex items-center justify-center text-2xl font-bold border border-rose-100 dark:border-gray-600 shrink-0 z-10">
            {{ getIniciais(perfil?.nome_completo || '') }}
          </div>

          <div class="z-10">
            <h2 class="text-2xl font-bold text-gray-800 dark:text-white">
              {{ perfil?.nome_completo }}
            </h2>
            <div class="mt-2 flex flex-wrap gap-2">
              <span class="px-2 py-0.5 rounded bg-stone-100 dark:bg-gray-700 text-xs font-bold uppercase tracking-wide border border-stone-200 dark:border-gray-600 text-stone-500">
                Estudante
              </span>
              <span :class="['px-2 py-0.5 rounded text-xs font-bold uppercase tracking-wide border', perfil?.estado === 'Activo' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-red-50 text-red-700 border-red-200']">
                {{ perfil?.estado }}
              </span>
            </div>
            <p class="text-sm text-stone-400 mt-4">
              <span class="font-bold uppercase text-[10px] tracking-wider">Email de Login:</span><br>
              {{ perfil?.email }}
            </p>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-[2rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm">
          <h3 class="text-lg font-bold text-gray-800 dark:text-white flex items-center gap-2 mb-6">
            <BootstrapIcon name="mortarboard" class="w-5 h-5 text-rose-500" />
            Dados Académicos
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
             <div class="bg-stone-50 dark:bg-gray-700/50 p-4 rounded-xl border border-stone-100 dark:border-gray-600">
                <p class="text-[10px] font-bold text-stone-400 uppercase tracking-wider mb-1">Nº Estudante</p>
                <p class="text-lg font-bold text-gray-800 dark:text-white">{{ perfil?.num_estudante }}</p>
             </div>

             <div class="bg-stone-50 dark:bg-gray-700/50 p-4 rounded-xl border border-stone-100 dark:border-gray-600">
                <p class="text-[10px] font-bold text-stone-400 uppercase tracking-wider mb-1">Curso</p>
                <p class="text-lg font-bold text-gray-800 dark:text-white truncate">{{ perfil?.curso }}</p>
             </div>

             <div class="bg-stone-50 dark:bg-gray-700/50 p-4 rounded-xl border border-stone-100 dark:border-gray-600">
                <p class="text-[10px] font-bold text-stone-400 uppercase tracking-wider mb-1">Alojamento</p>
                <div class="flex items-center gap-2">
                   <BootstrapIcon name="door-closed" class="w-5 h-5 text-stone-400" />
                   <p class="text-lg font-bold text-gray-800 dark:text-white">Quarto {{ perfil?.quarto }}</p>
                </div>
             </div>
          </div>
        </div>

         <div class="bg-white dark:bg-gray-800 rounded-[2rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm">
          <h3 class="text-lg font-bold text-gray-800 dark:text-white flex items-center gap-2 mb-6">
            <BootstrapIcon name="person-heart" class="w-5 h-5 text-rose-500" />
            Encarregado de Educação
          </h3>

          <div class="flex flex-col md:flex-row gap-6">
             <div class="flex-1 space-y-1">
                <p class="text-[10px] font-bold text-stone-400 uppercase tracking-wider">Nome Completo</p>
                <p class="text-base font-bold text-gray-800 dark:text-white">{{ perfil?.encarregado_nome }}</p>
             </div>
             <div class="flex-1 space-y-1">
                <p class="text-[10px] font-bold text-stone-400 uppercase tracking-wider">Contacto Principal</p>
                <p class="text-base font-bold text-gray-800 dark:text-white flex items-center gap-2">
                   <BootstrapIcon name="telephone" class="w-4 h-4 text-stone-400" />
                   {{ perfil?.encarregado_telefone }}
                </p>
             </div>
          </div>
        </div>

      </div>

      <div class="space-y-8">
        
        <div class="bg-white dark:bg-gray-800 rounded-[2rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm relative overflow-hidden">
          
          <div class="flex items-center gap-2 mb-6">
            <BootstrapIcon name="shield-lock" class="w-5 h-5 text-rose-500" />
            <h3 class="text-lg font-bold text-gray-800 dark:text-white">Segurança</h3>
          </div>

          <div v-if="msgPassword.text" :class="['mb-6 p-4 rounded-xl flex items-center gap-3 text-sm font-medium', msgPassword.type === 'success' ? 'bg-emerald-50 text-emerald-700 border border-emerald-100' : 'bg-rose-50 text-rose-700 border border-rose-100']">
             <BootstrapIcon v-if="msgPassword.type === 'success'" name="check-circle-fill" class="w-5 h-5" />
             <BootstrapIcon v-else name="exclamation-triangle-fill" class="w-5 h-5" />
             {{ msgPassword.text }}
          </div>

          <form @submit.prevent="handleChangePassword" class="space-y-5">
            <div class="space-y-1">
              <label class="text-xs font-bold text-stone-500 uppercase ml-1">Senha Atual</label>
              <input 
                v-model="formSenha.old_password" 
                type="password" 
                required 
                placeholder="••••••••"
                class="w-full bg-stone-50 dark:bg-gray-700 border border-stone-200 dark:border-gray-600 rounded-xl py-3 px-4 focus:outline-none focus:ring-2 focus:ring-rose-200 transition-all font-medium" 
              />
            </div>
            
            <div class="space-y-1">
              <label class="text-xs font-bold text-stone-500 uppercase ml-1">Nova Senha</label>
              <input 
                v-model="formSenha.new_password" 
                type="password" 
                required 
                placeholder="••••••••"
                class="w-full bg-stone-50 dark:bg-gray-700 border border-stone-200 dark:border-gray-600 rounded-xl py-3 px-4 focus:outline-none focus:ring-2 focus:ring-rose-200 transition-all font-medium" 
              />
            </div>

            <div class="space-y-1">
              <label class="text-xs font-bold text-stone-500 uppercase ml-1">Confirmar Nova Senha</label>
              <input 
                v-model="formSenha.confirm_password" 
                type="password" 
                required 
                placeholder="••••••••"
                class="w-full bg-stone-50 dark:bg-gray-700 border border-stone-200 dark:border-gray-600 rounded-xl py-3 px-4 focus:outline-none focus:ring-2 focus:ring-rose-200 transition-all font-medium" 
              />
            </div>

            <button 
              type="submit" 
              :disabled="pendingSenha"
              class="w-full py-3.5 rounded-xl bg-gray-900 dark:bg-white text-white dark:text-gray-900 font-bold text-sm hover:opacity-90 shadow-lg shadow-stone-200 dark:shadow-none transition-all disabled:opacity-50 mt-4 flex justify-center items-center gap-2"
            >
              <span v-if="pendingSenha" class="animate-spin h-4 w-4 border-2 border-current border-t-transparent rounded-full"></span>
              {{ pendingSenha ? 'A processar...' : 'Atualizar Senha' }}
            </button>
          </form>

        </div>

      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'

const { api } = useApi()

// Buscar os dados do perfil (Estudante)
// Atenção: Use o endpoint correto para estudante
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
    msgPassword.text = "Senha alterada com sucesso!"
    
    // Limpar campos
    formSenha.old_password = ''
    formSenha.new_password = ''
    formSenha.confirm_password = ''
  } catch (err: any) {
    msgPassword.type = 'error'
    // Tenta ler a mensagem de erro específica do backend
    if (err.response?._data?.old_password) msgPassword.text = "A senha antiga está incorreta."
    else if (err.response?._data?.new_password) msgPassword.text = err.response._data.new_password[0]
    else msgPassword.text = "Ocorreu um erro ao alterar a senha."
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
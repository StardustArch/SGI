<template>
  <div class="space-y-8 dark:text-white max-w-3xl mx-auto p-4 md:p-8">
    
    <div class="flex items-center gap-4">
      <NuxtLink to="/dashboard/admin/guardian" class="p-2 hover:bg-stone-100 dark:hover:bg-gray-700 rounded-full transition">
        <BootstrapIcon name="arrow-left" class="w-6 h-6" />
      </NuxtLink>
      <h1 class="text-3xl font-bold tracking-tight">Ficha do Encarregado</h1>
    </div>

    <div v-if="pending" class="animate-pulse h-64 bg-stone-100 dark:bg-gray-800 rounded-[2.5rem]"></div>

    <div v-else class="space-y-6">
      
      <div class="bg-white dark:bg-gray-800 rounded-[2.5rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm relative overflow-hidden">
        <div class="absolute top-0 right-0 w-32 h-32 bg-stone-50 dark:bg-gray-700/50 rounded-full -mr-10 -mt-10 opacity-50"></div>
        
        <div class="flex flex-col md:flex-row items-center md:items-start gap-6 relative z-10">
          <div class="h-20 w-20 rounded-3xl bg-stone-100 dark:bg-gray-700 text-stone-500 flex items-center justify-center text-3xl font-bold border border-stone-200 dark:border-gray-600">
            {{ form.nome_completo?.charAt(0) }}
          </div>
          <div class="text-center md:text-left space-y-1">
            <h2 class="text-2xl font-black">{{ form.nome_completo }}</h2>
            <p class="text-stone-400 font-medium text-sm">Perfil de Responsável / Contacto de Emergência</p>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-[2.5rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm">
        <h3 class="text-lg font-bold mb-6 flex items-center gap-2">
          <BootstrapIcon name="pencil" class="text-rose-500" />
          Atualizar Contactos
        </h3>

        <form @submit.prevent="handleUpdate" class="space-y-6">
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Nome Completo</label>
            <input v-model="form.nome_completo" type="text" class="admin-input" required />
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-1">
              <label class="text-[10px] font-bold text-stone-400 uppercase ml-1 flex items-center gap-1">
                <BootstrapIcon name="telephone-fill" /> Telefone Principal
              </label>
              <input v-model="form.telefone_principal" type="text" class="admin-input" required />
            </div>
            
            <div class="space-y-1">
              <label class="text-[10px] font-bold text-stone-400 uppercase ml-1 flex items-center gap-1">
                <BootstrapIcon name="envelope-fill" /> Email de Contacto
              </label>
              <input v-model="form.email_contacto" type="email" class="admin-input" />
            </div>
          </div>

          <div class="pt-4 flex justify-end">
            <button 
              type="submit" 
              :disabled="updating"
              class="px-8 py-3 rounded-xl bg-gray-900 dark:bg-white text-white dark:text-gray-900 font-bold text-sm shadow-lg hover:opacity-90 transition-all disabled:opacity-50 flex items-center gap-2"
            >
              <span v-if="updating" class="animate-spin h-4 w-4 border-2 border-current border-t-transparent rounded-full"></span>
              {{ updating ? 'A guardar...' : 'Guardar Alterações' }}
            </button>
          </div>
        </form>
      </div>

      <div class="bg-stone-50 dark:bg-gray-800/50 rounded-[2rem] p-8 border border-stone-100 dark:border-gray-700">
        <h3 class="text-sm font-bold text-stone-400 uppercase mb-4 tracking-widest flex items-center gap-2">
          <BootstrapIcon name="people-fill" class="text-stone-400" />
          Educandos Associados
        </h3>
        <div class="flex flex-wrap gap-2">
          <span v-for="(aluno, idx) in encarregado?.educandos" :key="idx" class="px-4 py-2 bg-white dark:bg-gray-700 rounded-xl text-sm font-bold text-gray-700 dark:text-gray-200 border border-stone-200 dark:border-gray-600 shadow-sm">
            {{ aluno }}
          </span>
          <span v-if="!encarregado?.educandos?.length" class="text-sm text-stone-400 italic">Nenhum educando associado.</span>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
const { api } = useApi()
const route = useRoute()
const updating = ref(false)

const form = reactive({
  nome_completo: '',
  telefone_principal: '',
  email_contacto: ''
})

// Buscar dados
const { data: encarregado, pending } = await useAsyncData('admin-encarregado-detail', 
  () => api<any>(`/admin/encarregados/${route.params.id}/`)
)
    console.log(encarregado.value)
// Preencher formulário
watch(encarregado, (val) => {
  if (val) {
    form.nome_completo = val.nome_completo
    form.telefone_principal = val.telefone_principal
    form.email_contacto = val.email || ''   // usando val.email
  }
}, { immediate: true })

async function handleUpdate() {
  updating.value = true
  try {
    await api(`/admin/encarregados/${route.params.id}/`, {
      method: 'PATCH',
      body: {
        nome_completo: form.nome_completo,
        telefone_principal: form.telefone_principal,
        email: form.email_contacto   // mapear para o campo email do modelo
      }
    })
    alert("Dados do encarregado atualizados com sucesso!")
  } catch (e: any) {
    alert(e.data?.telefone_principal ? "Este telefone já está em uso." : "Erro ao atualizar dados.")
  } finally {
    updating.value = false
  }
}
</script>

<style scoped>
.admin-input {
  @apply w-full bg-stone-50 dark:bg-gray-900 border border-stone-200 dark:border-gray-700 rounded-xl py-3 px-4 focus:outline-none focus:ring-2 focus:ring-rose-200 dark:focus:ring-rose-900 transition-all font-medium text-gray-800 dark:text-white;
}
</style>
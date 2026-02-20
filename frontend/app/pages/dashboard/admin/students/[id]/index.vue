<template>
  <div class="space-y-8 dark:text-white max-w-4xl mx-auto p-4 md:p-8">
    
    <div class="flex items-center gap-4">
      <NuxtLink to="/dashboard/admin/students" class="p-2 hover:bg-stone-100 rounded-full transition">
        <BootstrapIcon name="arrow-left" class="w-6 h-6" />
      </NuxtLink>
      <h1 class="text-3xl font-bold tracking-tight">Ficha do Interno</h1>
    </div>

    <div v-if="pending" class="animate-pulse space-y-4">
      <div class="h-64 bg-stone-100 rounded-[2.5rem]"></div>
    </div>

    <div v-else class="space-y-6">
      <div class="bg-white dark:bg-gray-800 rounded-[2.5rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm relative overflow-hidden">
        <div class="absolute top-0 right-0 w-32 h-32 bg-stone-50 rounded-full -mr-10 -mt-10 opacity-50"></div>
        
        <div class="flex flex-col md:flex-row items-center md:items-start gap-6 relative z-10">
          <div class="h-24 w-24 rounded-3xl bg-rose-50 text-rose-500 flex items-center justify-center text-3xl font-bold border border-rose-100">
            {{ form.nome_completo?.charAt(0) }}
          </div>
          <div class="text-center md:text-left space-y-2">
            <h2 class="text-2xl font-black">{{ form.nome_completo }}</h2>
            <p class="text-stone-400 font-medium">{{ form.email }}</p>
            <div class="flex gap-2 justify-center md:justify-start">
               <span class="px-2 py-0.5 rounded-lg bg-stone-100 text-[10px] font-bold uppercase text-stone-500 border border-stone-200">
                 {{ form.num_estudante }}
               </span>
               <span :class="['px-2 py-0.5 rounded-lg text-[10px] font-bold uppercase border', form.estado === 'Activo' ? 'bg-emerald-50 text-emerald-700 border-emerald-100' : 'bg-rose-50 text-rose-700 border-rose-100']">
                 {{ form.estado }}
               </span>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-[2.5rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm">
        <h3 class="text-lg font-bold mb-6 flex items-center gap-2">
          <BootstrapIcon name="pencil" class="text-rose-500" />
          Editar Informações
        </h3>

        <form @submit.prevent="handleUpdate" class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Nome Completo</label>
            <input v-model="form.nome_completo" type="text" class="admin-input" />
          </div>
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Curso</label>
            <input v-model="form.curso" type="text" class="admin-input" />
          </div>
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Quarto</label>
            <input v-model="form.quarto" type="text" class="admin-input" />
          </div>
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Estado no Internato</label>
            <select v-model="form.estado" class="admin-input appearance-none">
              <option value="Activo">Activo</option>
              <option value="Inactivo">Inactivo</option>
            </select>
          </div>

          <div class="md:col-span-2 pt-4 flex justify-end">
            <button 
              type="submit" 
              :disabled="updating"
              class="px-8 py-3 rounded-xl bg-gray-900 dark:bg-white text-white dark:text-gray-900 font-bold text-sm shadow-lg hover:opacity-90 transition-all disabled:opacity-50"
            >
              {{ updating ? 'A guardar...' : 'Guardar Alterações' }}
            </button>
          </div>
        </form>
      </div>

      <div class="bg-stone-50 dark:bg-gray-900/50 rounded-[2rem] p-8 border border-stone-100 dark:border-gray-800">
         <h3 class="text-sm font-bold text-stone-400 uppercase mb-4 tracking-widest">Encarregado Responsável</h3>
         <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
               <div class="h-12 w-12 rounded-full bg-white dark:bg-gray-800 flex items-center justify-center font-bold text-stone-400 shadow-sm border border-stone-100">
                  {{ aluno?.encarregado_nome?.charAt(0) }}
               </div>
               <div>
                  <p class="font-bold text-gray-800 dark:text-white">{{ aluno?.encarregado_nome }}</p>
                  <p class="text-xs text-stone-500">Contacto principal associado</p>
               </div>
            </div>
            <BootstrapIcon name="shield-check" class="text-emerald-500 w-6 h-6" />
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
  num_estudante: '',
  quarto: '',
  curso: '',
  estado: '',
  email: ''
})

// Buscar dados
const { data: aluno, pending } = await useAsyncData('admin-student-detail', 
  () => api<any>(`/admin/estudantes/${route.params.id}/`)
)

// Preencher formulário ao carregar
watch(aluno, (val) => {
  if (val) {
    form.nome_completo = val.nome_completo
    form.num_estudante = val.num_estudante
    form.quarto = val.quarto
    form.curso = val.curso
    form.estado = val.estado
    form.email = val.email
  }
}, { immediate: true })

async function handleUpdate() {
  updating.value = true
  try {
    await api(`/admin/estudantes/${route.params.id}/`, {
      method: 'PATCH',
      body: form
    })
    alert("Dados do aluno atualizados com sucesso!")
  } catch (e) {
    alert("Erro ao atualizar dados.")
  } finally {
    updating.value = false
  }
}
</script>

<style scoped>
.admin-input {
  @apply w-full bg-stone-50 dark:bg-gray-700 border border-stone-200 dark:border-gray-600 rounded-xl py-3 px-4 focus:outline-none focus:ring-2 focus:ring-rose-200 transition-all font-medium text-gray-800 dark:text-white;
}
</style>
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
            <p class="text-stone-400 font-medium">{{ form.email || 'Sem email de login' }}</p>
            <div class="flex gap-2 justify-center md:justify-start">
              <span class="px-2 py-0.5 rounded-lg bg-stone-100 text-[10px] font-bold uppercase text-stone-500 border border-stone-200">
                {{ form.bi || 'Sem BI' }}
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
            <input v-model="form.quarto_numero" type="text" disabled class="admin-input bg-stone-100 dark:bg-gray-700" />
          </div>
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Estado</label>
            <select v-model="form.estado" class="admin-input">
              <option value="Activo">Activo</option>
              <option value="Inactivo">Inactivo</option>
            </select>
          </div>
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Data de Nascimento</label>
            <input v-model="form.data_nascimento" type="date" class="admin-input" />
          </div>
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">BI/NUIT</label>
            <input v-model="form.bi" type="text" class="admin-input" />
          </div>
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Telefone Pessoal</label>
            <input v-model="form.telefone_pessoal" type="tel" class="admin-input" />
          </div>
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Email Pessoal</label>
            <input v-model="form.email_pessoal" type="email" class="admin-input" />
          </div>
          <div class="md:col-span-2 space-y-1">
            <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Morada</label>
            <textarea v-model="form.morada" rows="2" class="admin-input"></textarea>
          </div>
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Nome da Mãe</label>
            <input v-model="form.nome_mae" type="text" class="admin-input" />
          </div>
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Nome do Pai</label>
            <input v-model="form.nome_pai" type="text" class="admin-input" />
          </div>
          <div class="md:col-span-2 pt-4 flex justify-end">
            <button type="submit" :disabled="updating" class="px-8 py-3 rounded-xl bg-gray-900 dark:bg-white text-white dark:text-gray-900 font-bold text-sm shadow-lg hover:opacity-90 transition-all disabled:opacity-50">
              {{ updating ? 'A guardar...' : 'Guardar Alterações' }}
            </button>
          </div>
        </form>
      </div>

<div v-if="encarregado" class="bg-stone-50 dark:bg-gray-900/50 rounded-[2rem] p-8 border border-stone-100 dark:border-gray-800">
    <div class="flex items-center justify-between">
      <NuxtLink 
        :to="`/dashboard/admin/guardian/${encarregado.id}`" 
        class="flex items-center gap-4 group hover:bg-stone-100 dark:hover:bg-gray-800/50 rounded-xl p-2 -m-2 transition-colors"
      >
        <div class="h-12 w-12 rounded-full bg-white dark:bg-gray-800 flex items-center justify-center font-bold text-stone-400 shadow-sm border border-stone-100 dark:border-gray-700">
          {{ encarregado.nome_completo?.charAt(0) }}
        </div>
        <div>
          <p class="font-bold text-gray-800 dark:text-white group-hover:text-rose-600 dark:group-hover:text-rose-400 transition-colors">
            {{ encarregado.nome_completo }}
          </p>
          <p class="text-xs text-stone-500">
            {{ encarregado.parentesco || 'Contacto' }} • Tel: {{ encarregado.telefone_principal }}
          </p>
        </div>
      </NuxtLink>
      <BootstrapIcon name="arrow-right-short" class="text-stone-400 group-hover:text-rose-500 transition-colors" />
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
  curso: '',
  quarto_numero: '',
  estado: '',
  email: '',
  data_nascimento: '',
  bi: '',
  telefone_pessoal: '',
  email_pessoal: '',
  morada: '',
  nome_mae: '',
  nome_pai: ''
})
const encarregado = ref<any>(null)

const { data: aluno, pending } = await useAsyncData('admin-student-detail', 
  () => api<any>(`/admin/estudantes/${route.params.id}/`)
)

watch(aluno, (val) => {
  if (val) {
    form.nome_completo = val.nome_completo
    form.curso = val.curso
    form.quarto_numero = val.quarto_numero
    form.estado = val.estado
    form.email = val.email
    form.data_nascimento = val.data_nascimento || ''
    form.bi = val.bi || ''
    form.telefone_pessoal = val.telefone_pessoal || ''
    form.email_pessoal = val.email_pessoal || ''
    form.morada = val.morada || ''
    form.nome_mae = val.nome_mae || ''
    form.nome_pai = val.nome_pai || ''
    encarregado.value = val.encarregado || null
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
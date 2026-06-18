<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
      <div>
        <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">Utilizadores Internos</h1>
        <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">Gestão de contas administrativas do sistema.</p>
      </div>
      <NuxtLink 
        to="/dashboard/admin/users/create" 
        class="px-5 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors flex items-center gap-2 min-h-[44px]"
      >
        <BootstrapIcon name="person-plus-fill" class="w-4 h-4" />
        Novo Utilizador
      </NuxtLink>
    </div>

    <!-- Filtros -->
    <div class="bg-white dark:bg-slate-900 rounded-xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm mb-6">
      <div class="flex flex-col sm:flex-row gap-3">
        <div class="flex-1 relative">
          <BootstrapIcon name="search" class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
          <input 
            v-model="filtros.search"
            type="text"
            placeholder="Pesquisar por nome ou email..."
            class="w-full pl-10 pr-4 py-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            @input="buscar"
          />
        </div>
        <select 
          v-model="filtros.perfil" 
          class="px-4 py-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-medium cursor-pointer sm:w-48"
          @change="buscar"
        >
          <option value="">Todos os Perfis</option>
          <option v-for="p in perfisDisponiveis" :key="p" :value="p">{{ p }}</option>
        </select>
        <select 
          v-model="filtros.ativo" 
          class="px-4 py-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-medium cursor-pointer sm:w-40"
          @change="buscar"
        >
          <option value="">Todos</option>
          <option value="true">Activos</option>
          <option value="false">Inactivos</option>
        </select>
        <button 
          @click="limparFiltros" 
          class="px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors text-sm font-medium"
        >
          Limpar Filtros
        </button>
      </div>
    </div>

    <!-- Tabela -->
    <div class="overflow-x-auto bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
      <table class="min-w-full divide-y divide-slate-200 dark:divide-slate-800">
        <thead class="bg-slate-50 dark:bg-slate-800/50">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-300 uppercase tracking-wider">Nome</th>
            <th class="px-4 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-300 uppercase tracking-wider">Email</th>
            <th class="px-4 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-300 uppercase tracking-wider">Perfis</th>
            <th class="px-4 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-300 uppercase tracking-wider">Estado</th>
            <th class="px-4 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-300 uppercase tracking-wider">Criação</th>
            <th class="px-4 py-3 text-right text-xs font-semibold text-slate-600 dark:text-slate-300 uppercase tracking-wider">Acções</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-200 dark:divide-slate-800 bg-white dark:bg-slate-900">
          <tr v-if="carregando">
            <td colspan="6" class="px-4 py-8 text-center text-slate-400">
              <span class="inline-block animate-spin h-5 w-5 border-2 border-blue-600 border-t-transparent rounded-full"></span>
              <span class="ml-2 text-sm">A carregar...</span>
            </td>
          </tr>
          <tr v-else-if="lista.length === 0">
            <td colspan="6" class="px-4 py-12 text-center text-slate-500 dark:text-slate-400">
              <BootstrapIcon name="people" class="w-10 h-10 mx-auto text-slate-300 dark:text-slate-600 mb-2" />
              <p class="font-medium">Nenhum utilizador encontrado</p>
              <p class="text-xs mt-1">Ajuste os filtros ou crie um novo utilizador.</p>
            </td>
          </tr>
          <tr v-for="user in lista" :key="user.id" class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
            <td class="px-4 py-3 text-sm font-medium text-slate-900 dark:text-white">{{ user.nome_completo || user.email }}</td>
            <td class="px-4 py-3 text-sm text-slate-600 dark:text-slate-300">{{ user.email }}</td>
            <td class="px-4 py-3">
              <div class="flex flex-wrap gap-1">
                <span v-for="perfil in user.perfis_nomes" :key="perfil"
                      class="inline-block px-2.5 py-0.5 rounded-md text-xs font-medium border bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-900/20 dark:text-blue-400 dark:border-blue-800/30">
                  {{ perfil }}
                </span>
              </div>
            </td>
            <td class="px-4 py-3">
              <span :class="user.is_active 
                ? 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30' 
                : 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-slate-800 dark:text-slate-400 dark:border-slate-700'"
                class="inline-block px-2.5 py-0.5 rounded-md text-xs font-medium border">
                {{ user.is_active ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td class="px-4 py-3 text-sm text-slate-600 dark:text-slate-300">
              {{ formatDate(user.date_joined) }}
            </td>
            <td class="px-4 py-3 text-right">
              <div class="flex justify-end gap-1">
                <button @click="editar(user)" class="p-2 rounded-lg text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors" title="Editar">
                  <BootstrapIcon name="pencil-square" class="w-4 h-4" />
                </button>
                <button @click="toggleAtivo(user)" class="p-2 rounded-lg text-slate-400 hover:text-amber-600 dark:hover:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-900/20 transition-colors" :title="user.is_active ? 'Desactivar' : 'Activar'">
                  <BootstrapIcon :name="user.is_active ? 'person-x' : 'person-check-fill'" class="w-4 h-4" />
                </button>
                <button @click="resetarSenha(user)" class="p-2 rounded-lg text-slate-400 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-900/20 transition-colors" title="Redefinir senha">
                  <BootstrapIcon name="key" class="w-4 h-4" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Paginação -->
    <div class="mt-4 flex flex-col sm:flex-row justify-between items-center gap-3">
      <p class="text-sm text-slate-500 dark:text-slate-400">
        Mostrando <span class="font-medium">{{ (pagina-1)*limite+1 }}</span> a <span class="font-medium">{{ Math.min(pagina*limite, total) }}</span> de <span class="font-medium">{{ total }}</span>
      </p>
      <div class="flex gap-2">
        <button 
          @click="pagina--" 
          :disabled="pagina === 1" 
          class="px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Anterior
        </button>
        <button 
          @click="pagina++" 
          :disabled="pagina * limite >= total" 
          class="px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Próxima
        </button>
      </div>
    </div>

    <!-- Modal de Edição -->
    <Teleport to="body">
      <div v-if="modalEdicao" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50" @click.self="fecharModal">
        <div class="bg-white dark:bg-slate-900 rounded-xl max-w-md w-full p-6 shadow-xl border border-slate-200 dark:border-slate-800">
          <h2 class="text-lg font-semibold text-slate-900 dark:text-white mb-4 border-b border-slate-100 dark:border-slate-800 pb-3 flex items-center gap-2">
            <BootstrapIcon name="pencil-square" class="w-5 h-5 text-slate-400" />
            Editar Utilizador
          </h2>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Nome</label>
              <input v-model="editForm.first_name" class="w-full px-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors" placeholder="Primeiro nome" />
              <input v-model="editForm.last_name" class="w-full px-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors mt-2" placeholder="Último nome" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Perfis</label>
              <div class="flex flex-wrap gap-2">
                <label v-for="perfil in perfisDisponiveis" :key="perfil" class="cursor-pointer">
                  <input type="checkbox" v-model="editForm.perfis_nomes" :value="perfil" class="peer sr-only" />
                  <div class="px-4 py-2 rounded-lg text-sm font-medium border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 peer-checked:border-blue-500 peer-checked:bg-blue-50 peer-checked:text-blue-600 dark:peer-checked:bg-blue-900/20 dark:peer-checked:text-blue-400 transition-all">
                    {{ perfil }}
                  </div>
                </label>
              </div>
            </div>
          </div>
          <div class="flex justify-end gap-3 mt-6 pt-3 border-t border-slate-100 dark:border-slate-800">
            <button @click="fecharModal" class="px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
              Cancelar
            </button>
            <button @click="salvarEdicao" :disabled="salvando" class="px-5 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-2">
              <span v-if="salvando" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
              {{ salvando ? 'A salvar...' : 'Salvar' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'

const { api } = useApi()

const perfisDisponiveis = ['Gestor', 'Financeiro', 'Disciplinar', 'Suporte']

const lista = ref<any[]>([])
const total = ref(0)
const pagina = ref(1)
const limite = ref(10)
const carregando = ref(false)

const filtros = reactive({
  search: '',
  perfil: '',
  ativo: '',
})

const modalEdicao = ref(false)
const editForm = reactive({
  id: null as number | null,
  first_name: '',
  last_name: '',
  perfis_nomes: [] as string[],
})
const salvando = ref(false)

async function buscar() {
  carregando.value = true
  try {
    const params: any = {
      page: pagina.value,
      page_size: limite.value,
      search: filtros.search || undefined,
      perfis__nome_perfil: filtros.perfil || undefined,
      is_active: filtros.ativo !== '' ? filtros.ativo === 'true' : undefined,
    }
    const resp = await api('/admin/utilizadores/', { params }) as { results: any[]; count: number }
    lista.value = resp.results || []
    total.value = resp.count || 0
  } catch (err) {
    console.error(err)
  } finally {
    carregando.value = false
  }
}

function limparFiltros() {
  filtros.search = ''
  filtros.perfil = ''
  filtros.ativo = ''
  pagina.value = 1
  buscar()
}

function editar(user: any) {
  editForm.id = user.id
  editForm.first_name = user.first_name || ''
  editForm.last_name = user.last_name || ''
  editForm.perfis_nomes = [...user.perfis_nomes]
  modalEdicao.value = true
}

async function salvarEdicao() {
  if (editForm.id === null) return
  salvando.value = true
  try {
    await api(`/admin/utilizadores/${editForm.id}/`, {
      method: 'PATCH',
      body: {
        first_name: editForm.first_name,
        last_name: editForm.last_name,
        perfis_nomes: editForm.perfis_nomes,
      }
    })
    fecharModal()
    await buscar()
  } catch (err) {
    alert('Erro ao atualizar utilizador')
  } finally {
    salvando.value = false
  }
}

function fecharModal() {
  modalEdicao.value = false
}

async function toggleAtivo(user: any) {
  if (!confirm(`Tem certeza que deseja ${user.is_active ? 'desactivar' : 'activar'} ${user.nome_completo || user.email}?`)) return
  try {
    await api(`/admin/utilizadores/${user.id}/toggle-active/`, { method: 'PATCH' })
    await buscar()
  } catch (err) {
    alert('Erro ao alterar estado')
  }
}

async function resetarSenha(user: any) {
  if (!confirm(`Enviar link de redefinição de senha para ${user.email}?`)) return
  try {
    await api('/auth/password-reset/', { method: 'POST', body: { email: user.email } })
    alert(`Link de redefinição enviado para ${user.email}`)
  } catch (err) {
    alert('Erro ao enviar email de redefinição')
  }
}

const formatDate = (date: string) => new Date(date).toLocaleDateString('pt-PT')

watch([pagina, () => filtros.search, () => filtros.perfil, () => filtros.ativo], buscar)

onMounted(buscar)
</script>

<style scoped>
/* Estilos vazios - o Tailwind já trata tudo */
</style>
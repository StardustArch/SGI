// composables/useAuth.ts
export const useAuth = () => {
  // Estado global do utilizador
  const user = useState<any | null>('auth_user', () => null)

  const refreshToken = useCookie<string | null>('auth_refresh_token', {
    maxAge: 60 * 60 * 24 * 7,
    httpOnly: false,
    secure: process.env.NODE_ENV === 'production',
    default: () => null,
  })

  const accessToken = useCookie<string | null>('auth_access_token', {
    maxAge: 60 * 15,
    httpOnly: false,
    secure: process.env.NODE_ENV === 'production',
    default: () => null,
  })

  const isLoggedIn = computed(() => !!accessToken.value)

  // 1. Função de busca usando $fetch direto para evitar dependência circular
  async function fetchUser() {
    if (!accessToken.value) return
    
    try {
      const data = await $fetch<any>('/api/v1/users/me/', {
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        }
      })
      user.value = data
    } catch (err) {
      console.error('Erro ao carregar perfil:', err)
      // Se der erro de auth no perfil, limpamos tudo
      if ((err as any).response?.status === 401) clearTokens()
    }
  }

  function setTokens(access: string, refresh: string) {
    accessToken.value = access
    refreshToken.value = refresh
    fetchUser() // Busca o perfil assim que logar
  }

  function clearTokens() {
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    if (process.client) {
      window.location.href = '/'
    }
  }

  return { 
    accessToken, 
    refreshToken, 
    user, 
    isLoggedIn, 
    setTokens, 
    clearTokens, 
    fetchUser 
  }
}
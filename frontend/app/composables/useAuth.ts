// composables/useAuth.ts
export const useAuth = () => {
  const refreshToken = useCookie<string | null>('auth_refresh_token', {
    maxAge: 60 * 60 * 24 * 7, // 7 dias
    httpOnly: false, // ❗ tem de ser false para o cliente ler e atualizar
    secure: process.env.NODE_ENV === 'production',
    default: () => null,
  })

  const accessToken = useCookie<string | null>('auth_access_token', {
    maxAge: 60 * 15, // 15 minutos
    httpOnly: false, // ❗ também false, pois o cliente precisa ler
    secure: process.env.NODE_ENV === 'production',
    default: () => null,
  })

  const isLoggedIn = computed(() => !!accessToken.value)

  function setTokens(access: string, refresh: string) {
    console.log('🔐 Salvando tokens...', { access, refresh }) // <-- debug
    accessToken.value = access
    refreshToken.value = refresh
  }

  function clearTokens() {
    console.log('🚪 Limpando tokens...')
    accessToken.value = null
    refreshToken.value = null
  }

  return { accessToken, refreshToken, isLoggedIn, setTokens, clearTokens }
}

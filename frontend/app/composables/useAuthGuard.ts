import { useAuth } from '~/composables/useAuth'
import { useRouter } from '#app'

export const useAuthGuard = () => {
  const { isLoggedIn } = useAuth()
  const router = useRouter()

  // Chame isso no setup() de páginas privadas
  const guard = () => {
    if (!isLoggedIn.value) {
      router.replace('/login')
    }
  }

  return { guard }
}

// composables/useApi.ts
import { useAuth } from '~/composables/useAuth'

export const useApi = () => {
    const { accessToken, refreshToken, setTokens, clearTokens } = useAuth()
    const router = useRouter()

    async function api<T>(url: string, options: any = {}): Promise<T> {
        // 🔹 1. Adiciona token de acesso (se existir)
        options.headers = {
            ...(options.headers || {}),
            Authorization: accessToken.value ? `Bearer ${accessToken.value}` : undefined,
        }

        try {
            const data = await $fetch<T>(`/api/v1${url}`, options)
            console.log(data)
            return data;
        } catch (error: any) {
            // 🔹 2. Detecta token expirado
            if (error?.response?.status === 401 && refreshToken.value) {
                console.warn('Access token expirou, tentando refresh...')

                try {
                    // 🔹 3. Faz refresh
                    const data = await $fetch<{ access: string; refresh: string }>(
                        '/api/v1/token/refresh/',
                        {
                            method: 'POST',
                            body: { refresh: refreshToken.value },
                        }
                    )

                    if (!data.access) {
                        throw new Error('Refresh falhou — sem access token no retorno.')
                    }

                    console.info('Refresh bem-sucedido! Atualizando tokens...')
                    setTokens(data.access, data.refresh ?? refreshToken.value)

                    // 🔹 4. Refaz o pedido original com o novo token
                    options.headers.Authorization = `Bearer ${data.access}`
                    return await $fetch<T>(`/api/v1${url}`, options)
                } catch (refreshError) {
                    console.error('Falha no refresh token:', refreshError)
                    clearTokens()
                    await router.push('/')
                    throw refreshError
                }
            }

            // 🔹 5. Qualquer outro erro
            throw error
        }
    }

    return { api }
}

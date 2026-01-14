<template>
  <!-- 
    Este é o layout 'avô'.
    Agora ele só fornece o fundo e o <slot />.
    Toda a navegação (navbar/sidebar) foi movida para o 'dashboard.vue'
    para permitir um design 100% responsivo.
  -->
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <slot />
  </div>
</template>
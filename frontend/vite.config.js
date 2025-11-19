import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,        // permet d'utiliser describe, it, expect directement
    environment: 'jsdom', // simule un navigateur
    include: ['tests/**/*.spec.js'], // chemins vers tes tests
  },
})

import { defineConfig } from 'vite';

const { resolve } = require('path');

export default defineConfig({
  plugins: [],
  root: resolve('./static/src'),
  base: '/static/',
  server: {
    host: 'localhost',
    port: 3000,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  resolve: {
    extensions: ['.mjs', '.js', '.mts', '.ts', '.jsx', '.tsx', '.json'], // default
  },
  build: {
    outDir: resolve('./assets/bundles/'),
    assetsDir: '',
    manifest: true,
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve('./assets/ts/index.ts'),
      },
      output: {
        chunkFileNames: undefined,
      },
    },
  },
})

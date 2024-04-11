import { defineConfig } from 'vite';
import { resolve } from 'path';
import react from '@vitejs/plugin-react';

// eslint-disable-next-line import/no-default-export
export default defineConfig({
  plugins: [react()],
  root: resolve('./assets/ts/'),
  base: '/static/',
  server: {
    host: '127.0.0.1',
    port: 3000,
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
        status: resolve('./assets/ts/status.ts'),
      },
    },
  },
});

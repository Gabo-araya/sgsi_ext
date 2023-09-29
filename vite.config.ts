import { defineConfig } from 'vite';
import { resolve } from 'path';
import react from '@vitejs/plugin-react';

// eslint-disable-next-line import/no-default-export
export default defineConfig({
  plugins: [
    react(),
  ],
  root: resolve('./assets/ts/'),
  base: '/static/',
  server: {
    host: 'localhost',
    port: 3000,

    /////////TODO: enable on WSL?
    // see warning in https://vitejs.dev/config/server-options.html#server-watch
    //watch: { usePolling: true },
    // alternative: CHOKIDAR_USEPOLLING env var
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

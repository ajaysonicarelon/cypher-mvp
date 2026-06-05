import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    lib: {
      entry: 'src/cypher-widget.js',
      name: 'CypherWidget',
      fileName: (format) => `cypher-widget.${format}.js`,
      formats: ['umd', 'es']
    },
    rollupOptions: {
      output: {
        globals: {
          // No external dependencies - everything is bundled
        }
      }
    },
    minify: 'terser',
    sourcemap: true
  },
  server: {
    port: 3001,
    open: false
  }
});

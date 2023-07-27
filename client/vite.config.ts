import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import Icons from "unplugin-icons/vite";
import IconsResolver from "unplugin-icons/resolver";
import Components from "unplugin-vue-components/vite";

import * as child_process from "child_process";

const commitHash = child_process
  .execSync("git rev-parse --short HEAD")
  .toString();
const commitTime = child_process
  .execSync("git show -s --format=%ci")
  .toString();
const commitDirty =
  child_process.execSync("git diff --stat").toString().length > 0;

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    Icons({}),
    Components({ dts: true, resolvers: [IconsResolver()] }),
  ],
  define: {
    __COMMIT_HASH__: JSON.stringify(commitHash),
    __COMMIT_TIME__: JSON.stringify(commitTime),
    __COMMIT_DIRTY__: commitDirty,
  },
  base: "/",
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
        ws: true,
      },
    },
  },
});

// vite.config.ts
import path from "path";
import { defineConfig } from "file:///C:/Users/LENOVO/Desktop/SEwork/BUPT-2023-SE-Homework/frontend/node_modules/.pnpm/vite@5.0.5_sass@1.69.5/node_modules/vite/dist/node/index.js";
import Vue from "file:///C:/Users/LENOVO/Desktop/SEwork/BUPT-2023-SE-Homework/frontend/node_modules/.pnpm/@vitejs+plugin-vue@4.5.1_vite@5.0.5_vue@3.3.10/node_modules/@vitejs/plugin-vue/dist/index.mjs";
import Icons from "file:///C:/Users/LENOVO/Desktop/SEwork/BUPT-2023-SE-Homework/frontend/node_modules/.pnpm/unplugin-icons@0.17.4/node_modules/unplugin-icons/dist/vite.mjs";
import IconsResolver from "file:///C:/Users/LENOVO/Desktop/SEwork/BUPT-2023-SE-Homework/frontend/node_modules/.pnpm/unplugin-icons@0.17.4/node_modules/unplugin-icons/dist/resolver.mjs";
import AutoImport from "file:///C:/Users/LENOVO/Desktop/SEwork/BUPT-2023-SE-Homework/frontend/node_modules/.pnpm/unplugin-auto-import@0.16.7/node_modules/unplugin-auto-import/dist/vite.js";
import Components from "file:///C:/Users/LENOVO/Desktop/SEwork/BUPT-2023-SE-Homework/frontend/node_modules/.pnpm/unplugin-vue-components@0.25.2_vue@3.3.10/node_modules/unplugin-vue-components/dist/vite.mjs";
import { ElementPlusResolver } from "file:///C:/Users/LENOVO/Desktop/SEwork/BUPT-2023-SE-Homework/frontend/node_modules/.pnpm/unplugin-vue-components@0.25.2_vue@3.3.10/node_modules/unplugin-vue-components/dist/resolvers.mjs";
import Inspect from "file:///C:/Users/LENOVO/Desktop/SEwork/BUPT-2023-SE-Homework/frontend/node_modules/.pnpm/vite-plugin-inspect@0.7.42_vite@5.0.5/node_modules/vite-plugin-inspect/dist/index.mjs";
var __vite_injected_original_dirname = "C:\\Users\\LENOVO\\Desktop\\SEwork\\BUPT-2023-SE-Homework\\frontend";
var pathSrc = path.resolve(__vite_injected_original_dirname, "src");
var vite_config_default = defineConfig({
  resolve: {
    alias: {
      "@": pathSrc
    }
  },
  plugins: [
    Vue(),
    AutoImport({
      // Auto import functions from Vue, e.g. ref, reactive, toRef...
      // 自动导入 Vue 相关函数，如：ref, reactive, toRef 等
      imports: ["vue"],
      // Auto import functions from Element Plus, e.g. ElMessage, ElMessageBox... (with style)
      // 自动导入 Element Plus 相关函数，如：ElMessage, ElMessageBox... (带样式)
      resolvers: [ElementPlusResolver()],
      dts: path.resolve(pathSrc, "auto-imports.d.ts")
    }),
    Components({
      resolvers: [
        // Auto register icon components
        // 自动注册图标组件
        IconsResolver({
          enabledCollections: ["ep"]
        }),
        // Auto register Element Plus components
        // 自动导入 Element Plus 组件
        ElementPlusResolver()
      ],
      dts: path.resolve(pathSrc, "components.d.ts")
    }),
    Icons({
      autoInstall: true
    }),
    Inspect()
  ]
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCJDOlxcXFxVc2Vyc1xcXFxMRU5PVk9cXFxcRGVza3RvcFxcXFxTRXdvcmtcXFxcQlVQVC0yMDIzLVNFLUhvbWV3b3JrXFxcXGZyb250ZW5kXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCJDOlxcXFxVc2Vyc1xcXFxMRU5PVk9cXFxcRGVza3RvcFxcXFxTRXdvcmtcXFxcQlVQVC0yMDIzLVNFLUhvbWV3b3JrXFxcXGZyb250ZW5kXFxcXHZpdGUuY29uZmlnLnRzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9DOi9Vc2Vycy9MRU5PVk8vRGVza3RvcC9TRXdvcmsvQlVQVC0yMDIzLVNFLUhvbWV3b3JrL2Zyb250ZW5kL3ZpdGUuY29uZmlnLnRzXCI7aW1wb3J0IHBhdGggZnJvbSBcInBhdGhcIjtcclxuaW1wb3J0IHsgZGVmaW5lQ29uZmlnIH0gZnJvbSBcInZpdGVcIjtcclxuaW1wb3J0IFZ1ZSBmcm9tIFwiQHZpdGVqcy9wbHVnaW4tdnVlXCI7XHJcbmltcG9ydCBJY29ucyBmcm9tIFwidW5wbHVnaW4taWNvbnMvdml0ZVwiO1xyXG5pbXBvcnQgSWNvbnNSZXNvbHZlciBmcm9tIFwidW5wbHVnaW4taWNvbnMvcmVzb2x2ZXJcIjtcclxuaW1wb3J0IEF1dG9JbXBvcnQgZnJvbSBcInVucGx1Z2luLWF1dG8taW1wb3J0L3ZpdGVcIjtcclxuaW1wb3J0IENvbXBvbmVudHMgZnJvbSBcInVucGx1Z2luLXZ1ZS1jb21wb25lbnRzL3ZpdGVcIjtcclxuaW1wb3J0IHsgRWxlbWVudFBsdXNSZXNvbHZlciB9IGZyb20gXCJ1bnBsdWdpbi12dWUtY29tcG9uZW50cy9yZXNvbHZlcnNcIjtcclxuaW1wb3J0IEluc3BlY3QgZnJvbSBcInZpdGUtcGx1Z2luLWluc3BlY3RcIjtcclxuXHJcbi8vQHRzLWlnbm9yZVxyXG5jb25zdCBwYXRoU3JjID0gcGF0aC5yZXNvbHZlKF9fZGlybmFtZSwgXCJzcmNcIik7XHJcblxyXG5leHBvcnQgZGVmYXVsdCBkZWZpbmVDb25maWcoe1xyXG4gICAgcmVzb2x2ZToge1xyXG4gICAgICAgIGFsaWFzOiB7XHJcbiAgICAgICAgICAgIFwiQFwiOiBwYXRoU3JjXHJcbiAgICAgICAgfVxyXG4gICAgfSxcclxuICAgIHBsdWdpbnM6IFtcclxuICAgICAgICBWdWUoKSxcclxuICAgICAgICBBdXRvSW1wb3J0KHtcclxuICAgICAgICAgICAgLy8gQXV0byBpbXBvcnQgZnVuY3Rpb25zIGZyb20gVnVlLCBlLmcuIHJlZiwgcmVhY3RpdmUsIHRvUmVmLi4uXHJcbiAgICAgICAgICAgIC8vIFx1ODFFQVx1NTJBOFx1NUJGQ1x1NTE2NSBWdWUgXHU3NkY4XHU1MTczXHU1MUZEXHU2NTcwXHVGRjBDXHU1OTgyXHVGRjFBcmVmLCByZWFjdGl2ZSwgdG9SZWYgXHU3QjQ5XHJcbiAgICAgICAgICAgIGltcG9ydHM6IFtcInZ1ZVwiXSxcclxuXHJcbiAgICAgICAgICAgIC8vIEF1dG8gaW1wb3J0IGZ1bmN0aW9ucyBmcm9tIEVsZW1lbnQgUGx1cywgZS5nLiBFbE1lc3NhZ2UsIEVsTWVzc2FnZUJveC4uLiAod2l0aCBzdHlsZSlcclxuICAgICAgICAgICAgLy8gXHU4MUVBXHU1MkE4XHU1QkZDXHU1MTY1IEVsZW1lbnQgUGx1cyBcdTc2RjhcdTUxNzNcdTUxRkRcdTY1NzBcdUZGMENcdTU5ODJcdUZGMUFFbE1lc3NhZ2UsIEVsTWVzc2FnZUJveC4uLiAoXHU1RTI2XHU2ODM3XHU1RjBGKVxyXG4gICAgICAgICAgICByZXNvbHZlcnM6IFtFbGVtZW50UGx1c1Jlc29sdmVyKCldLFxyXG5cclxuICAgICAgICAgICAgZHRzOiBwYXRoLnJlc29sdmUocGF0aFNyYywgXCJhdXRvLWltcG9ydHMuZC50c1wiKVxyXG4gICAgICAgIH0pLFxyXG5cclxuICAgICAgICBDb21wb25lbnRzKHtcclxuICAgICAgICAgICAgcmVzb2x2ZXJzOiBbXHJcbiAgICAgICAgICAgICAgICAvLyBBdXRvIHJlZ2lzdGVyIGljb24gY29tcG9uZW50c1xyXG4gICAgICAgICAgICAgICAgLy8gXHU4MUVBXHU1MkE4XHU2Q0U4XHU1MThDXHU1NkZFXHU2ODA3XHU3RUM0XHU0RUY2XHJcbiAgICAgICAgICAgICAgICBJY29uc1Jlc29sdmVyKHtcclxuICAgICAgICAgICAgICAgICAgICBlbmFibGVkQ29sbGVjdGlvbnM6IFtcImVwXCJdXHJcbiAgICAgICAgICAgICAgICB9KSxcclxuICAgICAgICAgICAgICAgIC8vIEF1dG8gcmVnaXN0ZXIgRWxlbWVudCBQbHVzIGNvbXBvbmVudHNcclxuICAgICAgICAgICAgICAgIC8vIFx1ODFFQVx1NTJBOFx1NUJGQ1x1NTE2NSBFbGVtZW50IFBsdXMgXHU3RUM0XHU0RUY2XHJcbiAgICAgICAgICAgICAgICBFbGVtZW50UGx1c1Jlc29sdmVyKClcclxuICAgICAgICAgICAgXSxcclxuXHJcbiAgICAgICAgICAgIGR0czogcGF0aC5yZXNvbHZlKHBhdGhTcmMsIFwiY29tcG9uZW50cy5kLnRzXCIpXHJcbiAgICAgICAgfSksXHJcblxyXG4gICAgICAgIEljb25zKHtcclxuICAgICAgICAgICAgYXV0b0luc3RhbGw6IHRydWVcclxuICAgICAgICB9KSxcclxuXHJcbiAgICAgICAgSW5zcGVjdCgpXHJcbiAgICBdXHJcbn0pO1xyXG4iXSwKICAibWFwcGluZ3MiOiAiO0FBQXVYLE9BQU8sVUFBVTtBQUN4WSxTQUFTLG9CQUFvQjtBQUM3QixPQUFPLFNBQVM7QUFDaEIsT0FBTyxXQUFXO0FBQ2xCLE9BQU8sbUJBQW1CO0FBQzFCLE9BQU8sZ0JBQWdCO0FBQ3ZCLE9BQU8sZ0JBQWdCO0FBQ3ZCLFNBQVMsMkJBQTJCO0FBQ3BDLE9BQU8sYUFBYTtBQVJwQixJQUFNLG1DQUFtQztBQVd6QyxJQUFNLFVBQVUsS0FBSyxRQUFRLGtDQUFXLEtBQUs7QUFFN0MsSUFBTyxzQkFBUSxhQUFhO0FBQUEsRUFDeEIsU0FBUztBQUFBLElBQ0wsT0FBTztBQUFBLE1BQ0gsS0FBSztBQUFBLElBQ1Q7QUFBQSxFQUNKO0FBQUEsRUFDQSxTQUFTO0FBQUEsSUFDTCxJQUFJO0FBQUEsSUFDSixXQUFXO0FBQUE7QUFBQTtBQUFBLE1BR1AsU0FBUyxDQUFDLEtBQUs7QUFBQTtBQUFBO0FBQUEsTUFJZixXQUFXLENBQUMsb0JBQW9CLENBQUM7QUFBQSxNQUVqQyxLQUFLLEtBQUssUUFBUSxTQUFTLG1CQUFtQjtBQUFBLElBQ2xELENBQUM7QUFBQSxJQUVELFdBQVc7QUFBQSxNQUNQLFdBQVc7QUFBQTtBQUFBO0FBQUEsUUFHUCxjQUFjO0FBQUEsVUFDVixvQkFBb0IsQ0FBQyxJQUFJO0FBQUEsUUFDN0IsQ0FBQztBQUFBO0FBQUE7QUFBQSxRQUdELG9CQUFvQjtBQUFBLE1BQ3hCO0FBQUEsTUFFQSxLQUFLLEtBQUssUUFBUSxTQUFTLGlCQUFpQjtBQUFBLElBQ2hELENBQUM7QUFBQSxJQUVELE1BQU07QUFBQSxNQUNGLGFBQWE7QUFBQSxJQUNqQixDQUFDO0FBQUEsSUFFRCxRQUFRO0FBQUEsRUFDWjtBQUNKLENBQUM7IiwKICAibmFtZXMiOiBbXQp9Cg==

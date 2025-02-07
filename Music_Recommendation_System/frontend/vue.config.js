const { defineConfig } = require("@vue/cli-service");
const path = require("path");
const webpack = require("webpack");

module.exports = defineConfig({
  publicPath: "/",
  outputDir: "dist",

  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },

  assetsDir: "assets",

  configureWebpack: {
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src"),
        fecha: path.resolve(__dirname, "node_modules/fecha"),
      },
      fallback: {
        util: require.resolve("util/"),
        os: require.resolve("os-browserify/browser"),
        events: require.resolve("events/"),
        fs: false, // ✅ Ensure fs is not included
        path: require.resolve("path-browserify"),
        zlib: require.resolve("browserify-zlib"),
        http: require.resolve("stream-http"),
        https: require.resolve("https-browserify"),
        assert: require.resolve("assert/"),
        stream: require.resolve("stream-browserify"),
        url: require.resolve("url/"),
        process: require.resolve("process/browser"), // ✅ Fix for "process is not defined"
      },
      modules: [path.resolve(__dirname, "node_modules"), "node_modules"],
    },
    plugins: [
      new webpack.ProvidePlugin({
        process: "process/browser", // ✅ Ensures `process` is available globally
      }),
    ],
    externals: {
      fs: "commonjs2 fs", // ✅ Explicitly exclude `fs` module
    },
  },

  chainWebpack: (config) => {
    config.plugin("define").tap((args) => {
      args[0]["process.env"] = JSON.stringify(process.env || {});
      return args;
    });
  },

  transpileDependencies: true,
});

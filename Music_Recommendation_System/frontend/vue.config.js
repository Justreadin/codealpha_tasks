// vue.config.js
const path = require("path");

module.exports = {
  // Change the base URL for the app
  publicPath: process.env.NODE_ENV === "production" ? "/my-app/" : "/",

  // Specify where the built files will be output
  outputDir: "dist",

  // Enable or configure a development server proxy for API calls
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },

  // Configure assets directory
  assetsDir: "assets",

  // Configure alias for easier imports
  configureWebpack: {
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src"),
      },
      fallback: {
        util: require.resolve("util/"),
        os: require.resolve("os-browserify/browser"),
        events: require.resolve("events/"),
        fs: false, // Avoid including file system in the browser
        path: require.resolve("path-browserify"),
        zlib: require.resolve("browserify-zlib"),
        http: require.resolve("stream-http"),
        https: require.resolve("https-browserify"),
      },
    },
  },

  transpileDependencies: true,
};

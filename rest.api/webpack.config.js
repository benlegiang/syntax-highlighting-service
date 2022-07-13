const path = require('path');
module.exports = {
 entry: './src/main.ts',
 resolve: {
   extensions: ['.webpack.js', '.web.js', '.ts', '.js'],
   fallback: {
    "url": require.resolve("url/"),
    "path": require.resolve("path-browserify"),
    "util": require.resolve("util/"),
    "stream": require.resolve("stream-browserify"),
    "buffer": require.resolve("buffer/"),
    "http": require.resolve("stream-http"),
    "crypto": require.resolve("crypto-browserify"),
    "zlib": require.resolve("browserify-zlib"),
    "assert": require.resolve("assert/"),
    "net": require.resolve("net"),
    "fs": require.resolve("fs"),
   }
 },
 module: {
   rules: [
     { test: /\.ts$/, loader: 'ts-loader' }
   ]
 },
 output: {
   filename: 'main.js',
   path: path.resolve(__dirname, 'dist')
 }
}
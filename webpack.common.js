/* eslint-disable import/no-extraneous-dependencies */
const path = require('path');

// Packages
const webpack = require('webpack');

// Plugins
const BundleTracker = require('webpack-bundle-tracker');
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

// Config
module.exports = {
  context: __dirname,

  entry: {
    main: './assets/ts/index.ts',
    status: './assets/ts/status.ts',
  },

  output: {
    path: path.resolve('./assets/bundles/'),
  },

  plugins: [
    new BundleTracker({
      filename: './webpack-stats.json',
    }),
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      openAnalyzer: false,
    }),
    // Note: this causes the dev server to print some errors
    // (Error parsing bundle asset "...": no such file)
    // but the html report is generated anyway.
    // https://github.com/webpack-contrib/webpack-bundle-analyzer/blob/c93fd2b/README.md#i-dont-see-gzip-or-parsed-sizes-it-only-shows-stat-size
  ],

  module: {
    rules: [
      {
        test: /\.m?js$/,
        include: path.resolve('./assets/js'),
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          },
        },
      },
      {
        test: /.(jpg|png|woff(2)?|eot|ttf|svg)$/,
        exclude: /node_modules/,
        use: {
          loader: 'file-loader',
        },
      },
    ],
  },

  resolve: {
    modules: ['./node_modules'],
    extensions: ['*', '.tsx', '.ts', '.js'],
  },
};

var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var path = require('path');

module.exports = {
    entry: './app/static/index.js',

    output: {
        path: path.resolve('./static/bundles/'),
        filename: "[name]-[hash].js"
    },

    module: {
        loaders: [
            { test: /\.scss$/, loader: ExtractTextPlugin.extract('style', 'css!sass') }
        ]
    },

    plugins: [
        new ExtractTextPlugin('[name]-[hash].css'),
        new BundleTracker({filename: './webpack-stats.json'})
    ]
};
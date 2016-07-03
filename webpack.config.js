var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var path = require('path');

module.exports = {
    entry: './app/static/index.js',

    output: {
        path: path.resolve('./dist'),
        filename: "bundle.js"
    },

    module: {
        loaders: [
            { test: /\.scss$/, loader: ExtractTextPlugin.extract('style', 'css!resolve-url!sass?sourceMap') },
            { test: /\.png$/, loader: 'url?limit=10000' },
        ]
    },

    plugins: [
        new ExtractTextPlugin('bundle.css'),
    ]
};
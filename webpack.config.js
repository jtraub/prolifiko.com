var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var path = require('path');

module.exports = {
    entry: './app/static/index.js',

    output: {
        path: path.resolve('./dist/'),
        filename: "bundle.js"
    },

    module: {
        loaders: [
            { test: /\.scss$/, loader: ExtractTextPlugin.extract('style', 'css!sass') }
        ]
    },

    plugins: [
        new ExtractTextPlugin('bundle.css'),
    ]
};
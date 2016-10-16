var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var CopyWebpackPlugin = require('copy-webpack-plugin');
var path = require('path');

module.exports = {
    entry: {
        bundle: './app/static/index.js',
        'create-goal': './app/static/create-goal.js',
        'create-five-day-challenge': './app/static/create-five-day-challenge.js',
        'create-midnight-step': './app/static/create-midnight-step.js',
        'create-step': './app/static/create-step.js',
    },

    output: {
        path: path.resolve('./dist'),
        filename: '[name].js'
    },

    resolve: { alias: { moment: 'moment/moment.js' } },

    module: {
        loaders: [
            { test: /\.js$/, loader: 'babel' },
            { test: /\.scss$/, loader: ExtractTextPlugin.extract('style', 'css!resolve-url!sass?sourceMap') },
            { test: /\.png$/, loader: 'url?limit=10000' },
        ]
    },

    devtool: 'source-map',

    plugins: [
        new ExtractTextPlugin('bundle.css'),
        new CopyWebpackPlugin([
            { from: path.resolve('./node_modules/moment-timezone/builds/moment-timezone-with-data-2010-2020.min.js'), to: 'moment-timezone.min.js' },
            { from: path.resolve('./node_modules/moment/min/moment.min.js'), to: 'moment.min.js' }
        ])
    ]
};

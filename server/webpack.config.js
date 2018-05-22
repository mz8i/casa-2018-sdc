var webpack = require('webpack');
var VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
    entry: ['./client-src/index.js'],
    output: {
        path: __dirname + '/public/scripts',
        filename: 'bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader'
                }
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.css$/,
                use: [
                    'vue-style-loader',
                    'css-loader'
                ]
            }
        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
            mapboxgl: 'mapbox-gl'
        }),
        new VueLoaderPlugin(),
        new webpack.NamedModulesPlugin()
    ],
    stats: {
        colors: true
    },
    devtool: 'source-map'
};

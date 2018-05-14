let webpack = require('webpack');

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
            }
        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
            mapboxgl: 'mapbox-gl'
        })
    ],
    stats: {
        colors: true
    },
    devtool: 'source-map'
};

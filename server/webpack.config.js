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
                exclude: /node-modules/,
                use: {
                    loader: 'babel-loader'
                }
            }
        ]
    },
    stats: {
        colors: true
    },
    devtool: 'source-map'
};

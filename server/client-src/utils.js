let chicagoCenter = [-87.6297982, 41.8781136];

function getApi(url){
    return fetch(url)
        .then(res => res.json());
}

function clamp(num, min, max) {
    return (min && num <= min) ? min : (max && num >= max) ? max : num;
}

function hexToRgb(hex) {
    var c;
    if (/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)) {
        c = hex.substring(1).split('');
        if (c.length == 3) {
            c = [c[0], c[0], c[1], c[1], c[2], c[2]];
        }
        c = '0x' + c.join('');  
        return [(c >> 16) & 255, (c >> 8) & 255, c & 255, ];
    }
    throw new Error('Bad Hex');
}

function hexToDeckColor(hex){
    return [...hexToRgb(hex), 255];
}

function getStyle() {
    return getApi('/api/style')
        .then(data => {
            let styles = {};
            for(let s of data){
                styles[s.name] = s.value;
            }
            return styles;
        });
}

export { 
    chicagoCenter,
    getApi,
    clamp,
    hexToDeckColor,
    getStyle
};
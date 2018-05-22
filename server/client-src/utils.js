let chicagoCenter = [-87.6297982, 41.8781136];

function getApi(url){
    return fetch(url)
        .then(res => res.json());
}

function clamp(num, min, max) {
    return (min && num <= min) ? min : (max && num >= max) ? max : num;
}

export { 
    chicagoCenter,
    getApi,
    clamp
};
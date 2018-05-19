let chicagoCenter = [-87.6297982, 41.8781136];

function getApi(url){
    return fetch(url)
        .then(res => res.json());
}
export { chicagoCenter, getApi};
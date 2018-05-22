import turfTag from '@turf/tag';

function worker(self) {
    self.addEventListener('message', event => {
        let input = event.data;
        let result = turfTag(input[0], input[1], input[2], input[3]);
        self.postMessage(result);
    });
};

export default worker;
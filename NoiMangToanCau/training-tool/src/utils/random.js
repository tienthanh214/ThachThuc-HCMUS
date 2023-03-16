function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

export function genHexValue(min, max) {
    return getRandomInt(min, max).toString(16).toUpperCase()
}

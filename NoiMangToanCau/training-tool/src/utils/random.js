export function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

export function genHexValue(min, max) {
    return getRandomInt(min, max).toString(16).toUpperCase()
}

export function genCharValue(min, max) {
    return String.fromCharCode(getRandomInt(min, max))
}

export function genBinValue(min, max) {
    return getRandomInt(min, max).toString(2).padStart(4, '0')
}
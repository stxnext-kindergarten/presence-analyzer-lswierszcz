/**
 * Returns date object
 *
 * @param int value  Time in seconds counted from midnight
 * @returns Date Date object based on input value
 */
function parseInterval(value) {
    var result = new Date(1, 1, 1);
    result.setMilliseconds(value * 1000);
    return result;
}

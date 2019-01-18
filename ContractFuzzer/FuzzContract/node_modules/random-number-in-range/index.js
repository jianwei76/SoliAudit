module.exports = function randomInRange(min, max) {
  if (!min) min = 0
  if (!max) max = 100
  return Math.floor(Math.random() * (max - min)) + min
}



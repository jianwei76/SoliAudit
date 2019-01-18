module.exports = function (arr, nameLabel, countLabel) {
  var counts = {}
  nameLabel = nameLabel || 'value'
  countLabel = countLabel || 'count'

  arr.forEach(function (value) {
    if (typeof value !== 'string') return
    counts[value] ? counts[value]++ : counts[value] = 1
  })

  return Object.keys(counts)
    .map(function (key) {
      var obj = {}
      obj[nameLabel] = key
      obj[countLabel] = counts[key]
      return obj
    })
    .sort(function (a, b) { return b[countLabel] - a[countLabel] })
}

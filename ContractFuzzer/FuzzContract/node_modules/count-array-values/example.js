var count = require('./')
count(['foo', 'bar', 'Bar', 451, 'bar', 'bar', 'baz', 'foo', null, undefined])

// [
//   {value: 'bar', count: 3},
//   {value: 'foo', count: 2},
//   {value: 'Bar', count: 1},
//   {value: 'baz', count: 1},
// ]

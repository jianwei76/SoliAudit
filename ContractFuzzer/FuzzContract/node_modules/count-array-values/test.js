var test = require('tape')
var countArrayValues = require('./')

test('countArrayValues', function (t) {
  var input = ['foo', 'bar', 'Bar', 451, 'bar', 'bar', 'baz', 'foo', null, undefined]
  var output = [
    {value: 'bar', count: 3},
    {value: 'foo', count: 2},
    {value: 'Bar', count: 1},
    {value: 'baz', count: 1}
  ]
  t.deepEqual(countArrayValues(input), output, 'returns an array of objects, each with a `value` and `count` property, sorted descending by count.')

  input = ['apple', 'banana', 'apple']
  output = [
    {fruit: 'apple', count: 2},
    {fruit: 'banana', count: 1}
  ]
  t.deepEqual(countArrayValues(input, 'fruit'), output, 'allows a custom property to be set for name')

  input = ['banana', 'express', 'lodash', 'express', 'lodash', 'express']
  output = [
    {package: 'express', dependents: 3},
    {package: 'lodash', dependents: 2},
    {package: 'banana', dependents: 1}
  ]
  t.deepEqual(countArrayValues(input, 'package', 'dependents'), output, 'allows a custom property to be set for count')

  t.end()
})

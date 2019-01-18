Object
======
[![NPM version][npm-image]][npm-url] [![Build Status][travis-image]][travis-url] [![Coverage][coveralls-image]][coveralls-url] [![Dependencies][dependencies-image]][dependencies-url]

> Validates if a value is a JavaScript object.



## Installation

``` bash
$ npm install validate.io-object
```

For use in the browser, use [browserify](https://github.com/substack/node-browserify).


## Usage

``` javascript
var isObject = require( 'validate.io-object' );
```


#### isObject( value )

Validates if a `value` is a JavaScript `object`.

``` javascript
var value = {};

var bool = isObject( value );
// returns true
```

__Note__: in this implementation, `arrays` and `null` are __not__ considered valid `objects`.


## Examples

``` javascript
console.log( isObject( {} ) );
// returns true

console.log( isObject( null ) );
// returns false

console.log( isObject( [] ) );
// returns false
```

To run the example code from the top-level application directory,

``` bash
$ node ./examples/index.js
```


## Tests

### Unit

Unit tests use the [Mocha](http://mochajs.org) test framework with [Chai](http://chaijs.com) assertions. To run the tests, execute the following command in the top-level application directory:

``` bash
$ make test
```

All new feature development should have corresponding unit tests to validate correct functionality.


### Test Coverage

This repository uses [Istanbul](https://github.com/gotwarlost/istanbul) as its code coverage tool. To generate a test coverage report, execute the following command in the top-level application directory:

``` bash
$ make test-cov
```

Istanbul creates a `./reports/coverage` directory. To access an HTML version of the report,

``` bash
$ make view-cov
```


---
## License

[MIT license](http://opensource.org/licenses/MIT). 


## Copyright

Copyright &copy; 2014-2015. Athan Reines.



[npm-image]: http://img.shields.io/npm/v/validate.io-object.svg
[npm-url]: https://npmjs.org/package/validate.io-object

[travis-image]: http://img.shields.io/travis/validate-io/object/master.svg
[travis-url]: https://travis-ci.org/validate-io/object

[coveralls-image]: https://img.shields.io/coveralls/validate-io/object/master.svg
[coveralls-url]: https://coveralls.io/r/validate-io/object?branch=master

[dependencies-image]: http://img.shields.io/david/validate-io/object.svg
[dependencies-url]: https://david-dm.org/validate-io/object

[dev-dependencies-image]: http://img.shields.io/david/dev/validate-io/object.svg
[dev-dependencies-url]: https://david-dm.org/dev/validate-io/object

[github-issues-image]: http://img.shields.io/github/issues/validate-io/object.svg
[github-issues-url]: https://github.com/validate-io/object/issues

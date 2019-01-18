Euclidean Distance
===
[![NPM version][npm-image]][npm-url] [![Build Status][travis-image]][travis-url] [![Coverage Status][coveralls-image]][coveralls-url] [![Dependencies][dependencies-image]][dependencies-url]

> Computes the [Euclidean distance](http://en.wikipedia.org/wiki/Euclidean_distance) between two arrays.

The [Euclidean distance](http://en.wikipedia.org/wiki/Euclidean_distance) is the straight line distance between two points in Euclidean space.


<div class="equation" align="center" data-raw-text="d(\mathbf{x},\mathbf{y}) = \left( \sum_{i=0}^{n-1} |x_i - y_i|^2 \right)^{1/2}" data-equation="eq:euclidean_distance">
	<img src="https://cdn.rawgit.com/compute-io/euclidean-distance/c554ead93c215e769cbd78cff43ab97d802d344a/docs/img/eqn.svg" alt="Euclidean distance formula">
	<br>
</div>


## Installation

``` bash
$ npm install compute-euclidean-distance
```

For use in the browser, use [browserify](https://github.com/substack/node-browserify).


## Usage

``` javascript
var euclidean = require( 'compute-euclidean-distance' );
```

#### euclidean( x, y[, accessor] )

Computes the [Euclidean distance](http://en.wikipedia.org/wiki/Euclidean_distance) between two arrays.

``` javascript
var x = [ 2, 4, 5, 3, 8, 2 ],
	y = [ 3, 1, 5, -3, 7, 2 ];

var d = euclidean( x, y );
// returns ~6.86
```

For object `arrays`, provide an accessor `function` for accessing `numeric` values.

``` javascript
var x, y, d;

x = [
	[1,2],
	[2,4],
	[3,5],
	[4,3],
	[5,8],
	[6,2]
];

y = [
	{'y':3},
	{'y':1},
	{'y':5},
	{'y':-3},
	{'y':7},
	{'y':2}
];

function getValue( d, i, j ) {
	if ( j === 0 ) {
		return d[ 1 ];
	}
	return d.y;
}

d = euclidean( x, y, getValue );
// returns ~6.86
```

The accessor `function` is provided three arguments:

-	__d__: current datum.
-	__i__: current datum index.
-	__j__: array index; e.g., array `x` has index `0`, and array `y` has index `1`.

If provided empty `arrays`, the function returns `null`.


## Examples

``` javascript
var euclidean = require( 'compute-euclidean-distance' );

var x = new Array( 100 ),
	y = new Array( 100 );

for ( var i = 0; i < x.length; i++ ) {
	x[ i ] = Math.round( Math.random()*10 );
	y[ i ] = Math.round( Math.random()*10 );
}

console.log( euclidean( x, y ) );
```

To run the example code from the top-level application directory,

``` bash
$ node ./examples/index.js
```


## References

- 	Dahlquist, Germund and Bjorck, Ake. _Numerical Methods in Scientific Computing_.
- 	Blue, James (1978) "A Portable Fortran Program To Find the Euclidean Norm of a Vector". _ACM Transactions on Mathematical Software_.
- 	Higham, Nicholas J. _Accuracy and Stability of Numerical Algorithms, Second Edition_.

This module implements a one-pass algorithm proposed by S.J. Hammarling.


## Tests

### Unit

Unit tests use the [Mocha](http://mochajs.org/) test framework with [Chai](http://chaijs.com) assertions. To run the tests, execute the following command in the top-level application directory:

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

Copyright &copy; 2015. Athan Reines.


[npm-image]: http://img.shields.io/npm/v/compute-euclidean-distance.svg
[npm-url]: https://npmjs.org/package/compute-euclidean-distance

[travis-image]: http://img.shields.io/travis/compute-io/euclidean-distance/master.svg
[travis-url]: https://travis-ci.org/compute-io/euclidean-distance

[coveralls-image]: https://img.shields.io/coveralls/compute-io/euclidean-distance/master.svg
[coveralls-url]: https://coveralls.io/r/compute-io/euclidean-distance?branch=master

[dependencies-image]: http://img.shields.io/david/compute-io/euclidean-distance.svg
[dependencies-url]: https://david-dm.org/compute-io/euclidean-distance

[dev-dependencies-image]: http://img.shields.io/david/dev/compute-io/euclidean-distance.svg
[dev-dependencies-url]: https://david-dm.org/dev/compute-io/euclidean-distance

[github-issues-image]: http://img.shields.io/github/issues/compute-io/euclidean-distance.svg
[github-issues-url]: https://github.com/compute-io/euclidean-distance/issues

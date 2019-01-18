Minkowski Distance
===
[![NPM version][npm-image]][npm-url] [![Build Status][travis-image]][travis-url] [![Coverage Status][coveralls-image]][coveralls-url] [![Dependencies][dependencies-image]][dependencies-url]

> Computes the [Minkowski distance](http://en.wikipedia.org/wiki/Minkowski_distance) between two arrays.

The [Minkowski distance](http://en.wikipedia.org/wiki/Minkowski_distance) defines a distance between two points in a normed vector space.

<div class="equation" align="center" data-raw-text="d(\mathbf{x},\mathbf{y}) = \left( \sum_{i=0}^{n-1}|x_i - y_i|^p \right )^{1/p}" data-equation="eq:minkowski_distance">
	<img src="https://cdn.rawgit.com/compute-io/minkowski-distance/77475c73614385d8ae28532f8ec111d2abf9e191/docs/img/eqn.svg" alt="Minkowski distance formula">
	<br>
</div>

Special cases:

* 	When `p=1`, the distance is known as the [Manhattan distance](https://github.com/compute-io/manhattan-distance).
* 	When `p=2`, the distance is known as the [Euclidean distance](https://github.com/compute-io/euclidean-distance).
* 	In the limit that `p --> +infinity`, the distance is known as the [Chebyshev distance](https://github.com/compute-io/chebyshev-distance).


## Installation

``` bash
$ npm install compute-minkowski-distance
```

For use in the browser, use [browserify](https://github.com/substack/node-browserify).


## Usage

``` javascript
var minkowski = require( 'compute-minkowski-distance' );
```

#### minkowski( x, y, [opts] )

Computes the [Minkowski distance](http://en.wikipedia.org/wiki/Minkowski_distance) between two `arrays`.

``` javascript
var x = [ 2, 4, 5, 3, 8, 2 ],
	y = [ 3, 1, 5, -3, 7, 2 ];

var d = minkowski( x, y );
// returns ~6.86
```

The function accepts the following `options`:

*	__p__: norm order (`p > 0`).
*	__accessor__: accessor function for accessing `array` values.

By default, the norm order is `2` ([Euclidean distance](https://github.com/compute-io/euclidean-distance)). To specify a different order, set the `p` option.

``` javascript
var x = [ 2, 4, 5, 3, 8, 2 ],
	y = [ 3, 1, 5, 3, 7, 2 ];

var d = minkowski( x, y, {
	'p': 1
});
// returns 5
```

For object `arrays`, provide an accessor `function` for accessing `numeric` values.

``` javascript
var x = [
	{'x':2},
	{'x':4},
	{'x':5}
];

var y = [
	[1,1],
	[2,2],
	[3,7]
];

function getValue( d, i, j ) {
	if ( j === 0 ) {
		return d.x;
	}
	return d[ 1 ];
}

var dist = minkowski( x, y, {
	'accessor': getValue
});
// returns 3
```

The accessor `function` is provided three arguments:

-	__d__: current datum.
-	__i__: current datum index.
-	__j__: array index; e.g., array `x` has index `0`, and array `y` has index `1`.

If provided empty `arrays`, the function returns `null`.


## Notes

__Warning__: only specific `p` values allow for proper consideration of overflow and underflow; i.e., [Euclidean](https://github.com/compute-io/euclidean-distance), [Manhattan](https://github.com/compute-io/manhattan-distance), and [Chebyshev](https://github.com/compute-io/chebyshev) distances. In the general case, you may overflow for large `p` values.


## Examples

``` javascript
var minkowski = require( 'compute-minkowski-distance' );

var x = new Array( 100 ),
	y = new Array( 100 );

for ( var i = 0; i < x.length; i++ ) {
	x[ i ] = Math.round( Math.random()*100 );
	y[ i ] = Math.round( Math.random()*100 );
}

// Euclidean distance (default):
console.log( minkowski( x, y ) );

// Manhattan (city block) distance:
console.log( minkowski( x, y, {
	'p': 1
}));

// Chebyshev distance:
console.log( minkowski( x, y, {
	'p': Number.POSITIVE_INFINITY
}));

// Some other distance:
console.log( minkowski( x, y, {
	'p': 3
}));
```

To run the example code from the top-level application directory,

``` bash
$ node ./examples/index.js
```


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

Copyright &copy; 2015. Philipp Burckhardt.


[npm-image]: http://img.shields.io/npm/v/compute-minkowski-distance.svg
[npm-url]: https://npmjs.org/package/compute-minkowski-distance

[travis-image]: http://img.shields.io/travis/compute-io/minkowski-distance/master.svg
[travis-url]: https://travis-ci.org/compute-io/minkowski-distance

[coveralls-image]: https://img.shields.io/coveralls/compute-io/minkowski-distance/master.svg
[coveralls-url]: https://coveralls.io/r/compute-io/minkowski-distance?branch=master

[dependencies-image]: http://img.shields.io/david/compute-io/minkowski-distance.svg
[dependencies-url]: https://david-dm.org/compute-io/minkowski-distance

[dev-dependencies-image]: http://img.shields.io/david/dev/compute-io/minkowski-distance.svg
[dev-dependencies-url]: https://david-dm.org/dev/compute-io/minkowski-distance

[github-issues-image]: http://img.shields.io/github/issues/compute-io/minkowski-distance.svg
[github-issues-url]: https://github.com/compute-io/minkowski-distance/issues

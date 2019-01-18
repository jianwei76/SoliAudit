Chebyshev Distance
===
[![NPM version][npm-image]][npm-url] [![Build Status][travis-image]][travis-url] [![Coverage Status][coveralls-image]][coveralls-url] [![Dependencies][dependencies-image]][dependencies-url]

> Computes the [Chebyshev distance](http://en.wikipedia.org/wiki/Chebyshev_distance) between two arrays.

The [Chebyshev distance](http://en.wikipedia.org/wiki/Chebyshev_distance) is a metric defined on a vector space where the distance between two vectors is the greatest difference along any coordinate dimension.

<div class="equation" align="center" data-raw-text="d(\mathbf{x},\mathbf{y})= \lim_{p \to \infty} \left( \sum_{i=0}^{n-1} | x_i - y_i|^p \right)^{1/p} = \max_{i=0,\ldots,n-1} | x_i - y_i |" data-equation=“eq:chebyshev_distance”>
	<img src="https://cdn.rawgit.com/compute-io/chebyshev-distance/master/docs/img/eqn.svg" alt="Chebyshev distance formula">
	<br>
</div>


## Installation

``` bash
$ npm install compute-chebyshev-distance
```

For use in the browser, use [browserify](https://github.com/substack/node-browserify).


## Usage

``` javascript
var chebyshev = require( 'compute-chebyshev-distance' );
```

#### chebyshev( x, y[, accessor] )

Computes the [Chebyshev distance](http://en.wikipedia.org/wiki/Chebyshev_distance) between two arrays.

``` javascript
var x = [ 2, 4, 5, 3, 8, 2 ],
	y = [ 3, 1, 5, -3, 7, 2 ];

var d = chebyshev( x, y );
// returns 6
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

var d = chebyshev( x, y, getValue );
// returns 6
```

The accessor `function` is provided three arguments:

-	__d__: current datum.
-	__i__: current datum index.
-	__j__: array index; e.g., array `x` has index `0` and array `y` has index `1`.


If provided empty `arrays`, the function returns `null`.



## Examples

``` javascript
var chebyshev = require( 'compute-chebyshev-distance' );

var x = new Array( 100 ),
	y = new Array( 100 );

for ( var i = 0; i < x.length; i++ ) {
	x[ i ] = Math.round( Math.random()*100 );
	y[ i ] = Math.round( Math.random()*100 );
}

console.log( chebyshev( x, y ) );
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


[npm-image]: http://img.shields.io/npm/v/compute-chebyshev-distance.svg
[npm-url]: https://npmjs.org/package/compute-chebyshev-distance

[travis-image]: http://img.shields.io/travis/compute-io/chebyshev-distance/master.svg
[travis-url]: https://travis-ci.org/compute-io/chebyshev-distance

[coveralls-image]: https://img.shields.io/coveralls/compute-io/chebyshev-distance/master.svg
[coveralls-url]: https://coveralls.io/r/compute-io/chebyshev-distance?branch=master

[dependencies-image]: http://img.shields.io/david/compute-io/chebyshev-distance.svg
[dependencies-url]: https://david-dm.org/compute-io/chebyshev-distance

[dev-dependencies-image]: http://img.shields.io/david/dev/compute-io/chebyshev-distance.svg
[dev-dependencies-url]: https://david-dm.org/dev/compute-io/chebyshev-distance

[github-issues-image]: http://img.shields.io/github/issues/compute-io/chebyshev-distance.svg
[github-issues-url]: https://github.com/compute-io/chebyshev-distance/issues

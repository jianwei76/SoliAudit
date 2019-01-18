Manhattan Distance
===
[![NPM version][npm-image]][npm-url] [![Build Status][travis-image]][travis-url] [![Coverage Status][coveralls-image]][coveralls-url] [![Dependencies][dependencies-image]][dependencies-url]

> Computes the Manhattan (city block) distance between two arrays.

In an *n*-dimensional real vector space with a fixed Cartesian coordinate system, two points can be connected by a straight line. The sum of the line's projections onto the coordinate axes is the [Manhattan distance](http://en.wikipedia.org/wiki/Taxicab_geometry) (also known as the rectilinear distance, *L1* distance, taxicab distance, or city block distance).

<div class="equation" align="center" data-raw-text="d(\mathbf{x},\mathbf{y}) = \sum_{i=0}^{n-1} |x_i - y_i|" data-equation="eq:manhattan_distance">
	<img src="https://cdn.rawgit.com/compute-io/manhattan-distance/5610254d71a1ed646a35eb58c0ac717dbf5fc59a/docs/img/eqn.svg" alt="Manhattan distance formula">
	<br>
</div>

## Installation

``` bash
$ npm install compute-manhattan-distance
```

For use in the browser, use [browserify](https://github.com/substack/node-browserify).


## Usage

``` javascript
var manhattan = require( 'compute-manhattan-distance' );
```

#### manhattan( x, y[, accessor] )

Computes the [Manhattan distance](http://en.wikipedia.org/wiki/Taxicab_geometry) between two arrays.

``` javascript
var x = [ 2, 4, 5, 3, 8, 2 ],
	y = [ 3, 1, 5, -3, 7, 2 ];

var d = manhattan( x, y );
// returns 11
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

d = manhattan( x, y, getValue );
// returns 11
```

The accessor `function` is provided three arguments:

-	__d__: current datum.
-	__i__: current datum index.
-	__j__: array index; e.g., array `x` has index `0`, and array `y` has index `1`.

If provided empty `arrays`, the function returns `null`.


## Examples

``` javascript
var manhattan = require( 'compute-manhattan-distance' );

var x = new Array( 100 ),
	y = new Array( 100 );

for ( var i = 0; i < x.length; i++ ) {
	x[ i ] = Math.round( Math.random()*10 );
	y[ i ] = Math.round( Math.random()*10 );
}

console.log( manhattan( x, y ) );
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

Copyright &copy; 2015. Athan Reines.


[npm-image]: http://img.shields.io/npm/v/compute-manhattan-distance.svg
[npm-url]: https://npmjs.org/package/compute-manhattan-distance

[travis-image]: http://img.shields.io/travis/compute-io/manhattan-distance/master.svg
[travis-url]: https://travis-ci.org/compute-io/manhattan-distance

[coveralls-image]: https://img.shields.io/coveralls/compute-io/manhattan-distance/master.svg
[coveralls-url]: https://coveralls.io/r/compute-io/manhattan-distance?branch=master

[dependencies-image]: http://img.shields.io/david/compute-io/manhattan-distance.svg
[dependencies-url]: https://david-dm.org/compute-io/manhattan-distance

[dev-dependencies-image]: http://img.shields.io/david/dev/compute-io/manhattan-distance.svg
[dev-dependencies-url]: https://david-dm.org/dev/compute-io/manhattan-distance

[github-issues-image]: http://img.shields.io/github/issues/compute-io/manhattan-distance.svg
[github-issues-url]: https://github.com/compute-io/manhattan-distance/issues

'use strict';

// MODULES //

var isArray = require( 'validate.io-array' ),
	isFunction = require( 'validate.io-function' );


// EUCLIDEAN DISTANCE //

/**
* FUNCTION: euclidean( x, y[, accessor] )
*	Computes the Euclidean distance between two arrays.
*
* @param {Number[]|Array} x - input array
* @param {Number[]|Array} y - input array
* @param {Function} [accessor] - accessor function for accessing array values
* @returns {Number|Null} Euclidean distance or null
*/
function euclidean( x, y, clbk ) {
	var len,
		val,
		abs,
		t,
		s,
		r,
		i;
	if ( !isArray( x ) ) {
		throw new TypeError( 'euclidean()::invalid input argument. First argument must be an array. Value: `' + x + '`.' );
	}
	if ( !isArray( y ) ) {
		throw new TypeError( 'euclidean()::invalid input argument. Second argument must be an array. Value: `' + y + '`.' );
	}
	if ( arguments.length > 2 ) {
		if ( !isFunction( clbk ) ) {
			throw new TypeError( 'euclidean()::invalid input argument. Accessor must be a function. Value: `' + clbk + '`.' );
		}
	}
	len = x.length;
	if ( len !== y.length ) {
		throw new Error( 'euclidean()::invalid input arguments. Input arrays must have the same length.' );
	}
	if ( !len ) {
		return null;
	}
	t = 0;
	s = 1;
	if ( clbk ) {
		for ( i = 0; i < len; i++ ) {
			val = clbk( x[ i ], i, 0 ) - clbk( y[ i ], i, 1 );
			abs = ( val < 0 ) ? -val : val;
			if ( abs > 0 ) {
				if ( abs > t ) {
					r = t / val;
					s = 1 + s*r*r;
					t = abs;
				} else {
					r = val / t;
					s += r*r;
				}
			}
		}
	} else {
		for ( i = 0; i < len; i++ ) {
			val = x[ i ] - y[ i ];
			abs = ( val < 0 ) ? -val : val;
			if ( abs > 0 ) {
				if ( abs > t ) {
					r = t / val;
					s = 1 + s*r*r;
					t = abs;
				} else {
					r = val / t;
					s += r*r;
				}
			}
		}
	}
	return t * Math.sqrt( s );
} // end FUNCTION euclidean()


// EXPORTS //

module.exports = euclidean;

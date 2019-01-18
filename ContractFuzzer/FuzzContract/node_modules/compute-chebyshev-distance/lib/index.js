'use strict';

// MODULES //

var isArray = require( 'validate.io-array' ),
	isFunction = require( 'validate.io-function' );


// CHEBYSHEV DISTANCE //

/**
* FUNCTION: chebyshev( x, y[, accessor] )
*	Computes the Chebyshev distance between two arrays.
*
* @param {Number[]|Array} x - input array
* @param {Number[]|Array} y - input array
* @param {Function} [accessor] - accessor function for accessing array values
* @returns {Number|Null} Chebyshev distance or null
*/
function chebyshev( x, y, clbk ) {
	var len,
		d, v,
		i;
	if ( !isArray( x ) ) {
		throw new TypeError( 'chebyshev()::invalid input argument. First argument must be an array. Value: `' + x + '`.' );
	}
	if ( !isArray( y ) ) {
		throw new TypeError( 'chebyshev()::invalid input argument. Second argument must be an array. Value: `' + y + '`.' );
	}
	if ( arguments.length > 2 ) {
		if ( !isFunction( clbk ) ) {
			throw new TypeError( 'chebyshev()::invalid input argument. Accessor must be a function. Value: `' + clbk + '`.' );
		}
	}
	len = x.length;
	if ( len !== y.length ) {
		throw new Error( 'chebyshev()::invalid input arguments. Input arrays must have the same length.' );
	}
	if ( !len ) {
		return null;
	}
	if ( clbk ) {
		v = clbk( x[0], 0, 0 ) - clbk( y[0], 0, 1 );
		d = ( v < 0 ) ? -v : v;
		for ( i = 1; i < len; i++ ) {
			v = clbk( x[i], i, 0 ) - clbk( y[i], i, 1 );
			if ( v < 0 ) {
				v = -v;
			}
			if ( v > d ) {
				d = v;
			}
		}
	} else {
		v = x[ 0 ] - y[ 0 ];
		d = ( v < 0 ) ? -v : v;
		for ( i = 1; i < len; i++ ) {
			v = x[ i ] - y[ i ];
			if ( v < 0 ) {
				v = -v;
			}
			if ( v > d ) {
				d = v;
			}
		}
	}
	return d;
} // end FUNCTION chebyshev()


// EXPORTS //

module.exports = chebyshev;

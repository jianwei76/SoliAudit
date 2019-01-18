'use strict';

// MODULES //

var isArray = require( 'validate.io-array' ),
	isFunction = require( 'validate.io-function' );


// MANHATTAN DISTANCE //

/**
* FUNCTION: manhattan( x, y[, accessor] )
*	Computes the Manhattan distance between two arrays.
*
* @param {Number[]|Array} x - input array
* @param {Number[]|Array} y - input array
* @param {Function} [accessor] - accessor function for accessing array values
* @returns {Number|Null} Manhattan distance or null
*/
function manhattan( x, y, clbk ) {
	var len,
		d, v,
		i;
	if ( !isArray( x ) ) {
		throw new TypeError( 'manhattan()::invalid input argument. First argument must be an array. Value: `' + x + '`.' );
	}
	if ( !isArray( y ) ) {
		throw new TypeError( 'manhattan()::invalid input argument. Second argument must be an array. Value: `' + y + '`.' );
	}
	if ( arguments.length > 2 ) {
		if ( !isFunction( clbk ) ) {
			throw new TypeError( 'manhattan()::invalid input argument. Accessor must be a function. Value: `' + clbk + '`.' );
		}
	}
	len = x.length;
	if ( len !== y.length ) {
		throw new Error( 'manhattan()::invalid input arguments. Input arrays must have the same length.' );
	}
	if ( !len ) {
		return null;
	}
	d = 0;
	if ( clbk ) {
		for ( i = 0; i < len; i++ ) {
			v = clbk( x[i], i, 0 ) - clbk( y[i], i, 1 );
			d += ( v < 0 ) ? -v : v;
		}
	} else {
		for ( i = 0; i < len; i++ ) {
			v = x[ i ] - y[ i ];
			d += ( v < 0 ) ? -v : v;
		}
	}
	return d;
} // end FUNCTION manhattan()


// EXPORTS //

module.exports = manhattan;

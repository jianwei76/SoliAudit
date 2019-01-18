'use strict';

// MODULES //

var isArray = require( 'validate.io-array' ),
	isObject = require( 'validate.io-object' ),
	isFunction = require( 'validate.io-function' ),
	isNumber = require( 'validate.io-number-primitive' ),
	euclidean = require( 'compute-euclidean-distance' ),
	manhattan = require( 'compute-manhattan-distance' ),
	chebyshev = require( 'compute-chebyshev-distance' );


// MINKOWSKI DISTANCE //

/**
* FUNCTION: minkowski( x, y[, options] )
*	Computes the Minkowski distance between two arrays.
*
* @param {Number[]|Array} x - input array
* @param {Number[]|Array} y - input array
* @param {Object} [options] - function options
* @param {Number} [options.p=2] - norm order
* @param {Function} [options.accessor] - accessor function for accessing array values
* @returns {Number|Null} Minkowski distance or null
*/
function minkowski( x, y, opts ) {
	var p = 2,
		clbk,
		len,
		d, v,
		i;

	if ( arguments.length > 2 ) {
		if ( !isObject( opts ) ) {
			throw new TypeError( 'minkowski()::invalid input argument. Options argument must be an object. Value: `' + opts + '`.' );
		}
		if ( opts.hasOwnProperty( 'p' ) ) {
			p = opts.p;
			if ( !isNumber( p ) || p <= 0 ) {
				throw new TypeError( 'minkowski()::invalid option. `p` option must be a positive number primitive. Option: `' + p + '`.' );
			}
		}
		if ( opts.hasOwnProperty( 'accessor' ) ) {
			clbk = opts.accessor;
			if ( !isFunction( clbk ) ) {
				throw new TypeError( 'minkowski()::invalid option. Accessor must be a function. Option: `' + clbk + '`.' );
			}
		}
	}
	// If norm order corresponds to a known metric, delegate type checking and execution to the respective implementation...
	if ( p === 2 ) {
		return ( clbk ) ? euclidean( x, y, clbk ) : euclidean( x, y );
	}
	else if ( p === 1 ) {
		return ( clbk ) ? manhattan( x, y, clbk ) : manhattan( x, y );
	}
	else if ( p === Number.POSITIVE_INFINITY ) {
		return ( clbk ) ? chebyshev( x, y, clbk ) : chebyshev( x, y );
	}
	// Proceed with the general distance algorithm...
	if ( !isArray( x ) ) {
		throw new TypeError( 'minkowski()::invalid input argument. First argument must be a number array. Value: `' + x + '`.' );
	}
	if ( !isArray( y ) ) {
		throw new TypeError( 'minkowski()::invalid input argument. Second argument must be a number array. Value: `' + y + '`.' );
	}
	len = x.length;
	if ( len !== y.length ) {
		throw new TypeError( 'minkowski()::invalid input arguments. Input arrays must have the same length.' );
	}
	if ( !len ) {
		return null;
	}
	d = 0;
	if ( clbk ) {
		for ( i = 0; i < len; i++ ) {
			v = clbk( x[i], i, 0 ) - clbk( y[i], i, 1 );
			if ( v < 0 ) {
				v = -v;
			}
			d += Math.pow( v, p );
		}
	} else {
		for ( i = 0; i < len; i++ ) {
			v = x[ i ] - y[ i ];
			if ( v < 0 ) {
				v = -v;
			}
			d += Math.pow( v, p );
		}
	}
	return Math.pow( d, 1/p );
} // end FUNCTION minkowski()


// EXPORTS //

module.exports = minkowski;

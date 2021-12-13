/* Acknowledgment: Canters and Decleir, for their 4th and 5th order polynomial
 * equations approximating Robinson map projections.
 *
 * Assumptions:
 * 1. At zoom=0, the map is 1052px x 531px.
 * 2. The center of the map is (x,y) = (0,0) after adjusting for the offset,
 *    effectively making (lat=0,lon=0) = (x=0,y=0) graphically.
 * 3. (lat,lon) are in degrees.
 */

/* Canters and Decleir's coefficients for their 4th and 5th degree polynomials,
   needed to approximate Robinson coordinates. */
const A = [0.8507, 0.9642, -0.1450, -0.0013, -0.0104, -0.0129];

/* Convert degrees to radians. */
function radians(degrees)
{
	return degrees * (Math.PI/180)
}

/* Convert radians to degrees. */
function degrees(radians)
{
	return (radians*180) / Math.PI
}

/* Given (lat,lon) geographic coordinates, output (x,y) Cartesian coordinates. */
function to_cartesian(lat, lon)
{
	/* Return -1 if the lat is out of bounds. */
	if (lat < -90 || lat >= 90)
	{
		return [-1, -1];
	}

	/* Return -2 if the lon is out of bounds. */
	if (lon < -180 || lon > 180)
	{
		return [-2, -2];
	}

	lat = radians(lat);
	lon = radians(lon);

	let R = 1052/(2*Math.PI);
	let x = R * lon * (A[0] + A[2]*Math.pow(lat, 2) + A[4]*Math.pow(lat, 4));
	let y = R * (A[1]*lat + A[3]*Math.pow(lat, 3) + A[5]*Math.pow(lat, 5));

	return [x,y];
}

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

/* Given (lat,lon) geographic coordinates, output (x,y) Cartesian coordinates.
   Zoom starts at 0 (no zoom) and can go infinitely in either way. */
function to_cartesian(lat, lon, zoom)
{
	/* Return -1 if the lat is out of bounds. */
	if (lat < -180 || lat > 180)
	{
		return [-1, -1];
	}

	/* Return -2 if the lon is out of bounds. */
	if (lon < -85.051129 || lon >= 85.051129)
	{
		return [-2, -2];
	}

	let x = Math.floor( (256/(2*Math.PI)) * Math.pow(2, zoom) * (radians(lat) + Math.PI) )
	let y = Math.floor( (256/(2*Math.PI)) * Math.pow(2, zoom) * (Math.PI - Math.log(
		Math.tan(Math.PI/4 + radians(lon)/2))) );

	return [x,y]
}

/* Given (x,y) Cartesian coordinates, output (lat,lon) geographic coordinates.
   Zoom starts at 0 (no zoom) and can go infinitely in either way. */
function to_geographic(x, y, zoom)
{
	/* Return -1 if x is out of bounds. */
	if (x < 0 || x > 256 * Math.pow(2, zoom))
	{
		return [-1, -1];
	}

	/* Return -2 if y is out of bounds. */
	if (y < 0 || y > 256 * Math.pow(2, zoom))
	{
		return [-2, -2];
	}

	let lat = degrees( ((x * Math.PI)/(Math.pow(2, 7+zoom))) - Math.PI );
	let lon = degrees( (2*Math.atan(Math.pow(Math.E, -((Math.PI*y) - (Math.PI*Math.pow(
		2, 7+zoom)))/(Math.pow(2, 7+zoom))))) - (Math.PI/2) );

	return [lat,lon];
}

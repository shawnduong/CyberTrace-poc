var img;
var width;
var height;
var newWidth;
var newHeight;
var updateLeft;
var updateTop;
var x = 0;
var y = 0;
var top = 0;
var left = 0;
var zoomValue = 1.0;
var originalWidth = document.getElementById("map-graphic").getBoundingClientRect().width;
var originalHeight = document.getElementById("map-graphic").getBoundingClientRect().height;

/* Zoom function that keeps track of the width and height as the user is zooming
   in or zooming out. */
function zoom_map(zoomNum)
{
	img = document.getElementById("map-graphic");
	zoomValue += zoomNum;

	/* Making sure that user can't zoom out past the set size. */
	if (zoomValue < 1.0) 
	{
		zoomValue = 1.0;
		img.style.top = "0px";
	}

	newWidth = (originalWidth * zoomValue);
	newHeight = (originalHeight * zoomValue);

	width = (originalWidth - newWidth);
	height = (originalHeight - newHeight);

	if (left < width) 
	{
		left = width;
	}

	if (top < height) 
	{
		top = height;
	}

	img.style.left = left + "px";
	img.style.top = top + "px";
	img.style.width = newWidth + "px";
	img.style.height = newHeight + "px";

	img = null;
}

/* Allows user to drag the map if user has zoomed in */
function dragging_map() 
{
	if (zoomValue > 1.0) 
	{
		img = this;
		x = window.event.clientX - document.getElementById("map-graphic").offsetLeft;
		y = window.event.clientY - document.getElementById("map-graphic").offsetTop;
	}
}

/* Function is used to stop dragging from happening when user is no longer
   dragging the map */
function stop_dragging() 
{
	img = null;
}


/* This function keeps tracks of the location where the user moved to. */
function while_dragging() 
{
	updateLeft = (window.event.clientX - x);
	updateTop = (window.event.clientY - y);

	/* Prevents the user from dragging the entire map. */
	if (updateLeft > 0) 
	{
		updateLeft = 0;
	}

	if (updateLeft < (originalWidth - img.width)) 
	{
		updateLeft = (originalWidth - img.width);
	}

	/* Prevents the user from dragging the entire map. */
	if (updateTop > 0) 
	{
		updateTop = 0;
	}

	if (updateTop < (originalHeight - img.height)) 
	{
		updateTop = (originalHeight - img.height);
	}

	img.style.left = updateLeft + "px";
	img.style.top = updateTop + "px";
}

/* Uses zoom_map function to zoom in and out. */
document.getElementById("zoomIn").addEventListener("click",function() { zoom_map(0.20) });
document.getElementById("zoomOut").addEventListener("click", function() { zoom_map(-0.20) });

document.getElementById("map").addEventListener("mouseup", stop_dragging);
document.getElementById("map-graphic").addEventListener("mousedown", dragging_map);
document.getElementById("map").addEventListener("mouseout", stop_dragging);
document.getElementById("map").addEventListener("mousemove", while_dragging);


function map_coord(event) 
{
	/* Uses clientX and clientY to get the horizontal and vertical coordinates */
	var x = event.clientX;
	var y = event.clientY;

	document.getElementById("x").value = x;
	document.getElementById("y").value = y;
}

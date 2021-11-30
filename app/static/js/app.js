/* Geogrid offset in the page. */
const OFFSET = $("#map-geogrid").offset();

/* Zoom step values per scroll event. */
const STEP = 0.1;

/* Effective x and y values of the cursor's last click. */
let x = 0;
let y = 0;

/* Effective scaling constants to calculate x and y from real dimensions. */
let scaleX = 1;
let scaleY = 1;

/* Zoom value from 0 (inclusive) to positive infinity. */
let zoom = 0;

/* Dragging boolean. */
let dragging = false;

/* Dynamically resize the geogrid based on resize detections in the map graphic.
   The map object itself should stay of constant dimensionality. */
let resize = new ResizeObserver(() =>
{
	/* Resize the geogrid. */
	$("#map-geogrid").width($("#map-graphic").width());
	$("#map-geogrid").height($("#map-graphic").height());

	/* Calculate new scaling constants for the updated geogrid dimensions. */
	scaleX = 1052/$("#map-geogrid").width();
	scaleY = 531/$("#map-geogrid").height();
});
resize.observe($("#map-graphic").get(0));

/* Assign the map dimensions after loading the graphic. */
$("#map-graphic").ready(function()
{
	$("#map").width($("#map-graphic").width());
	$("#map").height($("#map-graphic").height());
});

/* Update the map coordinates inside the geogrid div upon clicking. */
$("#map-geogrid").click(function(e)
{
	/* Scale the grid and anchor the center to (0,0). */
	x = 0.862 * (scaleX*(e.pageX - OFFSET.left) - 1052/2);
	y = -1 * 0.862 * 0.953 * (scaleY*(e.pageY - OFFSET.top) - 531/2);

	/* Adjust for the map offset. */
	x += 51.1175898931;
	y += 34.2487852284;

	/* Debug. */
	console.log("x =", x);
	console.log("y =", y);
});

/* Increment or decrement map zoom by step values of STEP upon scroll. */
$("#map").on("wheel", function(e)
{
	/* Increment or decrement the zoom variable by STEP. */
	if (e.originalEvent.deltaY > 0)  zoom -= STEP;
	else                             zoom += STEP;

	/* Ensure bounds. */
	if (zoom < 0)
	{
		zoom = 0;
		return false;
	}

	/* Calculate new widths and heights. */
	$("#map-geogrid").width($("#map").width() * (1+zoom));
	$("#map-graphic").width($("#map").width() * (1+zoom));
	$("#map-geogrid").height($("#map").height() * (1+zoom));
	$("#map-graphic").height($("#map").height() * (1+zoom));

	/* Prevent actual page scrolling. */
	return false;
});

/* Move the map grid and graphic by dragging the mouse. The actual map stays
   in the same place, however, and only the grid and graphic move. */
$("#map")
/* Allow the user to drag the map if the user has zoomed in */
.on("mousedown", function()
{
	dragging = true;
})
/* Function is used to stop dragging from happening when the user is no longer
   dragging the map. */
.on("mouseup", function()
{
	dragging = false;
})
/* Function is used to stop dragging from happening when the user is no longer
   dragging the map. */
.on("mouseout", function()
{
	dragging = false;
})
/* Keep track of the location where the user moved to. */
.on("mousemove", function(e)
{
	if (!dragging) return false;

	let updateLeft = e.pageX - OFFSET.left - x;
	let updateTop  = e.pageY - OFFSET.top  - y;

	console.log(updateLeft, updateTop);
	console.log("dragging");
});

///* Zoom function that keeps track of the width and height as the user is zooming
//   in or zooming out. */
//function zoom_map(zoomNum)
//{
//	img = document.getElementById("map-graphic");
//	zoomValue += zoomNum;
//
//	/* Making sure that user can't zoom out past the set size. */
//	if (zoomValue < 1.0) 
//	{
//		zoomValue = 1.0;
//		img.style.top = "0px";
//	}
//
//	newWidth = (originalWidth * zoomValue);
//	newHeight = (originalHeight * zoomValue);
//
//	width = (originalWidth - newWidth);
//	height = (originalHeight - newHeight);
//
//	if (left < width) 
//	{
//		left = width;
//	}
//
//	if (top < height) 
//	{
//		top = height;
//	}
//
//	img.style.left = left + "px";
//	img.style.top = top + "px";
//	img.style.width = newWidth + "px";
//	img.style.height = newHeight + "px";
//
//	img = null;
//}
//
///* Allows user to drag the map if user has zoomed in */
//function dragging_map() 
//{
//	if (zoomValue > 1.0) 
//	{
//		img = this;
//		x = window.event.clientX - document.getElementById("map-graphic").offsetLeft;
//		y = window.event.clientY - document.getElementById("map-graphic").offsetTop;
//	}
//}
//
///* Function is used to stop dragging from happening when user is no longer
//   dragging the map */
//function stop_dragging() 
//{
//	img = null;
//}
//
//
///* This function keeps tracks of the location where the user moved to. */
//function while_dragging() 
//{
//	updateLeft = (window.event.clientX - x);
//	updateTop = (window.event.clientY - y);
//
//	/* Prevents the user from dragging the entire map. */
//	if (updateLeft > 0) 
//	{
//		updateLeft = 0;
//	}
//
//	if (updateLeft < (originalWidth - img.width)) 
//	{
//		updateLeft = (originalWidth - img.width);
//	}
//
//	/* Prevents the user from dragging the entire map. */
//	if (updateTop > 0) 
//	{
//		updateTop = 0;
//	}
//
//	if (updateTop < (originalHeight - img.height)) 
//	{
//		updateTop = (originalHeight - img.height);
//	}
//
//	img.style.left = updateLeft + "px";
//	img.style.top = updateTop + "px";
//}

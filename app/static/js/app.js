/* Geogrid offset in the page. */
const OFFSET = $("#map-geogrid").offset();

/* Zoom step values per scroll event. */
const STEP = 0.1;

/* Effective x and y values of the cursor's last click. */
let x = 0;
let y = 0;

/* Effective scaling constants to calculate x and y at real dimensions. */
let scaleX = 1;
let scaleY = 1;

/* Zoom value. */
let zoom = 1;

/* Dynamically resize the geogrid based on resize detections in the map. */
let resize = new ResizeObserver(() =>
{
	/* Resize the geogrid. */
	$("#map-geogrid").width($("#map").width());
	$("#map-geogrid").height($("#map").height());

	/* Calculate new scaling constants for the updated geogrid dimensions. */
	scaleX = 256/$("#map-geogrid").width();
	scaleY = 256/$("#map-geogrid").height();
});
resize.observe($("#map").get(0));

/* Update the map coordinates inside the geogrid div upon clicking. */
$("#map-geogrid").click(function(e)
{
	x = scaleX * (e.pageX - OFFSET.left);
	y = scaleY * (e.pageY - OFFSET.top);

	/* Debug. */
	console.log("x =", x);
	console.log("y =", y);
});

/* Increment or decrement map zoom by step values of STEP upon scroll. */
$("#map").on("wheel", function(e)
{
	if (e.originalEvent.deltaY > 0 && zoom > 1)  zoom -= STEP;
	else                                         zoom += STEP;

	/* Prevent actual page scrolling. */
	return false;
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

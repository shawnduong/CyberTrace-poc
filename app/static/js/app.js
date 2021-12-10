/* Zoom step values per scroll event. */
const STEP = 0.1;

/* Map offset. */
const OFFSET = {x: 51.1175898931, y: 34.2487852284};

/* Specific scaling factors to turn a CyberTrace Robinson map into a standard
   Robinson map to simplify calculations. */
const RSCALE = {s: 0.862, x: 1.000, y: 0.953};

/* Polling interval for updates. */
const INTERVAL = 1000;

/* Counter for the last event serial number received. -1 will assign this to
   the most recent event serial number in the API's database upon start. */
let since = -1;

/* Effective x and y values of the cursor's last click. */
let coord = {x: 0, y: 0};

/* Effective scaling constants to calculate x and y from real dimensions. */
let scale = {x: 1, y: 1};

/* Pan offset buffers. */
let tmpPan  = {x: 0, y: 0};
let tmpDrag = {x: 0, y: 0};

/* Actual pan offsets. */
let pan = {x: 0, y: 0};

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
	scale.x = 1052/$("#map-geogrid").width();
	scale.y = 531/$("#map-geogrid").height();
});
resize.observe($("#map-graphic").get(0));

/* Begin periodic AJAX updates after the document is ready. */
$(document).ready(function()
{
	setTimeout(update, INTERVAL);
});

/* Assign the map dimensions and render viewBox after loading the window. */
$(window).on("load", function()
{
	let w = $("#map-graphic").width();
	let h = $("#map-graphic").height();

	$("#map").width(w);
	$("#map").height(h);
	$("#map-renders").attr("viewBox", `0 0 ${w} ${h}`);
});

/* Update the map coordinates inside the geogrid div upon clicking. */
$("#map-geogrid").click(function(e)
{
	/* Scale the grid and anchor the center to (0,0). */
	coord.x = RSCALE.s * RSCALE.x * (scale.x*(e.pageX - pan.x) - 1052/2);
	coord.y = -RSCALE.s * RSCALE.y * (scale.y*(e.pageY - pan.y) - 531/2);

	/* Adjust for the map offset. */
	coord.x += OFFSET.x;
	coord.y += OFFSET.y;
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

	/* Offset calculation function. Note that this is INCOMPLETE and should be replaced with a more
	   accurate function in the future. There is still an undesirable non-center weighted zoom bias. */
	let fun = function(D_o, D_n, D_m, O_n)
	{
		return -1*D_m*( (-O_n/D_n) + ((D_o/D_n - D_o/D_m)*( (-O_n/D_n) / ( (-O_n/D_n) + ((D_n-D_o+O_n)/D_n) ))));
	};

	/* Calculate and assign new pans to center-weight zooming width-wise. */
	let D_o = $("#map").width();
	let D_n = $("#map-graphic").width();
	let D_m = $("#map").width()*(1+zoom);
	let O_n = pan.x;

	if ((-O_n/D_n) + ((D_n-D_o+O_n)/D_n) != 0)
	{
		pan.x = fun(D_o, D_n, D_m, O_n);
	}
	else
	{
		pan.x = (D_n - D_m) / 2;
	}

	$("#map-graphic").css("left", pan.x);
	$("#map-renders").css("left", pan.x);

	/* Calculate and assign new pans to center-weight zooming height-wise. */
	D_o = $("#map").height();
	D_n = $("#map-graphic").height();
	D_m = $("#map").height()*(1+zoom);
	O_n = pan.y;

	if ((-O_n/D_n) + ((D_n-D_o+O_n)/D_n) != 0)
	{
		pan.y = fun(D_o, D_n, D_m, O_n);
	}
	else
	{
		pan.y = (D_n - D_m) / 2;
	}

	$("#map-graphic").css("top", pan.y);
	$("#map-renders").css("top", pan.y);

	/* Calculate and assign new widths and heights. */
	$("#map-graphic").width($("#map").width() * (1+zoom));
	$("#map-graphic").height($("#map").height() * (1+zoom));

	/* Prevent actual page scrolling. */
	return false;
});

/* Move the map grid and graphic by dragging the mouse. The actual map stays
   in the same place, however, and only the grid and graphic move. */
$("#map")
/* Allow the user to drag the map if the user has zoomed in */
.on("mousedown", function(e)
{
	tmpPan.x = e.pageX;
	tmpPan.y = e.pageY;

	dragging = true;
})
/* Function is used to stop dragging from happening when the user is no longer
   dragging the map. */
.on("mouseup mouseout", function()
{
	if (!dragging) return false;

	pan.x = tmpDrag.x;
	pan.y = tmpDrag.y;

	dragging = false;
})
/* Keep track of the location where the user moved to and pan the map on drag. */
.on("mousemove", function(e)
{
	if (!dragging) return false;

	tmpDrag.x = e.pageX - tmpPan.x + pan.x;
	tmpDrag.y = e.pageY - tmpPan.y + pan.y;

	/* Ensure bounds. */
	if (tmpDrag.x >= 0)
	{
		tmpDrag.x = 0;
	}
	else if (tmpDrag.x < $("#map").width() - $("#map-graphic").width())
	{
		tmpDrag.x = $("#map").width() - $("#map-graphic").width();
	}

	/* Ensure bounds. */
	if (tmpDrag.y >= 0)
	{
		tmpDrag.y = 0;
	}
	else if (tmpDrag.y < $("#map").height() - $("#map-graphic").height())
	{
		tmpDrag.y = $("#map").height() - $("#map-graphic").height();
	}

	$("#map-graphic").css("left", tmpDrag.x);
	$("#map-graphic").css("top", tmpDrag.y);
	$("#map-renders").css("left", tmpDrag.x);
	$("#map-renders").css("top", tmpDrag.y);
});

/* Sleep for ms many milliseconds. */
function sleep(ms)
{
	return new Promise(resolve => setTimeout(resolve, ms));
}

/* Update the application using AJAX by sending a query. */
function update()
{
	$.ajax(
	{
		url: "/api/update/"+since,
		type: "GET",
		dataType: "json",
		success: function(response)
		{
			/* -1 implies app just initialized and therefore needs to first
			   define the head before continuing. */
			if (since == -1)
			{
				since = response.HEAD;
				return;
			}

			/* Response length 0 implies delta of 0, thus nothing to do. */
			if (Object.keys(response).length == 0)  return;

			/* Handle each individual update. */
			$.each(response, function(id, v)
			{
				if (id > since)  since = id;

				draw_vector(id, v.attacker_lat, v.attacker_lon, v.victim_lat,
					v.victim_lon, "#FFFFFF", 5, 3,
					`[${v.module_name}] ${v.attack_description}`);

				/* TODO: Once Jet finishes the node render function, then that
				   function will also be called here. */
			});
		},
		complete: function()
		{
			setTimeout(update, INTERVAL);
		}
	});
}

/* Translate an effective Cartesian coordinate e into an unscaled Cartesian
 * coordinate within a constant-dimension SVG viewBox of equal dimensions to
 * the map's. This effectively allows one to translate effective coordinates
 * into coordinates compatible with the application SVG.
 */
function to_translated(e)
{
	let ex = e[0];
	let ey = e[1];

	return [ ((ex-OFFSET.x)/(RSCALE.s*RSCALE.x) + 1052/2)/(1052/$("#map").width()),
		-((ey-OFFSET.y)/(RSCALE.s*RSCALE.y) - 531/2)/(531/$("#map").height()) ];
}

/* Draw a vector of id with some color from A to B with a lifetime of TTL
 * seconds, making a splash of radius r at B. Note that this "vector" has no
 * "arrowhead," instead replaced by a splash. Also, type an adjacent message.
 */
async function draw_vector(id, latA, lonA, latB, lonB, color, ttl, r, msg)
{
	/* Create a new path and define its ID and color. */
	let path = document.createElementNS("http://www.w3.org/2000/svg", "path");
	path.setAttribute("id", id);
	path.setAttribute("stroke", color);
	path.setAttribute("fill", "transparent");

	/* Translate A and B to coordinates on the screen. */
	let a = to_translated(to_cartesian(latA, lonA));
	let b = to_translated(to_cartesian(latB, lonB));

	/* An artistic formulation of the curve's control point. */
	let c = [
		b[0] - (b[0]-a[0])/2,
		b[1] - a[1] - Math.sqrt(Math.pow(b[1]-a[1], 2) + Math.pow(b[0]-a[0], 2))*0.33
	];

	/* Define the path as a quadratic Bezier curve, forming an arc. */
	path.setAttribute("d", `M ${a[0]} ${a[1]} Q ${c[0]} ${c[1]} ${b[0]} ${b[1]}`);

	/* Append the newly created path to the map-renders SVG. */
	$("#map-renders").append(path);

	/* Create the message. */
	let message = document.createElement("p");
	message.setAttribute("id", id+"-msg");
	$("#map-text").append(message);
	$(message).css("color", color);
	$(message).css("left", a[0]);
	$(message).css("top", a[1]);

	/* Type the message. */
	typewriter($(message), msg, 25);

	/* Animate the vector. */
	let anim = $(path).drawsvg();
	anim.drawsvg("animate");

	/* Wait until the vector is done animating. */
	await sleep(1000);

	/* Create the splash. */
	let splash = document.createElementNS("http://www.w3.org/2000/svg", "circle");
	splash.setAttribute("id", id+"-splash");
	splash.setAttribute("cx", b[0]);
	splash.setAttribute("cy", b[1]);
	splash.setAttribute("r", r);
	splash.setAttribute("stroke", color);
	splash.setAttribute("fill", color);

	/* Append the newly created splash to the map-renders SVG. */
	$("#map-renders").append(splash);

	/* Fade out the splash. */
	$(splash).animate({opacity: 0}, 2500);

	/* Fade out the vector and text. */
	await sleep(ttl*1000);
	$(path).animate({opacity: 0}, 1000);
	$(message).animate({opacity: 0}, 1000);

	/* Delete the vector, splash, and text. */
	await sleep(1000);
	$(path).remove();
	$(splash).remove();
	$(message).remove();
}

/* Draw a node of id with some color at (lat,lon) and radius r with an attached
   message printed near it. */
function draw_node(id, lat, lon, color, r, msg)
{
	/* Translate (lat,lon) to coordinates on the screen. */
	let point = to_translated(to_cartesian(lat, lon));

	/* Create a new node and define its ID and color. */
	let node = document.createElementNS("http://www.w3.org/2000/svg", "circle");
	node.setAttribute("id", id+"-node");
	node.setAttribute("cx", point[0]);
	node.setAttribute("cy", point[1]);
	node.setAttribute("r", r);
	node.setAttribute("stroke", color);
	node.setAttribute("fill", color);

	/* Append the newly created node to the map-renders SVG. */
	$("#map-renders").append(node);

	/* Create the message. */
	let message = document.createElement("p");
	message.setAttribute("id", id+"-node-msg");
	$("#map-text").append(message);
	$(message).css("color", color);
	$(message).css("left", point[0]);
	$(message).css("top", point[1]);

	/* Type the message. */
	typewriter($(message), msg, 25);
}

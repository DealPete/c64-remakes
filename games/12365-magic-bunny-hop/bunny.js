var canvas = document.getElementById('bunny');
var ctx = canvas.getContext('2d');
ctx.font = "16px c64mono";

state = { state: "loading" };
hops = 0;

var bunny = new Image();
bunny.src = "bunny.png";

bunny.onload = function() {
	// Give the browser some time to load proper @font-face.
	// Replace this with FontFace API when proper browser support exists.
	window.setTimeout(startGame, 100);
};

function startGame() {
	state = { state: "waiting", x: 52, y: 284, vx: 0, vy: 0 };
	drawScreen();
}

function drawScreen() {
	ctx.clearRect(0, 0, 640, 400);
	ctx.fillStyle = "black";
	ctx.fillText("Magic Bunny Hop - Bob and Dave Snader", 16, 16);
	ctx.fillText("Remake by Peter Deal", 144, 32);

	ctx.fillStyle = 'rgb(238, 238, 119)';
	ctx.fillText("\uee4c", 21*16, 20*16);
	ctx.fillText("\uee7a", 24*16, 20*16);
	ctx.drawImage(bunny, state.x, state.y, 48, 32);
}

function updateState() {
	state.x += state.vx;
	state.vy -= 0.05;
	state.y -= state.vy;
	if (state.x >= 640 || state.y >= 284) {
		hops++;
		state.state = "landed";
		if (state.x > 342 && state.x < 376) {
			ctx.fillStyle = "black";
			ctx.fillText("GOOD WORK!", 5*16, 9*16);
			ctx.fillText("YOU DID IT IN " + hops + " HOPS.", 5*16, 10*16);
		} else {
			window.setTimeout(startGame, 750);
		}
	}
}
	
function moveBunny() {
	drawScreen();
	updateState();
	if (state.state == "jumping")
		window.setTimeout(moveBunny, 25);
}

ctx.canvas.onmousedown = function() {
	if (state.state == "waiting") {
		state.state = "powering";
		state.powerStartTime = (new Date()).getTime();
	}
};

ctx.canvas.onmouseup = function() {
	if (state.state == "powering") {
		state.state = "jumping";
		state.vx = state.vy = ((new Date()).getTime() - state.powerStartTime)/250;
		moveBunny();
	}
};

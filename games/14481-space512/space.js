MISSILE_VELOCITY = 4;
MISSILE_LENGTH = 16;
ALIEN_VELOCITY = 1;

var canvas = document.getElementById('space');
var ctx = canvas.getContext('2d');
ctx.font = "16px c64mono";

var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
var gain = audioCtx.createGain();
gain.gain.value = 0.1;
gain.connect(audioCtx.destination);

state = { state: "loading" };
hops = 0;

var defender = new Image();
defender.src = "defender.png";

var invader = new Image();
invader.src = "invader.png";

let imagesLoaded = 0;

[invader, defender].map( image => {
	image.onload = () => {
		imagesLoaded += 1;
		if (imagesLoaded == 2)
			// Give the browser some time to load proper @font-face.
			// Replace this with FontFace API when proper browser support exists.
			window.setTimeout(startGame, 100);
	}
});

function startGame() {
	aliens = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
		.map( x => ({
		x: 50 + (x%6) * 38,
		y: 30 + Math.floor(x/6) * 32,
		alive: true
	}));

	state = {
		state: "playing",
		player: {
			x: 160,
			y: 350,
			vx: 0
		},
		missile: false,
		missileSound: null,
		explodeNoise: null,
		alienMissile: false,
		aliens: aliens,
		aliensV: ALIEN_VELOCITY
	}

	window.setInterval(gameLoop, 10);
}

function gameLoop() {
	drawScreen();
	if (state.state == "playing")
		updateState();
}

function drawScreen() {
	ctx.clearRect(0, 0, 640, 400);

	for (let alien of state.aliens) {
		if (alien.alive)
			ctx.drawImage(invader, alien.x, alien.y, 22, 16);
	}
		
	if (state.state == "playing") {
		ctx.drawImage(defender, state.player.x, state.player.y, 48, 16);
		if (state.missile) {
			ctx.beginPath();
			ctx.moveTo(state.missile.x, state.missile.y);
			ctx.lineTo(state.missile.x, state.missile.y + MISSILE_LENGTH);
			ctx.lineWidth = 2;
			ctx.strokeStyle = "#FFFFFF";
			ctx.stroke();
		}
		if (state.alienMissile) {
			ctx.beginPath();
			ctx.moveTo(state.alienMissile.x, state.alienMissile.y);
			ctx.lineTo(state.alienMissile.x, state.alienMissile.y + MISSILE_LENGTH);
			ctx.lineWidth = 2;
			ctx.strokeStyle = "#FFFFFF";
			ctx.stroke();
		}
	}
}

function updateState() {
	if (state.missile) {
		state.missileSound.frequency.value -= 128 * c64HertzFactor;
		if (state.missileSound.frequency.value <= 0)
			state.missileSound.frequency.value = 0;
		state.missile.y -= MISSILE_VELOCITY;
		if (state.missile.y < -MISSILE_LENGTH) {
			state.missileSound.stop();
			state.missile = false;
		}
		else {
			for (let alien of state.aliens) {
				if (alien.alive) {
					var x = state.missile.x - alien.x;
					var y = state.missile.y - alien.y;
					if (x > 0 && x < 22 && y > 0 && y < 16) {
						alien.alive = false;
						state.missile = false;
						state.missileSound.stop();
						noiseBuffer = audioCtx.createBuffer(1, 14700, 44100);
						output = noiseBuffer.getChannelData(0);
						var previousSample;
						for(i = 0; i < 44100; i++) {
							if (i % 80 == 0)
								previousSample = Math.random() * 2 - 1;
							output[i] = previousSample;
						}
						noise = audioCtx.createBufferSource();
						noise.buffer = noiseBuffer;
						noise.start();
						noise.connect(gain);
					}
				}
			}
		}
	}

	if (state.alienMissile) {
		state.alienMissile.y += MISSILE_VELOCITY;
		if (state.alienMissile.y > 400 + MISSILE_LENGTH)
			state.alienMissile = false;
		else {
			var x = state.alienMissile.x - state.player.x;
			var y = state.alienMissile.y - state.player.y;
			if (x > 0 && x < 48 && y > 0 && y < 48) {
				if (state.missileSound)
					state.missileSound.stop();
				state.state = "game over";
				noiseBuffer = audioCtx.createBuffer(1, 44100, 44100);
				output = noiseBuffer.getChannelData(0);
				var previousSample;
				for(i = 0; i < 44100; i++) {
					if (i % 80 == 0)
						previousSample = Math.random() * 2 - 1;
					output[i] = previousSample;
				}
				noise = audioCtx.createBufferSource();
				noise.buffer = noiseBuffer;
				noise.start();
				noise.connect(gain);
			}
		}
	} else {
		alien = state.aliens[Math.floor(Math.random() * 16)];
		if (alien.alive) {
			state.alienMissile = {
				x: alien.x + 11,
				y: alien.y + 16
			};
		}
	}

	if (state.aliens[0].x == 10)
		state.aliensV = ALIEN_VELOCITY;
	if (state.aliens[0].x == 418)
		state.aliensV = -ALIEN_VELOCITY;
	for (alien of state.aliens) {
		alien.x += state.aliensV;
	}
	
	state.player.x += state.player.vx;
	if (state.player.x < 10)
		state.player.x = 10;
	if (state.player.x > 582)
		state.player.x  = 582;
	
}

window.onkeyup = (event) => {
	if (state.state == "playing") {
		if (event.keyCode == 37 && state.player.vx < 0 ||
			event.keyCode == 39 && state.player.vx > 0) {
			state.player.vx = 0;
		}
	}
}

window.onkeydown = (event) => {
	if (state.state == "playing") {
		if (event.keyCode == 37)
			state.player.vx = -2;
		else if (event.keyCode == 39)
			state.player.vx = 2;
		else if (event.keyCode == 32 && state.missile == false) {
			state.missile = { x: state.player.x + 24, y: state.player.y - MISSILE_LENGTH }
			state.missileSound = audioCtx.createOscillator();
			state.missileSound.type = "sawtooth";
			state.missileSound.frequency.value = c64HertzFactor * 8448;
			state.missileSound.connect(gain);
			state.missileSound.start();
		}
	}
}	

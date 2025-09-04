const wheel = document.getElementById('wheel');
const btn = document.getElementById('spinBtn');
const resultEl = document.getElementById('result');
const confettiCanvas = document.getElementById('confetti');
const ctx = confettiCanvas.getContext && confettiCanvas.getContext('2d');

let spinning = false;
const count = 8;
const sectorAngle = 360 / count;

function resizeCanvas(){
	if(!ctx) return;
	confettiCanvas.width = innerWidth;
	confettiCanvas.height = innerHeight;
}
addEventListener('resize', resizeCanvas);
resizeCanvas();

btn.addEventListener('click', () => {
	if(spinning) return;
	spinning = true;
	btn.disabled = true;
	resultEl.textContent = 'Крутим...';
	wheel.classList.add('spinning');

	// случайный выигрышный индекс от 0 до count-1
	const chosen = Math.floor(Math.random() * count);

	// число полных оборотов (визуально эффектно) и угол, чтобы центр сектора совпал с указателем (вверх)
	const spins = Math.floor(Math.random() * 3) + 5; // 5-7 полных оборотов
	const centerAngle = chosen * sectorAngle + (sectorAngle / 2);
	const finalDeg = spins * 360 + (360 - centerAngle);

	// длительность адаптируем к spins
	const duration = 4000 + spins * 600; // ms
	wheel.style.transition = `transform ${duration}ms cubic-bezier(.12,.68,.28,1)`;
	// запускаем вращение
	requestAnimationFrame(()=> {
		wheel.style.transform = `rotate(${finalDeg}deg)`;
	});

	// по окончании анимации показываем результат
	const onEnd = () => {
		wheel.style.transition = '';
		wheel.classList.remove('spinning');
		spinning = false;
		btn.disabled = false;
		resultEl.textContent = `Вы выиграли: ${getLabel(chosen)}`;
		launchConfetti();
		wheel.removeEventListener('transitionend', onEnd);
	};
	wheel.addEventListener('transitionend', onEnd);
});

function getLabel(i){
	const labels = ['Звезда','Подарок','Монеты','Алмаз','Любовь','Трофей','Ракета','Сюрприз'];
	return labels[i] || `Сектор ${i+1}`;
}

/* простая confetti-анимация на canvas */
function launchConfetti(){
	if(!ctx) return;
	const pieces = [];
	const colors = ['#ff5c7c','#ffd166','#6ee7b7','#7dd3fc','#c084fc'];
	for(let i=0;i<120;i++){
		pieces.push({
			x: Math.random()*confettiCanvas.width,
			y: -Math.random()*confettiCanvas.height*0.5,
			vx: (Math.random()-0.5)*6,
			vy: 2+Math.random()*6,
			size: 6+Math.random()*8,
			color: colors[Math.floor(Math.random()*colors.length)],
			rot: Math.random()*360,
			velRot: (Math.random()-0.5)*10,
			alpha: 1
		});
	}
	let t = 0;
	function frame(){
		t++;
		ctx.clearRect(0,0,confettiCanvas.width,confettiCanvas.height);
		for(let p of pieces){
			p.x += p.vx;
			p.y += p.vy;
			p.vy += 0.08; // gravity
			p.rot += p.velRot;
			p.alpha -= 0.004;
			ctx.save();
			ctx.globalAlpha = Math.max(0, p.alpha);
			ctx.translate(p.x,p.y);
			ctx.rotate(p.rot*Math.PI/180);
			ctx.fillStyle = p.color;
			ctx.fillRect(-p.size/2, -p.size/2, p.size, p.size*0.6);
			ctx.restore();
		}
		// убрать старые
		if(t < 220){
			requestAnimationFrame(frame);
		} else {
			ctx.clearRect(0,0,confettiCanvas.width,confettiCanvas.height);
		}
	}
	frame();
}

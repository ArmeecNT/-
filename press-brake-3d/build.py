from pathlib import Path
root=Path(__file__).resolve().parent
head='''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TOPSTANKI • Станина 3D</title><style>
*{box-sizing:border-box}body{margin:0;background:#edf1f0;color:#172c26;font:14px system-ui,Segoe UI,sans-serif}header{height:72px;background:#123c30;color:white;display:flex;align-items:center;justify-content:space-between;padding:0 26px}h1{font-size:19px;margin:0}header small{color:#abc7bc}b.logo{letter-spacing:2px;color:#ff973d}main{display:grid;grid-template-columns:290px 1fr;height:calc(100vh - 72px);height:calc(100dvh - 72px)}aside{background:#fff;padding:25px 22px;overflow:auto;border-right:1px solid #dce4df}h2{font-size:12px;text-transform:uppercase;letter-spacing:1.5px;margin:0 0 14px;color:#6c8077}.sizes{display:grid;grid-template-columns:1fr 1fr;gap:8px}button{font:inherit;border:1px solid #d1ddd6;border-radius:8px;background:white;color:#153f31;padding:11px;cursor:pointer}button:hover{background:#edf5f0}button.active{background:#176749;color:white;border-color:#176749}section{margin-bottom:25px}dl{display:grid;grid-template-columns:1fr auto;gap:12px;font-size:13px}dt{color:#687e73}dd{margin:0;font-weight:600}.views{display:grid;grid-template-columns:1fr 1fr;gap:7px}.wide{width:100%;margin-top:8px}.export{background:#f18a33;color:#172d24;border:0;font-weight:650}label{display:block;margin:12px 0}p.note{font-size:12px;line-height:1.6;color:#738078}.stage{position:relative;min-width:0;overflow:hidden}canvas{width:100%;height:100%;display:block;touch-action:none}.badge{position:absolute;top:20px;left:24px;background:#ffffffdc;border:1px solid #dbe3de;padding:12px 16px;border-radius:10px;pointer-events:none}.badge strong{font-size:22px}.help{position:absolute;bottom:18px;left:24px;color:#567065;font-size:12px;pointer-events:none}#error{display:none;position:absolute;inset:25%;background:white;padding:25px;color:#a32b15}@media(max-width:700px){main{grid-template-columns:210px 1fr}aside{padding:18px 12px}header{padding:0 15px}h1{font-size:15px}.badge{left:12px;top:12px}.help{left:12px;max-width:200px}}
</style><header><div><b class="logo">TOPSTANKI</b><h1>Станина • траверса • гидравлика</h1></div><small>3D / v3.3</small></header><main><aside><section><h2>Рабочая длина, мм</h2><div class="sizes" id="sizes"></div></section><section><h2>Положение плиты</h2><label for="stroke">Ход вниз: <b id="strokeValue">0 мм</b></label><input id="stroke" type="range" min="0" max="200" step="1" value="0" style="width:100%;accent-color:#176749"><div class="views"><button id="up">ВМТ · 425 мм</button><button id="down">НМТ · 225 мм</button></div><button class="wide" id="animate">▶ Показать ход</button><dl><dt>Зазор над столом</dt><dd id="clearance">425 мм</dd><dt>Полный ход</dt><dd>200 мм</dd><dt>Толщина плиты</dt><dd>40 мм</dd><dt>Нижний участок</dt><dd>55 × 100 мм</dd></dl><p class="note">Зазор от нижней кромки подвижной плиты до верха стола, без инструмента.</p></section><section><h2>Гидравлика</h2><p class="note" id="hydroNote"></p></section><section><h2>Геометрия</h2><dl><dt>Рабочая длина</dt><dd id="lengthValue">3200 мм</dd><dt>Просвет между стенками</dt><dd id="gapValue">2600 мм</dd><dt>Отступы от краёв</dt><dd>300 + 300 мм</dd><dt>Высота</dt><dd>2950 мм</dd><dt>Глубина основания</dt><dd>2000 мм</dd><dt>Ширина стола</dt><dd>210 мм</dd><dt>Выступ низа боковин</dt><dd>72,5 мм</dd><dt>Боковины</dt><dd>40 мм</dd><dt>Глубина зева</dt><dd>350 мм</dd><dt>Смещение балки</dt><dd>150 мм</dd><dt>Болтов / цилиндр</dt><dd>8 · всего 16</dd><dt>Рёбер / плита</dt><dd>2</dd></dl></section><section><h2>Вид</h2><div class="views"><button data-view="iso">Общий</button><button data-view="front">Спереди</button><button data-view="side">Сбоку</button><button data-view="rear">Сзади</button></div><button class="wide" data-view="top">Сверху</button><button class="wide" id="boltsView">Крепление цилиндра · крупно</button><input id="edges" type="checkbox" hidden><p class="note">Совместимый режим 3D · без WebGL</p><label><input id="grid" type="checkbox" checked> Сетка пола</label><button class="wide" id="fit">Вписать в экран</button></section><button class="wide export" id="obj">Скачать модель OBJ</button><button class="wide" id="scad">Скачать модель OpenSCAD</button><p class="note">Вращение — левая кнопка мыши.<br>Перемещение — правая кнопка.<br>Масштаб — колесо; на телефоне — два пальца.</p><p class="note">Схематичная модель выбранного варианта. Недостающие размеры деталей приняты для визуализации. Не является рабочим чертежом или расчётом на 160 тс. Глубина основания — от переднего до заднего края опор. Зев — от оси инструмента до задней границы выреза.</p></aside><div class="stage" id="stage"><canvas id="c"></canvas><div class="badge"><small>СБОРКА / БЕЗ ИНСТРУМЕНТА</small><br><strong id="badge">3200 мм</strong></div><div class="help">Выберите длину • вращайте модель • скачайте геометрию</div><div id="error"></div><noscript><div style="position:absolute;inset:25%;background:white;padding:24px">Для интерактивной модели скачайте этот HTML-файл и откройте его в Chrome, Edge или Яндекс Браузере с включённым JavaScript.</div></noscript></div></main><script>'''
js=r'''
const scene=new THREE.Scene();scene.background=new THREE.Color(0xedf1f0);
const canvas=document.getElementById('c'),stage=document.getElementById('stage');

// Canvas projection uses the same real meshes and camera without requiring WebGL.
class CompatibleRenderer{
 constructor(canvas){this.canvas=canvas;this.ctx=canvas.getContext('2d');this.ratio=1;if(!this.ctx)throw Error('Canvas 2D недоступен');}
 setPixelRatio(r){this.ratio=1}
 setSize(w,h){this.w=Math.max(1,w);this.h=Math.max(1,h);const pw=Math.round(this.w*this.ratio),ph=Math.round(this.h*this.ratio);if(this.canvas.width!==pw||this.canvas.height!==ph){this.canvas.width=pw;this.canvas.height=ph;}}
 render(scene,camera){
 const c=this.ctx,w=this.w,h=this.h;c.setTransform(this.ratio,0,0,this.ratio,0,0);c.fillStyle='#edf1f0';c.fillRect(0,0,w,h);
 scene.updateMatrixWorld(true);camera.updateMatrixWorld(true);
 const vp=new THREE.Matrix4().multiplyMatrices(camera.projectionMatrix,camera.matrixWorldInverse);
 const project=(x,y,z)=>{const v=new THREE.Vector3(x,y,z).applyMatrix4(vp);return [(v.x+1)*w/2,(1-v.y)*h/2,v.z]};
 if(document.getElementById('grid').checked){c.strokeStyle='#d3ddd6';c.lineWidth=.6;for(let k=-4000;k<=4000;k+=200){for(const line of [[[k,-4,-4000],[k,-4,4000]],[[-4000,-4,k],[4000,-4,k]]]){const a=project(...line[0]),b=project(...line[1]);c.beginPath();c.moveTo(a[0],a[1]);c.lineTo(b[0],b[1]);c.stroke()}}}
 const tris=[];const light=new THREE.Vector3(-.35,.75,.55).normalize();
 scene.traverse(o=>{if(!o.isMesh||!o.visible)return;const g=o.geometry,pos=g.attributes.position,idx=g.index;const mv=new THREE.Matrix4().multiplyMatrices(vp,o.matrixWorld);const coords=new Array(pos.count),world=new Array(pos.count);for(let i=0;i<pos.count;i++){const v=new THREE.Vector3().fromBufferAttribute(pos,i);world[i]=v.clone().applyMatrix4(o.matrixWorld);v.applyMatrix4(mv);coords[i]=[(v.x+1)*w/2,(1-v.y)*h/2,v.z]}
 const color=o.material.color;const count=idx?idx.count:pos.count;
 for(let j=0;j<count;j+=3){const ia=idx?idx.getX(j):j,ib=idx?idx.getX(j+1):j+1,ic=idx?idx.getX(j+2):j+2;const a=coords[ia],b=coords[ib],d=coords[ic];const area=(b[0]-a[0])*(d[1]-a[1])-(b[1]-a[1])*(d[0]-a[0]);if(area>=-.005)continue;if(Math.max(a[0],b[0],d[0])<0||Math.min(a[0],b[0],d[0])>w||Math.max(a[1],b[1],d[1])<0||Math.min(a[1],b[1],d[1])>h)continue;
 const n=new THREE.Vector3().subVectors(world[ib],world[ia]).cross(new THREE.Vector3().subVectors(world[ic],world[ia])).normalize();const shade=.65+.35*Math.max(0,n.dot(light));const srgb=color.clone().convertLinearToSRGB();const rgb=[srgb.r,srgb.g,srgb.b].map(v=>Math.round(Math.min(255,v*255*shade)));tris.push({a,b,d,z:(a[2]+b[2]+d[2])/3,fill:`rgb(${rgb.join(',')})`,rgb});}
 });
 const iw=this.canvas.width,ih=this.canvas.height;
 const image=c.getImageData(0,0,iw,ih),pixels=image.data;
 if(!this.depth||this.depth.length!==iw*ih)this.depth=new Float32Array(iw*ih);const depth=this.depth;depth.fill(Infinity);
 for(const t of tris){const [a,b,d]=[t.a,t.b,t.d];const area=(b[0]-a[0])*(d[1]-a[1])-(b[1]-a[1])*(d[0]-a[0]);
 const x0=Math.max(0,Math.floor(Math.min(a[0],b[0],d[0]))),x1=Math.min(iw-1,Math.ceil(Math.max(a[0],b[0],d[0]))),y0=Math.max(0,Math.floor(Math.min(a[1],b[1],d[1]))),y1=Math.min(ih-1,Math.ceil(Math.max(a[1],b[1],d[1])));
 const ux=(b[1]-d[1])/area,vx=(d[1]-a[1])/area;
 for(let y=y0;y<=y1;y++){const py=y+.5,px=x0+.5;let u=((b[0]-px)*(d[1]-py)-(b[1]-py)*(d[0]-px))/area,v=((d[0]-px)*(a[1]-py)-(d[1]-py)*(a[0]-px))/area;
 for(let x=x0;x<=x1;x++,u+=ux,v+=vx){if(u<-.00001||v<-.00001||u+v>1.00001)continue;const z=u*a[2]+v*b[2]+(1-u-v)*d[2],i=y*iw+x;if(z>=depth[i])continue;depth[i]=z;const q=i*4;pixels[q]=t.rgb[0];pixels[q+1]=t.rgb[1];pixels[q+2]=t.rgb[2];pixels[q+3]=255;}
 }}c.putImageData(image,0,0);
 this.trianglesDrawn=tris.length;
 }
}
const renderer=new CompatibleRenderer(canvas);renderer.setPixelRatio(Math.min(devicePixelRatio,2));
const camera=new THREE.OrthographicCamera();scene.add(new THREE.HemisphereLight(0xffffff,0x687b71,2.3));
for(const [x,y,z,i] of [[-3000,6000,4000,2.8],[4000,3000,-2000,1.4]]){const l=new THREE.DirectionalLight(0xffffff,i);l.position.set(x,y,z);scene.add(l)}
const mat=new THREE.MeshStandardMaterial({color:0x969f9c,roughness:.62,metalness:.28});
const plateMat=new THREE.MeshStandardMaterial({color:0xb6bcb9,roughness:.47,metalness:.35});
const lineMat=new THREE.LineBasicMaterial({color:0x485a51,transparent:true,opacity:.34});
let stroke=0,moving=[],rods=[],running=false,animationTime=0;
let group,parts=[],L=3200,yaw=2.95,pitch=.28,zoom=1,panX=0,panY=0;
const floor=new THREE.GridHelper(8000,40,0xc2cec6,0xdce4de);floor.position.y=-4;scene.add(floor);
function add(geo,x,y,z,name,material=mat){const m=new THREE.Mesh(geo,material);m.position.set(x,y,z);m.name=name;group.add(m);parts.push(m);const e=new THREE.LineSegments(new THREE.EdgesGeometry(geo,22),lineMat);e.visible=document.getElementById('edges').checked;m.add(e);return m}
function box(w,h,d,x,y,z,name){return add(new THREE.BoxGeometry(w,h,d),x,y,z,name)}
function extrudeShape(shape,t){return new THREE.ExtrudeGeometry(shape,{depth:t,bevelEnabled:false,curveSegments:32})}
// Y vertical, X along bending length, Z toward operator. Sidewall front is Z=0.
function sideShape(){const s=new THREE.Shape();s.moveTo(-72.5,0);s.lineTo(1717.5,0);s.lineTo(1717.5,2950);s.lineTo(0,2950);s.lineTo(0,1700);s.absellipse(0,1350,172.5,350,Math.PI/2,-Math.PI/2,true);s.lineTo(-72.5,1000);s.lineTo(-72.5,0);return s}
function build(){if(group){scene.remove(group);group.traverse(o=>{if(o.geometry)o.geometry.dispose()})}group=new THREE.Group();scene.add(group);parts=[];moving=[];rods=[];
for(const sign of [-1,1]){const x=sign*(L/2-280);let g=extrudeShape(sideShape(),40);g.rotateY(Math.PI/2);add(g,x-20,0,0,'Sidewall_'+sign);
box(260,50,2000,x,25,-717.5,'Foot_'+sign);
const s=new THREE.Shape();s.moveTo(-110,0);s.lineTo(110,0);s.lineTo(110,800);s.lineTo(-110,800);s.closePath();for(const hx of [-65,65])for(const hy of [65,225,575,735]){const hole=new THREE.Path();hole.absarc(hx,hy,20,0,Math.PI*2,true);s.holes.push(hole)}
add(extrudeShape(s,40),x,2000,0,'Cylinder_plate_'+sign,plateMat);
for(const y of [2120,2450])box(220,25,420,x,y,-210,'Horizontal_rib_'+sign+'_'+y);
// Foot gussets only. No diagonal gussets behind cylinder mounting plates.
for(const dx of [-75,75]){const t=new THREE.Shape();t.moveTo(-300,50);t.lineTo(200,50);t.lineTo(-60,420);t.closePath();const gg=extrudeShape(t,20);gg.rotateY(Math.PI/2);add(gg,x+dx-10,0,-600,'Foot_gusset_'+sign+'_'+dx)}
}
box(L,1000,210,0,500,177.5,'Lower_bed');
const inner=L-600;
box(inner,550,40,0,2500,-170,'Upper_web');
box(inner,40,650,0,2220,-475,'Upper_flange_2220');

box(inner,180,45,0,150,-1120,'Rear_lower_tie');
buildActuators();
buildHydraulics();
// Taller ram: place fixed upper equipment for 425 mm daylight, preserve bottom working datums.
for(const p of parts)if(/^(Cylinder_|Gland_bolt_|Hydraulic_port_|Mount_bolt_|Horizontal_rib_|Upper_|Hydro_)/.test(p.name))p.position.y-=45;
setStroke(stroke);
document.getElementById('lengthValue').textContent=L+' мм';document.getElementById('gapValue').textContent=(L-600)+' мм';document.getElementById('badge').textContent=L+' мм';document.querySelectorAll('[data-length]').forEach(b=>b.classList.toggle('active',+b.dataset.length===L));render();}

const rodMetal=new THREE.MeshStandardMaterial({color:0xd0d8da,roughness:.23,metalness:.75});
const dark=new THREE.MeshStandardMaterial({color:0x35413d,roughness:.45,metalness:.5});
function cyl(radius,height,x,y,z,name,material=rodMetal){return add(new THREE.CylinderGeometry(radius,radius,height,48),x,y,z,name,material)}
function buildActuators(){
for(const sign of [-1,1]){const x=sign*(L/2-280);
// Blind rear attachment holes match the fixed plate; closed smooth front face.
const back=new THREE.Shape();back.moveTo(-130,0);back.lineTo(130,0);back.lineTo(130,800);back.lineTo(-130,800);back.closePath();
for(const hx of [-65,65])for(const hy of [65,225,575,735]){const h=new THREE.Path();h.absarc(hx,hy,20,0,Math.PI*2,true);back.holes.push(h)}
add(extrudeShape(back,20),x,2000,40,'Cylinder_rear_'+sign,plateMat);
// Eight rear-inserted bolts in the existing mounting-hole pattern. Nominal schematic sizes.
for(const dx of [-65,65])for(const y of [2065,2225,2575,2735]){
 const name=sign+'_'+dx+'_'+y;
 const shaft=cyl(18,66,x+dx, y,27,'Mount_bolt_shank_'+name,dark);shaft.rotation.x=Math.PI/2;
 const washerShape=new THREE.Shape();washerShape.absarc(0,0,35,0,Math.PI*2,false);const hole=new THREE.Path();hole.absarc(0,0,19,0,Math.PI*2,true);washerShape.holes.push(hole);
 add(extrudeShape(washerShape,6),x+dx,y,-6,'Mount_bolt_washer_'+name,rodMetal);
 const head=add(new THREE.CylinderGeometry(30,30,23,6),x+dx,y,-17.5,'Mount_bolt_head_'+name,dark);head.rotation.x=Math.PI/2;
}

box(260,800,240,x,2400,180,'Cylinder_body_'+sign);
cyl(115,60,x,1970,170,'Cylinder_gland_'+sign);
cyl(94,8,x,1936,170,'Cylinder_wiper_'+sign,dark);
for(let i=0;i<12;i++){const a=i*Math.PI/6;cyl(7,12,x+105*Math.cos(a),1934,170+105*Math.sin(a),'Gland_bolt_'+sign+'_'+i,dark)}
for(const y of [2110,2680]){const port=cyl(18,6,x+sign*133,y,170,'Hydraulic_port_'+sign+'_'+y,dark);port.rotation.z=Math.PI/2;}
const rod=cyl(90,1,x,1930,170,'Cylinder_rod_'+sign);rods.push(rod);
}
const half=L/2-480;
// Single stepped plate represented as two touching solids for exact 40/55 mm depths.
const s=new THREE.Shape();s.moveTo(-L/2,100);s.lineTo(L/2,100);s.lineTo(L/2,450);s.lineTo(half+30,450);s.quadraticCurveTo(half,450,half,480);s.lineTo(half,900);s.lineTo(-half,900);s.lineTo(-half,480);s.quadraticCurveTo(-half,450,-half-30,450);s.lineTo(-L/2,450);s.closePath();
const ram=add(extrudeShape(s,40),0,1425,150,'Ram_40mm',plateMat);moving.push({mesh:ram,y:1425});
const lip=box(L,100,55,0,1475,177.5,'Ram_lower_55x100');lip.material=plateMat;moving.push({mesh:lip,y:1475});
}
// Fixed schematic hydraulic equipment; positions use Y up and Z toward operator.
function buildHydraulics(){
 const note=document.getElementById('hydroNote');
 note.textContent=L===1600?'1600 мм: бак 1010 мм и мотор рядом не помещаются в просвет 1000 мм. Нужна отдельная компоновка.':'Бак 200 л полного объёма · сервомотор 10 кВт · насос · гидроблок на баке. Габариты компонентов условные.';
 if(L===1600)return;
 const tx=Math.min(0,(L-600-1710)/2),mx=tx+700;
 const hb=(w,h,d,x,y,z,n,m=plateMat)=>{const o=box(w,h,d,x,y,z,'Hydro_'+n);o.material=m;return o};
 const hc=(r,h,x,y,z,n,m=rodMetal,axis='y')=>{const o=cyl(r,h,x,y,z,'Hydro_'+n,m);if(axis==='z')o.rotation.x=Math.PI/2;if(axis==='x')o.rotation.z=Math.PI/2;return o};
 const pipe=(points,r,n,m=rodMetal)=>{for(let i=1;i<points.length;i++){const a=new THREE.Vector3(...points[i-1]),b=new THREE.Vector3(...points[i]),v=b.clone().sub(a);const o=hc(r,v.length(),...(a.clone().add(b).multiplyScalar(.5).toArray()),n+'_'+i,m);o.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),v.normalize());}for(let i=0;i<points.length;i++)add(new THREE.SphereGeometry(r,10,8),...points[i],'Hydro_'+n+'_elbow'+i,m);};
 // Hollow tank: inside 1000 x 500 x 400 = 200 liters, wall thickness 5 mm.
 hb(1010,5,510,tx,2242.5,-480,'Tank_bottom');hb(1010,5,510,tx,2647.5,-480,'Tank_lid');
 for(const sign of [-1,1]){hb(5,400,510,tx+sign*502.5,2445,-480,'Tank_end_'+sign);hb(1000,400,5,tx,2445,-480+sign*252.5,'Tank_side_'+sign);}
 for(const dx of [-460,0,460])for(const z of [-710,-250])hc(7,7,tx+dx,2654,z,'Lid_bolt');
 hc(28,22,tx-340,2661,-400,'Breather',dark);hc(42,65,tx-360,2682.5,-600,'Return_filter');
 hb(28,220,12,tx-60,2465,-742,'Sight_frame',dark);hb(12,185,6,tx-60,2465,-751,'Sight_oil',new THREE.MeshStandardMaterial({color:0xc7a745}));
 hb(280,20,540,mx,2250,-485,'Motor_base');
 hb(240,230,270,mx,2380,-405,'Servo_10kW',dark);
 for(let i=-4;i<=4;i++)hb(245,7,260,mx,2380+i*23,-405,'Cooling_fin_'+i,dark);
 hb(260,260,20,mx,2380,-550,'Servo_flange');
 hc(102,70,mx,2380,-595,'Coupling_guard',rodMetal,'z');
 hb(150,150,125,mx,2380,-692.5,'Pump');
 for(const dx of [-60,60])hc(18,34,mx+dx,2512,-360,'Connector',dark);
 hb(450,15,200,tx+40,2657.5,-490,'Manifold_mount');
 hb(420,130,170,tx+40,2730,-490,'Manifold');
 for(const dx of [-100,40,160]){hb(65,55,110,tx+dx,2822.5,-480,'Valve_'+dx,dark);hc(25,80,tx+dx,2810,-570,'Solenoid_'+dx,dark,'z');}
 hc(17,110,tx-130,2850,-480,'Pressure_valve');
 hc(10,60,tx-120,2825,-560,'Gauge_stem');hc(42,24,tx-120,2870,-560,'Gauge',rodMetal,'z');hc(36,3,tx-120,2870,-574,'Gauge_face',new THREE.MeshStandardMaterial({color:0xf1f3ed}),'z');
 pipe([[tx+505,2320,-570],[mx-20,2320,-570],[mx-20,2320,-690],[mx,2320,-690]],22,'Suction',dark);
 pipe([[mx+75,2380,-690],[mx+100,2380,-690],[mx+100,2690,-690],[tx+250,2690,-690],[tx+250,2730,-490]],9,'Pressure');
 pipe([[tx-170,2730,-490],[tx-280,2730,-490],[tx-280,2690,-600],[tx-360,2690,-600]],15,'Return');
 for(const sign of [-1,1]){
 const cx=sign*(L/2-280),ix=sign*(L/2-430);
 hb(90,90,80,cx,2845,170,'Prefill_'+sign);
 pipe([[tx+sign*400,2650,-300],[tx+sign*400,2845,-300],[ix,2845,-300],[ix,2845,170],[cx,2845,170]],24,'Fill_'+sign,dark);
 pipe([[cx,2800,170],[cx,2810,170]],20,'Cylinder_fill_'+sign,dark);
 for(let k=0;k<2;k++){
 const z=-780-k*28,yy=2160-k*45,x=tx+sign*(80+k*45);
 pipe([[x,2730,-575],[x,2730,z],[x,yy,z],[ix,yy,z],[ix,yy,170],[cx-sign*133,yy,170]],8,'Work_'+sign+'_'+k);
 for(const f of [.25,.6])hb(26,26,80,x+(ix-x)*f,yy,z,'Pipe_clamp_'+sign+'_'+k+'_'+f,dark);
 }
 }
}
// Export hydraulic meshes in the same Z-up convention as the parametric frame.
function hydraulicScad(){group.updateMatrixWorld(true);let out='\n// Hydraulic layout is fixed for exported length. Re-export after changing length.\n';out+='if (L == '+L+') {\n';for(const m of parts.filter(p=>p.name.startsWith('Hydro_'))){const g=m.geometry,pa=g.attributes.position,ix=g.index,pts=[];for(let i=0;i<pa.count;i++){const v=new THREE.Vector3().fromBufferAttribute(pa,i).applyMatrix4(m.matrixWorld);pts.push([v.x,-v.z,v.y].map(n=>+n.toFixed(3)));}const faces=[];const count=ix?ix.count:pa.count;for(let i=0;i<count;i+=3)faces.push([0,1,2].map(k=>ix?ix.getX(i+k):i+k));out+='// '+m.name+'\npolyhedron(points='+JSON.stringify(pts)+',faces='+JSON.stringify(faces)+',convexity=10);\n';}return out+'} else echo("Re-export hydraulic layout for the selected length");\n';}

function setStroke(value){stroke=Math.max(0,Math.min(200,Number(value)||0));for(const m of moving)m.mesh.position.y=m.y-stroke;for(const r of rods){r.scale.y=20+stroke;r.position.y=1895-(20+stroke)/2;}document.getElementById('stroke').value=stroke;document.getElementById('strokeValue').textContent=Math.round(stroke)+' мм';document.getElementById('clearance').textContent=Math.round(425-stroke)+' мм';render();}
function stop(){running=false;document.getElementById('animate').textContent='▶ Показать ход';}
document.getElementById('stroke').oninput=e=>{stop();setStroke(e.target.value)};
document.getElementById('up').onclick=()=>{stop();setStroke(0)};
document.getElementById('down').onclick=()=>{stop();setStroke(200)};
document.getElementById('animate').onclick=()=>{if(running){stop();return;}running=true;animationTime=0;document.getElementById('animate').textContent='Ⅱ Остановить';requestAnimationFrame(tick)};
function tick(t){if(!running)return;if(!animationTime)animationTime=t;setStroke(100*(1-Math.cos((t-animationTime)*Math.PI/4000)));requestAnimationFrame(tick)}

function render(){const w=stage.clientWidth,h=stage.clientHeight;renderer.setSize(w,h,false);let half=2100/zoom;camera.left=-half*w/h;camera.right=half*w/h;camera.top=half;camera.bottom=-half;camera.near=1;camera.far=30000;camera.updateProjectionMatrix();const target=new THREE.Vector3(0,1400,-450);camera.position.set(target.x+8000*Math.sin(yaw)*Math.cos(pitch),target.y+8000*Math.sin(pitch),target.z+8000*Math.cos(yaw)*Math.cos(pitch));camera.lookAt(target);camera.updateMatrixWorld();const right=new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld,0),up=new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld,1);camera.position.addScaledVector(right,panX).addScaledVector(up,panY);camera.updateMatrixWorld();renderer.render(scene,camera)}
document.getElementById('boltsView').onclick=()=>{yaw=2.75;pitch=.08;zoom=2.35;panX=-(L/2-280)*Math.cos(Math.PI-yaw);panY=1150;render()};
function fit(){zoom=Math.min(1,stage.clientWidth/stage.clientHeight*3800/(L+1300));panX=panY=0;render()}
for(const n of [1600,2000,2500,3200]){const b=document.createElement('button');b.textContent=n;b.dataset.length=n;b.onclick=()=>{L=n;build();fit()};document.getElementById('sizes').append(b)}
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>{const v={iso:[-.60,.24],front:[0,0],side:[-Math.PI/2,0],rear:[Math.PI,.15],top:[0,Math.PI/2-.001]}[b.dataset.view];[yaw,pitch]=v;fit()});
document.getElementById('edges').onchange=e=>{group.traverse(o=>{if(o.isLineSegments)o.visible=e.target.checked});render()};document.getElementById('grid').onchange=e=>{floor.visible=e.target.checked;render()};document.getElementById('fit').onclick=fit;
canvas.oncontextmenu=e=>e.preventDefault();const pointers=new Map();let lastPinch=0;
canvas.onpointerdown=e=>{canvas.setPointerCapture(e.pointerId);pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});lastPinch=0};canvas.onpointerup=canvas.onpointercancel=e=>{pointers.delete(e.pointerId);lastPinch=0};
canvas.onpointermove=e=>{if(!pointers.has(e.pointerId))return;const old=pointers.get(e.pointerId);const dx=e.clientX-old.x,dy=e.clientY-old.y;pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});if(pointers.size===2){const [a,b]=[...pointers.values()];const d=Math.hypot(a.x-b.x,a.y-b.y);if(lastPinch)zoom=Math.max(.3,Math.min(5,zoom*d/lastPinch));lastPinch=d}else if(e.buttons===2||e.shiftKey){panX-=dx*4200/zoom/stage.clientHeight;panY+=dy*4200/zoom/stage.clientHeight}else{yaw-=dx*.007;pitch=Math.max(-1.5,Math.min(1.5,pitch+dy*.006))}render()};
canvas.onwheel=e=>{e.preventDefault();zoom=Math.max(.3,Math.min(5,zoom*Math.exp(-e.deltaY*.001)));render()};
function download(text,name){const u=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),1000)}
function objText(){group.updateMatrixWorld(true);let out='# TOPSTANKI frame; units mm; schematic model\n',offset=1;for(const p of parts){out+='o '+p.name+'\n';const g=p.geometry.index?p.geometry.toNonIndexed():p.geometry;const pos=g.attributes.position;for(let i=0;i<pos.count;i++){const v=new THREE.Vector3().fromBufferAttribute(pos,i).applyMatrix4(p.matrixWorld);out+=`v ${v.x.toFixed(4)} ${v.y.toFixed(4)} ${v.z.toFixed(4)}\n`}for(let i=0;i<pos.count;i+=3)out+=`f ${offset+i} ${offset+i+1} ${offset+i+2}\n`;offset+=pos.count;if(g!==p.geometry)g.dispose()}return out}
document.getElementById('obj').onclick=()=>download(objText(),'TOPSTANKI-frame-'+L+'.obj');
function scadText(){return `// Schematic frame, millimeters. Not a fabrication drawing.\nL = ${L}; // [1600,2000,2500,3200]\nstroke = ${stroke.toFixed(3)}; // [0:200]\n$fn=64;\nmodule box(s,p){translate(p)cube(s,center=true);}\nmodule side(){rotate([90,0,90])linear_extrude(40,center=true)difference(){polygon([[-72.5,0],[1717.5,0],[1717.5,2950],[0,2950],[0,1000],[-72.5,1000]]);translate([0,1350])scale([172.5,350])circle(1);}}\nfor(sign=[-1,1]){x=sign*(L/2-280);translate([x,0,0])side();box([260,2000,50],[x,717.5,25]);translate([x,-20,2355])difference(){cube([220,40,800],center=true);for(dx=[-65,65],dz=[-335,-175,175,335])translate([dx,0,dz])rotate([90,0,0])cylinder(h=60,r=20,center=true);}for(z=[2075,2405])box([220,420,25],[x,210,z]);for(dx=[-75,75])translate([x+dx,600,0])rotate([90,0,90])linear_extrude(20,center=true)polygon([[300,50],[-200,50],[60,420]]);}\nbox([L,210,1000],[0,-177.5,500]);\nbox([L-600,40,550],[0,170,2455]);box([L-600,650,40],[0,475,2175]);box([L-600,45,180],[0,1120,150]);\nfor(sign=[-1,1]){x=sign*(L/2-280);difference(){box([260,260,800],[x,-170,2355]);for(dx=[-65,65],z=[2020,2180,2530,2690])translate([x+dx,-39,z])rotate([90,0,0])cylinder(h=21,r=20);}for(dx=[-65,65],z=[2020,2180,2530,2690]){translate([x+dx,-27,z])rotate([90,0,0])cylinder(h=66,r=18,center=true);translate([x+dx,3,z])rotate([90,0,0])difference(){cylinder(h=6,r=35,center=true);cylinder(h=8,r=19,center=true);}translate([x+dx,17.5,z])rotate([90,0,0])cylinder(h=23,r=30,center=true,$fn=6);}translate([x,-170,1895])cylinder(h=60,r=115);translate([x,-170,1887])cylinder(h=8,r=94);translate([x,-170,1875-stroke])cylinder(h=20+stroke,r=90);for(i=[0:11])translate([x+105*cos(i*30),-170-105*sin(i*30),1883])cylinder(h=12,r=7);for(z=[2065,2635])translate([x+sign*133,-170,z])rotate([0,90,0])cylinder(h=6,r=18,center=true);}\na=L/2-480;\nunion(){translate([0,-150,1425-stroke])rotate([90,0,0])linear_extrude(40)polygon(concat([[-L/2,100],[L/2,100],[L/2,450],[a+30,450]],[for(i=[1:32])let(t=i/32)[a+30*(1-t)*(1-t),450+30*t*t]],[[a,900],[-a,900],[-a,480]],[for(i=[1:32])let(t=i/32)[-a-30*t*t,450+30*(1-t)*(1-t)]],[[-L/2,450]]));box([L,55,100],[0,-177.5,1475-stroke]);}\n`}
document.getElementById('scad').onclick=()=>download(scadText()+hydraulicScad(),'TOPSTANKI-frame-parametric.scad');
window.frameAPI={setLength:n=>{if(![1600,2000,2500,3200].includes(n))throw Error('length');L=n;build();fit()},getParts:()=>parts,getLength:()=>L,getRenderer:()=>renderer,setStroke,getStroke:()=>stroke,scadText,hydraulicScad,objText};
build();fit();if(typeof ResizeObserver!=='undefined')new ResizeObserver(()=>render()).observe(stage);else window.addEventListener('resize',render);
'''
(root/'index.html').write_text(head+(root/'vendor'/'three.min.js').read_text()+'</script><script>'+js+'</script></html>')

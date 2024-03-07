import os, io, time, sys
from PIL import Image, ImageDraw
import discord
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from random import *
from math import *
from colorsys import hsv_to_rgb 
uf = uniform
rint = randint
def rmint(): return rint(-1*sys.maxsize, sys.maxsize)
def mul(c1, c2):
  return (c1[0] * c2[0], c1[1] * c2[1], c1[2] * c2[2])
def sub(c1, c2):
  return (c1[0] - c2[0], c1[1] - c2[1], c1[2] - c2[2])
def cast(c):
  return (int(c[0]), int(c[1]), int(c[2]))
def alpha(c, a):
  return (c[0], c[1], c[2], a)
def to_rgb(c):
  return cast((c[0]*255, c[1]*255, c[2]*255))
def hsv(h, s, v):
  return to_rgb(hsv_to_rgb(h, s, v))
def limit(c, mx=1, stop=False):
  if c < 0:
    return 0 if stop else limit(c + 1, mx, False)
  elif c > mx:
    return mx if stop else limit(c - 1, mx, False)
  return c
def prob(p): return rint(0,100) < p
##### my preferences ######
admin_id = 1197983067726426204
api = os.environ['API']
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
mgdb = os.environ["MGDB"]
mclient = MongoClient(mgdb, server_api=ServerApi('1'))
try:
    mclient.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = mclient.users # you have to create a database called users
users = db.users # you have to create a collection called users
def emp_opt():
  return {
      "seed":None,
      "col1":None,
      "col2":None,
      "scl":None,
      "atm":None,
      "ring":None,
      "ring_col":None,
      "moon":None, 
      "star":None,
      "sky":None
  }
def r_opt(yem=None):
  if yem is None:
    seed()
    yem = rmint()
  seed(yem)
  bc1 = uf(0,1)
  bc2 = limit(bc1+choice([-1,1])*uf(1/16,1/2))
  mon = rint(0,3) == 1
  return {
    "seed":yem,
    "col1":bc1,
    "col2":bc2,
    "scl":round(32/(1+pow(uf(0,1), 10))),
    "atm":hsv(uf(0,1),0.3,0.8) if rint(0,6) == 1 else None,
    "tatm":0,#rint(0,1),
    "ring":rint(0,3) if not mon else 0,
    "ring_col":uf(0,1),
    "moon": uf(0,1) if mon else None, 
    "star":uf(0,1) if rint(0,2) != 1 else None,
    "sky":limit(choice([bc1, bc2])+choice([-1,1])*uf(0.07,0.252))
  }
def atm_hole(yem=None, r=16, col=(0,0,0)):
  seed(yem)
  sz = 96
  im = Image.new('RGBA', (sz, sz), (0, 0, 0, 0))
  pix = im.load()
  fac = uf(0.1,0.5)
  for i in range(sz):
    x = i-sz/2
    mx = abs(x/sz*2)
    for j in range(sz):
      y = j-sz/2
      dis = (x*x+y*y)/r**2
      df = dis-(abs(y)+1)/sz/2
      if df < 1:
        pix[i,j] = alpha(col,floor(255*df)) 
  return im
def create_pla(yem=None, opt=None, resize=False):
  #init pla
  w, h = 32, 32
  ow, oh = w*3, h*3
  out = Image.new("RGBA", (ow, oh), (0,0,0,0))
  # options
  if opt is None:
    opt = r_opt(yem)
  else:# type(opt) is type({}):
    topt = r_opt(yem)
    topt.update(opt)
    opt = topt
  seed(opt["seed"])
  #colors
  bc1 = opt["col1"]
  bc2 = opt["col2"] 
  rl = uf(1,8)
  rb = uf(-0.2,0.2)
  cw, cb = uf(0.4,0.95), uf(0.6,0.95)
  #planet
  im = Image.new('RGBA', (w, h), (0,0,0,0)) 
  pix = im.load()
  t = 0
  for x in range(0,w):
    t = x/rl
    for y in range(0,h):
      rc = uf(-0.1,0.1) 
      c1 = hsv(limit(bc1+rc),cw,cb)
      c2 = hsv(limit(bc2+rc),cw,cb)
      s = sin(t)
      ds = (s+1)/2 *100
      pix[x,y] = c2 if prob(ds+10)else c1
      t += 0.5 + rb
  mask = Image.new('L', (w, h), 0)
  draw = ImageDraw.Draw(mask)
  aw, ah = rint(-2,0), rint(-2,0) 
  nsz = opt["scl"]
  draw.ellipse((0,0,nsz+aw,nsz+ah), fill=255)
  pla = Image.new('RGBA',(nsz,nsz),(0,0,0,0))
  pla.paste(im, (0, 0), mask)
  #atmosphere
  at = opt["atm"]
  if at is not None:
    atc = at
    if opt["tatm"] == 0 or opt["ring"] != 0:
      at = Image.new('RGBA', (ow, oh), (0,0,0,0))
      ats = uf(0.5,1.1)
      mxat = nsz/192+uf(0.05,0.1)
      apix = at.load()
      swmt = 0
      for x in range(ow):
        _x = x/ow-0.5
        for y in range(oh):
          _y = y/oh-0.5
          d = sqrt(_x**2+_y**2)
          if d < mxat:
            apix[x,y] = alpha(atc,int(abs(swmt-d/mxat)**ats*255))
    else:
      at = atm_hole(yem=opt["seed"], r=opt["scl"], col=atc)
  #rings
  cr = opt["ring_col"]
  cw, cb = uf(0.4,0.95), uf(0.4,0.95)
  rot = rint(0,360) 
  r = opt["ring"]
  qs = []
  for n in range(r):
    rs = rint(300,500)
    sx, sy = uf(0.5,1), uf(1.5,2)
    acr = uf(-0.1, 0.1) 
    q = Image.new('RGBA', (ow, oh), (0,0,0,0)) 
    hpix = q.load()
    mw, mh = w/2,h/2
    fr = sqrt(mw**2+mh**2) 
    for x in range(0,ow):
      for y in range(0,oh):
        dx = abs(x-ow//2)*sx
        dy = abs(y-oh//2)*sy
        dr = sqrt(dx**2+dy**2)
        if not prob((abs(fr-dr)**1/fr**1) *rs):
          rc = uf(-0.1,0.1)
          hpix[x,y] = hsv(limit(cr+acr+rc), cw, cb)
    ai = Image.new('RGBA', (ow, oh//2), (0,0,0,0))
    ro = rint(1,35)
    q1, q2 = q.copy(), q.copy()
    q1.paste(ai, (0,0))
    q2.paste(ai, (0,oh//2))
    qs.append([q1.rotate(rot +180*n/r+ro), q2.rotate(rot+180*n/r+ro)])
  for q in qs:
    out.paste(q[0], (0,0), q[0])
  if at is not None:
    out.paste(at, (0,0), at)  
  out.paste(pla, (ow//2-nsz//2, oh//2-nsz//2), pla)
  for q in qs:
    out.paste(q[1], (0,0), q[1]) 
  #flag
  def to_t(c): return hsv(c, 0.9, 0.9)
  colors = [to_t(bc1), to_t(bc2)]
  colors += [(0,0,0,255)]*rint(0,5)
  if False and opt["ring"] != 0 and rint(0,1)==1:
    colors.append(to_t(opt["ring_col"]))
  size = 8
  fim = Image.new('RGBA', (size, size), (255, 255, 255, 255))
  pix = fim.load()
  for x in range(size):
    for y in range(size):
      pix[x,y] = choice(colors)
  nim = Image.new('RGBA', (size*2, size), (255, 255, 255, 255)) 
  nim.paste(fim, (0,0))
  fim = fim.transpose(Image.FLIP_LEFT_RIGHT) 
  nim.paste(fim, (size,0))
  #falan
  fim = None
  if resize:
    out = out.resize((500,500), resample=Image.NEAREST)
    im = im.resize((500,500), resample=Image.NEAREST) 
    nim = nim.resize((1000,500), resample=Image.NEAREST) 
    fim = Image.new('RGBA', (1000, 1000), (0, 0, 0, 255))
  
    fim.paste(out, (0,0), out)
    fim.paste(im, (500,0))
    fim.paste(nim, (0,500))
  return {
    "out":out, 
    "tex":im, 
    "flag":nim, 
    "seed":yem, 
    "res":fim,
    "star":opt["star"],
    "pla":pla,
    "moon":opt["moon"], 
    "sky":opt["sky"]
  }
  #return [out,im,nim,yem,fim,star,pla,esmoone]
fstarim = Image.new('RGBA', (3, 3), (255, 255, 255, 255))
for x in [0,2]:
  for y in [0,2]:
    fstarim.putpixel((x,y), (0,0,0,0)) 
space_things = [None]*3
fspaceim = Image.open("space-sey.png")
for x in range(0,3):
  for y in range(0,2):
    spc = fspaceim.crop((x*15,y*15,(x+1)*15,(y+1)*15))
    space_things.append(spc)
def add_star(im, pix, w, h):
  pr = rint(60,90)
  for x in range(w):
    for y in range(h):
      if rint(0,pr) == 7:
        if rint(0,31) == 2:
          im.paste(fstarim, (x,y), fstarim)
        else:
          pix[x,y] = hsv(uf(0,1),0.1,1)
def fallin_star(yem=None, alp=255):
  seed(yem)
  w = rint(40,55)
  im = Image.new('RGBA', (w,w), (0, 0, 0, 0))
  pix = im.load()
  mcol = uf(0,1)
  cols = [limit(mcol+i/12) for i in range(3)]
  seed()
  for _x in range(6):
    x = w//2+_x-3
    for y in range(w):
      prob = 1 - (y/w)**2 - abs(3-_x)*y/(3*w)
      col = (0,0,0,0)
      if rint(0,100) < prob*100:
        c = int(y/w*len(cols))
        ch = c+choice([-1,0,0,1])
        ch = limit(ch, len(cols)-1, True)
        col = alpha(hsv(cols[ch], 1, 1), alp) 
      pix[x,y] = col
  pix[w//2+2,0] = pix[w//2-2,0] = (0,0,0,0)
  for x in [-1,0,1]:
    for y in [1,2]:
      pix[w//2+x,y] = (255,255,255,255)
  return im
def planet(id, opt=None, resize=True, starry=True):
  gif = []
  rsize = 350
  pln = create_pla(id, opt)
  pla = pln["out"]
  fla = pln["flag"]
  w, h = pla.size
  out = Image.new("RGBA", (w, h), (0,0,0,255))
  pix = out.load()
  mim = None
  if pln["moon"] is not None:
    monsz = rint(10,14)
    seed(pln["moon"]) 
    mopt = {
      "moon":None, 
      "ring":0,
      "atm":None,
      "col1":pln["moon"],
      "col2":limit(pln["moon"] + choice([-1,1])*uf(1/16,1/2))
    }
    mim = create_pla(pln["moon"], mopt)["pla"].resize((monsz,monsz), resample=Image.NEAREST)
  seed()
  if starry:
    add_star(out, pix, w, h)
  mrot = uf(0,3.14)
  away = rint(32,45)
  flstar = None
  flthing = None
  if rint(0,1) == 1 and starry:
    thng = choice(space_things)
    if thng is None:
      flstar = random()
    else:
      flthing = thng
  fltrot = rint(0,45)
  flrot = rint(150,210)
  flpos = [96.0,float(rint(30,66))]
  nf = w
  for i in range(nf):
    cout = out.copy()
    ir = i % w
    if starry:
      cim = Image.new("RGBA", (w, h), (0,0,0,255))
      cim.paste(cout.crop((ir, 0, w, h)),(0,0))
      cim.paste(cout.crop((0, 0, ir, h)),(w-ir,0))
      cout = cim
    if flthing is not None and i < 40:
      cthng = flthing.rotate(fltrot)
      cout.paste(cthng, (int(flpos[0]), int(flpos[1])), cthng)
      flpos[0] += cos(flrot/180*3.14)*4
      flpos[1] += sin(flrot/180*3.14)*4
      fltrot -= 2
    elif flstar is not None and i < 37:
      cflstar = fallin_star(flstar).rotate(270-flrot)
      cout.paste(cflstar, (int(flpos[0]), int(flpos[1])), cflstar)
      flpos[0] += cos(flrot/180*3.14)*4
      flpos[1] += sin(flrot/180*3.14)*4
    p = pla.rotate(i*(360/nf))
    cout.paste(p, (0,0), p)
    if pln["moon"] is not None:
      cmim = mim.rotate(i*3)
      cout.paste(cmim, (int(w//2+cos(mrot)*away) , int(h//2+sin(mrot)*away)), cmim)
      mrot += 3.14/nf*2
    cout.paste(fla, (0,0))
    if resize:
      cout = cout.resize((rsize,rsize), resample=Image.NEAREST)
    gif.append(cout)
  print(flstar)
  return gif
def go_pla(fro, to):
  c1, c2 = create_pla(fro), create_pla(to)
  p1, p2 = planet(c1[0],c1[2],c1[7],False), planet(c2[0],c2[2],c2[7],False) 
  nf = len(p1)
  gif = []
  for i in range(nf):
    out = Image.new("RGBA", (96*2,96), (0,0,0,255))
    out.paste(p1[i],(0,0),p1[i])
    out.paste(p2[i],(96,0),p2[i])
    gif.append(out)
  return gif

def set_pla(yem):
  seed(yem)
  w = 96
  seeds = [rmint() for _ in range(9)]
  plas = [planet(seeds[i], False) for i in range(9)]
  gif = []
  im = Image.new("RGBA", (w*3, w*3), (0,0,0,0))
  for n in range(w):
    for j in range(3):
      for i in range(3):
        im.paste(plas[i*3+j][n], (w*i, w*j))
    gif.append(im.resize((w*3*3, w*3*3), resample=Image.NEAREST))
  return gif, seeds
def set_im(yem, count):
  seed(yem)
  w = 96
  #count = 20
  seeds = [rmint() for _ in range(count**2)]
  crats = [create_pla(seeds[i]) for i in range(count**2)]
  out = Image.new("RGBA", (w*count, w*count), (0,0,0,255))
  pix = out.load()
  for x in range(w*count):
    for y in range(w*count):
      if rint(0,65) == 7:
        pix[x,y] = (255,255,255)
        
  for i in range(count):
    for j in range(count):
      pos = i*count+j
      p = crats[pos]["out"]
      f = crats[pos]["flag"]
      out.paste(p, (w*j, w*i), p)
      out.paste(f, (w*j, w*i), f)
  return out.resize((w*count*2,w*count*2),resample=Image.NEAREST), seeds
  
def blend(c1, c2, per, s=1):
  o1 = (per/100)**s
  o2 = (100 - o1)/100
  return (c1[0]*o1 + c2[0]*o2, c1[1]*o1 + c2[1]*o2, c1[2]*o1 + c2[2]*o2, 255)
def sky(t, sun, at):
  ss = 48
  sx, sy = 2*ss, (3*ss)//2
  im = Image.new('RGBA', (sx, sy), (0, 0, 0, 255))
  pix = im.load()
  ws = rint(4,8)
  bsc1 = uf(0,1)
  colors = [hsv(limit(bsc1+uf(-0.2,0.2)), 1, 0.8) for _ in range(3) ]
  lcol = len(colors)
  lcol1 = lcol - 1
  for i in range(lcol1):
    c1 = colors[i]
    c2 = colors[i+1]
    dv = 1/(sy/lcol1)
    fac = mul(sub(c1, c2), (dv, dv, dv))
    s = int(i*sy/lcol1)
    e = int((i+1)*sy/lcol1)
    for y in range(s, e):
      for x in range(sx):
        pix[x,y] = cast(blend(c1,(0,0,0),t))
        if rint(0,60) == 7:
          pix[x,y] = cast(blend(pix[x,y], (255,255,255), 90)) 
      c1 = sub(c1, fac) 
  im.paste(sun, at, sun)
  for x in range(sx):
    for y in range(sy):
      if (sin(x/16)+1)/ws + y/sy > 1:
          pix[x,y] = (0,0,0,0)
  return im
""" kendime NOT
√halkasi olmayan gezegenlere ay lazim
kaya sistemi hos karsilanmadi
√gece gunduz sistemi eklendi gelisebilir
agac ve lake sistemi icin henuz erken
gezegen bos gorunuyor
"""
def uzayli(yem, c):
  seed(yem)
  im = Image.new("RGBA", (4,8), (0,0,0,0))
  #c = (255,255,255)
  #foot
  fh = rint(1,3)
  fx = rint(0,2)
  for h in range(fh):
    im.putpixel((fx,h), c) 
  #body
  bh = rint(1,3)
  for h in range(bh):
    for x in range(3-fx):
      im.putpixel((fx+1+x,h+fh), c)
  #arm
  ax = rint(1,3)
  for w in range(ax):
    im.putpixel((fx-w,fh+bh-1), c)
  #head
  eh = rint(1,8-fh-bh)
  ex = rint(1,(ax-1) if ax != 1 else 2)
  for h in range(eh):
    for x in range(ex):
      im.putpixel((3-x,fh+bh+h), c)
      
  out = Image.new("RGBA",(8,8), (0,0,0,0))
  out.paste(im, (0,0))
  out.paste( im.transpose(Image.FLIP_LEFT_RIGHT), (4,0))
  out = out.transpose(Image.FLIP_TOP_BOTTOM)
  seed()
  return out
def inside(u):
  if type(u) is int:
    u = {
      "pl":u, 
      "pM":1,
      "pW":1
    }
  gif = []
  pli = create_pla(u["pl"], False)
  pl = pli["tex"]
  tpl = Image.new("RGBA", (96,96), (0,0,0,0))
  for x in range(0,3):
    for y in range(0,3):
      tpl.paste(pl, (x*32, y*32))
  pl = tpl
  scl = rint(24,30)
  star = create_pla(pli["star"], False, pli["star"])["pla"].resize((scl,scl), resample=Image.NEAREST)
  t = int(time.strftime("%S")) 
  at = abs(t-30)/30*100
  pt = (t-30)/30+0.5
  psx = int(cos(pt*3.14)*rint(30,36)+48)
  psy = int(sin(pt*3.14)*24+48)
  sk = sky(at, star, (psx,psy)) 
  pl.paste(sk, (0,0), sk)
  mans = u["pM"]
  wmans = u["pW"]
  def cp(wm):
    cl = hsv(uf(0.41, 0.76), uf(0.8,1), 0.4) if wm else hsv(uf(0.80, 1),uf(0.8, 1), 0.4)
    return [rint(4,90),rint(72,90), uzayli(u["pl"], cl)]
  mpos = [cp(True) for _ in range(mans)]
  wpos = [cp(False) for _ in range(wmans)]
  nf = 15
  mv = 2
  for _ in range(nf):
    p = pl.copy()
    for m in mpos:
      p.paste(m[2], (m[0],m[1]), m[2])
      m[0] += rint(-mv,mv)
      m[1] += rint(-mv,mv)
      if m[1] < 72: m[1] = 72
    for w in wpos:
      p.paste(w[2], (w[0],w[1]), w[2])
      w[0] += rint(-mv,mv)
      w[1] += rint(-mv,mv)
      if w[1] < 72: w[1] = 72
    p = p.resize((350,350), resample=Image.NEAREST)
    gif.append(p)
  return gif

def sky2(yem=None, shy=12, bcol=None):
  seed(yem)
  ss = 96//3
  sx, sy = 3*ss, shy*ss
  im = Image.new('RGBA', (sx, sy), (0, 0, 0, 255))
  pix = im.load()
  if bcol is None:
    bcol = uf(0,1)
  colors = [hsv(limit(bcol+uf(0.2, 0.5)), 0.4+0.6*abs(i-3)/3, (3-abs(i-3))/3) for i in range(shy-4)] + [hsv(uf(0.5, 0.8), uf(0.3,0.5), uf(0.1,0.2)) for _ in range(3)] + [(0,0,0)]
  lcol = len(colors)
  lcol1 = lcol - 1
  for i in range(lcol1):
    c1 = colors[i]
    c2 = colors[i+1]
    dv = lcol1/sy
    fac = mul(sub(c1, c2), (dv, dv, dv))
    s = int(i*sy/lcol1)
    e = int((i+1)*sy/lcol1)
    for y in range(s, e):
      for x in range(sx):
        cc = c1 if rint(0,80) != 7 else blend(c1, (255,255,255), 60, 2) 
        pix[x,y] = cast(cc) 
      c1 = sub(c1, fac) 
  return im 
def inside2(u):
  if type(u) is int:
    u = {
      "pl":u, 
      "pM":1,
      "pW":1
    }
  s = u["pl"]
  pli = create_pla(s)
  sk = sky2(s, 10, pli["sky"])
  pl = pli["tex"]
  tpl = Image.new("RGBA", (96, 64), (0,0,0,0))
  for x in range(3):
    for y in range(2):
      tpl.paste(pl, (x*32, y*32))
  pl = tpl
  pix = pl.load()
  scl = rint(10,24)
  star = None
  if pli["star"] is not None:
    seed(pli["star"])
    sopt = {
      "moon":None, 
      "ring":0,
      "atm":None,
      "col1":pli["star"],
      "col2":limit(pli["star"] + choice([-1,1])*uf(1/16,1/2)), 
      "ring":0
    }
    star = create_pla(pli["star"], sopt)["pla"].resize((scl,scl), resample=Image.NEAREST)
  moon = None
  scl = rint(10,16)
  if pli["moon"] is not None:
    seed(pli["moon"])
    mopt = {
      "moon":None, 
      "ring":0,
      "atm":None,
      "col1":pli["moon"],
      "col2":limit(pli["moon"] + choice([-1,1])*uf(1/16,1/2)),
      "ring":0
    }
    moon = create_pla(pli["moon"], mopt)["pla"].resize((scl,scl), resample=Image.NEAREST)
  sy = sk.size[1]
  sx = sk.size[0]
  scl = sx//3*2
  gif = []
  nf = sy
  mans = u["pM"]
  wmans = u["pW"]
  def cp(wm):
    cl = hsv(uf(0.41, 0.76), uf(0.8,1), 0.4) if wm else hsv(uf(0.80, 1),uf(0.8, 1), 0.4)
    return [rint(16,80),rint(72,80), uzayli(u["pl"], cl)]
  mpos = [cp(True) for _ in range(mans)]
  wpos = [cp(False) for _ in range(wmans)]
  mv = 1
  seed()
  mh = uf(6.5,9.5)
  for x in range(96):
    for y in range(64):
      if (sin(x/16)+1)/(mh+uf(0,1))+ y/64 < 0.5:
          pix[x,y] = (0,0,0,0)
  flstar = None
  if rint(0,2) == 1:
    flstar = random()
  flrot = rint(150,210)
  flpos = [96.0,float(rint(30,50))]
  # loop
  step=1
  for n in range(0,nf,step):
    out = Image.new("RGBA", (96,96), (0,0,0,0))
    nn = n/nf + 0.5
    hsk = sk.crop((0,n,sx,limit(n+scl, sy, True)))
    csk = Image.new("RGBA", (96,64), (0,0,0,0))
    if n+scl>sy:
      mxn = n+scl-sy
      csk.paste(hsk)
      csk.paste(sk.crop((0, 0, sx, mxn)), (0,scl-mxn))
    else:
      csk = hsk
    out.paste(csk, (0,0), csk)
    if star is not None:
      stx = round(cos(nn*3.14*2)*34+48)
      sty = round(sin(nn*3.14*2)*24+48)
      out.paste(star, (stx,sty), star)
    if moon is not None:
      mnx = round(cos(nn*3.14*2-3.24)*34+48)
      mny = round(sin(nn*3.14*2-3.24)*24+48)
      out.paste(moon, (mnx,mny), moon)
    if flstar is not None and n < 35:
      cflstar = fallin_star(flstar, 180).rotate(270-flrot)
      out.paste(cflstar, (int(flpos[0]), int(flpos[1])), cflstar)
      flpos[0] += cos(flrot/180*3.14)*4*step
      flpos[1] += sin(flrot/180*3.14)*4*step
    out.paste(pl, (0,32), pl)
    for m in mpos:
      out.paste(m[2], (m[0],m[1]), m[2])
      m[0] += rint(-mv,mv)
      m[1] += rint(-mv,mv)
      if m[1] < 72: m[1] = 72
    for w in wpos:
      out.paste(w[2], (w[0],w[1]), w[2])
      w[0] += rint(-mv,mv)
      w[1] += rint(-mv,mv)
      if w[1] < 72: w[1] = 72
    gif.append(out.resize((350,350), resample=Image.NEAREST))
  return gif, step
  
def create_user(id):
  global users
  user = {
    "id" : id,
    "pl":id,
    "pM":1,
    "pW":1,
    "blood":100, 
    "rb":100
  }
  return users.insert_one(user)
def change(quser, what, value):
  global user
  users.update_one({
    '_id': quser['_id']
  },{
    '$set': {what: value}
  }, upsert=False)

def save_im(im, fn="anan"):
  with io.BytesIO() as bin:
    im.save(bin, "PNG", quality=100, optimize=True, progressive=True)
    bin.seek(0)
    return discord.File(fp=bin, filename=fn+'.png') 
def save_gif(gif, dur=100,fn="anan"):
  with io.BytesIO() as bin:
    gif[0].save(bin, format="GIF", save_all=True, append_images=gif[1:], optimize=False, duration=dur, loop=0)
    bin.seek(0)
    return discord.File(fp=bin, filename=fn+".gif") 

async def add_react(mes):
  #em = choice(emojis)
  #await mes.add_reaction(em)
  pass

@client.event
async def on_ready():
  print("basladi")

@client.event
async def on_reaction_add(r, user):
  pass
  
help_message = """```cpp
type `q mein` to view your planet and stats. 
type `q view [integer]` to view another planets.
→ you can also type `q fuck` to grove your population
→ you can kill your peoples by typing `q sacrifice [man|women]`
→ peoples can find rubs for you by typing `q rub`
→ also you can type `q shop` to buying somethings
```"""
@client.event 
async def on_message(messages):
  global users
  mes = messages
  user = messages.author
  id = int(user.id)
  ch = messages.channel
  mess = mes.content.lower()
  mesl = mess.split()
  if mess.startswith("q"):
    quser = users.find_one({"id":id})
    if quser is None:
      create_user(id)
    quser = users.find_one({"id":id})
    pop = quser["pM"]+quser["pW"]
    if mess == "q help":
      await ch.send(help_message)
    elif mess == "q mein":
      im = planet(quser["pl"]) 
      m = await ch.send(file=save_gif(im), content=f"""```py
{user.name}'s planet [id:{quser["pl"]}]:
Δ blood = {quser["blood"]}
Δ ruby = {quser["rb"]}
Δ population = {pop}
  → ♂️ man : {quser["pM"]}
  → ♀️ woman : {quser["pW"]}
```""")
      await add_react(m)
    elif mess.startswith("q inside"):
      qs = quser
      if len(mesl) == 3:
        qs = rmint() if mesl[2] == "r" else int(mesl[2])
      im = inside2(qs)
      sstr = qs if len(mesl) == 3 else ""
      m = await ch.send(file=save_gif(im[0], dur=40*im[1]), content=sstr) 
    elif mess.startswith("q r"):
      r = rmint() 
      im = planet(r)
      m = await ch.send(file=save_gif(im), content=f"{r}") 
    elif mess.startswith("q view") and len(mesl) == 3:
      s = int(mesl[2])
      im = planet(s)
      m = await ch.send(file=save_gif(im), content="` how's it goin'  brah? `")
    elif mess.startswith("q opt "):
      astr = mess[6:].split(",")
      opt={}
      for arg in astr:
        asp = arg.split(":")
        key = asp[0]
        value = asp[1]
        opt[key] = None if value == "none" else eval(value)
      im = planet(None, opt=opt)
      await ch.send(file=save_gif(im))
    elif mess.startswith("q set") and len(mesl) == 3:
      setp = set_pla(mesl[2])
      im = setp[0]
      s = f"```py\n{setp[1]}\n```" 
      m = await ch.send(file=save_gif(im),content=s)
    elif mess.startswith("q seti") and len(mesl) == 4:
      setp = set_im(mesl[2], int(mesl[3]))
      im = setp[0]
      s = f"```py\n{setp[1]}\n```" 
      if len(s) > 1000: s = "."
      m = await ch.send(file=save_im(im),content=s)
    elif mess == "q fuck":
      if quser["blood"] <= 0:
        await mes.reply("you have no blood")
        return
      seed()
      p = choice(["pM","pW"]) 
      change(quser, p, quser[p]+1)
      change(quser, "blood", quser["blood"]-1)
      await ch.send(f"""```py
one person was born current population is {pop+1}
your current blood is {quser['blood']-1}
```""")
    elif mess == "q sacrifice man":
      if quser["pM"] <= 1:
        await mes.reply("you cannot sacrifice your last peoples")
        return
      change(quser, "pM", quser["pM"]-1)
      change(quser, "blood", quser["blood"]+2)
      await ch.send(f"```py\nsacrificed successfully\ncurrent blood is {quser['blood']+2}```") 
    elif mess == "q sacrifice woman":
      if quser["pW"] <= 1:
        await mes.reply("you cannot sacrifice your last peoples")
        return
      change(quser, "pW", quser["pW"]-1)
      change(quser, "blood", quser["blood"]+2)
      await ch.send(f"```py\nsacrificed successfully\ncurrent blood is {quser['blood']+2}```")  
    elif mess.startswith("q dig"):
      if quser["pM"] <= 1 or quser["pW"] <= 1:
        await mes.reply("some peoples will be dead, this is your last peoples..")
        return
      change(quser, "rb", quser["rb"]+1)
      p = choice(["pM", "pW"])
      change(quser, p, quser[p]-1)
      await ch.send(f"""```py
current rubs is {quser['rb']+1} now.
```""")
    elif id == admin_id and mess.startswith("q give"):
      mesl = mes.content.split()
      wt = mesl[2]
      mid = int(mesl[3])
      hw = int(mesl[4])
      u = users.find_one({"id":mid})
      change(u, wt, hw)
      await mes.reply("okey halloldu")
    elif mess.startswith("q buy") and quser["rb"] > 0:
      if len(mesl) == 4 and mesl[2] == "planet":
        if quser["rb"] > 10 and quser["blood"] > 5:
          change(quser, "rb", quser["rb"]-10)
          change(quser, "blood", quser["blood"]-5)
          change(quser, "pl", int(mesl[3]))
          await mes.reply("successfuly! gule gule kullan kardesim")
        else:
          await ch.send("you don't have enough rub or blood")
        return
      elif mess.endswith("man"):
        change(quser, "man", quser["man"]+1)
        change(quser, "rb", quser["rb"]-1)
      elif mess.endswith("woman"):
        change(quser, "woman", quser["woman"]+1)
        change(quser, "rb", quser["rb"]-1)
      else:
        await mes.reply("please type man or women.")
        return
      await ch.send("human trafficking is successful")
    elif mess == "q shop":
      s = """```py
type `q buy [item]` to buy something
1. man | women : 1 rub
2. planet [integer] : 10 rub 5 blood
```"""
      await ch.send(s)
client.run(api)

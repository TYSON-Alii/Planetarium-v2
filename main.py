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
def mul(c1, c2):
  return (c1[0] * c2[0], c1[1] * c2[1], c1[2] * c2[2])
def sub(c1, c2):
  return (c1[0] - c2[0], c1[1] - c2[1], c1[2] - c2[2])
def col(c):
  return (c, c, c, c)
def cast(c):
  return (int(c[0]), int(c[1]), int(c[2]))
def alpha(c, a):
  return (c[0], c[1], c[2], a)
def to_rgb(c):
  return cast((c[0]*255, c[1]*255, c[2]*255))
def hsv(h, s, v):
  return to_rgb(hsv_to_rgb(h, s, v))
def limit(c):
  return ((c+1) if c < 0 else ((c-1) if c > 1 else c)) 
def prob(p): return randint(0,100) < p
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
def create_pla(yem=None, resize=True, base_col=None):
  if yem is None: yem = time.time()
  seed(yem)
  #init pla
  w, h = 32, 32
  aw, ah = rint(-2,0), rint(-2,0)
  ow, oh = w*3, h*3
  out = Image.new("RGBA", (ow, oh), (0,0,0,0))
  #colors
  bc1 = uf(0,1)
  bc2 = limit(bc1+choice([uf(1/16,1/2), uf(-1/2,-1/16)])) 
  if base_col is not None:
    bc1 = base_col
    bc2 = limit(bc1+choice([uf(1/40,1/30), uf(-1/40, -1/30)]))
  rl = rint(1,7) + uf(0,1)
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
  ekx, eky = rint(0,3),rint(0,3)
  draw.ellipse((0,0,w+aw,h+ah),fill=255)
  pla = Image.new('RGBA',(w+ekx,h+eky),(0,0,0,0))
  pla.paste(im, (0, 0), mask)
  #rings
  cr = uf(0, 1)
  cw, cb = uf(0.4,0.95), uf(0.4,0.95)
  rot = rint(0,360) 
  r = rint(0,3) if base_col is None else 0
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
    ro = rint(1,10)
    q1, q2 = q.copy(), q.copy()
    q1.paste(ai, (0,0))
    q2.paste(ai, (0,oh//2))
    qs.append([q1.rotate(rot*n/r+ro), q2.rotate(rot*n/r+ro)])
  for q in qs:
    out.paste(q[0], (0,0), q[0])
  out.paste(pla, (ow//2-w//2, oh//2-h//2), pla)
  for q in qs:
    out.paste(q[1], (0,0), q[1]) 
  #flag
  def to_t(c): return hsv(c, 0.9, 0.9)
  colors = [to_t(bc1), to_t(bc2)]
  colors += [(0,0,0,255)]*rint(0,5)
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
  star = uf(0.02,0.1)
  esmoone = r==0 and rint(0,3) == 1
  return [out,im,nim,yem,fim,star,pla,esmoone]  

def planet(pla, fla, moon=False, resize_=True):
  gif = []
  rsize = 350
  w, h = pla.size
  out = Image.new("RGBA", (w, h), (0,0,0,255))
  pix = out.load()
  pr = rint(50,80)
  for x in range(w):
    for y in range(h):
      if rint(0,pr) == 7:
        c = hsv(uf(0,1),0.1,1)
        pix[x,y] = alpha(c, rint(100,250))
  mim = None
  if moon:
    mim = create_pla(random(), resize=False)[6].resize((12,12), resample=Image.NEAREST)
  mrot = uf(0,3.14)
  away = rint(32,45)
  nf = w
  for i in range(nf):
    cout = out.copy()
    cim = Image.new("RGBA", (w, h), (0,0,0,255))
    ir = i % w
    cim.paste(cout.crop((ir, 0, w, h)),(0,0))
    cim.paste(cout.crop((0, 0, ir, h)),(w-ir,0))
    cout = cim
    #cout.paste(cim.rotate(-i), (0,0)) 
    p = pla.copy().rotate(i*(360/nf))
    cout.paste(p, (0,0), p)
    if moon:
      cmim = mim.rotate(i*3)
      cout.paste(cmim, (int(w//2+cos(mrot)*away) , int(h//2+sin(mrot)*away)), cmim)
      mrot += 3.14/nf*2
    cout.paste(fla, (0,0))
    if resize_:
      cout = cout.resize((rsize,rsize), resample=Image.NEAREST)
    gif.append(cout)
  print(len(gif)*(rsize**2*4) / (1024*1024)) 
  return gif

def set_pla(yem):
  seed(yem)
  w = 96
  seeds = [rint(-1*sys.maxsize, sys.maxsize) for _ in range(9)]
  crats = [create_pla(seeds[i], False) for i in range(9)]
  plas = [planet(crats[i][0], crats[i][2], crats[i][7], False) for i in range(9)]
  gif = []
  im = Image.new("RGBA", (w*3, w*3), (0,0,0,0))
  for n in range(w):
    for i in range(3):
      for j in range(3):
        im.paste(plas[i*3+j][n], (w*i, w*j))
    gif.append(im.resize((w*3*3, w*3*3), resample=Image.NEAREST))
  return gif, seeds

def set_im(yem, count):
  seed(yem)
  w = 96
  #count = 20
  seeds = [rint(-1*sys.maxsize, sys.maxsize) for _ in range(count**2)]
  crats = [create_pla(seeds[i], False) for i in range(count**2)]
  out = Image.new("RGBA", (w*count, w*count), (0,0,0,255))
  pix = out.load()
  for x in range(w*count):
    for y in range(w*count):
      if rint(0,65) == 7:
        pix[x,y] = (255,255,255)
        
  for i in range(count):
    for j in range(count):
      pos = i*count+j
      p = crats[pos][0]
      f = crats[pos][2]
      out.paste(p, (w*i, w*j), p)
      out.paste(f, (w*i, w*j), f)
  return out.resize((w*count*2,w*count*2),resample=Image.NEAREST), seeds
  
def blend(c1, c2, per):
  o1 = per/100
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
halkasi olmayan gezegenlere ay lazim
kaya sistemi hos karsilanmadi
gece gunduz sistemi eklendi gelisebilir
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
  gif = []
  pli = create_pla(u["pl"], False)
  pl = pli[1]
  tpl = Image.new("RGBA", (96,96), (0,0,0,0))
  for x in range(0,3):
    for y in range(0,3):
      tpl.paste(pl, (x*32, y*32))
  pl = tpl
  scl = rint(24,30)
  star = create_pla(pli[5], False, pli[5])[6].resize((scl,scl), resample=Image.NEAREST)
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
    return [rint(4,90),rint(72,90), uzayli(u["id"], cl)]
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
import noise
def perlin(width, height):
  scale = 10.0
  octaves = 50
  persistence = 0.5
  lacunarity = 2.0
  world = []
  for y in range(height):
    row = []
    for x in range(width):
      n = noise.pnoise2(x/scale, y/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=0)
      row.append(n)
    world.append(row)
  return world
def inside2(u):
  seed(u["pl"])
  a, b = rint(-2,0), rint(-2,0)
  bc1 = uf(0,1)
  bc2 = limit(bc1+choice([uf(1/16,1/2), uf(-1/2,-1/16)]))
  print(bc1, bc2)
  p = perlin(96,96)
  mx = max([max(row) for row in p])
  im = Image.new("RGBA", (96, 96), (0,0,0,0))
  pix = im.load()
  for x in range(96):
    for y in range(96):
      pl = (p[x][y]+mx)/2
      c = bc1*(pl/mx) + bc2*(1-pl/mx)
      pix[x,y] = hsv(limit(c), 0.8, 0.8)
      #c1 = hsv(limit(bc1), 0.8, 0.8) 
      #c2 = hsv(limit(bc2), 0.8, 0.8)
      #pix[x,y] = cast(blend(c2, c1, limit(p[x][y])*100)) 
    print()
  return im.resize((350,350), resample=Image.NEAREST)

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
    
def save_gif(gif, fn="anan"):
  with io.BytesIO() as bin:
    gif[0].save(bin, format="GIF", save_all=True, append_images=gif[1:], optimize=False, duration=100, loop=0)
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
      im = create_pla(quser["pl"], False) 
      im = planet(im[0], im[2], im[7]) 
      m = await ch.send(file=save_gif(im), content=f"""```py
{user.name}'s planet [id:{quser["pl"]}]:
Δ blood = {quser["blood"]}
Δ ruby = {quser["rb"]}
Δ population = {pop}
  → ♂️ man : {quser["pM"]}
  → ♀️ woman : {quser["pW"]}
```""")
      await add_react(m)
    elif mess == "q inside":
      im = inside(quser)
      im[0].save("yarak.gif", "GIF", save_all=True, append_images=im[1:], optimize=False, duration=100, loop=0)
      m = await ch.send(file=save_gif(im)) 
    elif mess.startswith("q view") and len(mesl) == 3:
      s = 0
      b = None
      if mesl[2][0] == "#":
        s = b = float(mesl[2][1:])/360
      else:
        s = int(mesl[2])
      im = create_pla(s, False, b) 
      im = planet(im[0], im[2], im[7])
      m = await ch.send(file=save_gif(im), content="` how's it goin'  brah? `") 
      await add_react(m)
    elif mess.startswith("q set") and len(mesl) == 3:
      setp = set_pla(mesl[2])
      im = setp[0]
      s = f"```py\n{setp[1]}\n```" 
      m = await ch.send(file=save_gif(im),content=s)
    elif mess.startswith("q seti") and len(mesl) == 4:
      setp = set_im(mesl[2], int(mesl[3]))
      im = setp[0]
      s = f"```py\n{setp[1]}\n```" 
      if len(s) > 1000: s = s[:1000]
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

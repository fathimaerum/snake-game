import tkinter, random, math
from collections import deque

T = TS = 25; ROWS = COLS = 25; W = H = T * COLS
GSPD, RSPD, INS = 90, 16, 2

class Tile:
    def __init__(self, x, y): self.x = x; self.y = y

window = tkinter.Tk(); window.title("🐍 Snake"); window.resizable(False, False)
canvas = tkinter.Canvas(window, bg="#fbadc8", width=W, height=H, borderwidth=0, highlightthickness=0)
canvas.pack(); window.update()
ww, wh = window.winfo_width(), window.winfo_height()
window.geometry(f"{ww}x{wh}+{int(window.winfo_screenwidth()/2-ww/2)}+{int(window.winfo_screenheight()/2-wh/2)}")

snake = Tile(T*5, T*5); food = Tile(T*10, T*10)
vx = vy = 0; body = []; over = False; score = 0; tick = 0
iq = deque(maxlen=2)

def build_grid():
    img = tkinter.PhotoImage(width=W, height=H)
    img.put("#fbadc8", to=(0, 0, W, H))
    for r in range(ROWS+1): img.put("#f797be", to=(0, r*T, W, r*T+1))
    for c in range(COLS+1): img.put("#f797be", to=(c*T, 0, c*T+1, H))
    return img
grid_img = build_grid()

def reset():
    global snake, food, body, over, score, vx, vy
    snake=Tile(T*5,T*5); food=Tile(T*10,T*10); vx=vy=0; body=[]; over=False; score=0; iq.clear()

def seg(x, y, i):
    cx, cy = x+T//2, y+T//2
    bc = "#4caf3a" if i%2==0 else "#5dc94a"; sc = "#3a9929" if i%2==0 else "#4ab83a"
    canvas.create_oval(x+INS, y+INS, x+T-INS, y+T-INS, fill=bc, outline="#2d7a1f", width=1)
    canvas.create_oval(cx-4, cy-4, cx+4, cy+4, fill=sc, outline="")
    canvas.create_oval(cx-3, cy-3, cx, cy, fill="#7deb60", outline="")

def head(x, y):
    cx, cy = x+T//2, y+T//2
    canvas.create_oval(x+1, y+1, x+T-1, y+T-1, fill="#66dd44", outline="#2d7a1f", width=2)
    canvas.create_oval(x+4, y+4, x+T//2, y+T//2, fill="#aaff77", outline="")
    eyes = {(1,0):(cx+4,cy-4,cx+4,cy+4), (-1,0):(cx-4,cy-4,cx-4,cy+4),
            (0,-1):(cx-4,cy-4,cx+4,cy-4), (0,1):(cx-4,cy+4,cx+4,cy+4)}.get((vx,vy),(cx+4,cy-4,cx+4,cy+4))
    for ex, ey in [(eyes[0],eyes[1]),(eyes[2],eyes[3])]:
        canvas.create_oval(ex-2,ey-2,ex+2,ey+2, fill="white", outline="#1a5c10", width=1)
        canvas.create_oval(ex-1,ey-1,ex+1,ey+1, fill="#111", outline="")
    if vx or vy:
        tx, ty = cx+vx*10, cy+vy*10
        canvas.create_line(cx+vx*7, cy+vy*7, tx, ty, fill="#ff3355", width=2)
        canvas.create_line(tx, ty, tx+vx*5+vy*3, ty+vy*5+vx*3, fill="#ff3355", width=1)
        canvas.create_line(tx, ty, tx+vx*5-vy*3, ty+vy*5-vx*3, fill="#ff3355", width=1)

def apple(x, y):
    cx = x+T//2; bob = int(math.sin(tick*0.15)*1.5)
    canvas.create_oval(x+3, y+5+bob, x+T-3, y+T-2+bob, fill="#e8242a", outline="#9b1010", width=1)
    canvas.create_oval(x+6, y+7+bob, x+11, y+11+bob, fill="#ff7a7a", outline="")
    canvas.create_line(cx, y+5+bob, cx, y+2+bob, fill="#5a3210", width=2)
    canvas.create_oval(cx, y+1+bob, cx+7, y+5+bob, fill="#55c244", outline="#2d7a1f", width=1)

def on_key(e):
    global over
    if over:
        if e.keysym.lower()=="r": reset()
        return
    cvx, cvy = iq[-1] if iq else (vx, vy)
    if e.keysym=="Up"    and cvy!= 1: iq.append((0,-1))
    elif e.keysym=="Down"  and cvy!=-1: iq.append((0, 1))
    elif e.keysym=="Left"  and cvx!= 1: iq.append((-1,0))
    elif e.keysym=="Right" and cvx!=-1: iq.append(( 1,0))

def update():
    global vx, vy, over, score
    if not over:
        if iq: vx, vy = iq.popleft()
        if snake.x<0 or snake.x>=W or snake.y<0 or snake.y>=H or any(snake.x==t.x and snake.y==t.y for t in body):
            over=True
        else:
            if snake.x==food.x and snake.y==food.y:
                body.append(Tile(food.x,food.y)); food.x=random.randint(0,COLS-1)*T; food.y=random.randint(0,ROWS-1)*T; score+=1
            for i in range(len(body)-1,-1,-1):
                body[i].x,body[i].y = (snake.x,snake.y) if i==0 else (body[i-1].x,body[i-1].y)
            snake.x+=vx*T; snake.y+=vy*T
    window.after(GSPD, update)

def draw():
    global tick; tick+=1
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=grid_img)
    apple(food.x, food.y)
    for i,t in enumerate(reversed(body)): seg(t.x, t.y, i)
    head(snake.x, snake.y)
    if over:
        canvas.create_rectangle(0,0,W,H, fill="#1a0a10", stipple="gray50", outline="")
        canvas.create_text(W/2,H/2-30, font="Arial 26 bold", text=f"🍎 Score: {score}", fill="white")
        canvas.create_text(W/2,H/2+10, font="Arial 16", text="Game Over 🐍", fill="#ff6688")
        canvas.create_text(W/2,H/2+42, font="Arial 11", text="Press R to restart", fill="#cc99aa")
    else:
        canvas.create_rectangle(4,4,100,26, fill="#e8749a", outline="#c05070", width=1)
        canvas.create_text(52,15, font="Arial 11 bold", text=f"🍎 {score}", fill="white")
    window.after(RSPD, draw)

window.bind("<KeyPress>", on_key)
update(); draw(); window.mainloop()

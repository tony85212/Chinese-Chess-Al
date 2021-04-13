from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from subprocess import Popen, PIPE
import threading, time


root = Tk()
root.minsize(750,700)
root.maxsize(750,700)
root.title("Chinese Chess")

piece_image = []
background_image =  PhotoImage(file='image/board2.png')
history_image = PhotoImage(file='image/history.png')
for i in range(15):
     piece_image.append(PhotoImage(file='image/' + str(i) + '.png'))   
select = True
engine = 'layla_ver1.4.exe'
pre_click_position = 0
pre_piece = 0
history_piece = 100
piece_move = []
record_list = []

symbol_transform = [' ', 'K', 'A', 'B', 'N', 'R', 'C', 'P', 'k', 'a', 'b', 'n', 'r', 'c', 'p']
board_transform = ['a9', 'b9', 'c9', 'd9', 'e9', 'f9', 'g9', 'h9', 'i9',
                   'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8', 'i8',
                   'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'i7',
                   'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6', 'i6',
                   'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5', 'i5',
                   'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4', 'i4',
                   'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3', 'i3',
                   'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2', 'i2',
                   'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'i1',
                   'a0', 'b0', 'c0', 'd0', 'e0', 'f0', 'g0', 'h0', 'i0']

img_piece = []


class Board():
     boardinfo = []
     turn = 0
     moves = []
     move_history = []
     fen = ''
     player = [0, 0]
     player_engine = ['layla_ver1.4.exe', 'layla_ver1.4.exe']
     mode = ''
     step = 0
     def move_gen(self):
          str = self.fen + '\nmoves\n'
          self.moves = []
          data = []        
          data = childprocess(engine, str)
          for i in range(1, len(data)):
               self.moves.append(data[i][1:5])
          if(len(self.moves) == 0):
               messagebox.showinfo("Info", "GAMEOVER!")
          #print(self.moves)
     def update_fen(self):
          if(len(self.move_history) == 1):
               self.fen += ' moves'
          self.fen += ' '
          self.fen += self.move_history[-1][0]
          self.fen += self.move_history[-1][1]
     def regret(self):
          global history_piece
          x = 1
          if((b.player[0] | b.player[1]) == 1):
               x = 2
          for i in range(x):
               if(len(self.move_history) != 0):
                    old_move = self.move_history.pop()
                    pos = board_transform.index(old_move[0])
                    next_pos = board_transform.index(old_move[1])
                    piece = self.boardinfo[next_pos]
                    eat_piece = old_move[2]
                    history_piece = 100
                    self.boardinfo[pos] = piece
                    self.boardinfo[next_pos] = eat_piece
                    self.turn = (self.turn + 1 )%2
                    gui_board.itemconfig(img_piece[next_pos], image = piece_image[eat_piece])
                    gui_board.itemconfig(img_piece[pos], image = piece_image[piece])
                    self.fen = self.fen[:-5]
                    if(len(self.move_history) == 0):
                         self.fen = self.fen[:-6]
                    b.move_gen()
     def initialize(self):
          global history_piece
          global board_transform
          board_transform = ['a9', 'b9', 'c9', 'd9', 'e9', 'f9', 'g9', 'h9', 'i9',
                   'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8', 'i8',
                   'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'i7',
                   'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6', 'i6',
                   'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5', 'i5',
                   'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4', 'i4',
                   'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3', 'i3',
                   'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2', 'i2',
                   'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'i1',
                   'a0', 'b0', 'c0', 'd0', 'e0', 'f0', 'g0', 'h0', 'i0']
          self.turn = 0
          self.step = 0
          self.player[0] = setrp()
          self.player[1] = setbp()
          self.boardinfo = [12, 11, 10, 9, 8, 9, 10, 11, 12,
                             0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 13, 0, 0, 0, 0, 0, 13, 0,
                             14, 0, 14, 0, 14, 0, 14, 0, 14,
                             0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0,
                             7, 0, 7, 0, 7, 0, 7, 0, 7,
                             0, 6, 0, 0, 0, 0, 0, 6, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0,
                             5, 4, 3, 2, 1, 2, 3, 4, 5]
          self.fen =  'position fen rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1'
          self.move_gen()
          self.move_history[:] = []
          history_piece = 100
class AI_thread(threading.Thread):
       def run(self): 
              AI(b)

     
def childprocess(cmd, string):
     data = []
     process = Popen(cmd, stdout = PIPE, stdin = PIPE, stderr = PIPE, creationflags = 0x08000000)
     output = process.communicate(string.encode())[0].decode()
     data = output.splitlines()
     process.terminate()
     return data
def asign_click(b, click_position):
    global select
    global pre_click_position
    global history_piece
    global pre_piece
    global piece_move
    if(select and b.boardinfo[click_position] != 0 and (int(b.boardinfo[click_position]/8) == b.turn)  and b.player[b.turn] == 0):
          pre_click_position = click_position
          pre_piece = b.boardinfo[click_position]
          piece_move = []
          for i in range(len(b.moves)):
               if(b.moves[i][:2] == board_transform[pre_click_position]):
                    piece_move.append(b.moves[i][2:])
          select = False
    elif(select == False):
          #print(board_transform[click_position])
          if(board_transform[click_position] in piece_move):
               if(history_piece != 100):
                    gui_board.itemconfig(img_piece[history_piece], image = piece_image[0])
               gui_board.itemconfig(img_piece[pre_click_position], image = history_image)
               gui_board.itemconfig(img_piece[click_position], image = piece_image[pre_piece])
               history_piece = pre_click_position
               eat_piece = b.boardinfo[click_position]
               b.boardinfo[click_position] = b.boardinfo[pre_click_position]
               b.boardinfo[pre_click_position] = 0
               b.turn = (b.turn + 1 )%2
               select = True                     
               b.move_history.append([board_transform[pre_click_position], board_transform[click_position], eat_piece])
               b.update_fen()
               b.move_gen()
               #buttonAI.config(state = "disabled")
               if((b.player[0] | b.player[1]) == 1):
                    AI_thread().start()
          elif( b.boardinfo[click_position] != 0 and (int(b.boardinfo[click_position]/8) == b.turn) and b.player[b.turn] == 0):            
               pre_click_position = click_position
               pre_piece = b.boardinfo[click_position]
               #print(pre_click_position)
               piece_move = []
               for i in range(len(b.moves)):
                    if(b.moves[i][:2] == board_transform[pre_click_position]):
                         piece_move.append(b.moves[i][2:])
               #print(piece_move)
               select = False
def save(b):
     file = filedialog.asksaveasfile(mode='w', title = "Select file", filetypes=((".dat files", "*.dat"),
                                           ("All files", "*.*") ))
     if file is None: # asksaveasfile return `None` if dialog closed with "cancel".
          return
     for i in range(len(b.move_history)):
          file.write(str(b.move_history[i][0]) + str(b.move_history[i][1]))
     print(b.move_history)
def AI(b):
     global history_piece
     string = ''
     if(b.mode[0].isdigit()):
          second = int(b.mode[:2])
          string = b.fen + '\ngo movetime ' +  str(second * 1000) + '\ngo depth 1'
     else:
          depth = b.mode[-2:]
          print(depth)
          string = b.fen + '\ngo depth ' + depth + '\ngo depth 1'
     data = childprocess(b.player_engine[b.turn], string)
     search_info = []
     #print(data)
     for i in range(0, len(data)-2):
          search_info.append(data[i])
     print(search_info[-3][:13])
     print(search_info[-2])
     best_move = search_info[-1][9:13]
     ponder = search_info[-1][21:25]
     print(best_move)
     pos = board_transform.index(best_move[:2])
     next_pos = board_transform.index(best_move[2:])
     piece = b.boardinfo[pos]
     if(history_piece != 100):
          gui_board.itemconfig(img_piece[history_piece], image = piece_image[0])
     gui_board.itemconfig(img_piece[pos], image = history_image)
     gui_board.itemconfig(img_piece[next_pos], image = piece_image[piece])
     eat_piece = b.boardinfo[next_pos]
     history_piece = pos
     b.boardinfo[next_pos] = b.boardinfo[pos]
     b.boardinfo[pos] = 0
     b.turn = (b.turn + 1 )%2
     select = True                     
     b.move_history.append([board_transform[pos], board_transform[next_pos], eat_piece])
     b.update_fen()
     b.move_gen()
def gui_ini(b):
    gui_board.delete('all')
    img_piece[:] = []
    gui_board.image = background_image
    gui_board.create_image(315, 350, image = background_image)
    for i in range(90):
        symbol  = b.boardinfo[i]
        img_piece.append(gui_board.create_image(int(i%9)* 68 + 40, int(i/9) * 68 + 40, image = piece_image[symbol]))
        gui_board.tag_bind(img_piece[i], '<1>', lambda event ,x = i:asign_click(b, x))
def readygo(b):
     b.initialize()
     # 0 = human, 1 = computer
     b.mode = box_value.get()
     if(setboard() == 1):
          board_transform.reverse()
          b.boardinfo.reverse()
     if(b.player[0] == 1 and b.player[1] == 0):
          AI_thread().start()
     elif(b.player[0] == 1 and b.player[1] == 1):
          board_transform.reverse()
          b.boardinfo.reverse()
          while(len(b.moves) != 0 and b.step <= 150):
               AI(b)
               b.step += 1
               root.update()
          messagebox.showinfo("Info", "GAMEOVER!")
     gui_ini(b)
     
    #buttonAI.config(state = "active")
def red_change_engine(b):
     b.player_engine[0] = filedialog.askopenfilename(filetypes=((".exe files", "*.exe"),
                                           ("All files", "*.*") ))
     i = len(b.player_engine[0])-1
     char = ''
     while(char !='/'):
          char =  b.player_engine[0][i]
          i -= 1
     labelRedengine.config(text = b.player_engine[0][i + 2:])
def black_change_engine(b):
     b.player_engine[1] = filedialog.askopenfilename(filetypes=((".exe files", "*.exe"),
                                           ("All files", "*.*") ))
     i = len(b.player_engine[1])-1
     char = ''
     while(char !='/'):
          char =  b.player_engine[1][i]
          i -= 1
     labelBlackengine.config(text = b.player_engine[1][i + 2:])
def setrp():
     return var.get()
def setbp():
     return var2.get()
def setboard():
     return var3.get()

b = Board()

var = IntVar()
var2 = IntVar()
var3 = IntVar()
radiobuttonRedhuman = Radiobutton(root, text = "Human", variable = var, value = 0, command = setrp, indicatoron = 0)
radiobuttonRedhuman.grid(row = 0 ,column = 0, padx = 635, pady = 0, sticky = N +W)
Redhuman = PhotoImage(file='image/redbrain.png')
radiobuttonRedhuman.config(image = Redhuman)
radiobuttonRedcomputer = Radiobutton(root, text = "Computer", variable = var, value = 1, command = setrp, indicatoron = 0)
radiobuttonRedcomputer.grid(row = 0 ,column = 0, padx = 635, pady = 50, sticky = N +W)
Redcomputer = PhotoImage(file='image/redcomputer.png')
radiobuttonRedcomputer.config(image = Redcomputer)
#buttonRedengine = Button(root, text = "Redengine", command = lambda: red_change_engine(b))
#buttonRedengine.grid(row = 0 ,column = 0, padx = 635, pady = 100, sticky = N + E)
#Redengine = PhotoImage(file='image/redengine.png')
#buttonRedengine.config(image = Redengine)
#labelRedengine = Label(root, text = b.player_engine[0])
#labelRedengine.grid(row = 0 ,column = 0, padx = 635, pady = 170, sticky = N + E)

radiobuttonBlackhuman = Radiobutton(root, text = "Human", variable = var2, value = 0, command = setbp, indicatoron = 0)
radiobuttonBlackhuman.grid(row = 0 ,column = 0, padx = 635, pady = 200, sticky = N +W)
Blackhuman = PhotoImage(file='image/blackbrain.png')
radiobuttonBlackhuman.config(image = Blackhuman)
radiobuttonBlackcomputer = Radiobutton(root, text = "Computer", variable = var2, value = 1, command = setbp, indicatoron = 0)
Blackcomputer = PhotoImage(file='image/blackcomputer.png')
radiobuttonBlackcomputer.config(image = Blackcomputer)
radiobuttonBlackcomputer.grid(row = 0 ,column = 0, padx = 635, pady = 250, sticky = N +W)
#buttonBlackengine = Button(root, text = "blackengine", command = lambda: black_change_engine(b))
#buttonBlackengine.grid(row = 0 ,column = 0, padx = 635, pady = 300, sticky = N + E)
#Blackengine = PhotoImage(file='image/blackengine.png')
#buttonBlackengine.config(image = Blackengine)
#labelBlackengine = Label(root, text = b.player_engine[1])
#labelBlackengine.grid(row = 0 ,column = 0, padx = 635, pady = 370, sticky = N + E)
checkbox = Checkbutton(root, text = "Red Up", variable = var3)
checkbox.grid(row = 0 ,column = 0, padx = 635, pady = 300, sticky = N + W)



buttonReadygo = Button(root, text = "Readygo", command = lambda: readygo(b))
buttonReadygo.grid(row = 0 ,column = 0, padx = 635, pady = 400, sticky = N + W )
Readygo = PhotoImage(file='image/readygo.png')
buttonReadygo.config(image = Readygo)
buttonRegret = Button(root, text = "Regret", command = b.regret)
buttonRegret.grid(row = 0 ,column = 0, padx = 635, pady = 500, sticky = N + W)
Regret = PhotoImage(file='image/regret.png')
buttonRegret.config(image = Regret)
buttonSave = Button(root, text = "Save", command = lambda: save(b))
buttonSave.grid(row = 0 ,column = 0, padx = 635, pady = 600, sticky = N + W )
Save = PhotoImage(file='image/save.png')
buttonSave.config(image = Save)

radiobuttonRedhuman.select()
radiobuttonBlackcomputer.select()

box_value = StringVar()
comboboxRedmode = ttk.Combobox(root, width=12, textvariable = box_value, state = "readonly")
comboboxRedmode['values'] = ('1 Sec', '3 Sec', '5 Sec', '30 Sec', 'depth 5', 'depth 10')  
comboboxRedmode.grid(row = 0 ,column = 0, padx = 635, pady = 650, sticky = N + W ) 
comboboxRedmode.current(0)  


gui_board = Canvas(root, width = 630, height = 700, bg = 'black') 
gui_board.grid(row = 0 ,column = 0, sticky = N +W)
readygo(b)


root.mainloop()    

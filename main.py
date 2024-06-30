import pygame
from settings import *
import random

random.seed(0)

def draw_background():
    screen.fill(BACKGROUND_COLOR)

def init_cell(size):
    cells=[]
    status_cells=[]
    choice=[]

    for i in range (size):
        t1=[]
        t2=[]
        for j in range(size):
            choice.append([i,j])
            t1.append('')
            t2.append(0)
        cells.append(t1)
        status_cells.append(t2)

    return(cells,status_cells, choice)
    
def draw_hidden_cells(cell_width):
    pygame.draw.rect(screen, GRAY, (20,20,560,560))

    x,y =20,20
    offset=cell_width/8
    for i in range(size):
        x=20
        for j in range (size):
            pygame.draw.polygon(screen, DARK_GRAY, [(x+cell_width, y), (x+cell_width-offset,y+offset), (x+cell_width-offset,cell_width+y-offset), (x+cell_width, cell_width+y)])
            pygame.draw.polygon(screen, DARK_GRAY, [(x, y+cell_width), (x+offset,y+cell_width-offset), (x+cell_width-offset,cell_width+y-offset), (x+cell_width, cell_width+y)])


            pygame.draw.polygon(screen, LIGHT_GRAY, [(x, y), (x+offset,y+offset), (x+cell_width-offset,y+offset), (x+cell_width, y)])
            pygame.draw.polygon(screen, LIGHT_GRAY, [(x, y), (x+offset,y+offset), (x+offset,cell_width+y-offset), (x, cell_width+y)])
            x=x+cell_width
        y=y+cell_width
    
    for i in range (20,581,cell_width):
        pygame.draw.line(screen, BACKGROUND_COLOR, (i,20),(i,580), 2)
        pygame.draw.line(screen, BACKGROUND_COLOR, (20,i),(580,i), 2)

def gen_buttons():
    x,y,w,h=640,20,100,30
    buttons=[]
    for i in range (1,5):
        buttons.append({'name': 'Level '+str(i), 'coordinates': (x,y,w,h)})
        y=y+h+10
    buttons.append({'name': 'Play', 'coordinates': (x,y,w,h)})

    return(buttons)

def draw_buttons(selected):
    
    for b in buttons[:len(buttons)]:
        pygame.draw.rect(screen, GRAY, b['coordinates'])
        pygame.draw.rect(screen, BLACK, b['coordinates'], 3)
        text=font.render(b['name'], True, BLACK)
        screen.blit(text, (b['coordinates'][0]+17,b['coordinates'][1]+3))
    
    if selected!=-1:
        pygame.draw.rect(screen, PINK, buttons[selected]['coordinates'])
        pygame.draw.rect(screen, BLACK, buttons[selected]['coordinates'], 3)
        text=font.render(buttons[selected]['name'], True, BLACK)
        screen.blit(text, (buttons[selected]['coordinates'][0]+17,buttons[selected]['coordinates'][1]+3))

    pygame.draw.rect(screen, GRAY, buttons[-1]['coordinates'])
    pygame.draw.rect(screen, BLACK,  buttons[-1]['coordinates'], 3)
    text=font.render( buttons[-1]['name'], True, BLACK)
    screen.blit(text, ( buttons[-1]['coordinates'][0]+30, buttons[-1]['coordinates'][1]+3))

def reveal_cell(row,col):
    if (status_cells[row][col]==0):
        status_cells[row][col]=1

        pygame.draw.rect(screen, GRAY, (cell_width*col+20,cell_width*row+20,cell_width,cell_width))

        for i in range (20,581,cell_width):
            pygame.draw.line(screen, BACKGROUND_COLOR, (i,20),(i,580), 2)
            pygame.draw.line(screen, BACKGROUND_COLOR, (20,i),(580,i), 2)
        match select_game:
            case 0:
                font = pygame.font.SysFont('arial', 80)
                y_offset,x_offset=20,-4
            case 1:
                font = pygame.font.SysFont('arial', 60)
                y_offset,x_offset=14,-4
            case 2:
                font = pygame.font.SysFont('arial', 40)
                y_offset,x_offset=11,-1
            case 3:
                font = pygame.font.SysFont('arial', 25)
                y_offset,x_offset=8,2

        n=cells[row][col]
        text=font.render(str(n), True, BLACK)
        screen.blit(text, (col*cell_width+20+y_offset, row*cell_width+20+x_offset))
    
def get_cell_size():
    match select_game:
        case 0:
            return(140, 560//140)
        case 1:
            return(70, 560//70)
        case 2:
            return(56, 560//56)
        case 3:
            return(40, 560//40)
        
def draw_hidden_cell(row,col):
    x=col*cell_width+20
    y=row*cell_width+20
    pygame.draw.rect(screen, GRAY, (x,y,cell_width,cell_width))

    offset=cell_width/8

    pygame.draw.polygon(screen, DARK_GRAY, [(x+cell_width, y), (x+cell_width-offset,y+offset), (x+cell_width-offset,cell_width+y-offset), (x+cell_width, cell_width+y)])
    pygame.draw.polygon(screen, DARK_GRAY, [(x, y+cell_width), (x+offset,y+cell_width-offset), (x+cell_width-offset,cell_width+y-offset), (x+cell_width, cell_width+y)])

    pygame.draw.polygon(screen, LIGHT_GRAY, [(x, y), (x+offset,y+offset), (x+cell_width-offset,y+offset), (x+cell_width, y)])
    pygame.draw.polygon(screen, LIGHT_GRAY, [(x, y), (x+offset,y+offset), (x+offset,cell_width+y-offset), (x, cell_width+y)])

    for i in range (20,581,cell_width):
        pygame.draw.line(screen, BACKGROUND_COLOR, (i,20),(i,580), 2)
        pygame.draw.line(screen, BACKGROUND_COLOR, (20,i),(580,i), 2)

def fill_cell(cells, choices):
    while len(choices)>0:
        c1=random.choice(choices)
        choices.remove(c1)
        c2=random.choice(choices)
        choices.remove(c2)
        s=CHAR[random.randint(0,len(CHAR)-1)]
        cells[c1[0]][c1[1]]=s
        cells[c2[0]][c2[1]]=s
    return(cells)
    
def check_win():
    for row in range (size):
        for col in range (size):
            if status_cells[row][col]==0:
                return
    end()
                
def end():
    font = pygame.font.SysFont('arial', 40)
    pygame.draw.rect(screen, BACKGROUND_COLOR, (640,490,100,100))
    text=font.render("Win", True, RED)
    screen.blit(text, (650, 500))

def check_match(cell_reveal_now):
    if (cells[cell_reveal_now[0][0]][cell_reveal_now[0][1]] and cells[cell_reveal_now[1][0]][cell_reveal_now[1][1]]):
        status_cells[cell_reveal_now[0][0]][cell_reveal_now[0][1]]==1
        status_cells[cell_reveal_now[1][0]][cell_reveal_now[1][1]]==1
    draw_hidden_cell(cell_reveal_now[0][0],cell_reveal_now[0][1])
    draw_hidden_cell(cell_reveal_now[1][0],cell_reveal_now[1][1])

if __name__=='__main__':

    pygame.init()
    clock=pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags, vsync=1)
    pygame.display.set_caption('Campo minato♥')
    font = pygame.font.SysFont('arial', 20)


    cell_width=0
    size=0
    selected = -1
    cell_reveal_now=[]

    buttons=gen_buttons()
    draw_buttons(-1)
    select_game=-1
    loose=False
    win=False

    run  = True

    while run:

        for event in pygame.event.get():
            if (event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()

                if(x>=20 and x<=560 and y>=20 and x<=560):
                    row=(y-20)//cell_width
                    col=(x-20)//cell_width
                    print(cells)
                    if status_cells[row][col]==0:
                        reveal_cell(row, col)
                        cell_reveal_now.append([row,col])
                        if len(cell_reveal_now)==2:
                            check_match(cell_reveal_now)
                        check_win()
                else:
                    for i in range (len(buttons)):
                        if(x>=buttons[i]['coordinates'][0] and x<=buttons[i]['coordinates'][0]+buttons[i]['coordinates'][2] and y>=buttons[i]['coordinates'][1] and y<=buttons[i]['coordinates'][1]+buttons[i]['coordinates'][3]):
                            if(i<len(buttons)-1):
                                selected=i
                                select_game=selected
                                draw_buttons(selected)
                                break
                            elif(i==4):
                                if(selected!=-1):
                                    pygame.draw.rect(screen, BACKGROUND_COLOR, (640,490,100,100))   
                                    select_game=selected
                                    win=False
                                    loose=False
                                    game_started=True
                                    first_cell=True
                                    cell_width, size=get_cell_size()
                                    draw_hidden_cells(cell_width)
                                    cells,status_cells,choices=init_cell(size)
                                    cells=fill_cell(cells,choices)
                                    print(cells)
                                    buttons=gen_buttons()
                                    draw_buttons(selected)
                                break
                    else:
                        selected=-1
                    draw_buttons(selected)



            if (event.type == pygame.KEYDOWN):
                pass
        if (loose and game_started):
            print('LOST')
            end()
            game_started=False
        elif(win and game_started):
            print('WIN')
            end()
            game_started=False

        pygame.display.flip()
        clock.tick(30)
        

    pygame.quit()
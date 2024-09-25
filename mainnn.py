import pygame
import math
import random

# setup display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT)) # thiết lập cửa sổ 
pygame.display.set_caption("Hangman Games!") #title game trên thanh công cụ

# button variables
RADIUS = 20 # ban kính của hình tròn chứa chữ cái
GAP = 15 # khoảngc cách các hình tròn 
letters = [] # danh sách chứa chữ cái gòm vị trí, kí tự , trangj thái hiển thị 
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2) #vi trí bắt đàua cua 1 hàng chữ cái 
starty = 400 #là vị trí y bắt đầu của hàng chữ cái. T
A = 65 #là mã ASCII của ký tự 'A'. 
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))#Khi i lớn hơn hoặc bằng 13 (chữ cái thuộc hàng thứ hai), i // 13 == 1 và tọa độ y sẽ được tăng thêm GAP + RADIUS * 2, tạo thành hàng 
    letters.append([x, y, chr(A + i), True])

# fonts tài liệu tham khảo font chữ https://coderslegacy.com/python/pygame-font/
LETTER_FONT = pygame.font.SysFont('comicsans', 40) #font chữ cái
WORD_FONT = pygame.font.SysFont('lucidaconsole', 60) #font từ
TITLE_FONT = pygame.font.SysFont('microsofthimalaya', 70) #tieu de trò chơi

# load images. 
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# game variables
hangman_status = 0
words = [ "BANANA"] #danh sách các từ cần tìm 
word = random.choice(words) #random từ 
guessed = []

# colors
WHITE = (205,230,255) # cường độ màu đỏ, xanh las , xanh dương 
BLACK = (0,0,0)


def draw():
    win.fill(WHITE)

    # draw title
    text = TITLE_FONT.render("DEVELOPER HANGMAN", 1, BLACK) #Phương thức này trả về một surface chứa văn bản "DEVELOPER HANGMAN" được render .1 là hủy răng cưa trên các chữ (nét rox hơn)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20)) #win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3) # bề mặt vẽ, màu , tọa độ , bán kính , độ dày đường tròn 
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    global hangman_status

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS) # phương thức này sẽ kiểm soát tốc độ khung hình, đảm bảo rằng vòng lặp không chạy quá nhanh và giữ ở mức 60 FPS.

        for event in pygame.event.get(): #pygame.event.get(): Hàm này trả về danh sách tất cả các sự kiện hiện tại trong hàng đợi sự kiện của Pygame. Các sự kiện này có thể bao gồm nhấp chuột, nhấn phím, di chuyển chuột
            if event.type == pygame.QUIT: #: Đây là một sự kiện được kích hoạt khi người dùng nhấn nút đóng cửa sổ (thường là nút "X" ở góc trên bên phải của cửa sổ). 
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN: #: Đây là một sự kiện được kích hoạt khi người dùng nhấn nút đóng cửa sổ (thường là nút "X" ở góc trên bên phải của cửa sổ). 
                m_x, m_y = pygame.mouse.get_pos() #vị tris chuôtj khi nhấn đúp 
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible: #Nếu visible là True, nghĩa là chữ cái này có thể được người chơi nhấn vào.
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False  #letter[3]: Trạng thái hiển thị của chữ cái (có phải là True hay False).
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
        
        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        
        if won:
            display_message("You WON!")
            break

        if hangman_status == 6:
            display_message("You LOST!")
            break
    
while True:
    
    main()
pygame.quit() ## Giải phóng tài nguyên và đóng Pygame
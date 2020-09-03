from pygame.locals import *
import pygame
import sys

def main():
    pygame.init()    # Pygameを初期化
    screen = pygame.display.set_mode((200, 100))    # 画面を作成
    pygame.display.set_caption("Pygame sample app")    # タイトルを作成
    
    button = pygame.Rect(30, 30, 50, 50)  # creates a rect object
    button2 = pygame.Rect(100, 30, 70, 50)  # creates a rect object

    #STEP1.フォントの用意  
    font = pygame.font.SysFont(None, 25)
    
    #STEP2.テキストの設定
    text1 = font.render("RED", True, (0,0,0))
    text2 = font.render("GREEN", True, (0,0,0))
    
    
    running = True
    #メインループ
    while running:
        screen.fill((0,0,0))  #画面を黒で塗りつぶす
        
        pygame.draw.rect(screen, (255, 0, 0), button)
        pygame.draw.rect(screen, (0, 255, 0), button2)

        screen.blit(text1, (40, 45))
        screen.blit(text2, (105,45))

        pygame.display.update() #描画処理を実行
        for event in pygame.event.get():
            if event.type == QUIT:  # 終了イベント
                running = False
                pygame.quit()  #pygameのウィンドウを閉じる
                sys.exit() #システム終了
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    print("red button was pressed")
                if button2.collidepoint(event.pos):
                    print("green button was pressed")
                    
                    
if __name__=="__main__":
    main()

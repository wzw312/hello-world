import pygame
import time
import random

# 初始化 pygame
pygame.init()

# 设定屏幕大小和颜色
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# 创建屏幕
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('贪吃蛇游戏')

# 设置蛇的初始大小
snake_block = 10
snake_speed = 5

# 设置时钟
clock = pygame.time.Clock()

# 使用 pygame.freetype 来加载中文字体
font_path = "C:/Windows/Fonts/SimHei.ttf"  # 使用字体文件的完整路径
font_style = pygame.freetype.Font(font_path, 25)  # 使用pygame.freetype.Font来加载字体

score_font = pygame.freetype.Font(font_path, 35)  # 分数的字体

# 加载音效文件
eat_sound = pygame.mixer.Sound("eat_sound.wav")  # 请替换为你自己的音效文件路径

# 加载背景音乐
pygame.mixer.music.load("background_music.wav")  # 请替换为你的背景音乐文件路径
pygame.mixer.music.set_volume(0.1)  # 设置音乐的音量，范围是 0.0 到 1.0
pygame.mixer.music.play(-1)  # -1 表示循环播放背景音乐

# 显示得分
def your_score(score):
    value, _ = score_font.render(f"你的得分: {score}", black)
    screen.blit(value, [0, 0])

# 画蛇
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, black, [x[0], x[1], snake_block, snake_block])

# 游戏主循环
def gameLoop():
    game_over = False
    game_close = False

    # 初始位置
    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    # 蛇身体
    snake_List = []
    Length_of_snake = 1

    # 食物的位置
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            screen.fill(blue)
            message, _ = font_style.render("你输了! 按 Q 退出 或 按 C 再来一次", red)
            screen.blit(message, [width / 6, height / 3])
            your_score(Length_of_snake - 1)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # 确保蛇不反向
        if x1 + x1_change > width or x1 + x1_change < 0 or y1 + y1_change > height or y1 + y1_change < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(blue)

        # 画食物
        pygame.draw.rect(screen, yellow, [foodx, foody, snake_block, snake_block])

        # 更新蛇的身体
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 碰到自己
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        # 吃到食物，播放音效，生成新的食物
        if x1 == foodx and y1 == foody:
            eat_sound.play()  # 播放吃到食物的声音
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()

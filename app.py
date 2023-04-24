import tkinter as tk
import pygame
# import pyautogui
import random
import math
import os
import pandas as pd


pygame.init()
# 색깔
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

FONT = pygame.font.SysFont('malgungothic', 30)

# display_info = pygame.display.Info()
# # DPI = min(display_info.current_w, display_info.current_h) / 24.5

# print(display_info.current_w, display_info.current_h)

def cal_dpi(diagonal_in):
    display_info = pygame.display.Info()
    diagonal_px = math.sqrt(display_info.current_w ** 2 + display_info.current_h ** 2)

    dpi = diagonal_px / diagonal_in
    print (dpi/2.54)
    return dpi/2.54


# WIN_WIDTH = display_info.current_w
# WIN_HEIGHT = display_info.current_h

# screen_size = [display_info.current_w, display_info.current_h]

# 시작 위치와 목적지 사이의 거리 계산 함수
def calculate_distance(position1, position2):
    if position1 and position2:
        start_x, start_y = position1
        target_x, target_y = position2
        return ((target_x - start_x) ** 2 + (target_y - start_y) ** 2) ** 0.5
    else:
        return 100

# # 타겟 원 그리기 함수
# def draw_circle(screen, center_size, target_size, number_of_target):
#     for angle in range(0, number_of_target):
#         x = WIN_WIDTH/2 + center_size * math.cos(math.radians(360/number_of_target*angle))
#         y = WIN_HEIGHT/2 + center_size * math.sin(math.radians(360/number_of_target*angle))
#         pygame.draw.circle(screen, BLACK, (x, y), int(target_size/2), 2)
#         number = FONT.render("%d"%(int(angle)+1),True, BLACK)
#         #숫자쓰기
#         screen.blit(number, (x-20, y-20))

def circle_pos(center_size, number_of_target, angle):
    display_info = pygame.display.Info()
    WIN_WIDTH = display_info.current_w
    WIN_HEIGHT = display_info.current_h
    x = WIN_WIDTH/2 + center_size/2 * math.cos(math.radians(360/number_of_target*angle))
    y = WIN_HEIGHT/2 + center_size/2 * math.sin(math.radians(360/number_of_target*angle))
    return (int(x), int(y))
        
def test_pygame(subject_number, target_size=1, center_size=1, number_of_target=16, repeat_cycle=1, target_show=1, control_show=0, DPI=None):

    pygame.init()
    # 폰트
    FONT = pygame.font.SysFont('malgungothic', 30)
    
    #입력한 크기
    input_data = (target_size, center_size)
    
    #타겟 및 중심원 DPI로
    target_size = round(target_size * DPI, 1)
    center_size = round(center_size * DPI, 1)
    
    display_info = pygame.display.Info()
    # DPI = min(display_info.current_w, display_info.current_h) / 24.5

    print(display_info.current_w, display_info.current_h)

    WIN_WIDTH = display_info.current_w
    WIN_HEIGHT = display_info.current_h

    screen_size = [display_info.current_w, display_info.current_h]

    # pygame 창 생성
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

    #랜덤 타겟 시작
    start_target = random.randrange(0,number_of_target)+1
    first_target_num = start_target
    
    target_pos = circle_pos(center_size, number_of_target, start_target)
    first_target_pos = circle_pos(center_size, number_of_target, start_target)
    
    goal_pos = circle_pos(center_size, number_of_target, int(start_target+int(number_of_target/2))%number_of_target)
    
    # 타겟 슬라이더 설정
    target_slider_x = 100
    target_slider_y = 100
    target_slider_width = 100
    target_slider_height = 20
    target_slider_value = target_size
    target_slider_rect = pygame.Rect(target_slider_x, target_slider_y, target_slider_width, target_slider_height)

    # 센터 슬라이더 설정
    center_slider_x = 100
    center_slider_y = 160
    center_slider_width = 100
    center_slider_height = 20
    center_slider_value = center_size
    center_slider_rect = pygame.Rect(center_slider_x, center_slider_y, center_slider_width, center_slider_height)

    # 실험 횟수
    num_circle = repeat_cycle
    
    num_trials = 0

    # 실험 결과 기록
    results = []
    results2 = []

    screen.fill(WHITE)

        
    running = True
    
    target_draging = False
    target_con_draging = False
    center_con_dragging = False
    
    while running:

        screen.fill(WHITE)
        
        #타겟 위치들 보여주기
        if (target_show):
            for angle in range(0, number_of_target):
                x = WIN_WIDTH/2 + center_size/2 * math.cos(math.radians(360/number_of_target*angle))
                y = WIN_HEIGHT/2 + center_size/2 * math.sin(math.radians(360/number_of_target*angle))
                pygame.draw.circle(screen, BLACK, (x, y), int(target_size/2), 2)
                number = FONT.render("%d"%(int(angle)+1),True, BLACK)
                #숫자쓰기
                if control_show:
                    screen.blit(number, (x-20, y-20))
        
        if control_show:
            # 타겟 슬라이더 그리기
            pygame.draw.rect(screen, BLACK, target_slider_rect, 2)
            target_slider_value_rect = pygame.Rect(target_slider_x + (target_slider_value/(10*DPI) * target_slider_width) - 5, target_slider_y - 4, 10, target_slider_height + 8)
            pygame.draw.rect(screen, RED, target_slider_value_rect)
            
            # 타겟 슬라이더 값 텍스트 그리기
            target_slider_value_text = FONT.render(str(round(target_slider_value/DPI,1 )), True, BLACK)
            screen.blit(target_slider_value_text, (target_slider_x + target_slider_width + 10, target_slider_y - 4))

            # 센터 슬라이더 그리기
            pygame.draw.rect(screen, BLACK, center_slider_rect, 2)
            center_slider_value_rect = pygame.Rect(center_slider_x + (center_slider_value/(40*DPI) * center_slider_width) - 5, center_slider_y - 4, 10, center_slider_height + 8)
            pygame.draw.rect(screen, RED, center_slider_value_rect)

            # 센터 슬라이더 값 텍스트 그리기
            center_slider_value_text = FONT.render(str(round(center_slider_value/DPI, 1)), True, BLACK)
            screen.blit(center_slider_value_text, (center_slider_x + center_slider_width + 10, center_slider_y - 4))

        #목적지
        pygame.draw.circle(screen, BLUE, goal_pos, int(target_size/2))
        
        #시작점
        pygame.draw.circle(screen, RED, target_pos, int(target_size/2))
        
        pygame.display.update()

    # 마우스 이벤트 처리 함수
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #타겟 슬라이더 인식
                    if target_slider_rect.collidepoint(event.pos) and control_show:
                        target_con_draging = True

                    
                    #센터 슬라이더 인식
                    elif center_slider_rect.collidepoint(event.pos) and control_show:
                        center_con_dragging = True

                    else:
                        num_trials += 1
                        grap_x, grap_y = None, None
                        start_time = pygame.time.get_ticks()
                        print(target_size/DPI, calculate_distance(event.pos, target_pos)/DPI*2)            
                        if calculate_distance(event.pos, target_pos) < target_size/2:
                            # print(target_size/DPI, calculate_distance(event.pos, target_pos)/DPI*2)
                            target_draging = True
                            mouse_x, mouse_y = event.pos
                            grap_x, grap_y = event.pos
                            first_target_pos = circle_pos(center_size, number_of_target, start_target)
                            target_pos = (mouse_x, mouse_y)
                            results.append({"Part_num": subject_number,
                                "Target_size(cm)": input_data[0], 
                                "Center_size(cm)": input_data[1],
                                "Number_of_target": number_of_target,
                                "Result": "Grap",
                                "Num_of_try": num_trials,
                                "Target_num": start_target+1,
                                "Target_pos": first_target_pos, 
                                "Goal_num": int(start_target+int(number_of_target/2))%number_of_target+1,
                                "Goal_pos": goal_pos,
                                "Click_pos": event.pos,
                                "Release_pos": None,
                                "Dist_to_Target(cm)": calculate_distance(event.pos, first_target_pos)/DPI,
                                "Dist_to_Goal(cm)": calculate_distance(event.pos, goal_pos)/DPI,
                                "Start_time": start_time,
                                "End_time": None, 
                                "Task_duration(ms)": None})
                            results2.append({"Part_num": subject_number,
                                "Target_size(cm)": input_data[0], 
                                "Center_size(cm)": input_data[1],
                                "Number_of_target": number_of_target,
                                "Result": "Grap",
                                "Num_of_try": num_trials,
                                "Target_num": start_target+1,
                                "Target_pos": first_target_pos, 
                                "Goal_num": int(start_target+int(number_of_target/2))%number_of_target+1,
                                "Goal_pos": goal_pos,
                                "Click_pos": event.pos,
                                "Release_pos": None,
                                "Dist_to_Target(cm)": calculate_distance(event.pos, first_target_pos)/DPI,
                                "Dist_to_Goal(cm)": calculate_distance(event.pos, goal_pos)/DPI,
                                "Start_time": start_time,
                                "End_time": None, 
                                "Task_duration(ms)": None})

                        else:
                            results.append({"Part_num": subject_number,
                                            "Target_size(cm)": input_data[0], 
                                            "Center_size(cm)": input_data[1],
                                            "Number_of_target": number_of_target,
                                            "Result": "Grap_miss",
                                            "Num_of_try": num_trials,
                                            "Target_num": start_target+1,
                                            "Target_pos": target_pos, 
                                            "Goal_num": int(start_target+int(number_of_target/2))%number_of_target+1,
                                            "Goal_pos": goal_pos,
                                            "Click_pos": event.pos,
                                            "Release_pos": None,
                                            "Dist_to_Target(cm)": calculate_distance(event.pos, target_pos)/DPI,
                                            "Dist_to_Goal(cm)": calculate_distance(event.pos, goal_pos)/DPI,
                                            "Start_time": start_time,
                                            "End_time": None, 
                                            "Task_duration(ms)": None})
                            results2.append({"Part_num": subject_number,
                                            "Target_size(cm)": input_data[0], 
                                            "Center_size(cm)": input_data[1],
                                            "Number_of_target": number_of_target,
                                            "Result": "Grap_miss",
                                            "Num_of_try": num_trials,
                                            "Target_num": start_target+1,
                                            "Target_pos": target_pos, 
                                            "Goal_num": int(start_target+int(number_of_target/2))%number_of_target+1,
                                            "Goal_pos": goal_pos,
                                            "Click_pos": event.pos,
                                            "Release_pos": None,
                                            "Dist_to_Target(cm)": calculate_distance(event.pos, target_pos)/DPI,
                                            "Dist_to_Goal(cm)": calculate_distance(event.pos, goal_pos)/DPI,
                                            "Start_time": start_time,
                                            "End_time": None, 
                                            "Task_duration(ms)": None})


                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 & target_con_draging:
                    target_con_draging = False
                    target_slider_value = (event.pos[0] - target_slider_x) / target_slider_width * 10 * DPI # 슬라이더 값 계산 0~10
                    target_slider_value = round(max(0, min(10 * DPI, target_slider_value)), 1)  # 슬라이더 값 범위 제한
                    target_size = target_slider_value

                    target_pos = circle_pos(center_size, number_of_target, start_target)
                    goal_pos = circle_pos(center_size, number_of_target, int(start_target+int(number_of_target/2))%number_of_target)
                    input_data = (round(target_size/DPI,1), round(center_size/DPI,1))

                elif event.button == 1 & center_con_dragging:
                    center_con_dragging = False
                    center_slider_value = (event.pos[0] - center_slider_x) / center_slider_width * 40 * DPI # 슬라이더 값 계산 0~40
                    center_slider_value = round(max(0, min(40*DPI, center_slider_value)), 1)  # 슬라이더 값 범위 제한
                    center_size = center_slider_value

                    target_pos = circle_pos(center_size, number_of_target, start_target)
                    goal_pos = circle_pos(center_size, number_of_target, int(start_target+int(number_of_target/2))%number_of_target)
                    input_data = (round(target_size/DPI,1), round(center_size/DPI,1))

                elif event.button == 1 & target_draging:
                    end_time  = pygame.time.get_ticks()            
                    target_draging = False
                    if calculate_distance(event.pos, goal_pos) < target_size/2:
                        print(target_size/DPI, calculate_distance(event.pos, goal_pos)/DPI)

                        results.append({"Part_num": subject_number,
                                        "Target_size(cm)": input_data[0], 
                                        "Center_size(cm)": input_data[1],
                                        "Number_of_target": number_of_target,
                                        "Result": "Success",
                                        "Num_of_try": num_trials,
                                        "Target_num": start_target+1,
                                        "Target_pos": first_target_pos, 
                                        "Goal_num": int(start_target+int(number_of_target/2))%number_of_target+1,
                                        "Goal_pos": goal_pos,
                                        "Click_pos": (grap_x, grap_y),
                                        "Release_pos": event.pos,
                                        "Dist_to_Target(cm)": calculate_distance(event.pos, first_target_pos)/DPI,
                                        "Dist_to_Goal(cm)": calculate_distance(event.pos, goal_pos)/DPI,
                                        "Start_time": start_time,
                                        "End_time": end_time, 
                                        "Task_duration(ms)": end_time - start_time})
                        results2.append({"Part_num": subject_number,
                                        "Target_size(cm)": input_data[0], 
                                        "Center_size(cm)": input_data[1],
                                        "Number_of_target": number_of_target,
                                        "Result": "Success",
                                        "Num_of_try": num_trials,
                                        "Target_num": start_target+1,
                                        "Target_pos": first_target_pos, 
                                        "Goal_num": int(start_target+int(number_of_target/2))%number_of_target+1,
                                        "Goal_pos": goal_pos,
                                        "Click_pos": (grap_x, grap_y),
                                        "Release_pos": event.pos,
                                        "Dist_to_Target(cm)": calculate_distance(event.pos, first_target_pos)/DPI,
                                        "Dist_to_Goal(cm)": calculate_distance(event.pos, goal_pos)/DPI,
                                        "Start_time": start_time,
                                        "End_time": end_time, 
                                        "Task_duration(ms)": end_time - start_time})
                        
                        start_target = int(start_target+int(number_of_target/2))%number_of_target
                        target_pos = circle_pos(center_size, number_of_target, start_target)
                        goal_pos = circle_pos(center_size, number_of_target, int(start_target+int(number_of_target/2))%number_of_target)
                        num_trials = 0
                        if start_target == first_target_num:
                            repeat_cycle -= 1
                            if repeat_cycle < 1:
                                running = False
                    else:
                        target_pos = circle_pos(center_size, number_of_target, start_target)
                        results.append({"Part_num": subject_number,
                                        "Target_size(cm)": input_data[0], 
                                        "Center_size(cm)": input_data[1],
                                        "Number_of_target": number_of_target,
                                        "Result": "Move_miss",
                                        "Num_of_try": num_trials,
                                        "Target_num": start_target+1,
                                        "Target_pos": first_target_pos, 
                                        "Goal_num": int(start_target+int(number_of_target/2))%number_of_target+1,
                                        "Goal_pos": goal_pos,
                                        "Click_pos": (grap_x, grap_y),
                                        "Release_pos": event.pos,
                                        "Dist_to_Target(cm)": calculate_distance(event.pos, first_target_pos)/DPI,
                                        "Dist_to_Goal(cm)": calculate_distance(event.pos, goal_pos)/DPI,
                                        "Start_time": start_time,
                                        "End_time": end_time, 
                                        "Task_duration(ms)": end_time - start_time})
                        results2.append({"Part_num": subject_number,
                                        "Target_size(cm)": input_data[0], 
                                        "Center_size(cm)": input_data[1],
                                        "Number_of_target": number_of_target,
                                        "Result": "Success",
                                        "Num_of_try": num_trials,
                                        "Target_num": start_target+1,
                                        "Target_pos": first_target_pos, 
                                        "Goal_num": int(start_target+int(number_of_target/2))%number_of_target+1,
                                        "Goal_pos": goal_pos,
                                        "Click_pos": (grap_x, grap_y),
                                        "Release_pos": event.pos,
                                        "Dist_to_Target(cm)": calculate_distance(event.pos, first_target_pos)/DPI,
                                        "Dist_to_Goal(cm)": calculate_distance(event.pos, goal_pos)/DPI,
                                        "Start_time": start_time,
                                        "End_time": end_time, 
                                        "Task_duration(ms)": end_time - start_time})
                    end_time = None
            elif event.type == pygame.MOUSEMOTION:
                if target_draging:
                    mouse_x, mouse_y = event.pos
                    # target_pos = (mouse_x + offset_x, mouse_y + offset_y)
                    target_pos = (mouse_x, mouse_y)
                    results2.append({"Part_num": subject_number,
                                    "Target_size(cm)": input_data[0], 
                                    "Center_size(cm)": input_data[1],
                                    "Number_of_target": number_of_target,
                                    "Result": "Moving",
                                    "Num_of_try": num_trials,
                                    "Target_num": start_target+1,
                                    "Target_pos": target_pos, 
                                    "Goal_num": int(start_target+int(number_of_target/2))%number_of_target+1,
                                    "Goal_pos": goal_pos,
                                    "Click_pos": event.pos,
                                    "Release_pos": None,
                                    "Dist_to_Target(cm)": calculate_distance(event.pos, target_pos)/DPI,
                                    "Dist_to_Goal(cm)": calculate_distance(event.pos, goal_pos)/DPI,
                                    "Start_time": start_time,
                                    "End_time": None, 
                                    "Task_duration(ms)": None})
                if target_con_draging:
                    target_slider_value = (event.pos[0] - target_slider_x) / target_slider_width * 10 * DPI # 슬라이더 값 계산 0~10
                    target_slider_value = round(max(0, min(10 * DPI, target_slider_value)), 1)  # 슬라이더 값 범위 제한
                    target_size = target_slider_value

                    target_pos = circle_pos(center_size, number_of_target, start_target)
                    goal_pos = circle_pos(center_size, number_of_target, int(start_target+int(number_of_target/2))%number_of_target)
                
                if center_con_dragging:
                    center_slider_value = (event.pos[0] - center_slider_x) / center_slider_width * 40 * DPI # 슬라이더 값 계산 0~40
                    center_slider_value = round(max(0, min(40*DPI, center_slider_value)), 1)  # 슬라이더 값 범위 제한
                    center_size = center_slider_value

                    target_pos = circle_pos(center_size, number_of_target, start_target)
                    goal_pos = circle_pos(center_size, number_of_target, int(start_target+int(number_of_target/2))%number_of_target)



    # # 대기
    # pygame.time.wait(1000)
    
    #데이터 cv로 기록
    results_pd = pd.DataFrame(results)
    #기록
    os.makedirs("./data", exist_ok=True)
    file_name = "./data/{0}_{1}_{2}_{3}.csv".format(subject_number, input_data[0], input_data[1], int(number_of_target))
    if not os.path.exists(file_name):
        results_pd.to_csv(file_name,
                                index=False,
                                mode="w",
                                encoding="utf-8-sig")
    else:
        results_pd.to_csv(file_name,
                                index=False,
                                mode="a",
                                encoding="utf-8-sig",
                                header=False)
        
    #데이터 cv로 기록
    results2_pd = pd.DataFrame(results2)
    #기록
    os.makedirs("./data", exist_ok=True)
    file_name = "./data/{0}_{1}_{2}_{3}_moving.csv".format(subject_number, input_data[0], input_data[1], int(number_of_target))
    if not os.path.exists(file_name):
        results2_pd.to_csv(file_name,
                                index=False,
                                mode="w",
                                encoding="utf-8-sig")
    else:
        results2_pd.to_csv(file_name,
                                index=False,
                                mode="a",
                                encoding="utf-8-sig",
                                header=False)



    # pygame 종료
    pygame.quit()
    



def start_program():
    pygame.init()
    # 입력받은 값들을 가져옴
    subject_number = subject_number_entry.get()
    target_size = float(target_size_entry.get())
    center_size = float(center_size_entry.get())
    number_of_target = int(number_of_target_entry.get())
    repeat_cycle = int(repeat_cycle_entry.get())
    target_show = int(target_button_Var.get())
    control_show = int(control_button_Var.get())
    
    DPI = cal_dpi(float(monitor_diagoanl_entry.get()))

    # 실행할 프로그램 작성
    test_pygame(subject_number, target_size, center_size, number_of_target, repeat_cycle, target_show, control_show, DPI)
    
    # # 입력받은 값을 초기화
    # subject_number_entry.delete(0, tk.END)
    # target_size_entry.delete(0, tk.END)
    # center_size_entry.delete(0, tk.END)
    # number_of_target_entry.delete(0, tk.END)

# tkinter 윈도우 생성
window = tk.Tk()

# 창 크기 설정
window.geometry('500x500')


# 피험자 번호 입력 위젯
subject_number_label = tk.Label(window, text="Subject Number")
subject_number_label.pack()
subject_number_entry = tk.Entry(window)
subject_number_entry.pack()
subject_number_entry.focus()

# target size 입력 위젯
target_size_label = tk.Label(window, text="Target size(cm):")
target_size_label.pack()
target_size_entry = tk.Entry(window)
target_size_entry.pack()
target_size_entry.focus()

# center size 입력 위젯
center_size_label = tk.Label(window, text="Center size(cm):")
center_size_label.pack()
center_size_entry = tk.Entry(window)
center_size_entry.pack()

# number of target 입력 위젯
number_of_target_label = tk.Label(window, text="Number of target:")
number_of_target_label.pack()
number_of_target_entry = tk.Entry(window)
number_of_target_entry.insert(0, "15")
number_of_target_entry.pack()

#repeat cycle
repeat_cycle_label = tk.Label(window, text="Repeat cycle (원 한바퀴가 1회):")
repeat_cycle_label.pack()
repeat_cycle_entry = tk.Entry(window)
repeat_cycle_entry.insert(0, "1")
repeat_cycle_entry.pack()

lable0 = tk.Label(window, width=300)
lable0.pack()

# 타겟 나타내는 위젯
target_button_Label = tk.Label(lable0, text="-----------Target Show-------------")
target_button_Var = tk.IntVar()
target_button0 = tk.Radiobutton(lable0, text="No", variable=target_button_Var, value=0)
target_button1 = tk.Radiobutton(lable0, text="Yes(default)", variable=target_button_Var, value=1)
target_button1.select()
target_button_Label.pack()
target_button0.pack(side="left")
target_button1.pack(side="left")

lable2 = tk.Label(window, width=300)
lable2.pack()

# 타겟 나타내는 위젯
control_button_Label = tk.Label(lable2, text="-------Control Panel Show---------")
control_button_Var = tk.IntVar()
control_button0 = tk.Radiobutton(lable2, text="No(default)", variable=control_button_Var, value=0)
control_button1 = tk.Radiobutton(lable2, text="Yes", variable=control_button_Var, value=1)
control_button0.select()
control_button_Label.pack()
control_button0.pack(side="left")
control_button1.pack(side="left")

#repeat cycle
monitor_diagoanl_label = tk.Label(window, text="Monitor Diagonal (Inch):")
monitor_diagoanl_label.pack()
monitor_diagoanl_entry = tk.Entry(window)
# monitor_diagoanl_entry.insert(0, "15.6")
monitor_diagoanl_entry.pack()

lable1 = tk.Label(window, width=300)
lable1.pack()

# 실행 버튼
start_button = tk.Button(lable1, text="실험시작", command=start_program)

# 종료 버튼
end_button = tk.Button(lable1, text="실험종료", command=window.destroy)
start_button.pack(side="left")
end_button.pack(side="left")


# 창 중앙에 배치
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
x_pos = int(window.winfo_screenwidth() / 2 - window_width / 2)
y_pos = int(window.winfo_screenheight() / 2 - window_height / 2)
window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

# 윈도우 실행
window.mainloop()



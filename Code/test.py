import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 设置字体大小
plt.rcParams['font.size'] = 20
# 加粗图片边框
plt.rcParams['axes.linewidth'] = 2

data_path = r'Question\Wimbledon_featured_matches.csv'
data = pd.read_csv(data_path)
print(data.head())

def analyse_all_match(all_match):
    # 统计所有球员的姓名
    player1 = all_match['player1']
    player2 = all_match['player2']
    player = pd.concat([player1, player2], axis=0)
    # 取唯一值
    player = player.unique()
    # 字典序
    player.sort()
    player2index = {name: i for i, name in enumerate(player)}
    print(player2index)
    # 构建胜负矩阵
    win_matrix_serve_start = np.zeros((len(player), len(player)))
    win_matrix_return_start = np.zeros((len(player), len(player)))
    win_matrix_serve_after_win = np.zeros((len(player), len(player)))
    win_matrix_return_after_win = np.zeros((len(player), len(player)))
    win_matrix_serve_after_lose = np.zeros((len(player), len(player)))
    win_matrix_return_after_lose = np.zeros((len(player), len(player)))
    # 遍历每场比赛
    i = 0
    groupby_match = all_match.groupby('match_id')
    for match_id, match in groupby_match:
        # 一场比赛的数据
        player1 = match['player1'].values[0]
        player2 = match['player2'].values[0]
        groupby_set = match.groupby('set_no')
        for set_no, one_set in groupby_set:
            groupby_game = one_set.groupby('game_no')
            pre_winner = 0
            for point_no, one_point in groupby_game:
                for index, point in one_point.iterrows():
                    i += 1
                    print(i)
                    point_victor = point['point_victor']
                    serve_flag = point['server']
                    
                    if pre_winner == 0:
                        pre_winner = point_victor
                        if serve_flag == 1:
                            if point_victor == 1:
                                win_matrix_serve_start[player2index[player1], player2index[player2]] += 1
                            else:
                                win_matrix_return_start[player2index[player2], player2index[player1]] += 1
                        else:
                            if point_victor == 1:
                                win_matrix_return_start[player2index[player1], player2index[player2]] += 1
                            else:
                                win_matrix_serve_start[player2index[player2], player2index[player1]] += 1
                        continue
                    if pre_winner == 1:
                        if serve_flag == 1:
                            if point_victor == 1:
                                win_matrix_serve_after_win[player2index[player1], player2index[player2]] += 1
                            else:
                                win_matrix_return_after_lose[player2index[player2], player2index[player1]] += 1
                        else:
                            if point_victor == 1:
                                win_matrix_return_after_lose[player2index[player1], player2index[player2]] += 1
                            else:
                                win_matrix_serve_after_win[player2index[player2], player2index[player1]] += 1
                    else:
                        if serve_flag == 1:
                            if point_victor == 1:
                                win_matrix_serve_after_lose[player2index[player1], player2index[player2]] += 1
                            else:
                                win_matrix_return_after_win[player2index[player2], player2index[player1]] += 1
                        else:
                            if point_victor == 1:
                                win_matrix_return_after_lose[player2index[player1], player2index[player2]] += 1
                            else:
                                win_matrix_serve_after_win[player2index[player2], player2index[player1]] += 1
    return win_matrix_serve_start, win_matrix_return_start, win_matrix_serve_after_win, win_matrix_return_after_win, win_matrix_serve_after_lose, win_matrix_return_after_lose, player
win_matrix_serve_start, win_matrix_return_start, win_matrix_serve_after_win, win_matrix_return_after_win, win_matrix_serve_after_lose, win_matrix_return_after_lose, player = analyse_all_match(data)
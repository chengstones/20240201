import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 设置字体大小
plt.rcParams['font.size'] = 20

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
    # 构建胜负矩阵
    win_matrix = np.zeros((len(player), len(player)))
    lose_matrix = np.zeros((len(player), len(player)))
    # 遍历每场比赛
    for row in all_match.iterrows():
        # 获取比赛结果
        row = row[1]
        player1 = row['player1']
        player2 = row['player2']
        win_index = row['point_victor']
        winner_index = player2index[player1] if win_index == 1 else player2index[player2]
        loser_index = player2index[player1] if win_index == 2 else player2index[player2]
        # 更新胜负矩阵
        win_matrix[winner_index, loser_index] += 1
        lose_matrix[loser_index, winner_index] += 1
    return win_matrix, lose_matrix, player
win_matrix, lose_matrix, player = analyse_all_match(data)

def cal_likelihood(gamma, win_matrix, lose_matrix):
    likelihood = 0
    for i in range(len(player)):
        for j in range(len(player)):
            if i != j:
                likelihood += win_matrix[i, j] * np.log(gamma[i] / (gamma[i] + gamma[j]))
    return likelihood

def Bradley_Terry(win_matrix, lose_matrix, player):
    # 初始化参数
    gamma = np.ones(len(player))
    # 迭代次数
    max_iter = 100
    likelihood_list = []
    # 迭代
    for _ in range(max_iter):
        # 更新参数
        gamma_copy = gamma.copy()
        for i in range(len(player)):
            W = np.sum(win_matrix[i, :])
            N = win_matrix[i, :] + lose_matrix[i, :]
            gamma_sum = gamma[i] + gamma
            sum_ = np.sum(N / gamma_sum)
            gamma_copy[i] = W / sum_
        gamma = gamma_copy
        # 计算似然函数值
        # likelihood = cal_likelihood(gamma, win_matrix, lose_matrix)
        # likelihood_list.append(likelihood)
    return gamma, likelihood_list

gamma, likelihood_list = Bradley_Terry(win_matrix, lose_matrix, player)
plt.plot(likelihood_list)
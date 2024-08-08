import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sympy as sp#导入SymPy库

plt.rcParams['font.sans-serif'] = ['SimHei']


# 假设
# 1. 交配期结束同一栏中的所有母羊同时受孕
# 2. 公羊与母羊配对比例为1:14
# 3. 多批所占羊栏数求和时不考虑配种期导致的种公羊栏数减少
# 4. 公羊数与间隔时间相互独立
# 5. 忽略闰年


# 常量

## 时间
mating_days = 20  # 配种期天数
gestation_days = 149  # 母羊怀孕期天数
lactation_days = 40  # 哺乳期天数
weaning_days = 210  # 育肥期天数
empty_days = 20  # 母羊空怀休整期天数


## 羊栏容量
capacity_mating = 15  # 配种期每栏最多容纳 1只种公羊 + 14只母羊
capacity_pregnant = 8  # 怀孕期每栏最多容纳8只待产母羊
capacity_lactation = 6  # 哺乳期每栏最多容纳6只母羊及其羔羊
capacity_weaning = 14  # 育肥期每栏最多容纳14只羔羊
capacity_rest = 14  # 空怀休整期每栏最多容纳14只母羊
capacity_rams = 4  # 非交配期每栏最多容纳4只种公羊

## 现有羊栏数量
total_sheds = 112  # 养殖场现有的标准羊栏数量

## 产羔数
lambing_rate = 2  # 母羊平均每胎产羔数

rate=14 # 母羊与公羊配种之比
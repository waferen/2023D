import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sympy #导入SymPy库

plt.rcParams['font.sans-serif'] = ['SimHei']

# 输出
with open('2023D\Q1\\result\\result_1.txt', 'w',encoding='UTF-8') as f:

    # 假设
    # 1. 交配期结束同一栏中的所有母羊同时受孕
    # 2. 公羊与母羊配对比例为1:14

    # 常量

    ## 时间
    gestation_days = 149  # 母羊怀孕期天数
    lactation_days = 40  # 哺乳期天数
    weaning_days = 210  # 育肥期天数
    empty_days = 20  # 母羊空怀休整期天数
    mating_days = 20  # 配种期天数

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

    ## 母羊与公羊之比
    rate = 14

    # 变量

    num_rams = 4 #种公羊数量
    num_ewes = rate*num_rams  # 基础母羊数量
    num_pregnant = 0  # 待产母羊数量
    num_lactation = 0  # 哺乳期母羊数量
    num_rest = 0  # 空怀休整期母羊数量
    num_lambs = 0  # 羔羊数量

    # 计算

    ## 计算最大容量，即固定公羊数量，母羊数量，求最大容量
    ## 由于种羊数目固定，母羊个数固定，则生产效率固定。由于从第一批羔羊育肥出栏需要210天，出栏速率固定。所以找出210天中需要羊栏数最多的情况即可推出最多多少只羊，即为最大容量。
    ## 这里母羊是主要生产资料，根据母羊数量，由于要提高空间利用率，按1:14的整数倍配种公羊。在母羊数目确定的情况下，生产效率是固定的。对于一个母羊，于209天，即20+149+40产生2只育肥羊。
    ## 育肥羊于210天后出栏，于209+210=419天后出栏。所以，对于一个母羊，于419天后产生2只出栏羊。
    ## 假设公羊数为x,母羊数为14x,
    ## 于第一批育肥羊育肥的210天中， 在0-20天时，母羊进入休整期。                     于20-40天时，母羊进入配种期。             于40-189天时，母羊进入怀孕期。                           于189-210天时，母羊进入哺乳期。                于210-229天时，母羊进入哺乳期。               于229-249天时，母羊进入休整期。
    ## 所需羊栏数量：               配种羊栏为-(-x//4)，育肥羊栏为2x，休整母羊为x.    母羊羊栏x，育肥羊羊栏2x。                 公羊羊栏为-(-x//4)，母羊羊栏-(-14x//8)，育肥羊羊栏为2x。  母羊-(-14x//6)，公羊-(-x//4)，育肥羊羊栏为2x。 母羊-(-14x//6)，公羊-(-x//4)，育肥羊羊栏为0   母羊x，公羊-(-x//4)，育肥羊羊栏为0
    ## 在一次循环中，需要羊栏最多的时刻为第438天时，此时上一轮育肥羊差一天出栏，而母羊进入空怀休整期，此时需要的羊栏数为x-(-x//4)+4x,分别为种羊羊栏，母羊羊栏，育肥羊羊栏。
    ## 最大为112只羊栏。
    
    ## 计算向上取整
    def ceil(x,y):
        return -(-x//y) 

    ## 对于固定的公羊母羊数量，我们先计算一组即1_14的比例来计算一组419天中每天的羊栏占用数
    def occupied_sheds(num_rams):
        days=0
        list_sheds=[]
        while days<=478:
            days+=1
            # 第一轮交配期
            if days<=20:
                list_sheds.append(ceil(rate*num_rams,capacity_mating))
            # 第一轮怀孕期
            elif days<=169:
                list_sheds.append(ceil(num_rams,capacity_rams)+ceil(rate*num_rams,capacity_pregnant))
            # 第一轮哺乳期
            elif days<=209:
                list_sheds.append(ceil(num_rams,capacity_rams)+ceil(rate*num_rams,capacity_lactation))
            # 第一轮休整期
            elif days<=229:
                list_sheds.append(ceil(num_rams,capacity_rams)+ceil(rate*num_rams,capacity_rest)+ceil(rate*num_rams*lambing_rate,capacity_weaning))
            # 第二轮交配期
            elif days<=249:
                list_sheds.append(ceil(rate*num_rams,capacity_mating)+ceil(rate*num_rams*lambing_rate,capacity_weaning))
            # 第二轮怀孕期
            elif days<=398:
                list_sheds.append(ceil(num_rams,capacity_rams)+ceil(rate*num_rams,capacity_pregnant)+ceil(rate*num_rams*lambing_rate,capacity_weaning))
            # 第二轮哺乳期第一阶段
            elif days<=419:
                list_sheds.append(ceil(num_rams,capacity_rams)+ceil(rate*num_rams,capacity_lactation)+ceil(rate*num_rams*lambing_rate,capacity_weaning))
            # 第二轮哺乳期第二阶段
            elif days<=438:
                list_sheds.append(ceil(num_rams,capacity_rams)+ceil(rate*num_rams,capacity_lactation))
            # 第二轮休整期
            elif days<=458:
                list_sheds.append(ceil(num_rams,capacity_rams)+ceil(rate*num_rams,capacity_rest))
            # 第三轮交配期
            elif days<=478:
                list_sheds.append(ceil(rate*num_rams,capacity_mating))
        return list_sheds
    # 绘图
    ## 绘制羊栏占用数随时间变化的折线图
    def plot_1(occupied_sheds_list):
        plt.figure(figsize=(12, 6))
        
        # 绘制数据
        plt.plot(occupied_sheds_list, linestyle='-', color='b', linewidth=2, label='羊栏占用数')
        
        # 设置标题和标签
        plt.xlabel('天数/天', fontsize=14, fontweight='bold')
        plt.ylabel('羊栏占用数/栏', fontsize=14, fontweight='bold')
        plt.title('1_14羊栏占用数随时间的变化周期', fontsize=16, fontweight='bold')
        
        # 添加网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='grey', alpha=0.7)
        
        # 添加图例
        plt.legend(loc='upper left', fontsize=12)
        
        # 设置x轴和y轴刻度字体大小
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        
        # 调整子图的布局，使得标题和标签不重叠
        plt.tight_layout()
        
        # 保存图像
        plt.savefig('2023D\\figs\\1_14羊栏占用数随时间的变化周期.pdf', format='pdf')
        
        # 显示图像
        plt.show()
    
    ## 绘制年产羔数随年份变化的折线图
    def plot_2(num_rams):
        x = np.arange(0, 25, 1)

        y = [round(rate * lambing_rate * num_rams * times * 365 / (419 + 229 * (times - 1))) for times in x]

        plt.figure(figsize=(10, 6))
        plt.plot(x, y, marker="o", mfc="white", ms=8, linestyle="-", color="#1f77b4", label="年产羔数")

        plt.xlabel('轮次/次', fontsize=12, fontweight='bold')
        plt.ylabel('年产羔数/只', fontsize=12, fontweight='bold')
        plt.title('1_14年出栏数与出栏次数关系', fontsize=14, fontweight='bold')

        plt.grid(ls="--", lw=0.5, color="#4E616C")
        plt.legend()

        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)

        # 添加平均值线
        y_mean = np.mean(y)
        plt.axhline(y=y_mean, color='r', linestyle='--', label='平均值')
        plt.legend()
        plt.text( -3, y_mean, f'{y_mean:.2f}', color='r', va='center', ha='left', fontsize=10)

        # 添加极限值
        x = sympy.symbols('x')
        y_limit=sympy.limit(rate*lambing_rate*num_rams*x*365/(419+229*(x-1)),x,sympy.oo)
        y_limit=float(y_limit)
        plt.axhline(y=y_limit, color='g', linestyle='--', label='极限')
        plt.legend()
        plt.text( -3, y_limit, f'{y_limit:.2f}', color='g', va='center', ha='left', fontsize=10)

        # 保存图像为矢量图格式
        plt.savefig('2023D\\figs\\1_14年出栏数与出栏次数关系.pdf', format='pdf')
        plt.show()

    
    #通过公羊数反推最大的羊栏数
    def max_sheds(num_rams):
        occupied_sheds_list=occupied_sheds(num_rams)
        max_capacity=max(occupied_sheds_list)
        return max_capacity
    
    # 主程序
    occupied_sheds_list=occupied_sheds(num_rams)
    num_rams=1
    
    # 求最大种公羊数
    while max(occupied_sheds_list)<=total_sheds:
        num_rams+=1
        occupied_sheds_list=occupied_sheds(num_rams)
    # 求值
    num_rams-=1
    num_ewes=num_rams*rate
    num_lambs=num_rams*rate*lambing_rate
    max_capacity=max(occupied_sheds_list)
    # 当公羊数为36时
    max_capacity=max_sheds(36)

    # 求极限
    x = sympy.symbols('x')
    y_limit = round(sympy.limit(rate*lambing_rate*num_rams*x*365/(419+229*(x-1)),x,sympy.oo))

    # 输出
    print("当年份趋向无穷大时，年出栏数为：",y_limit,file=f)
    print('最多占用羊栏数为：',max_capacity,file=f)
    print("种公羊数：",num_rams,'母羊数：',num_ewes,'单次出栏数：',num_lambs,'年出栏数：',y_limit,file=f)
    print("当公羊数为36时，最大羊栏数为：",max_capacity,file=f)
    
    # 绘图
    plot_1(occupied_sheds_list)
    plot_2(num_rams)
    


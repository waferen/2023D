from head import *
# 输出
with open('2023D\Q1\\result\\result_3.txt', 'w',encoding='UTF-8') as f:
   
    # 变量
    num_rate = 42 # 母羊与公羊数量之比
    num_rams = 4 #种公羊数量
    num_ewes = rate*num_rams  # 基础母羊数量
    num_pregnant = 0  # 待产母羊数量
    num_lactation = 0  # 哺乳期母羊数量
    num_rest = 0  # 空怀休整期母羊数量
    num_lambs = 0  # 羔羊数量
    
 
    # 计算
    
    ## 计算向上取整
    def ceil(x,y):
        return -(-x//y) 

    ## 对于固定的公羊母羊数量，我们先计算一组即1_14的比例来计算一组419天中每天的羊栏占用数
    def occupied_sheds(num_rams):
        days=0
        list_sheds=[]
        while days<=458:
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
        return list_sheds
    
    # 绘图
    ## 1-42 羊栏占用图
    def plot_3(occupied_sheds_list, day1, day2, new_sheds1, new_sheds2, original_sheds):
        # 确保 new_sheds1, new_sheds2 和 original_sheds 的长度与 occupied_sheds_list 一致
        new_sheds1 = new_sheds1[:len(occupied_sheds_list)]
        new_sheds2 = new_sheds2[:len(occupied_sheds_list)]
        original_sheds = original_sheds[:len(occupied_sheds_list)]
        
        plt.figure(figsize=(12, 6))
        x = np.arange(0, len(occupied_sheds_list), 1)
        
        # 绘制数据
        plt.plot(x, occupied_sheds_list, linestyle='-', color='b', linewidth=2, label='羊栏占用数')
        plt.plot(x, new_sheds1, linestyle='--', color='r', linewidth=2, label='第一批羊栏占用数')
        plt.plot(x, new_sheds2, linestyle=':', color='orange', linewidth=2, label='第二批羊栏占用数')
        plt.plot(x, original_sheds, linestyle='-.', color='g', linewidth=2, label='第三批羊栏占用数')
        
        # 设置标题和标签
        plt.xlabel('天数/天', fontsize=14, fontweight='bold')
        plt.ylabel('羊栏占用数/栏', fontsize=14, fontweight='bold')
        plt.title('1_42羊栏占用数随时间的变化周期', fontsize=16, fontweight='bold')
        
        # 添加网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='grey', alpha=0.7)
        
        # 添加图例
        plt.legend(loc='upper left', fontsize=12)
        
        # 设置x轴和y轴刻度字体大小
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        
        # 在 x 轴上标出 day1 和 day2 的值
        plt.axvline(x=day1, color='purple', linestyle=':', linewidth=2)
        plt.text(day1, plt.ylim()[0] - 0.05*(plt.ylim()[1] - plt.ylim()[0]), f'Day {day1}', 
                color='purple', fontsize=12, verticalalignment='top', horizontalalignment='center', 
                rotation=0, fontweight='bold')
        
        plt.axvline(x=day2, color='brown', linestyle=':', linewidth=2)
        plt.text(day2, plt.ylim()[0] - 0.05*(plt.ylim()[1] - plt.ylim()[0]), f'Day {day2}', 
                color='brown', fontsize=12, verticalalignment='top', horizontalalignment='center', 
                rotation=0, fontweight='bold')
        
        # 调整子图的布局，使得标题和标签不重叠
        plt.tight_layout()
        
        # 保存图像
        plt.savefig('2023D\\figs\\1_42羊栏占用数随时间的变化周期.pdf', format='pdf')
        
        # 显示图像
        plt.show()

    ## 1-28 求间隔天数
    def find_min_max_sheds_2(num_rams):
        original_sheds = occupied_sheds(num_rams)
        min_max_value = float('inf')
        imin=0
        for i in range(20,len(original_sheds)):
            new_sheds = original_sheds[i:] + original_sheds[:i]
            original_sheds = original_sheds
            max_sheds = max([original + new for original, new in zip(original_sheds, new_sheds)])
            if max_sheds < min_max_value:
                imin=i
            min_max_value = min(min_max_value, max_sheds)
        
        return min_max_value,imin
    
    ## 1-42 求间隔天数
    def find_min_max_sheds_3(num_rams):
        original_sheds = occupied_sheds(num_rams)
        min_max_value = float('inf')
        imin1 = 0
        imin2 = 0
        
        for i in range(20, len(original_sheds)):
            new_sheds1 = original_sheds[i:] + original_sheds[:i]
            for j in range(20, len(original_sheds)):
                new_sheds2 = original_sheds[j:] + original_sheds[:j]
                
                # 计算 original_sheds, new_sheds1, new_sheds2 的和
                max_sheds = max([original + new1 + new2 for original, new1, new2 in zip(original_sheds, new_sheds1, new_sheds2)])
                
                if max_sheds < min_max_value:
                    imin1 = i
                    imin2 = j
                min_max_value = min(min_max_value, max_sheds)
        
        return min_max_value, imin1, imin2
    
    
    def sheds(num_rams,day1,day2):
        original_sheds = occupied_sheds(num_rams)
        new_sheds1 = original_sheds[day2:] + original_sheds[:day2]+original_sheds[day2:] + original_sheds[:day2]
        new_sheds2 = original_sheds[day2-day1:] + original_sheds[:day2-day1]+original_sheds[day2-day1:] + original_sheds[:day2-day1]
        original_sheds = original_sheds+original_sheds
        new_sheds1 = original_sheds[:day2]+new_sheds1
        # 创建一个填充数组，长度为 day1，值为 num_rams * rate / capacity_rest
        prefix = np.full(day1, num_rams * rate / capacity_rest)

        # 取出 original_sheds 的子数组
        sliced_original = original_sheds[0:day2-day1]

        # 合并 prefix, sliced_original 和 new_sheds2
        new_sheds2 = np.concatenate([prefix, sliced_original, new_sheds2])

        original_sheds = np.concatenate((np.full(day2,num_rams*rate/capacity_rest), original_sheds))
        final_sheds = [original + new1 + new2 for original, new1, new2 in zip(original_sheds, new_sheds1, new_sheds2)]

        return final_sheds,new_sheds1,new_sheds2,original_sheds
    
    
    # 主程序
    ## 确定三批交配周期相差天数
    num_sheds,day1,day2=find_min_max_sheds_3(num_rams)
 

    # 当公羊数为4时的初值
    final_sheds,new_sheds1,new_sheds2,original_sheds = sheds(num_rams,day1,day2)

    ## 求最大种公羊数
    while max(final_sheds)<=total_sheds:
        num_rams+=1
        final_sheds,new_sheds1,new_sheds2,original_sheds = sheds(num_rams,day1,day2)
    
    # 回退一步，画图
    num_rams-=1
    num_ewes=num_rams*num_rate
    num_lambs=num_rams*rate*lambing_rate

    final_sheds,new_sheds1,new_sheds2,original_sheds = sheds(num_rams,day1,day2)
    plot_3(final_sheds,day1,day2,new_sheds1,new_sheds2,original_sheds)

    # 回带
    num_sheds,day1,day2=find_min_max_sheds_3(num_rams)
    print('当第一批与第二批交配周期相差',day1,'天，第一批与第三批相差',day2,'天时，羊栏占用数最少',file=f)
    print('最多占用羊栏数为：',num_sheds,'栏',file=f)
    print("种公羊数：",num_rams,'母羊数：',num_ewes,'单次出栏数：',num_lambs,file=f)

     # 当公羊数为12时
    max_capacity,day1,day2=find_min_max_sheds_3(12)
    print("当公羊数为12时，最大羊栏数为：",max_capacity,'间隔时间：',day1,day2,file=f)

    print('年出栏量如下：',file=f)
    # 设出栏次数x,则总出栏数为num_lambs*x
    # 当x%3==1 时，limit num_lambs*x*365/(419+(x-1)/3*229) x->oo
    # 当x%3==2 时，limit num_lambs*x*365/(440+(x-2)/3*229) x->oo
    # 当x%3==0 时，limit num_lambs*x*365/(419+(x-3)/3*229) x->oo
    x = sp.symbols('x')
    y_limit_1 = sp.limit(num_lambs*x*365/(419+(x-1)/3*229),x,sp.oo)
    print(f"x % 3 == 1 时的极限: {y_limit_1}",file=f)
    y_limit_2 = sp.limit(num_lambs*x*365/(440+(x-2)/3*229),x,sp.oo)
    print(f"x % 3 == 2 时的极限: {y_limit_2}",file=f)
    y_limit_3 = sp.limit(num_lambs*x*365/(629+(x-3)/3*229),x,sp.oo)
    print(f"x % 3 == 0 时的极限: {y_limit_3}",file=f)

    # 取整并打印
    y_limit_1_rounded = round(y_limit_1)
    y_limit_2_rounded = round(y_limit_2)
    y_limit_3_rounded = round(y_limit_3)

    print(f"x % 3 == 1 时的极限 (取整): {y_limit_1_rounded}",file=f)
    print(f"x % 3 == 2 时的极限 (取整): {y_limit_2_rounded}",file=f)
    print(f"x % 3 == 0 时的极限 (取整): {y_limit_3_rounded}",file=f)
    

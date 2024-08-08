from head import *
# 输出
with open('2023D\Q1\\result\\result_2.txt', 'w',encoding='UTF-8') as f: 
    
    # 变量
    num_rate = 28 # 母羊与公羊数量之比
    num_rams = 4 #种公羊数量
    num_ewes = num_rate*num_rams  # 基础母羊数量
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

    def plot_3(occupied_sheds_list, day, new_sheds, original_sheds):
        # 确保 new_sheds 和 original_sheds 的长度与 occupied_sheds_list 一致
        new_sheds = new_sheds[:len(occupied_sheds_list)]
        original_sheds = original_sheds[:len(occupied_sheds_list)]
        
        plt.figure(figsize=(12, 6))
        x = np.arange(0, len(occupied_sheds_list), 1)
        
        # 绘制数据
        plt.plot(x, occupied_sheds_list, linestyle='-', color='b', linewidth=2, label='羊栏占用数')
        plt.plot(x, new_sheds, linestyle='--', color='r', linewidth=2, label='第一批羊栏占用数')
        plt.plot(x, original_sheds, linestyle='-.', color='g', linewidth=2, label='第二批羊栏占用数')
        
        # 设置标题和标签
        plt.xlabel('天数/天', fontsize=14, fontweight='bold')
        plt.ylabel('羊栏占用数/栏', fontsize=14, fontweight='bold')
        plt.title('1_28羊栏占用数随时间的变化周期', fontsize=16, fontweight='bold')
        
        # 添加网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='grey', alpha=0.7)
        
        # 添加图例
        plt.legend(loc='upper left', fontsize=12)
        
        # 设置x轴和y轴刻度字体大小
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        
         # 在 x 轴上标出 day 的值
        plt.axvline(x=day, color='purple', linestyle=':', linewidth=2)
        plt.text(day, plt.ylim()[0] - 0.05*(plt.ylim()[1] - plt.ylim()[0]), f'Day {day}', 
             color='purple', fontsize=12, verticalalignment='top', horizontalalignment='center', 
             rotation=0, fontweight='bold')
    
        # 调整子图的布局，使得标题和标签不重叠
        plt.tight_layout()
        
        # 保存图像
        plt.savefig('2023D\\figs\\1_28羊栏占用数随时间的变化周期.pdf', format='pdf')
        
        # 显示图像
        plt.show()
    
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
    
    def sheds(num_rams,day):
        original_sheds = occupied_sheds(num_rams)
        new_sheds = original_sheds[day:] + original_sheds[:day]+original_sheds[day:] + original_sheds[:day]
        original_sheds = original_sheds+original_sheds
        new_sheds = original_sheds[:day]+new_sheds
        original_sheds = np.concatenate((np.full(day,num_rams*14/capacity_rest), original_sheds))
        final_sheds = [original + new for original, new in zip(original_sheds, new_sheds)]
        return final_sheds,new_sheds,original_sheds
    
    # 主程序
    num_sheds,day=find_min_max_sheds_2(num_rams)
    
    final_sheds,new_sheds,original_sheds = sheds(num_rams,day)

    # 求最大种公羊数
    while max(final_sheds)<=total_sheds:
        num_rams+=1
        final_sheds,new_sheds,original_sheds = sheds(num_rams,day)
    # 回退一步
    num_rams-=1
    num_ewes=num_rams*num_rate
    num_lambs=num_rams*rate*lambing_rate
    
    final_sheds,new_sheds,original_sheds = sheds(num_rams,day)
    num_sheds,day=find_min_max_sheds_2(num_rams)

    print('当两批交配周期相差',day,'天时，羊栏占用数最少',file=f)
    print('最多占用羊栏数为：',num_sheds,'栏',file=f)
    print("种公羊数：",num_rams,'母羊数：',num_ewes,'单次出栏数：',num_lambs,file=f)

    # 当公羊数为17时
    max_capacity,day=find_min_max_sheds_2(17)
    print("当公羊数为17时，最大羊栏数为：",max_capacity,file=f)
    # 绘图
    plot_3(final_sheds,day,new_sheds,original_sheds)
    
    # 第419天，即第一轮从交配期到出栏。往后229天出栏一次。419+229(x-1)天出栏x次。由于两批交配周期相差210天。第二批在第629天时出一次栏，往后每229天出一次栏。629+229(x-1)天出栏x次。
    # 设出栏次数x,则总出栏数为8*14*2*x=224x,在629天后，可以看作每229天，出栏两次。
    # 由于两批交配周期相差210天。当x为奇数，天数为419+(x-1)/2*229，当x为偶数，天数为629+(x/2-1)*229
    # x为奇数，limit 224*x*365/(419+(x-1)/2*229) x->oo
    # x为偶数，limit 224*x*365/(629+(x/2-1)*229) x->oo
    # 定义变量
    x = sp.symbols('x')

    print('年出栏数如下：',file=f)
    # 奇数情况
    expr_odd = num_lambs * x * 365 / (419 + (x - 1) / 2 * 229)
    limit_odd = sp.limit(expr_odd, x, sp.oo)
    print(f"奇数情况的极限: {limit_odd}",file=f)

    # 偶数情况
    expr_even = num_lambs * x * 365 / (629 + (x - 2)/2 * 229)
    limit_even = sp.limit(expr_even, x, sp.oo)
    print(f"偶数情况的极限: {limit_even}",file=f)

    # 取整并打印
    limit_odd_rounded = round(limit_odd)
    limit_even_rounded = round(limit_even)

    print(f"奇数情况的极限 (取整): {limit_odd_rounded}",file=f)
    print(f"偶数情况的极限 (取整): {limit_even_rounded}",file=f)
    
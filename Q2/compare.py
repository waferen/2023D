from head import *

# 已知
y_limit1 = 1071
y_limit2 = 1339
y_limit3 = 1205

num_rams1 = 24
num_rams2 = 15
num_rams3 = 9


## 绘制年产羔数随年份变化的折线图

def f1(num_rams,x):
    return round(rate * lambing_rate * num_rams ),(419 + 229 * (x - 1))

def f2(num_rams,x):
    if x%2==1:
        return round(rate * lambing_rate * num_rams ),(419 + 229 * (x - 1) / 2)
    else:
        return round(rate * lambing_rate * num_rams  ),(629 + 229 * (x - 2) / 2)

def f3(num_rams,x):
    if x%3==1:
        return round(rate * lambing_rate * num_rams  ),(419 + 229 * (x - 1) / 3)
    elif x%3==2:
        return round(rate * lambing_rate * num_rams  ),(440 + 229 * (x - 2) / 3)
    else:
        return round(rate * lambing_rate * num_rams  ),(629 + 229 * (x - 3) / 3)


def create_y1(num_rams1,x):
    list_y = []
    sum = 0
    i = 1
    for year in x:
        while f1(num_rams1, i)[1]/365 < year:
            sum += f1(num_rams1, i)[0]
            i += 1
        list_y.append(round(sum/year))
        year+=1
        
    return list_y

def create_y2(num_rams2,x):
    list_y = []
    sum = 0
    i = 1
    for year in x:
        while f2(num_rams2, i)[1]/365 < year:
            sum += f2(num_rams2, i)[0]
            i += 1
        list_y.append(round(sum/year))
        year+=1
        
    return list_y

def create_y3(num_rams3,x):
    list_y = []
    sum = 0
    i = 1
    for year in x:
        while f3(num_rams3, i)[1]/365 < year:
            sum += f3(num_rams3, i)[0]
            i += 1
        list_y.append(round(sum/year))
        year+=1
        
    return list_y



def plot_2(num_rams1, num_rams2, num_rams3):
    x = np.arange(1, 25, 1)

            
    y1 = create_y1(num_rams1, x)
    y2 = create_y2(num_rams2, x)
    y3 = create_y3(num_rams3, x)

    plt.figure(figsize=(10, 6))
    
    plt.plot(x, y1, marker="o", mfc="white", ms=8, linestyle="-", color="#1f77b4", label="1-14 年出栏数")
    plt.plot(x, y2, marker="s", mfc="white", ms=8, linestyle="--", color="#ff7f0e", label="1-28 年出栏数")
    plt.plot(x, y3, marker="^", mfc="white", ms=8, linestyle=":", color="#2ca02c", label="1-42 年出栏数")

    plt.xlabel('年份/年', fontsize=12, fontweight='bold')
    plt.ylabel('年产羔数/只', fontsize=12, fontweight='bold')
    plt.title('年出栏数与年份的关系', fontsize=14, fontweight='bold')

    plt.grid(ls="--", lw=0.5, color="#4E616C")
    plt.legend()

    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    
    plt.axhline(y=y_limit1, color='#1f77b4', linestyle='--', label=f'1-14 极限: {y_limit1:.2f}')
    plt.axhline(y=y_limit2, color='#ff7f0e', linestyle='--', label=f'1-28 极限: {y_limit2:.2f}')
    plt.axhline(y=y_limit3, color='#2ca02c', linestyle='--', label=f'1-42 极限: {y_limit3:.2f}')
    
    plt.legend()

     # 添加注释显示在右边
    plt.annotate(f'{y_limit1:.2f}', xy=(1, y_limit1), xytext=(25.5, y_limit1), 
                 textcoords='data', color='#1f77b4', va='center', ha='left', fontsize=10)
    plt.annotate(f'{y_limit2:.2f}', xy=(1, y_limit2), xytext=(25.5, y_limit2), 
                 textcoords='data', color='#ff7f0e', va='center', ha='left', fontsize=10)
    plt.annotate(f'{y_limit3:.2f}', xy=(1, y_limit3), xytext=(25.5, y_limit3), 
                 textcoords='data', color='#2ca02c', va='center', ha='left', fontsize=10)
    # 调整子图的布局，使得标题和标签不重叠
    plt.tight_layout()

    # 保存图像为矢量图格式
    plt.savefig('2023D\\figs\\年出栏数与年份的关系.pdf', format='pdf')
    plt.show()


plot_2(num_rams1, num_rams2, num_rams3)

with open('2023D\Q2\\result.txt', 'w',encoding='UTF-8') as f: 
    print('1-14 年出栏量范围',f1(num_rams1,1),'到',y_limit1,file=f)
    print('1-28 年出栏量范围',f2(num_rams2,1),'到',y_limit2,file=f)
    print('1-42 年出栏量范围',f3(num_rams3,1),'到',y_limit3,file=f)
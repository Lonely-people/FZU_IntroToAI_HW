import random
import heapq
from queue import Queue
import math
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch

plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP']
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 👇 请在下方填入你的学号（必须修改！）
# ==========================================
STUDENT_ID = 112401526  # 示例，请改为你的学号
# ==========================================

class MazeEnv:
    def __init__(self, size=20, obstacle_ratio=0.3):
        self.size = size
        # 使用学号作为种子，确保每个人生成的地图不同
        random.seed(STUDENT_ID)
        
        # 生成地图：0是路，1是墙
        self.map = [[0] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                if random.random() < obstacle_ratio:
                    self.map[i][j] = 1
        
        # 保证起点和终点必须是路
        self.map[0][0] = 0
        self.map[size-1][size-1] = 0

    def print_map(self, path=None):
        """
        简单打印地图
        path: 路径坐标列表 [(0,0), (0,1), ...]
        """
        print(f"\n当前学号: {STUDENT_ID} 的专属地图 (S:起点, E:终点, *:路径, #:墙, .:路)")
        print("-" * (self.size * 2 + 2))
        path_set = set(path) if path else set()
        
        for i in range(self.size):
            row_str = "|"
            for j in range(self.size):
                if (i, j) == (0, 0):
                    row_str += "S "
                elif (i, j) == (self.size-1, self.size-1):
                    row_str += "E "
                elif (i, j) in path_set:
                    row_str += "* " # 路径
                elif self.map[i][j] == 1:
                    row_str += "# " # 墙
                else:
                    row_str += ". " # 路
            row_str += "|"
            print(row_str)
        print("-" * (self.size * 2 + 2))

def solve_maze(env):
    """
    TODO: 请在此处实现 A* 算法
    输入: env (MazeEnv对象, 访问 env.map 获取地图)
    输出: path (列表, 包含从(0,0)到终点的坐标, 如 [(0,0), (0,1)...])
         如果无解，返回 None
    """
    start = (0, 0)
    end = (env.size - 1, env.size - 1)
    
    # === 你的代码开始 ===
    
    # 提示：你需要维护 open_list 和 closed_list
    # 提示：你需要定义 heuristic 函数 (如曼哈顿距离)

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, (heuristic(start, end), 0, start))
    cnt = 0; ok = False
    dis = {start: 0}
    pre = {}

    while open_list:
        f, g, u = heapq.heappop(open_list)
        if u in closed_list:
            continue
        closed_list.add(u)
        cnt += 1
        if u == end:
            ok = True
            break
        for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx = u[0] + i
            ny = u[1] + j
            if nx < 0 or nx >= env.size or ny < 0 or ny >= env.size or env.map[nx][ny] == 1:
                continue
            if (nx, ny) in closed_list:
                continue
            if (nx, ny) not in dis or g + 1 < dis[(nx, ny)]:
                pre[(nx, ny)] = u
                dis[(nx, ny)] = g + 1
                heapq.heappush(open_list, (dis[(nx, ny)] + heuristic((nx, ny), end), dis[(nx, ny)], (nx, ny)))

    path = [] # 这里替换为你的算法逻辑
    if ok:
        u = end
        while True:
            path.append(u)
            if u not in pre:
                break
            u = pre[u]
        path.reverse()
        print(f"a* 访问节点数: {cnt}")

    # 下面是一个伪造的路径，仅演示输出格式，请删除
    # path = [(0,0), (0,1), (0,2)] 
    
    # === 你的代码结束 ===
    
    return path

def bfs(env):
    start = (0, 0)
    end = (env.size - 1, env.size - 1)
    vis = {start}; pre = {}; cnt = 0; ok = False
    Q = Queue()
    Q.put(start)
    while not Q.empty():
        u = Q.get()
        cnt += 1
        if u == end:
            ok = True
            break
        for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx = u[0] + i; ny = u[1] + j
            nxt = (nx, ny)
            if nx < 0 or nx >= env.size or ny < 0 or ny >= env.size or env.map[nx][ny] == 1:
                continue
            if nxt not in vis:
                vis.add(nxt)
                pre[nxt] = u
                Q.put(nxt)
    path = []
    if ok == True:
        u = end
        while True:
            path.append(u)
            if u not in pre:
                break
            u = pre[u]
        path.reverse()
        print(f"bfs 访问节点数: {cnt}")
    return path

def visualize(env, path):
    col = [[env.map[i][j] for j in range(env.size)] for i in range(env.size)]
    if path:
        for (i, j) in path:
            col[i][j] = 2
    col[0][0] = 3; col[env.size - 1][env.size - 1] = 4
    cmap = ListedColormap(['white', 'black', 'red', 'blue', 'green'])
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
    norm = BoundaryNorm(bounds, cmap.N)
    fig, ax = plt.subplots(figsize = (10, 10))
    ax.imshow(col, cmap = cmap, norm = norm)
    ax.set_xticks([x - 0.5 for x in range(env.size + 1)])
    ax.set_yticks([y - 0.5 for y in range(env.size + 1)])
    ax.grid(which='major', linestyle='-', color='gray', linewidth=0.5)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    elements = [
        Patch(facecolor='white', edgecolor='gray', label='路'),
        Patch(facecolor='black', edgecolor='gray', label='墙'),
        Patch(facecolor='blue', label='起点'),
        Patch(facecolor='green', label='终点'),
        Patch(facecolor='red', label='路径')
    ]
    ax.legend(handles=elements, loc='upper right', bbox_to_anchor=(1.2, 1))
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # 1. 初始化环境
    if STUDENT_ID == 20220000:
        print("【警告】请先修改代码顶部的 STUDENT_ID 为你的真实学号！")
    
    env = MazeEnv(size=20)
    
    # 2. 打印未解出来的地图
    print("生成地图中...")
    env.print_map()
    
    # 3. 运行学生写的算法
    print("\n正在寻找路径...")
    path = solve_maze(env)
    # path = bfs(env)
    # print(path)

    # 4. 展示结果
    if path:
        print(f"找到路径！步数: {len(path)}")
        # env.print_map(path)
        visualize(env, path)
    else:
        print("未找到路径 或 算法尚未实现。")

    path = bfs(env)
    if path:
        print(f"找到路径！步数: {len(path)}")
        # env.print_map(path)
        visualize(env, path)
    else:
        print("未找到路径 或 算法尚未实现。")
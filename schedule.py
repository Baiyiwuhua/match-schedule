# -*- coding: utf-8 -*-
"""
单循环赛程生成器
----------------
用途：给系篮球赛、羽毛球赛这类单循环赛事自动排赛程。
输入：队伍名单（下方 TEAMS 或命令行参数）
输出：每一轮的对阵表，奇数支队伍自动轮空。

用法：
    python schedule.py
    python schedule.py 软件2501 软件2502 网络2501 网络2502 大数据2501
"""

import sys


def build_rounds(teams):
    """用轮转法生成单循环赛程。奇数队补一个“轮空”占位。"""
    teams = list(teams)
    bye = None
    if len(teams) % 2 == 1:          # 队伍数必须是偶数，否则两支两支配不起来
        bye = "轮空"
        teams.append(bye)            # 补一个假队伍，谁抽到它就等于这轮轮空

    n = len(teams)
    rounds = []
    fixed = teams[0]                 # 固定第一支队不动
    rotating = teams[1:]             # 其余队伍围成一圈，每轮转一位

    for r in range(n - 1):           # n 支队单循环一共 n-1 轮
        pairs = [(fixed, rotating[0])]
        for i in range(1, n // 2):
            pairs.append((rotating[i], rotating[n - 1 - i]))   # 首尾配对，保证每轮每队只打一场
        rounds.append(pairs)
        rotating = rotating[1:] + rotating[:1]   # 顺时针轮转一位

    return rounds


def print_schedule(rounds):
    total = 0
    for i, pairs in enumerate(rounds, 1):
        print(f"\n第 {i} 轮")
        print("-" * 34)
        for home, away in pairs:
            if "轮空" in (home, away):
                real = away if home == "轮空" else home
                print(f"  {real:<10} 轮空")
            else:
                print(f"  {home:<10} vs  {away}")
                total += 1
    print(f"\n共 {len(rounds)} 轮，{total} 场比赛。")


def to_csv(rounds, path="赛程表.csv"):
    try:
        with open(path, "w", encoding="utf-8-sig") as f:
            f.write("轮次,主队,客队\n")
            for i, pairs in enumerate(rounds, 1):
                for home, away in pairs:
                    f.write(f"{i},{home},{away}\n")
        print(f"\n已导出：{path}")
    except PermissionError:
        # 常见情况：这个 csv 正在 Excel 里打开着
        alt = "赛程表_新.csv"
        with open(alt, "w", encoding="utf-8-sig") as f:
            f.write("轮次,主队,客队\n")
            for i, pairs in enumerate(rounds, 1):
                for home, away in pairs:
                    f.write(f"{i},{home},{away}\n")
        print(f"\n{path} 被占用（可能正在 Excel 中打开），已改存为：{alt}")


if __name__ == "__main__":
    TEAMS = ["软件2501", "软件2502", "网络2501",
             "网络2502", "大数据2501"]
    teams = sys.argv[1:] if len(sys.argv) > 1 else TEAMS

    if len(teams) < 2:
        print("至少需要两支队伍。")
        sys.exit(1)

    print(f"参赛队伍（{len(teams)} 支）：" + "、".join(teams))
    rounds = build_rounds(teams)
    print_schedule(rounds)
    to_csv(rounds)

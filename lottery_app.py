import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import json


class LotteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 幸运抽奖小程序")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")

        # 数据存储
        self.participants = []
        self.prizes = []
        self.winners = {}  # prize -> list of winners

        self.build_ui()

    def build_ui(self):
        # 标题
        title = tk.Label(
            self.root,
            text="🎰 幸运抽奖小程序",
            font=("微软雅黑", 24, "bold"),
            bg="#2c3e50",
            fg="#f1c40f",
        )
        title.pack(pady=15)

        # 主内容区域（左右分栏）
        content_frame = tk.Frame(self.root, bg="#2c3e50")
        content_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # ===== 左侧：参与者管理 =====
        left_frame = tk.LabelFrame(
            content_frame,
            text="👥 参与者名单",
            font=("微软雅黑", 12, "bold"),
            bg="#34495e",
            fg="white",
            padx=10,
            pady=10,
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # 参与者输入
        input_frame = tk.Frame(left_frame, bg="#34495e")
        input_frame.pack(fill=tk.X, pady=5)

        self.participant_entry = tk.Entry(
            input_frame, font=("微软雅黑", 11), width=18
        )
        self.participant_entry.pack(side=tk.LEFT, padx=2)
        self.participant_entry.bind("<Return>", lambda e: self.add_participant())

        tk.Button(
            input_frame,
            text="添加",
            command=self.add_participant,
            bg="#27ae60",
            fg="white",
            font=("微软雅黑", 10),
            width=6,
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            input_frame,
            text="清空",
            command=self.clear_participants,
            bg="#e74c3c",
            fg="white",
            font=("微软雅黑", 10),
            width=6,
        ).pack(side=tk.LEFT, padx=2)

        # 导入/导出按钮
        file_frame = tk.Frame(left_frame, bg="#34495e")
        file_frame.pack(fill=tk.X, pady=2)

        tk.Button(
            file_frame,
            text="📁 导入",
            command=self.import_participants,
            bg="#3498db",
            fg="white",
            font=("微软雅黑", 9),
            width=8,
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            file_frame,
            text="💾 保存",
            command=self.save_participants,
            bg="#9b59b6",
            fg="white",
            font=("微软雅黑", 9),
            width=8,
        ).pack(side=tk.LEFT, padx=2)

        # 参与者列表
        self.participant_list = tk.Listbox(
            left_frame,
            font=("微软雅黑", 11),
            height=10,
            selectmode=tk.SINGLE,
            bg="#ecf0f1",
        )
        self.participant_list.pack(fill=tk.BOTH, expand=True, pady=5)

        self.participant_count_label = tk.Label(
            left_frame,
            text="当前人数: 0",
            font=("微软雅黑", 10),
            bg="#34495e",
            fg="#bdc3c7",
        )
        self.participant_count_label.pack()

        # ===== 右侧：奖项设置与抽奖 =====
        right_frame = tk.LabelFrame(
            content_frame,
            text="🏆 奖项设置",
            font=("微软雅黑", 12, "bold"),
            bg="#34495e",
            fg="white",
            padx=10,
            pady=10,
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # 奖项输入
        prize_input_frame = tk.Frame(right_frame, bg="#34495e")
        prize_input_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            prize_input_frame, text="奖项:", bg="#34495e", fg="white", font=("微软雅黑", 10)
        ).pack(side=tk.LEFT)
        self.prize_name_entry = tk.Entry(
            prize_input_frame, font=("微软雅黑", 11), width=12
        )
        self.prize_name_entry.pack(side=tk.LEFT, padx=2)

        tk.Label(
            prize_input_frame, text="数量:", bg="#34495e", fg="white", font=("微软雅黑", 10)
        ).pack(side=tk.LEFT)
        self.prize_count_entry = tk.Entry(
            prize_input_frame, font=("微软雅黑", 11), width=5
        )
        self.prize_count_entry.pack(side=tk.LEFT, padx=2)
        self.prize_count_entry.insert(0, "1")

        tk.Button(
            prize_input_frame,
            text="添加",
            command=self.add_prize,
            bg="#27ae60",
            fg="white",
            font=("微软雅黑", 10),
            width=6,
        ).pack(side=tk.LEFT, padx=2)

        # 奖项列表
        self.prize_list = tk.Listbox(
            right_frame,
            font=("微软雅黑", 11),
            height=5,
            bg="#ecf0f1",
        )
        self.prize_list.pack(fill=tk.X, pady=5)

        tk.Button(
            right_frame,
            text="🗑 清空奖项",
            command=self.clear_prizes,
            bg="#e74c3c",
            fg="white",
            font=("微软雅黑", 10),
        ).pack(fill=tk.X, pady=2)

        # 抽奖控制
        control_frame = tk.LabelFrame(
            right_frame,
            text="🎲 抽奖控制",
            font=("微软雅黑", 11, "bold"),
            bg="#34495e",
            fg="white",
            padx=10,
            pady=10,
        )
        control_frame.pack(fill=tk.X, pady=10)

        tk.Button(
            control_frame,
            text="🎰 开始抽奖",
            command=self.start_lottery,
            bg="#f39c12",
            fg="white",
            font=("微软雅黑", 14, "bold"),
            height=2,
        ).pack(fill=tk.X, pady=5)

        tk.Button(
            control_frame,
            text="🔄 重置结果",
            command=self.reset_results,
            bg="#95a5a6",
            fg="white",
            font=("微软雅黑", 11),
        ).pack(fill=tk.X, pady=2)

        # 结果显示区域
        result_frame = tk.LabelFrame(
            self.root,
            text="🎉 中奖结果",
            font=("微软雅黑", 12, "bold"),
            bg="#2c3e50",
            fg="white",
            padx=10,
            pady=10,
        )
        result_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.result_text = tk.Text(
            result_frame,
            font=("微软雅黑", 11),
            height=8,
            bg="#1a252f",
            fg="#2ecc71",
            wrap=tk.WORD,
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.insert("1.0", "还未开始抽奖，请添加参与者和奖项后点击「开始抽奖」！")
        self.result_text.config(state=tk.DISABLED)

    # ========== 功能方法 ==========

    def add_participant(self):
        name = self.participant_entry.get().strip()
        if not name:
            messagebox.showwarning("提示", "请输入参与者姓名！")
            return
        if name in self.participants:
            messagebox.showwarning("提示", f"'{name}' 已经在名单中了！")
            return
        self.participants.append(name)
        self.participant_list.insert(tk.END, name)
        self.participant_entry.delete(0, tk.END)
        self.update_counts()

    def clear_participants(self):
        if not self.participants:
            return
        if messagebox.askyesno("确认", "确定要清空所有参与者吗？"):
            self.participants.clear()
            self.participant_list.delete(0, tk.END)
            self.update_counts()

    def add_prize(self):
        name = self.prize_name_entry.get().strip()
        count_str = self.prize_count_entry.get().strip()

        if not name:
            messagebox.showwarning("提示", "请输入奖项名称！")
            return

        try:
            count = int(count_str)
            if count < 1:
                raise ValueError
        except ValueError:
            messagebox.showwarning("提示", "奖项数量必须是正整数！")
            return

        self.prizes.append({"name": name, "count": count})
        self.prize_list.insert(tk.END, f"{name} (×{count})")
        self.prize_name_entry.delete(0, tk.END)
        self.prize_count_entry.delete(0, tk.END)
        self.prize_count_entry.insert(0, "1")

    def clear_prizes(self):
        if not self.prizes:
            return
        if messagebox.askyesno("确认", "确定要清空所有奖项吗？"):
            self.prizes.clear()
            self.prize_list.delete(0, tk.END)

    def update_counts(self):
        self.participant_count_label.config(text=f"当前人数: {len(self.participants)}")

    def start_lottery(self):
        if not self.participants:
            messagebox.showwarning("提示", "请先添加参与者！")
            return
        if not self.prizes:
            messagebox.showwarning("提示", "请先添加奖项！")
            return

        total_prizes = sum(p["count"] for p in self.prizes)
        if total_prizes > len(self.participants):
            messagebox.showwarning(
                "提示",
                f"奖品总数({total_prizes})超过了参与者人数({len(self.participants)})！",
            )
            return

        # 抽奖逻辑
        available = self.participants.copy()
        random.shuffle(available)
        self.winners = {}

        for prize in self.prizes:
            winners = random.sample(available, min(prize["count"], len(available)))
            self.winners[prize["name"]] = winners
            for w in winners:
                available.remove(w)

        self.display_results()
        self.show_celebration()

    def display_results(self):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)

        lines = ["🎉🎉🎉 抽奖结果 🎉🎉🎉\n", "=" * 40 + "\n"]
        for prize_name, winners in self.winners.items():
            lines.append(f"🏆 {prize_name}:\n")
            for w in winners:
                lines.append(f"   ✨ {w}\n")
            lines.append("\n")
        lines.append("=" * 40 + "\n")
        lines.append("🎊 恭喜以上中奖者！")

        self.result_text.insert("1.0", "".join(lines))
        self.result_text.config(state=tk.DISABLED)

    def show_celebration(self):
        # 弹出中奖庆祝窗口
        popup = tk.Toplevel(self.root)
        popup.title("🎊 抽奖完成！")
        popup.geometry("400x200")
        popup.configure(bg="#2c3e50")
        popup.transient(self.root)
        popup.grab_set()

        tk.Label(
            popup,
            text="🎉 抽奖完成！",
            font=("微软雅黑", 24, "bold"),
            bg="#2c3e50",
            fg="#f1c40f",
        ).pack(pady=20)

        total = sum(len(v) for v in self.winners.values())
        tk.Label(
            popup,
            text=f"共抽出 {total} 位幸运儿！",
            font=("微软雅黑", 14),
            bg="#2c3e50",
            fg="white",
        ).pack(pady=10)

        tk.Button(
            popup,
            text="好的",
            command=popup.destroy,
            bg="#27ae60",
            fg="white",
            font=("微软雅黑", 12),
            width=10,
        ).pack(pady=20)

    def reset_results(self):
        self.winners = {}
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(
            "1.0", "结果已重置，请重新点击「开始抽奖」！"
        )
        self.result_text.config(state=tk.DISABLED)

    def import_participants(self):
        filepath = filedialog.askopenfilename(
            title="导入参与者名单",
            filetypes=[("文本文件", "*.txt"), ("JSON文件", "*.json"), ("所有文件", "*.*")],
        )
        if not filepath:
            return

        try:
            if filepath.endswith(".json"):
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    names = data if isinstance(data, list) else data.get("participants", [])
            else:
                with open(filepath, "r", encoding="utf-8") as f:
                    names = [line.strip() for line in f if line.strip()]

            added = 0
            for name in names:
                if name not in self.participants:
                    self.participants.append(name)
                    self.participant_list.insert(tk.END, name)
                    added += 1

            self.update_counts()
            messagebox.showinfo("导入成功", f"成功导入 {added} 位参与者！")
        except Exception as e:
            messagebox.showerror("导入失败", f"读取文件出错：{e}")

    def save_participants(self):
        if not self.participants:
            messagebox.showwarning("提示", "没有参与者可保存！")
            return

        filepath = filedialog.asksaveasfilename(
            title="保存参与者名单",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("JSON文件", "*.json")],
        )
        if not filepath:
            return

        try:
            if filepath.endswith(".json"):
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(self.participants, f, ensure_ascii=False, indent=2)
            else:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("\n".join(self.participants))

            messagebox.showinfo("保存成功", f"名单已保存到：\n{filepath}")
        except Exception as e:
            messagebox.showerror("保存失败", f"写入文件出错：{e}")


def main():
    root = tk.Tk()
    app = LotteryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

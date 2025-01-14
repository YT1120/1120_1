from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QInputDialog
from PyQt6.QtCore import QDate, QTime, QDateTime, QTimer
import sys

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('todo_app_3.ui', self)

        # 連接按鈕功能
        self.addButton.clicked.connect(self.add_task)
        self.deleteButton.clicked.connect(self.delete_task)
        self.markCompleteButton.clicked.connect(self.mark_complete)
        self.addCategoryButton.clicked.connect(self.add_category)

        # 預設分類
        self.categoryDropdown.addItem("Default")

        # 初始化優先級選單
        self.priorityDropdown.addItems(["高", "中", "低"])  # 預設優先級選項

        # 初始化日期與時間選擇器
        self.datePicker.setDate(QDate.currentDate())  # 設定默認為今天
        self.timePicker.setTime(QTime.currentTime())  # 設定默認為現在時間

        # 設定計時器，用於更新任務的倒數時間
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_task_timers)
        self.timer.start(60000)  # 每分鐘更新一次

    def add_task(self):
        # 獲取任務內容
        task = self.taskInput.text()
        category = self.categoryDropdown.currentText()  # 獲取分類
        priority = self.priorityDropdown.currentText()  # 獲取優先級
        date = self.datePicker.date().toString("yyyy-MM-dd")  # 獲取選擇的日期
        time = self.timePicker.time().toString("HH:mm")  # 獲取選擇的時間

        if task.strip():  # 確保任務非空
            # 組合任務顯示內容
            task_text = f"[{category}] {task} - 日期: {date}, 時間: {time}, 優先級: {priority}"
            self.taskList.addItem(task)
            self.taskInput.clear()  # 清空輸入框
        else:
            QMessageBox.warning(self, "錯誤", "任務內容不能為空！")

    def delete_task(self):
        selected_task = self.taskList.currentItem()
        if selected_task:
            self.taskList.takeItem(self.taskList.row(selected_task))
        else:
            QMessageBox.warning(self, "錯誤", "未選擇任務！")

    def mark_complete(self):
        selected_task = self.taskList.currentItem()
        if selected_task:
            selected_task.setText(f"{selected_task.text()} (已完成)")
        else:
            QMessageBox.warning(self, "錯誤", "未選擇任務！")

    def add_category(self):
        new_category, ok = QInputDialog.getText(self, "新增分類", "輸入新分類名稱：")
        if ok and new_category.strip():
            if new_category not in [self.categoryDropdown.itemText(i) for i in range(self.categoryDropdown.count())]:
                self.categoryDropdown.addItem(new_category)
            else:
                QMessageBox.warning(self, "錯誤", "分類已存在！")
        elif not new_category.strip():
            QMessageBox.warning(self, "錯誤", "分類名稱不能為空！")

    def update_task_timers(self):
        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            task_text = item.text()

            # 提取日期與時間
            if "日期" in task_text and "時間" in task_text:
                try:
                    date_str = task_text.split("日期: ")[1].split(", 時間: ")[0]
                    time_str = task_text.split("時間: ")[1].split(", 優先級")[0]
                    task_datetime = QDateTime.fromString(f"{date_str} {time_str}", "yyyy-MM-dd HH:mm")

                    # 計算剩餘時間
                    remaining_time = QDateTime.currentDateTime().secsTo(task_datetime)
                    if remaining_time > 0:
                        hours = remaining_time // 3600
                        minutes = (remaining_time % 3600) // 60
                        updated_text = f"{task_text} - 剩餘時間: {hours} 小時 {minutes} 分鐘"
                    else:
                        updated_text = f"{task_text} - 已過期"

                    # 更新任務顯示文字
                    item.setText(updated_text)
                except Exception as e:
                    print(f"解析時間時出錯: {e}")

# 主程式
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    app.exec()  

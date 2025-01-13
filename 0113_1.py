from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QInputDialog
from PyQt6.QtCore import QDate, QTime
import sys

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('todo_app_3.ui', self)

        # 連接功能
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

    def add_task(self):
        task = self.taskInput.text()  # 獲取任務內容
        category = self.categoryDropdown.currentText()  # 獲取分類
        priority = self.priorityDropdown.currentText()  # 獲取優先級
        date = self.datePicker.date().toString("yyyy-MM-dd")  # 獲取選擇的日期
        time = self.timePicker.time().toString("HH:mm")  # 獲取選擇的時間

        if task.strip():  # 確保任務非空
            # 將分類、優先級、任務、日期與時間結合，顯示在清單中
            self.taskList.addItem(f"[{category}] {task} - 日期: {date}, 時間: {time}, 優先級: {priority}")
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

# 主程式
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec())

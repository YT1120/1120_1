from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QInputDialog
import sys

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('todo_app_1.ui', self)

        # 連接功能
        self.addButton.clicked.connect(self.add_task)
        self.deleteButton.clicked.connect(self.delete_task)
        self.markCompleteButton.clicked.connect(self.mark_complete)
        self.addCategoryButton.clicked.connect(self.add_category)

        # 預設分類
        self.categoryDropdown.addItem("Default")

    def add_task(self):
        task = self.taskInput.text()
        category = self.categoryDropdown.currentText()
        if task.strip():
            self.taskList.addItem(f"[{category}] {task}")
            self.taskInput.clear()
        else:
            QMessageBox.warning(self, "Error", "Task cannot be empty")

    def delete_task(self):
        selected_task = self.taskList.currentItem()
        if selected_task:
            self.taskList.takeItem(self.taskList.row(selected_task))
        else:
            QMessageBox.warning(self, "Error", "No task selected")

    def mark_complete(self):
        selected_task = self.taskList.currentItem()
        if selected_task:
            selected_task.setText(f"{selected_task.text()} (Completed)")
        else:
            QMessageBox.warning(self, "Error", "No task selected")

    def add_category(self):
        new_category, ok = QInputDialog.getText(self, "Add Category", "Enter new category name:")
        if ok and new_category.strip():
            if new_category not in [self.categoryDropdown.itemText(i) for i in range(self.categoryDropdown.count())]:
                self.categoryDropdown.addItem(new_category)
            else:
                QMessageBox.warning(self, "Error", "Category already exists")
        elif not new_category.strip():
            QMessageBox.warning(self, "Error", "Category name cannot be empty")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec())
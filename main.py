import sys
import os

from PyQt6 import uic
from PyQt6.QtCore import QDir
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QFileDialog
)

import sysv_ipc

class TextToHtmlConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        
        ui_file = os.path.join(os.path.dirname(__file__), 'text_to_html_converter.ui')
        uic.loadUi(ui_file, self)
        
        self.message_queue = None
        self.setup_connections()
        
    def setup_connections(self):
        self.pushButton_browse.clicked.connect(self.browse_file)
        self.pushButton_upload.clicked.connect(self.process_file)
        
        self.actionOpen.triggered.connect(self.browse_file)
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.show_about)
    
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Text File",
            QDir.homePath(),
            "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            self.lineEdit_filepath.setText(file_path)
    
    def convert_text_to_html(self, text_content):
        """Convertește text în format HTML"""
        lines = text_content.strip().split('\n')
        html_parts = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '<meta charset="UTF-8">',
            '<title>Converted Document</title>',
            '</head>',
            '<body>'
        ]
        
        current_paragraph = []
        
        for line in lines:
            line = line.strip()
            
            if not line:
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph)
                    html_parts.append(f'<p>{self.escape_html(paragraph_text)}</p>')
                    current_paragraph = []
            else:
                if len(line) < 60 and line.isupper():
                    if current_paragraph:
                        paragraph_text = ' '.join(current_paragraph)
                        html_parts.append(f'<p>{self.escape_html(paragraph_text)}</p>')
                        current_paragraph = []
                    html_parts.append(f'<h1>{self.escape_html(line)}</h1>')
                elif len(line) < 60 and not current_paragraph and line[0].isupper():
                    html_parts.append(f'<h2>{self.escape_html(line)}</h2>')
                else:
                    current_paragraph.append(line)
        
        if current_paragraph:
            paragraph_text = ' '.join(current_paragraph)
            html_parts.append(f'<p>{self.escape_html(paragraph_text)}</p>')
        
        html_parts.extend(['</body>', '</html>'])
        
        return '\n'.join(html_parts)
    
    def escape_html(self, text):
        """Escape caractere speciale HTML"""
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#39;')
        return text
    
    def send_to_message_queue(self, html_content):
        """Trimite conținutul HTML către coada de mesaje pentru procesare în C"""
        try:
            key = sysv_ipc.ftok("message_queue_html", ord('B'))
            self.message_queue = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT, 0o666)
            
            # Trimite mesajul (type 1)
            self.message_queue.send(html_content.encode('utf-8'), type=1)
            
            self.label_status.setText('Status: HTML sent to C program via message queue')
            self.label_status.setStyleSheet('color: green; font-weight: bold;')
            
            return True
            
        except Exception as e:
            QMessageBox.warning(self, 'Message Queue Error', 
                              f'Failed to send to message queue: {str(e)}\n\n'
                              f'Make sure html_receiver is running!')
            self.label_status.setText(f'Status: Error - {str(e)}')
            self.label_status.setStyleSheet('color: red; font-weight: bold;')
            return False
    
    def process_file(self):
        """Funcția principală de procesare"""
        file_path = self.lineEdit_filepath.text().strip()
        
        if not file_path:
            QMessageBox.warning(self, 'No File', 'Please select a file first!')
            return
        
        if not os.path.exists(file_path):
            QMessageBox.warning(self, 'File Not Found', 
                              f'The file "{file_path}" does not exist!')
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            self.label_status.setText('Status: Converting to HTML...')
            self.label_status.setStyleSheet('color: orange; font-weight: bold;')
            
            html_content = self.convert_text_to_html(text_content)
 
            self.textEdit_result.setPlainText(html_content)
            
            self.send_to_message_queue(html_content)
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}')
            self.label_status.setText(f'Status: Error - {str(e)}')
            self.label_status.setStyleSheet('color: red; font-weight: bold;')
    
    def show_about(self):
        """Afișează dialogul About"""
        QMessageBox.about(self, 'About', 
                         '<h2>Text to HTML Converter</h2>'
                         '<p>Laborator 5 - Paradigme de Programare</p>'
                         '<p>Aplicație pentru conversia fișierelor text în HTML<br>'
                         'cu comunicare prin cozi de mesaje System V.</p>'
                         '<p><b>Funcționalități:</b></p>'
                         '<ul>'
                         '<li>Conversie text → HTML</li>'
                         '<li>Comunicare Python ↔ C prin message queue</li>'
                         '<li>Validare HTML cu regex în C</li>'
                         '<li>Scriere fișier output.html</li>'
                         '</ul>')
 
def main():
    app = QApplication(sys.argv)
    
    app.setStyle('Fusion')
    
    ui_file = os.path.join(os.path.dirname(__file__), 'text_to_html_converter.ui')
    if not os.path.exists(ui_file):
        print(f"Error: UI file not found: {ui_file}")
        print("Make sure text_to_html_converter.ui is in the same directory!")
        sys.exit(1)
    
    window = TextToHtmlConverter()
    window.show()
    
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()
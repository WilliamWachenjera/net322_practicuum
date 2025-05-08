import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLineEdit, QPushButton, QTabWidget, QLabel)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt, pyqtSignal
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import os
from urllib.parse import urlparse, quote_plus

class CustomSearchEngine:
    def __init__(self, local_server_url="http://localhost:8085", templates_dir="templates"):
        self.local_server_url = local_server_url.rstrip('/')
        self.templates_dir = templates_dir
        self.local_pages = self._discover_local_pages()
        self.network_manager = QNetworkAccessManager()
    
    def _discover_local_pages(self):
        #Scan templates directory to find available local pages
        pages = []
        if os.path.exists(self.templates_dir):
            for root, dirs, files in os.walk(self.templates_dir):
                for file in files:
                    if file.endswith('.html'):
                        rel_path = os.path.relpath(os.path.join(root, file), self.templates_dir)
                        url = f"{self.local_server_url}/{rel_path.replace(os.sep, '/')}"
                        pages.append({
                            'url': url,
                            'title': os.path.splitext(file)[0].replace('_', ' ').title(),
                            'path': rel_path
                        })
        return pages
    
    def search(self, query):
        #Custom search that prioritizes local pages with fallback to Google
        results = []
        
        # First add local pages that match the query
        for page in self.local_pages:
            if query.lower() in page['title'].lower() or query.lower() in page['path'].lower():
                results.append({
                    'title': f"Local Page: {page['title']}",
                    'url': page['url'],
                    'description': f"Local template page at {page['path']}",
                    'priority': 1  # Highest priority
                })
        
        # Always add Google search as an option
        google_url = f"https://www.google.com/search?q={quote_plus(query)}"
        results.append({
            'title': f"Search Google for '{query}'",
            'url': google_url,
            'description': "Search the web using Google",
            'priority': 0
        })
        
        # Sort by priority (highest first)
        results.sort(key=lambda x: x['priority'], reverse=True)
        
        return results

class BrowserTab(QWidget):
    loadFinished = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("about:blank"))
        
        # Navigation bar
        self.navbar = QHBoxLayout()
        self.back_btn = QPushButton("←")
        self.forward_btn = QPushButton("→")
        self.refresh_btn = QPushButton("↻")
        self.url_bar = QLineEdit()
        self.go_btn = QPushButton("Search")
        
        # Status label for errors
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: red;")
        self.status_label.setVisible(False)
        
        self.navbar.addWidget(self.back_btn)
        self.navbar.addWidget(self.forward_btn)
        self.navbar.addWidget(self.refresh_btn)
        self.navbar.addWidget(self.url_bar)
        self.navbar.addWidget(self.go_btn)
        
        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(self.navbar)
        layout.addWidget(self.status_label)
        layout.addWidget(self.browser)
        self.setLayout(layout)
        
        # Connect signals
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.refresh_btn.clicked.connect(self._reload_page)
        self.go_btn.clicked.connect(self._navigate_to_url)
        self.url_bar.returnPressed.connect(self._navigate_to_url)
        
        # Update URL bar when page changes
        self.browser.urlChanged.connect(self._update_url_bar)
        self.browser.loadFinished.connect(self._handle_load_finished)
    
    def _reload_page(self):
        #Reload current page and clear any error messages
        self.status_label.setVisible(False)
        self.browser.reload()
    
    def _navigate_to_url(self):
        #Handle navigation to URL or search query
        url = self.url_bar.text().strip()
        self.status_label.setVisible(False)
        
        # If empty, load blank page
        if not url:
            self.browser.setUrl(QUrl("about:blank"))
            return
        
        # If it's a valid URL, navigate directly
        if url.startswith(('http://', 'https://', 'file://')):
            self.browser.setUrl(QUrl(url))
        else:
            # Treat as search query
            self._handle_search_query(url)
    
    def _handle_search_query(self, query):
        #Process search query using our custom search engine
        search_engine = CustomSearchEngine()
        results = search_engine.search(query)
        
        if results:
            # Navigate to the top result
            self.browser.setUrl(QUrl(results[0]['url']))
        else:
            # Fallback to blank page
            self.browser.setUrl(QUrl("about:blank"))
    
    def _update_url_bar(self, q):
        #Update the URL bar when the page changes
        self.url_bar.setText(q.toString())
    
    def _handle_load_finished(self, success):
        #Handle page load completion
        if not success:
            current_url = self.browser.url().toString()
            if current_url.startswith("http"):
                self.status_label.setText(f"Failed to load page: {current_url}")
                self.status_label.setVisible(True)
                
                # Offer to search Google for the URL if it looks like a search term
                if not current_url.startswith(('http://', 'https://')):
                    search_url = f"https://www.google.com/search?q={quote_plus(current_url)}"
                    self.status_label.setText(
                        f"Failed to load local page. <a href='{search_url}'>Search Google instead</a>")
                    self.status_label.setOpenExternalLinks(True)

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NET322 SEARCH ENGINE")
        self.setGeometry(100, 100, 1024, 768)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self._close_tab)
        self.setCentralWidget(self.tabs)
        
        # Add initial tab
        self._add_new_tab("Home")
        
        # Navigation buttons
        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.clicked.connect(lambda: self._add_new_tab("New Tab"))
        self.tabs.setCornerWidget(self.new_tab_btn, Qt.TopRightCorner)
    
    def _add_new_tab(self, title):
        #Add a new browser tab
        tab = BrowserTab()
        i = self.tabs.addTab(tab, title)
        self.tabs.setCurrentIndex(i)
        
        # Load home page
        tab.browser.setUrl(QUrl("about:blank"))
        return tab
    
    def _close_tab(self, index):
        #Close a tab
        if self.tabs.count() > 1:
            widget = self.tabs.widget(index)
            widget.deleteLater()
            self.tabs.removeTab(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())
from kivy.app import App
from mainwidget import MainWidget
from kivy.lang.builder import Builder # Classe que vai fazer leitura
from kivy.core.window import Window

class MainApp(App):
    """
    Classe com o aplicativo
    """
    def build(self):
        """
        Método que gera o aplicativo com base no widget principal
        """
        self._widget = MainWidget(scan_time=1000, server_ip='127.0.0.1', server_port=502)
        return self._widget

if __name__ == '__main__':
    Window.size = (680,500)
    Builder.load_string(open("mainwidget.kv", encoding="utf-8").read(), rulesonly=True) # Para ler os caracteres especiais do mainwidget.kv
    Builder.load_string(open("popups.kv", encoding="utf-8").read(), rulesonly=True)
    MainApp().run()
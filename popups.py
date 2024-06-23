from kivy.uix.popup import Popup
from kivy.uix.label import Label

class ModbusPopup(Popup):
    """
    Popup da configuração do protocolo MODBUS
    """
    _info_lb = None
    def __init__(self, server_ip, server_port, **kwargs):

        """
        Construtor da classe ModbusPopup
        """
        super().__init__(**kwargs) # Inicializar o construtor da classe base para dar certo(isso para o kivy)
        self.ids.txt_ip.text = str(server_ip)
        self.ids.txt_port.text = str(server_port)

    def setInfo(self, message): # Para criar widget dinâmico, durante o tempo de execução
        self._info_lb = Label(text=message)
        self.ids.layout.add_widget(self._info_lb)

    def clearInfo(self):
        if self._info_lb is not None:
            self.ids.layout.remove_widget(self._info_lb)

class ScanPopup(Popup):
    """
    Popup da configurção do tempo de varredura
    """
    def __init__(self, scantime, **kwargs): # scantime: tempo de varredura / **kwargs: receber múltiplos argumetos sem ter que listar eles
        """
        Construtor da classe ScanPopup
        """
        super().__init__(**kwargs) # Inicializar o construtor da classe base para dar certo(isso para o kivy)
        self.ids.txt_st.text = str(scantime)
from kivy.uix.popup import Popup

class ModbusPopup(Popup):
    """
    Popup da configuração do protocolo MODBUS
    """
    def __init__(self, server_ip,server_port,**kwardgs): #**kwardgs: maneira de receber multiplos argumentos sem ter que declara-los aqui
        """
        Construtor da classe ModbusPopup
        """
        super().__init__(**kwardgs)
        self.ids.txt_ip.text = str(server_ip)
        self.ids.txt_porta.text = str(server_port)


class ScanPopup(Popup):
    """
    Popup da configuração do tempo de varredura
    """
    def __init__(self, scantime,**kwardgs): #**kwardgs: maneira de receber multiplos argumentos sem ter que declara-los aqui
        """
        Construtor da classe ScanPopup
        """
        super().__init__(**kwardgs)
        self.ids.txt_st.text = str(scantime)
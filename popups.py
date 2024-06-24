from kivy.uix.popup import Popup

class ModbusPopup(Popup):
    """
    Popup da configuração do protocolo MODBUS
    """
    pass

class ScanPopup(Popup):
    """
    Popup da configuração do tempo de varredura
    """
    def __init__(self, scantime,**kwardgs): #**kwardgs: maneira de receber multiplos argumentos sem ter que declara-los aqui
        """
        Constri=utor da classe ScanPopup
        """
        super().__init__(**kwardgs)
        self.ids.txt_st.text = str(scantime)
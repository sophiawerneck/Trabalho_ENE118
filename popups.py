from kivy.uix.popup import Popup
from kivy.uix.label import Label

class ModbusPopup(Popup):
    """
    Popup da configuração do protocolo MODBUS
    """
    _info_lb = None
    def __init__(self, server_ip,server_port,**kwardgs): #**kwardgs: maneira de receber multiplos argumentos sem ter que declara-los aqui
        """
        Construtor da classe ModbusPopup
        """
        super().__init__(**kwardgs)
        self.ids.txt_ip.text = str(server_ip)
        self.ids.txt_porta.text = str(server_port)

    def setInfo(self, message): #cria um widget em tempo de execução
        self._info_lb = Label(text = message)
        self.ids.layout.add_widget(self._info_lb)

    def clearInfo(self):
        if self._info_lb is not None:
            self.ids.layout.remove_widget(self._info_lb)

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

class MedicoesPopup(Popup):
    """
    Popup da configuração das medições
    """
    def __init__(self,**kwargs):
        """
        Construtor da classe MedicoesPopup
        """
        super().__init__(**kwargs)
   
    def update(self, medida):
        """
        Método para atualizar os valores das medições
        """
        #ARRUMAR O NOSSO
        self.ids['encoder'].text=str(self._meas['values']['encoder'])+' RPM'
   

class ComandoPopup(Popup):
     def __init__(self,**kwargs):
        """
        Construtor da classe ComandoPopup
        """
        super().__init__(**kwargs)

class PidPopup(Popup):
     def __init__(self,**kwargs):
        """
        Construtor da classe ComandoPopup
        """
        super().__init__(**kwargs)
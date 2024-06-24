from kivy.uix.boxlayout import BoxLayout
from popups import ModbusPopup,ScanPopup
from pyModbusTCP.client import ModbusClient
from time import sleep

class MainWidget(BoxLayout):
    """
    Widget principal da aplicação
    """
    def __init__(self, **kwargs):
        """
        Construtor do widget principal
        """
        super().__init__()
        self._scan_time = kwargs.get('scan_time') #buscar na lista de paramentros um arg chamado scantime
        self._serverIP = kwargs.get('server_ip')
        self._serverPort = kwargs.get('server_port')
        self._modbusPopup = ModbusPopup(self._serverIP, self._serverPort)
        self._scanPopup = ScanPopup(scantime=self._scan_time)
        self._modbusClient = ModbusClient(host = self._serverIP, port = self._serverPort)



    # def updater(self):
    #     """
    #     Método que invoca as rotinas de leitura de dados, atualização da interface e inserção dos dados no banco de daods
    #     """
    #     try:
    #         while self._uptadeWidgets:
    #             sleep(self._scantime/1000)
        
    #     except Exception as e:
    #         self._modbusClient.close()
    #         print("Erro: ", e.args)
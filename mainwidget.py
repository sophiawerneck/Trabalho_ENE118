from kivy.uix.boxlayout import BoxLayout
from popups import ModbusPopup,ScanPopup,MedicoesPopup,ComandoPopup
from pyModbusTCP.client import ModbusClient
from time import sleep
from kivy.core.window import Window
from threading import Thread
from datetime import datetime
import random

class MainWidget(BoxLayout):
    """
    Widget principal da aplicação
    """
    #_tags={'modbusaddrs':{},'atuadores':{}}
    _updateThread = None
    _updateWidgets = True
    _tags = {}

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
        self._medicoesPopup = MedicoesPopup()
        self._comandoPopup = ComandoPopup()
        self._modbusClient = ModbusClient(host = self._serverIP, port = self._serverPort)
        self._meas = {}
        self._meas['timestamp'] = None
        self._meas['values'] = {} # Valores das tags do sistema
        # Leitura das tags: # ATUADORES TEM QUE SEPARAR NA MAIN
        '''
        for key,value in kwargs.get('modbus_addrs').items():
            plot_color=(random.random(),random.random(),random.random(),1)
            self._tags['modbusaddrs'][key] = {'addr':value['addr'],'color':plot_color,'legenda':value['legenda'],'tipo':value['tipo'],'div':value['div']}
        
        for key,value in kwargs.get('atuadores').items():
           #self._tags['atuadores'][key] = {'addr':value['addr'],'tipo':value['tipo'],'div':value['div']}
        '''

    def startDataRead(self, ip, port): # Para inicializar coleta de dados
        """
        Método utilizado para a configuração do IP e porta do servidor MODBUS e
        inicializar uma thread para a leitura dos dados e atualização da interface
        """
        self._serverIP = ip
        self._serverPort = port
        self._modbusClient.ip = self._serverIP
        self._modbusClient.port = self._serverPort
        try:
            Window.set_system_cursor("wait")
            self._modbusClient.open()
            Window.set_system_cursor("arrow")
            if self._modbusClient.is_open():
                self._updateThread = Thread(target=self.updater)
                self._updateThread.start()
                self.ids.img_con.source = 'RecursosParaDesenvolvimento/imgs/conectado.png'
                self._modbusPopup.dismiss()
            else:
                self._modbusPopup.setInfo('Falha na conexão com o servidor')
        except Exception as e:
            print("Erro: ", e.args)

    def updater(self): # método de atualização
        """
        Método que invoca as rotinas de leitura dos dados, atualização da interface e 
        inserção dos dados no Banco de dados
        """
        try:
            while self._updateWidgets:
                self.readData() # Ler os dados MODBUS
                self.updateGUI() # Atualizar a interface
                # Inserir os dados no BD
                sleep(self._scantime/1000) 
        except Exception as e:
            self._modbusClient.close()
            print("Erro: ", e.args)

    def readData(self):
        """
        Método para a leitura dos dados por meio do protocolo MODBUS
        """
        # ADAPTAR PARA O NOSSO 
        self._meas['timestamp'] = datetime.now() # now retorna o horário correto do sistemna operacional
        for key,value in self._items():
            self._meas['values'][key] = self._modbusClient.read_holding_registers(value['addr'],1)[0] # 1 pq só lê 1 registrador e 0 pq read_holding_registers retorna uma tupla, então seleciona o primeiro elemento dessa tupla
        
    def updateGUI(self):
        """
        Método para atualização da interface gráfica a partir dos dados lidos
        """
        # ADAPTAR PARA O NOSSO
        # Atualização dos labels das temperaturas
        for key,value in self._tag.items(): 
            self.ids[key].text = str(self._meas['value'][key]) + '°C' # Atualiza cada label utilizando os valores lidos
        
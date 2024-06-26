from kivy.uix.boxlayout import BoxLayout
from popups import ModbusPopup,ScanPopup, ComandoPopup, MedicoesPopup
from pyModbusTCP.client import ModbusClient
from kivy.core.window import Window
from threading import Thread
from time import sleep
from datetime import datetime
import random
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian

class MainWidget(BoxLayout):
    """
    Widget principal da aplicação
    """
    _updateThread = None
    _uptadeWidgets = True
    _tags = {'modbusaddrs':{},'atuadores':{}}

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
        
        # Leitura das tags (readData vai iterar o dicionario)
        for key,value in kwargs.get('modbus_addrs').items():
            plot_color=(random.random(),random.random(),random.random(),1)
            self._tags['modbusaddrs'][key] = {'addr':value['addr'],'color':plot_color,'legenda':value['legenda'],'tipo':value['tipo'],'div':value['div']}
            #cria a tag com as mesmas chaves usadas no dicionario modbus_addrs
            
        for key,value in kwargs.get('atuadores').items():
           self._tags['atuadores'][key] = {'addr':value['addr'],'tipo':value['tipo'],'div':value['div']}


    def startDataRead(self, ip, port):
        """
        Método utilizado para configuração do IP e porta do servidor MODBUS e
        inicializar uma thread para leitura dos dados e atualização da interface gráfica
        """
        self._serverIP = ip
        self._serverPort = port
        self._modbusClient.host = self._serverIP
        self._modbusClient.port = self._serverPort
        try: #tentativa de conexão com o servidor
            Window.set_system_cursor("wait")
            self._modbusClient.open()
            Window.set_system_cursor("arrow")
            if callable(self._modbusClient.is_open) and self._modbusClient.is_open(): # se o cliente estiver conectado eu começo uma nova thread
                self._updateThread = Thread(target=self.updater) #thread secundaria para atualização da interface grafica (para leitura de dados e atualização do BD) (updater)
                self._updateThread.start()
                self.ids.img_con.sorce = 'imgs/conectado.png'
                self._modbusPopup.dismiss()
            else: 
                self._modbusPopup.setInfo("Falha na conexão com o servidor") 
        except Exception as e:
            print("Erro: ", e.args)  

    def updater(self):
        """
        Método que invoca as rotinas de leitura de dados, atualização da interface e 
        inserção dos dados no banco de daods
        """
        try:
            while self._uptadeWidgets:
                self.readData() #ler os dados MODBUS
                self.updateGUI() #atualizar a interface
                #inserir os dados no BD
                sleep(self._scantime/1000)     
        except Exception as e:
            self._modbusClient.close()
            print("Erro: ", e.args)


    def readData(self):
        """
        Método para a leitura dos dados por meio do protocolo MODBUS
        """ 
        self._meas['timestamp'] = datetime.now() # now retorna o horário corrente do sistema operacional
        for key,value in self._tags['modbusaddrs'].items():
            if value['tipo']=='4X': #Holding Register 16bits
                self._meas['values'][key]=(self._modbusClient.read_holding_registers(value['addr'],1)[0])/value['div']      
            elif value['tipo']=='FP': #Floating Point
                self._meas['values'][key]=(self.lerFloat(value['addr']))/value['div']
    def readDataAtuadores(self,chave):
        """
        Método para leitura dos dados dos atuadores
        """ 
        for key,value in self._tags['atuadores'].items():
            if key==chave:
                if value['tipo']=='4X':
                    return (self._modbusClient.read_holding_registers(value['addr'],1)[0])/value['div']
                elif value['tipo']=='FP':
                    return (self.lerFloat(value['addr']))/value['div']


    def lerFloat(self,addr):
        """
        Método para a leitura de um "float" na tabela MODBUS
        """
        result = self._modbusClient.read_holding_registers(addr,2)
        decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.Big, wordorder=Endian.Little)
        decoded = decoder.decode_32bit_float()
        return decoded
    def escreveFloat(self,addr,data):
        """
        Método para a escrita de um "float" na tabela MODBUS
        """
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
        builder.add_32bit_float(data)
        payload = builder.to_registers()
        return self._modbusClient.write_multiple_registers(addr,payload)



    def updateGUI(self):
        """
        Método para atualização da interface gráfica a partir dos dados lidos
        """
        # ADAPTAR PARA O NOSSO: AINDA FALTA ATUALIZAR OS POPUPS
        partida=self._meas['values']['indica_driver'] #armazena o valor selecionado do tipo de partida
        if partida == 1:
            self.ids['indica_driver'].text='Soft-Start'
        if partida == 2:
            self.ids['indica_driver'].text='Inversor'
        if partida == 3:
            self.ids['indica_driver'].text='Direta'
        self.ids['encoder'].text=str(self._meas['values']['encoder'])+' RPM'
        self.ids['torque'].text=str(self._meas['values']['torque'])+' N.m'
        self.ids['temp_carc'].text=str(self._meas['values']['temp_carc'])+' °C'
        self.ids['le_carga'].text=str(round(self._meas['values']['le_carga'],2))+' kgf/cm²' #round: arredondar o valor pra 2 casas decimais 
        self.ids['esteira'].text=str(round(self._meas['values']['esteira'],2))+' m/min'
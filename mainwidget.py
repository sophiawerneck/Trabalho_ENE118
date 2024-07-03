from kivy.uix.boxlayout import BoxLayout
from popups import ModbusPopup,ScanPopup, ComandoPopup, MedicoesPopup, PidPopup
from pyModbusTCP.client import ModbusClient
from kivy.core.window import Window
from threading import Thread
from time import sleep
from datetime import datetime
import random
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian
from threading import Lock

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
        self._pidPopup = PidPopup()
        self._modbusClient = ModbusClient(host = self._serverIP, port = self._serverPort)
        self._meas = {} #armazenar as tags
        self._meas['timestamp'] = None
        self._meas['values'] = {} # Valores das tags do sistema
        self._lock=Lock()
        
        # Leitura das tags (readData vai iterar o dicionario)
        for key,value in kwargs.get('modbusaddrs').items():
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
            if self._modbusClient.is_open: # se o cliente estiver conectado eu começo uma nova thread
                self._updateThread = Thread(target=self.updater) #thread secundaria para atualização da interface grafica (para leitura de dados e atualização do BD) (updater)
                self._updateThread.start()
                self.ids.img_con.source = 'imgs/conectado.png'
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
                sleep(self._scan_time/1000)     
        except Exception as e:
            self._modbusClient.close()
            print("Erro: ", e.args)


    def readData(self, esp_addr=None):
        """
        Método para a leitura dos dados por meio do protocolo MODBUS
        """ 
        self._meas['timestamp'] = datetime.now() # now retorna o horário corrente do sistema operacional
        for key,value in self._tags['modbusaddrs'].items():
            if esp_addr is not None and value['addr'] != esp_addr:
                continue
            
            if value['tipo']=='4X': #Holding Register 16bits
                self._lock.acquire()
                self._meas['values'][key]=(self._modbusClient.read_holding_registers(value['addr'],1)[0])/value['div'] 
                self._lock.release()
            elif value['tipo']=='FP': #Floating Point
                self._meas['values'][key]=(self.lerFloat(value['addr']))/value['div']    
    def readDataAtuadores(self,chave):
        """
        Método para leitura dos dados dos atuadores
        """
        self._lock.acquire() 
        for key,value in self._tags['atuadores'].items():
            if key==chave:
                if value['tipo']=='4X':
                    return (self._modbusClient.read_holding_registers(value['addr'],1)[0])/value['div']
                elif value['tipo']=='FP':
                    return (self.lerFloat(value['addr']))/value['div']
        self._lock.release()

    def writeData(self,addr,tipo,div,value):
        """
        Método para a escrita de dados por meio do protocolo MODBUS
        """
        if tipo=='4X':
            self._lock.acquire()
            self._modbusClient.write_single_register(addr,int(value*div))
            self._lock.release()
        elif tipo=='FP':
            self._lock.acquire()
            print(self.escreveFloat(addr,float(value*div)))
            self._lock.release()

    def lerFloat(self,addr):
        """
        Método para a leitura de um "float" na tabela MODBUS
        """
        self._lock.acquire()
        result = self._modbusClient.read_holding_registers(addr,2)
        decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        decoded = decoder.decode_32bit_float()
        self._lock.release()
        return decoded
    def escreveFloat(self,addr,data):
        """
        Método para a escrita de um "float" na tabela MODBUS
        """
        self._lock.acquire()
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        builder.add_32bit_float(data)
        payload = builder.to_registers()
        self._lock.release()
        return self._modbusClient.write_multiple_registers(addr,payload)
    
    def selPartida(self, part):
        """
        Método para selecionar o tipo de partida
        """
        self.writeData(self._tags['atuadores']['sel_driver']['addr'], '4X', self._tags['atuadores']['sel_driver']['div'], int(part))
        print("partida selecionada: ", part)

    def ligaEsteira(self, **kwargs):
        """
        Método para ligar o motor da esteira
        """
        print ("ligou")
        with self._lock:
            tipo = self._modbusClient.read_holding_registers(self._tags['modbusaddrs']['indica_driver']['addr'],1)[0]
        print(tipo)
        match tipo:
            case 1: #soft-start
                print ("ligou")
                self.writeData(self._tags['atuadores']['ats48']['addr'], '4X', self._tags['atuadores']['ats48']['div'], 1)
                self.writeData(self._tags['atuadores']['ats48_acc']['addr'], '4X', self._tags['atuadores']['ats48_acc']['div'],kwargs.get('acel'))
                self.writeData(self._tags['atuadores']['ats48_dcc']['addr'], '4X', self._tags['atuadores']['ats48_dcc']['div'],kwargs.get('desacel'))
            case 2: #inversor
                print ("ligou")
                self.writeData(self._tags['atuadores']['atv31']['addr'], '4X', self._tags['atuadores']['atv31']['div'], 1)
                self.writeData(self._tags['atuadores']['atv31_acc']['addr'], '4X', self._tags['atuadores']['atv31_acc']['div'],kwargs.get('acel'))
                self.writeData(self._tags['atuadores']['atv31_dcc']['addr'], '4X', self._tags['atuadores']['atv31_dcc']['div'],kwargs.get('desacel'))
                self.writeData(self._tags['atuadores']['atv31_velocidade']['addr'], '4X', self._tags['atuadores']['atv31_velocidade']['div'],kwargs.get('vel'))
            case 3: #direta
                print ("ligou")
                self.writeData(self._tags['atuadores']['tesys']['addr'], '4X', self._tags['atuadores']['tesys']['div'], 1)
            
    def desligaEsteira(self):
        """
        Método para desligar o motor da esteira
        """
        with self._lock:
            tipo = self._modbusClient.read_holding_registers(self._tags['modbusaddrs']['indica_driver']['addr'],1)[0]
        match tipo:
            case 1: #soft-start
                self.writeData(self._tags['atuadores']['ats48']['addr'], '4X', self._tags['atuadores']['ats48']['div'], 0)
            case 2: #inversor
                self.writeData(self._tags['atuadores']['atv31']['addr'], '4X', self._tags['atuadores']['atv31']['div'], 0)
            case 3: #direta
                self.writeData(self._tags['atuadores']['tesys']['addr'], '4X', self._tags['atuadores']['tesys']['div'], 0)

    def resetEsteira(self):
        """
        Método para desligar o motor da esteira
        """
        with self._lock:
            tipo = self._modbusClient.read_holding_registers(self._tags['modbusaddrs']['indica_driver']['addr'],1)[0]
        match tipo:
            case 1: #soft-start
                self.writeData(self._tags['atuadores']['ats48']['addr'], '4X', self._tags['atuadores']['ats48']['div'], 2)
            case 2: #inversor
                self.writeData(self._tags['atuadores']['atv31']['addr'], '4X', self._tags['atuadores']['atv31']['div'], 2)
            case 3: #direta
                self.writeData(self._tags['atuadores']['tesys']['addr'], '4X', self._tags['atuadores']['tesys']['div'], 2)
            

    def setMV(self):
        """
        Método para definir o setPoint da carga na esteira
        """
        self._MV= (self.ids.mv_escreve.text)
        self.writeData(self._tags['atuadores']['mv_escreve']['addr'],'FP',self._tags['atuadores']['mv_escreve']['div'],self._MV)
    
    def setP(self):
        """
        Método para definir o controle proporcional
        """
        self._P= (self.ids.p.text)
        self.writeData(self._tags['atuadores']['p']['addr'],'FP',self._tags['atuadores']['p']['div'],self._P)

    def setI(self):
        """
        Método para definir o controle integral
        """
        self._I= (self.ids.i.text)
        self.writeData(self._tags['atuadores']['i']['addr'],'FP',self._tags['atuadores']['i']['div'],self._I)

    def setD(self):
        """
        Método para definir o controle derivativo
        """
        self._D= (self.ids.d.text)
        self.writeData(self._tags['atuadores']['d']['addr'],'FP',self._tags['atuadores']['d']['div'],self._D)
        

    def updateGUI(self):
        """
        Método para atualização da interface gráfica a partir dos dados lidos
        """
        partida=self._meas['values']['indica_driver'] #armazena o valor selecionado do tipo de partida
        if partida == 1:
            self.ids['indica_driver'].text='Soft-start'
        if partida == 2:
            self.ids['indica_driver'].text='Inversor'
        if partida == 3:
            self.ids['indica_driver'].text='Direta'
        self.ids['encoder'].text=str(self._meas['values']['encoder'])+' RPM'
        self.ids['torque'].text=str(self._meas['values']['torque'])+' N.m'
        self.ids['temp_carc'].text=str(self._meas['values']['temp_carc'])+' °C'
        self.ids['le_carga'].text=str(round(self._meas['values']['le_carga'],2))+' kgf/cm²' #round: arredondar o valor pra 2 casas decimais 
        self.ids['esteira'].text=str(round(self._meas['values']['esteira'],2))+' m/min'

        self._medicoesPopup.update(self._meas)
        self._comandoPopup.update(self._meas)

        # Atualização das barras de escala dinâmica
        self.ids.seta_rpm.pos = (self.ids.seta_rpm.pos[0], self._meas['values']['encoder']/400*self.ids.barra_rpm.size[1]) # 400:valor máximo de cada barra, alterar pro valor certo
        self.ids.seta_nm.pos = (self.ids.seta_nm.pos[0], self._meas['values']['torque']/400*self.ids.barra_nm.size[1])
        self.ids.seta_temp.pos = (self.ids.seta_temp.pos[0], self._meas['values']['temp_carc']/400*self.ids.barra_temp.size[1])
        self.ids.seta_carga.pos = (self.ids.seta_carga.pos[0], self._meas['values']['le_carga']/400*self.ids.barra_carga.size[1])
        self.ids.seta_vel.pos = (self.ids.seta_vel.pos[0], self._meas['values']['esteira']/400*self.ids.barra_vel.size[1])

    def stopRefresh(self):
        self._updateThread = False

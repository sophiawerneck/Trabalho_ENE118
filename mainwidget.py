from kivy.uix.boxlayout import BoxLayout
from popups import ModbusPopup,ScanPopup, ComandoPopup, MedicoesPopup, PidPopup, SelectDataGraphPopup, HistGraphPopup, DataGraphPopup
from kivy.core.window import Window
from pyModbusTCP.client import ModbusClient
from threading import Thread
from time import sleep
from datetime import datetime
import random
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian
from threading import Lock
from models import DadosEsteira
from kivy_garden.graph import LinePlot
from db import Base,Session,engine
from timeseriesgraph import TimeSeriesGraph

class MainWidget(BoxLayout):
    """
    Widget principal da aplicação
    """
    _updateThread = None
    _uptadeWidgets = True
    _tags = {'modbusaddrs':{},'atuadores':{}}
    _dados={}
    _max_points = 20
    
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
        self._selectData= SelectDataGraphPopup()
        self._modbusClient = ModbusClient(host = self._serverIP, port = self._serverPort)
        self._meas = {} #armazenar as tags
        self._meas['timestamp'] = None
        self._meas['values'] = {} # Valores das tags do sistema
        self._lock=Lock()
        self._selection='potAtivaTotal'
        self._session = Session()
        
        # Leitura das tags (readData vai iterar o dicionario)
        for key,value in kwargs.get('modbusaddrs').items():
            plot_color=(random.random(),random.random(),random.random(),1)
            self._tags['modbusaddrs'][key] = {'addr':value['addr'],'color':plot_color,'legenda':value['legenda'],'tipo':value['tipo'],'div':value['div']}
            #cria a tag com as mesmas chaves usadas no dicionario modbus_addrs
            
        for key,value in kwargs.get('atuadores').items():
           self._tags['atuadores'][key] = {'addr':value['addr'],'tipo':value['tipo'],'div':value['div']}

        self._hgraph= HistGraphPopup(tags=self._tags['modbusaddrs'])
        self._graph = DataGraphPopup(self._max_points, self._tags['modbusaddrs']['temp_carc']['color']) 
        
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
                self._updateThread = Thread(target=self.updater)
                self._dataBankThread = Thread(target=self.updateDataBank) #thread secundaria para atualização da interface grafica (para leitura de dados e atualização do BD) (updater)
                self._updateThread.start()
                self._dataBankThread.start()
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
                self.updateGUI()#atualizar a interface
                #self.updateDataBank() #inserir os dados no BD
                sleep(self._scan_time/1000)     
        except Exception as e:
            self._modbusClient.close()
            print("Erro: ", e.args)

    def updateDataBank(self):
        """
        Método para a inserção dos dados no Banco de dados
        """
        try:
            self._dados['timestamp']=self._meas['timestamp']
            for key in self._tags['modbusaddrs']:
                self._dados[key]=self._meas['values'][key]
            dado=DadosEsteira(**self._dados)
            self._lock.acquire()
            self._session.add(dado)
            self._session.commit()
            self._lock.release()
        except Exception as e:
            print("Erro na atualização do banco:",e.args)
    def getDataDB(self):
        """
        Método que coleta as informações da interface pelo usuário
        e requisita a busca no Banco de dados
        """
        try:
            init_t=self._hgraph.ids.txt_init_time.text
            final_t=self._hgraph.ids.txt_final_time.text
            init_t=datetime.strptime(init_t,'%d/%m/%Y %H:%M:%S')
            final_t=datetime.strptime(final_t,'%d/%m/%Y %H:%M:%S')
                
            if init_t is None or final_t is None:
                return
            self._lock.acquire()
            results=self._session.query(DadosEsteira).filter(DadosEsteira.timestamp.between(init_t,final_t)).all()
            self._lock.release()
            results = [reg.get_resultsdic() for reg in results]
            sensorAtivo=[]
            for sensor in self._hgraph.ids.sensores.children:
                if sensor.ids.checkbox.active:
                    sensorAtivo.append(sensor.ids.label.text)
            if results is None or len(results)==0:
                return
            self._hgraph.ids.graph.clearPlots()
            tempo=[]
            for i in results:
                for key,value in i.items():
                    if key=='timestamp':
                        tempo.append(value)
                        continue
                    elif key=='id':
                        continue
                    for s in sensorAtivo:
                        if key==s:
                            p= LinePlot(line_width=1)
                            #p.points = [(x, results[x][key]) for x in range(0,len(results))]
                            self._hgraph.ids.graph.add_plot(p)
                            self._hgraph.ids.graph.ymax=self._tags['modbusaddrs'][s]['escalamax']
                            self._hgraph.ids.graph.y_ticks_major=self._tags['modbusaddrs'][s]['escalamax']/5
                            self._hgraph.ids.graph.ylabel= self._tags['modbusaddrs'][s]['legenda']
            self._hgraph.ids.graph.xmax=len(results)
            self._hgraph.ids.update_x_labels(tempo)
            

        except Exception as e:
            print("Erro na busca no banco:",e.args)



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
            print(self.escreveFloat(addr,float(value)*div))
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
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
        builder.add_32bit_float(data)
        payload = builder.to_registers()
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

    def setSlider(self,valor):
        """
        Método para habilitar o slider da velocidade do inversor
        """
        self.writeData(self._tags['atuadores']['atv31_velocidade']['addr'], '4X', self._tags['atuadores']['atv31_velocidade']['div'],valor)
            

    def setMV(self,mv):
        """
        Método para definir o valor da variável manipulada da carga na esteira em %
        """
        self.writeData(self._tags['atuadores']['mv_escreve']['addr'],'FP',self._tags['atuadores']['mv_escreve']['div'],float(mv))
    
    def setP(self,prop):
        """
        Método para definir o controle proporcional
        """
        self.writeData(self._tags['atuadores']['p']['addr'],'FP',self._tags['atuadores']['p']['div'],float(prop))

    def setI(self,integ):
        """
        Método para definir o controle integral
        """
        self.writeData(self._tags['atuadores']['i']['addr'],'FP',self._tags['atuadores']['i']['div'],float(integ))

    def setD(self,deriv):
        """
        Método para definir o controle derivativo
        """
        self.writeData(self._tags['atuadores']['d']['addr'],'FP',self._tags['atuadores']['d']['div'],float(deriv))
        

    def updateGUI(self):
        """
        Método para atualização da interface gráfica a partir dos dados lidos
        """
        partida=self._meas['values']['indica_driver'] #armazena o valor selecionado do tipo de partida
        if partida == 1:
            self.ids['indica_driver'].text='Soft-start'
        elif partida == 2:
            self.ids['indica_driver'].text='Inversor'
        elif partida == 3:
            self.ids['indica_driver'].text='Direta'
        self.ids['encoder'].text=str(self._meas['values']['encoder'])+' RPM'
        self.ids['torque'].text=str(self._meas['values']['torque'])+' N.m'
        self.ids['temp_carc'].text=str(self._meas['values']['temp_carc'])+' °C'
        self.ids['le_carga'].text=str(round(self._meas['values']['le_carga'],2))+' kgf/cm²' #round: arredondar o valor pra 2 casas decimais 
        self.ids['esteira'].text=str(round(self._meas['values']['esteira'],2))+' m/min'

        self._medicoesPopup.update(self._meas)
        self._comandoPopup.update(self._meas)
        self._pidPopup.update(self._meas)

        # Atualização das barras de escala dinâmica
        self.ids.seta_temp.pos_hint = {'x': self.ids.seta_temp.pos_hint['x'], 'y': 0.13 + (0.15/70)*self._meas['values']['temp_carc']} # 70:valor máximo da medida da temperatura
        self.ids.seta_rpm.pos_hint = {'x': self.ids.seta_rpm.pos_hint['x'], 'y': 0.13 + (0.15/2000)*self._meas['values']['encoder']} # Não tá atualizando
        self.ids.seta_nm.pos_hint = {'x': self.ids.seta_nm.pos_hint['x'], 'y': 0.13 + (0.15/10)*self._meas['values']['torque']} # Não tá certo o valor, a seta sobe muito rápido
        self.ids.seta_carga.pos_hint = {'x': self.ids.seta_carga.pos_hint['x'], 'y': 0.67 + (0.15/2000)*self._meas['values']['le_carga']}
        self.ids.seta_vel.pos_hint = {'x': self.ids.seta_vel.pos_hint['x'], 'y': 0.67 + (0.15/20)*self._meas['values']['esteira']}
        
        # Atualização dos gráficos
        if self._graph.ids.checktempcarcx.active == True:
            self._graph.ids.graph.updateGraph((self._meas['timestamp'],self._meas['values']['temp_carc']),0)
            self._graph.ids.graph.ylabel = 'Temperatura [°C]'
            self._graph.ids.graph.y_ticks_major = 5
            self._graph.ids.graph.ymax = 60

        elif self._graph.ids.checkrpm.active == True:
            self._graph.ids.graph.updateGraph((self._meas['timestamp'],self._meas['values']['encoder']),0)
            self._graph.ids.graph.ylabel = 'RPM'
            self._graph.ids.graph.y_ticks_major = 10
            self._graph.ids.graph.ymax = 2000

        elif self._graph.ids.checktorquex.active == True:
            self._graph.ids.graph.updateGraph((self._meas['timestamp'],self._meas['values']['torque']),0)
            self._graph.ids.graph.ylabel = 'N.m'
            self._graph.ids.graph.y_ticks_major = 5
            self._graph.ids.graph.ymax = 0.1

        elif self._graph.ids.checklecargax.active == True:
            self._graph.ids.graph.updateGraph((self._meas['timestamp'],self._meas['values']['le_carga']),0)
            self._graph.ids.graph.ylabel = 'kgf/cm²'
            self._graph.ids.graph.y_ticks_major = 5
            self._graph.ids.graph.ymax = 20

        elif self._graph.ids.checkesteirax.active == True:
            self._graph.ids.graph.updateGraph((self._meas['timestamp'],self._meas['values']['esteira']),0)
            self._graph.ids.graph.ylabel = 'm/min'
            self._graph.ids.graph.y_ticks_major = 5
            self._graph.ids.graph.ymax = 20

        elif self._graph.ids.checkcorrentex.active == True:
            self._graph.ids.graph.updateGraph((self._meas['timestamp'],self._meas['values']['corrente_media']),0)
            self._graph.ids.graph.ylabel = 'A'
            self._graph.ids.graph.y_ticks_major = 5
            self._graph.ids.graph.ymax = 20
    def stopRefresh(self):
        self._updateThread = False

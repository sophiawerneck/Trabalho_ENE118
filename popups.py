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
        self.ids.frequencia.text = str(medida['values']['frequencia'])+' Hz'
        self.ids.demanda_atual.text = str(medida['values']['demanda_atual'])+' W'
        self.ids.demanda_prevista.text = str(medida['values']['demanda_prevista'])+' W'
        self.ids.demanda_media.text = str(medida['values']['demanda_media'])+' W'
        self.ids.demanda_anterior.text = str(medida['values']['demanda_anterior'])+' W'
        self.ids.energia_ativa.text = str(medida['values']['energia_ativa'])+' kW/h'
        self.ids.ativa_total.text = str(medida['values']['ativa_total'])+' W'
        self.ids.reativa_total.text = str(medida['values']['reativa_total'])+' VA/r'
        self.ids.aparente_total.text = str(medida['values']['aparente_total'])+' VA'
        self.ids.fp_total.text = str(medida['values']['fp_total'])
        self.ids.tensao_rs.text = str(medida['values']['tensao_rs'])+' V'
        self.ids.tensao_st.text = str(medida['values']['tensao_st'])+' V'
        self.ids.tensao_tr.text = str(medida['values']['tensao_tr'])+' V'
        self.ids.corrente_media.text = str(medida['values']['corrente_media'])+' A'
        self.ids.corrente_r.text = str(medida['values']['corrente_r'])+' A'
        self.ids.corrente_s.text = str(medida['values']['corrente_s'])+' A'
        self.ids.corrente_t.text = str(medida['values']['corrente_t'])+' A'
        self.ids.corrente_n.text = str(medida['values']['corrente_n'])+' A'
        self.ids.temp_r.text = str(medida['values']['temp_r'])+' °C'
        self.ids.temp_s.text = str(medida['values']['temp_s'])+' °C'
        self.ids.temp_t.text = str(medida['values']['temp_t'])+' °C'
        self.ids.thd_tensao_rs.text = str(medida['values']['thd_tensao_rs'])
        self.ids.thd_tensao_st.text = str(medida['values']['thd_tensao_st'])
        self.ids.thd_tensao_tr.text = str(medida['values']['thd_tensao_tr'])
        self.ids.tipo_motor.text = str(medida['values']['tipo_motor'])
        self.ids.status_pid.text = str(medida['values']['status_pid'])
       

class ComandoPopup(Popup):
    """
    Popup para configurar os comandos do motor
    """
    def __init__(self,**kwargs):
        """
        Construtor da classe ComandoPopup
        """
        super().__init__(**kwargs)
        self._partida= None #Partida padrão como inversor
        self._operacao= 0 #Operação padrão como parado
        self._acel = float(self.ids.atv31_acc.text)
        self._desacel = float(self.ids.atv31_dcc.text)
        self._velInv = float(self.ids.atv31_velocidade.text)

    # def setPartida(self,partida):
    #     self._modbusClient.write_single_register(1324,partida)
    #     self._partida=partida
    # def setOperacao(self,operacao):
    #     if self._partida == 1:
    #         self._modbusClient.write_single_register(1316,operacao)
    #     elif self._partida == 2:
    #         self._modbusClient.write_single_register(1312,operacao)
    #     elif self._partida == 3:
    #         self._modbusClient.write_single_register(1319,operacao)

    # def setAcel(self):
    #     self._acel=float(self.ids.atv31_acc.text) #o id está relacionado ao inversor mas esse campo tb pode ser preenchido com dado do soft-start
    # def setDesacel(self):
    #     self._desacel=float(self.ids.atv31_dcc.text) #o id está relacionado ao inversor mas esse campo tb pode ser preenchido com dado do soft-start
    
    # def setVelInv(self):
    #     self._velInv=int(self.ids.atv31_velocidade.text)
    # def setVelSlider(self,vel):
    #     self._velInv=vel



    # def update(self,medida):
    #     medida['values']['tesys']=None #operação da partida direta
    #     medida['values']['ats48']=None #operação do soft-start
    #     medida['values']['atv31']=None #operação do inversor

    #     medida['values']['ats48_acc']=None #aceleração soft-started
    #     medida['values']['ats48_dcc']=None #desaceleração

    #     medida['values']['atv31_acc']=None #aceleração inversor
    #     medida['values']['atv31_dcc']=None #desacel
    #     medida['values']['atv31_velocidade']=None #vel


    #     if self._partida is not None:
    #         if self._partida== 'Direta':
    #             medida['values']['tesys']=self._operacao
    #             medida['values']['sel_driver']=3 #indica a partida


    #         elif self._partida == 'Soft-start':
    #             medida['values']['ats48']=self._operacao
    #             medida['values']['sel_driver']=1
    #             medida['values']['ats48_acc']= self._acel
    #             medida['values']['ats48_dcc']= self._desacel

    #         elif self._partida == 'Inversor':
    #             medida['values']['atv31']=self._operacao
    #             medida['values']['sel_driver']=2
    #             medida['values']['atv31_acc']= self._acel
    #             medida['values']['atv31_dcc']= self._desacel
    #             medida['values']['atv31_velocidade']= self._velInv


class PidPopup(Popup):
    def __init__(self,**kwargs):
        """
        Construtor da classe PidPopup
        """
        super().__init__(**kwargs)
        self._SP=0.0
        self._P=5.0
        self._I=5.0
        self._D=5.0

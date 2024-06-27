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
        #ARRUMAR O NOSSO: AINDA TA FALTANDO 11
        self.ids.frequencia.text = str(medida['values']['frequencia'])
        self.ids.demanda_atual.text = str(medida['values']['demanda_atual'])
        self.ids.demanda_prevista.text = str(medida['values']['demanda_prevista'])
        self.ids.demanda_media.text = str(medida['values']['demanda_media'])
        self.ids.demanda_anterior.text = str(medida['values']['demanda_anterior'])
        self.ids.energia_ativa.text = str(medida['values']['energia_ativa'])
        self.ids.ativa_total.text = str(medida['values']['ativa_total'])
        self.ids.reativa_total.text = str(medida['values']['reativa_total'])
        self.ids.aparente_total.text = str(medida['values']['aparente_total'])
        self.ids.fp_total.text = str(medida['values']['fp_total'])
        self.ids.tensao_rs.text = str(medida['values']['tensao_rs'])
        self.ids.tensao_st.text = str(medida['values']['tensao_st'])
        self.ids.tensao_tr.text = str(medida['values']['tensao_tr'])
        self.ids.corrente_media.text = str(medida['values']['corrente_media'])    


class ComandoPopup(Popup):
    """
    Popup para configurar os comandos do motor
    """
    _partida=None
    _operacao=None
    def __init__(self,**kwargs):
        """
        Construtor da classe ComandoPopup
        """
        super().__init__(**kwargs)
        self._partida= 'Inversor' #Partida padrão como inversor
        self._operacao= 0 #Operação padrão como parado

    def setPartida(self,partida):
        self._partida=partida
    def setOperacao(self,operacao):
        self._operacao=operacao

    def update(self,medida):
        medida['values']['tesys']=None #operação da partida direta
        medida['values']['ats48']=None #operação do soft-start
        medida['values']['atv31']=None #operação do inversor

        if self._partida is not None:
            if self._partida== 'Direta':
                medida['values']['tesys']=self._operacao
                medida['values']['sel_driver']=3 #indica a partida

            elif self._partida == 'Soft-Start':
                medida['values']['ats48']=self._operacao
                medida['values']['sel_driver']=1

            elif self._partida == 'Inversor':
                medida['values']['atv31']=self._operacao
                medida['values']['sel_driver']=2


class PidPopup(Popup):
    def __init__(self,**kwargs):
        """
        Construtor da classe ComandoPopup
        """
        super().__init__(**kwargs)
        self._MV=0.0
        self._P=5.0
        self._I=5.0
        self._D=5.0

    def atualiza(self, medida):
        pass
    def automatico(self):
        pass
    def manual(self):
        pass
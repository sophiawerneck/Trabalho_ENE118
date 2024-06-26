from kivy.app import App
from mainwidget import MainWidget
from kivy.lang.builder import Builder

class MainApp(App):
    """
    Classe com o aplicativo
    """
    def build(self):
        """
        Método que gera o aplicativo com base no widget principal
        """
        self._widget = MainWidget(scan_time =1000,server_ip='192.168.0.11',server_port=502,
        modbus_addrs={
            'indica_driver':{ 
            'addr':1216,
            'legenda': 'Partida do motor',
            'tipo': '4X',
            'div': 1,
            },

            'encoder':{
            'addr':884,
            'legenda': 'Frequência de rotação do motor',
            'tipo': 'FP',
            'div': 1,
            },

            'esteira':{
            'addr':724,
            'legenda': 'Velocidade da esteira',
            'tipo': 'FP',
            'div': 1,
            },

            'torque':{ 
            'addr':1420,
            'legenda': 'Torque do motor',
            'tipo': 'FP',
            'div': 100,
            },

            'temp_carc':{ 
            'addr':706,
            'legenda': 'Temperatura da carcaça',
            'tipo': 'FP',
            'div': 10,
            },

            'le_carga':{ 
            'addr':710,
            'legenda': 'Carga na esteira',
            'tipo': 'FP',
            'div': 1,
            },
            
            'tipo_motor':{ 
            'addr':708,
            'legenda': 'Tipo do motor(1 = Verde e 2 = Azul)',
            'tipo': '4X',
            'div': 1,
            },

            'status_pid':{ 
            'addr':722,
            'legenda': 'Status do PID(0 = Automático e 1 = Manual)',
            'tipo': '4X',
            'div': 1,
            },

            'temp_r':{ 
            'addr':700,
            'legenda': 'Temperatura Enrolamento R Motor',
            'tipo': 'FP',
            'div': 10,
            },

            'temp_s':{ 
            'addr':702,
            'legenda': 'Temperatura Enrolamento S Motor',
            'tipo': 'FP',
            'div': 10,
            },

            'temp_t':{ 
            'addr':704,
            'legenda': 'Temperatura Enrolamento T Motor',
            'tipo': 'FP',
            'div': 10,
            },

            'thd_tensao_rs':{ 
            'addr':804,
            'legenda': 'Medida THD Tensão entre fase R e Fase S',
            'tipo': '4X',
            'div': 10,
            },

            'thd_tensao_st':{ 
            'addr':805,
            'legenda': 'Medida THD Tensão entre fase S e Fase T',
            'tipo': '4X',
            'div': 10,
            },

            'thd_tensao_tr':{ 
            'addr':806,
            'legenda': 'Medida THD Tensão entre fase T e Fase R',
            'tipo': '4X',
            'div': 10,
            },

            'frequencia':{ 
            'addr':830,
            'legenda': 'Medida Frequência da Rede',
            'tipo': '4X',
            'div': 100,
            },

            'corrente_media':{ 
            'addr':845,
            'legenda': 'Corrente Média',
            'tipo': '4X',
            'div': 100,
            },

            'tensao_rs':{ 
            'addr':845,
            'legenda': 'ddp entre Fase R e S',
            'tipo': '4X',
            'div': 10,
            },

            'tensao_st':{ 
            'addr':845,
            'legenda': 'ddp entre Fase S e T',
            'tipo': '4X',
            'div': 10,
            },

            'tensao_tr':{ 
            'addr':845,
            'legenda': 'ddp entre Fase T e R',
            'tipo': '4X',
            'div': 10,
            },

            'ativa_total':{ 
            'addr':855,
            'legenda': 'Medida Potência Ativa Total',
            'tipo': '4X',
            'div': 1,
            },

            'reativa_total':{ 
            'addr':859,
            'legenda': 'Medida Potência Reativa Total',
            'tipo': '4X',
            'div': 1,
            },

            'aparente_total':{ 
            'addr':863,
            'legenda': 'Medida Potência Aparente Total',
            'tipo': '4X',
            'div': 1,
            },

            'fp_total':{ 
            'addr':871,
            'legenda': 'Medida do Fator de Potência Total',
            'tipo': '4X',
            'div': 1000,
            },

            'demanda_anterior':{ 
            'addr':1204,
            'legenda': 'Medida de Demanda Anterior',
            'tipo': '4X',
            'div': 1,
            },

            'demanda_atual':{ 
            'addr':1205,
            'legenda': 'Medida de Demanda Atual',
            'tipo': '4X',
            'div': 1,
            },

            'demanda_media':{ 
            'addr':1206,
            'legenda': 'Medida de Demanda Média',
            'tipo': '4X',
            'div': 1,
            },

            'demanda_prevista':{ 
            'addr':1208,
            'legenda': 'Medida de Demanda Prevista',
            'tipo': '4X',
            'div': 1,
            },

            'energia_ativa':{ 
            'addr':1210,
            'legenda': 'Medida de Energia Ativa',
            'tipo': '4X',
            'div': 1,
            },

            'habilita':{ 
            'addr':1330,
            'legenda': 'Indica Motor ligado ou não',
            'tipo': '4X',
            'div': 1,
            }
        },

        atuadores = {
            'sel_driver':{
                'addr':1324,
                #Seleção do tipo de partida(3=direta, 1=soft start, 2=inversor)
                'tipo':'4X',
                'div':1.0
            },
            'tesys':{
                'addr':1319,
                #Controla partida direta(0=desligado, 1=ligado, 2=reset)
                'tipo':'4X',
                'div':1.0
            },
            'ats48':{
                'addr':1316,
                #Controla partida soft start(0=desligado, 1=ligado, 2=reset)
                'tipo':'4X',
                'div':1.0
            },
            'atv31':{
                'addr':1312,
                #Controla partida inversor(0=desligado, 1=ligado, 2=reset)
                'tipo':'4X',
                'div':1.0
            },
            'atv31_velocidade':{
                'addr':1313,
                #Define a velocidade do inversor
                'tipo':'4X',
                'div':10.0
            },
            'carga':{
                'addr':1302,
                #Define a Carga na esteira no PID (SP- Set Point)
                'tipo':'FP',
                'div':1.0
            },
            'p':{
                'addr':1304,
                #Define o valor do Controle Proporcional
                'tipo':'FP',
                'div':1.0
            },
            'i':{
                'addr':1306,
                #Define o valor do Controle Integrativo
                'tipo':'FP',
                'div':1.0
            },
            'd':{
                'addr':1308,
                #Define o valor do Controle Derivativo
                'tipo':'FP',
                'div':1.0
            }

        }
        )
        return self._widget
    
    # def on_stop(self):
    #     """
    #     Método chamado quando o programa é fechado
    #     """
    #     self._widget.stopRefresh()
    
if __name__ == '__main__':
    Builder.load_string(open("mainwidget.kv",encoding="utf-8").read(),rulesonly=True)
    Builder.load_string(open("popups.kv",encoding="utf-8").read(),rulesonly=True)
    MainApp().run()
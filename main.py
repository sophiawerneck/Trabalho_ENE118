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
        self._widget = MainWidget(scan_time =1000,server_ip='127.0.0.1',server_port=502,
        modbus_addr = {
            'es.indica_driver':{ 
            'addr':1216,
            'legenda': 'Partida do motor',
            'tipo': '4X',
            'div': 1,
            },

            'es.encoder':{
            'addr':884,
            'legenda': 'Frequência de rotação do motor',
            'tipo': 'FP',
            'div': 1,
            },

            'es.esteira':{
            'addr':724,
            'legenda': 'Velocidade da esteira',
            'tipo': 'FP',
            'div': 1,
            },

            'es.torque':{ 
            'addr':1420,
            'legenda': 'Torque do motor',
            'tipo': 'FP',
            'div': 100,
            },

            'es.temp_carc':{ 
            'addr':706,
            'legenda': 'Temperatura da carcaça',
            'tipo': 'FP',
            'div': 10,
            },

            'es.le_carga':{ 
            'addr':710,
            'legenda': 'Carga na esteira',
            'tipo': 'FP',
            'div': 1,
            },
            
            'es.tipo_motor':{ 
            'addr':708,
            'legenda': 'Tipo do motor(1 = Verde e 2 = Azul)',
            'tipo': '4X',
            'div': 1,
            },

            'es.status_pid':{ 
            'addr':722,
            'legenda': 'Status do PID(0 = Automático e 1 = Manual)',
            'tipo': '4X',
            'div': 1,
            },

            'es.temp_r':{ 
            'addr':700,
            'legenda': 'Temperatura Enrolamento R Motor',
            'tipo': 'FP',
            'div': 10,
            },

            'es.temp_s':{ 
            'addr':702,
            'legenda': 'Temperatura Enrolamento S Motor',
            'tipo': 'FP',
            'div': 10,
            },

            'es.temp_t':{ 
            'addr':704,
            'legenda': 'Temperatura Enrolamento T Motor',
            'tipo': 'FP',
            'div': 10,
            },

            'es.thd_tensao_rs':{ 
            'addr':804,
            'legenda': 'Medida THD Tensão entre fase R e Fase S',
            'tipo': '4X',
            'div': 10,
            },

            'es.thd_tensao_st':{ 
            'addr':805,
            'legenda': 'Medida THD Tensão entre fase S e Fase T',
            'tipo': '4X',
            'div': 10,
            },

            'es.thd_tensao_tr':{ 
            'addr':806,
            'legenda': 'Medida THD Tensão entre fase T e Fase R',
            'tipo': '4X',
            'div': 10,
            },

            'es.frequencia':{ 
            'addr':830,
            'legenda': 'Medida Frequência da Rede',
            'tipo': '4X',
            'div': 100,
            },

            'es.corrente_media':{ 
            'addr':845,
            'legenda': 'Corrente Média',
            'tipo': '4X',
            'div': 100,
            },

            'es.tensao_rs':{ 
            'addr':845,
            'legenda': 'ddp entre Fase R e S',
            'tipo': '4X',
            'div': 10,
            },

            'es.tensao_st':{ 
            'addr':845,
            'legenda': 'ddp entre Fase S e T',
            'tipo': '4X',
            'div': 10,
            },

            'es.tensao_tr':{ 
            'addr':845,
            'legenda': 'ddp entre Fase T e R',
            'tipo': '4X',
            'div': 10,
            },

            'es.ativa_total':{ 
            'addr':855,
            'legenda': 'Medida Potência Ativa Total',
            'tipo': '4X',
            'div': 1,
            },

            'es.reativa_total':{ 
            'addr':859,
            'legenda': 'Medida Potência Reativa Total',
            'tipo': '4X',
            'div': 1,
            },

            'es.aparente_total':{ 
            'addr':863,
            'legenda': 'Medida Potência Aparente Total',
            'tipo': '4X',
            'div': 1,
            },

            'es.fp_total':{ 
            'addr':871,
            'legenda': 'Medida do Fator de Potência Total',
            'tipo': '4X',
            'div': 1000,
            },

            'es.demanda_anterior':{ 
            'addr':1204,
            'legenda': 'Medida de Demanda Anterior',
            'tipo': '4X',
            'div': 1,
            },

            'es.demanda_atual':{ 
            'addr':1205,
            'legenda': 'Medida de Demanda Atual',
            'tipo': '4X',
            'div': 1,
            },

            'es.demanda_media':{ 
            'addr':1206,
            'legenda': 'Medida de Demanda Média',
            'tipo': '4X',
            'div': 1,
            },

            'es.demanda_prevista':{ 
            'addr':1208,
            'legenda': 'Medida de Demanda Prevista',
            'tipo': '4X',
            'div': 1,
            },

            'es.energia_ativa':{ 
            'addr':1210,
            'legenda': 'Medida de Energia Ativa',
            'tipo': '4X',
            'div': 1,
            },

            'es.habilita':{ 
            'addr':1330,
            'legenda': 'Indica Motor ligado ou não',
            'tipo': '4X',
            'div': 1,
            }

        } 
        #atuadores = {

       # }    
        )
        return self._widget
    
if __name__ == '__main__':
    Builder.load_string(open("mainwidget.kv",encoding="utf-8").read(),rulesonly=True)
    Builder.load_string(open("popups.kv",encoding="utf-8").read(),rulesonly=True)
    MainApp().run()
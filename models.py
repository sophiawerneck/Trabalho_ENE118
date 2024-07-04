from db import Base
from sqlalchemy import Column, Integer, DateTime, Float

class DadosEsteira(Base):
    """
    Modelo dos dados do CLP
    """
    __tablename__ = 'dadosesteira'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    encoder = Column(Float)
    torque = Column(Float)
    temp_carc = Column(Float)
    le_carga = Column(Float)
    esteira = Column(Float)
    # acrescentar as variaveis aqui

    def get_resultsdic(self):
        return {'id':self.id,
        'timestamp':self.timestamp.strftime('%d/%m/%Y %H:%M:%S'),
        'encoder':self.encoder,
        'torque':self.torque,
        'temp_carc':self.temp_carc,
        'le_carga':self.le_carga,
        'esteira':self.esteira}

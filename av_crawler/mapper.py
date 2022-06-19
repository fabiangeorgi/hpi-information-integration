import logging

import pandas as pd

from av_crawler.av_extractor import AVExtractor

API_KEY = '2KAXFVFXLKF0TWUN'

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)


def extract_data():
    df = pd.read_csv('../frankfurt-stock-exchange-companies.csv')

    company_symbols = []
    for _, row in df.iterrows():
        company_symbols.append((row['Symbol'], row['Name'].strip()))


COMPANY_SYMBOLS = [('SAP', 'SAP'), ('VOW3.DE', 'Volkswagen'), ('SIE.DE', 'Siemens'), ('DTE.DE', 'Deutsche Telekom'),
                   ('ALV.DE', 'Allianz'), ('HLAG.DE', 'Hapag-Lloyd'), ('MRK.DE', 'Merck KGaA'),
                   ('MBG.DE', 'Mercedes-Benz'), ('SHL.DE', 'Siemens Healthineers'), ('BAYZF', 'Bayer'),
                   ('BMW.DE', 'BMW'), ('DPW.DE', 'Deutsche Post'), ('BAS.DE', 'BASF'), ('IFX.DE', 'Infineon'),
                   ('ADS.DE', 'Adidas'), ('BNTX', 'BioNTech'), ('MUV2.DE', 'Munich RE (Münchener Rück)'),
                   ('VNA.DE', 'Vonovia'), ('DB1.DE', 'Deutsche Börse'), ('RWE.DE', 'RWE'), ('EBK.DE', 'EnBW Energie'),
                   ('HEN3', 'Henkel'), ('EOAN.DE', 'E.ON'), ('DTG.F', 'Daimler Truck'), ('SRT.DE', 'Sartorius'),
                   ('PAH3.DE', 'Porsche SE'), ('FRE.DE', 'Fresenius'), ('BEI.DE', 'Beiersdorf'),
                   ('DB', 'Deutsche Bank'),
                   ('HNR1.DE', 'Hannover Rück'), ('FMS', 'Fresenius Medical Care'), ('SY1.DE', 'Symrise'),
                   ('CON.DE', 'Continental'), ('EVK.DE', 'Evonik Industries'), ('ENR.F', 'Siemens Energy'),
                   ('KBX.DE', 'Knorr-Bremse'), ('BNR.DE', 'Brenntag'), ('AFXA.F', 'Carl Zeiss Meditec'),
                   ('DWNI.DE', 'Deutsche Wohnen'), ('HEI.DE', 'HeidelbergCement'), ('TLX', 'Talanx'),
                   ('PUM.DE', 'PUMA'),
                   ('UN01.DE', 'Uniper'), ('MTX.DE', 'MTU Aero Engines'), ('ZAL.DE', 'Zalando'), ('8TRA.DE', 'Traton'),
                   ('CBK.F', 'Commerzbank'), ('WCH.F', 'Wacker Chemie'), ('RHM.F', 'Rheinmetall'),
                   ('LHA.DE', 'Lufthansa'),
                   ('1COV.F', 'Covestro'), ('DHER.F', 'Delivery Hero'), ('NEM.F', 'Nemetschek'),
                   ('HFG.DE', 'HelloFresh'),
                   ('LEG.DE', 'LEG Immobilien'), ('HLE.F', 'HELLA'), ('KGX.DE', 'KION Group'), ('DWS.F', 'DWS Group'),
                   ('G1A.F', 'GEA Group'), ('EVD.F', 'CTS Eventim'), ('RAA.F', 'Rational AG'),
                   ('UTDI.F', 'United Internet'),
                   ('SDF.F', 'K+S'), ('BC8.F', 'Bechtle'), ('TKA.F', 'Thyssenkrupp'), ('SIX2.F', 'Sixt'),
                   ('WWG.F', 'Gelsenwasser'), ('TUI1.F', 'TUI'), ('FRA.DE', 'Fraport'), ('LEC.F', 'Lechwerke'),
                   ('G24.F', 'Scout24'), ('EVO', 'Evotec'), ('HOT.F', 'Hochtief'), ('FIE.F', 'Fielmann'),
                   ('NDA.F', 'Aurubis'),
                   ('SHA.F', 'Schaeffler'), ('FPE.F', 'Fuchs Petrolub'), ('BOSS.DE', 'HUGO BOSS'), ('VBK.F', 'Verbio'),
                   ('1U1.DE', '1&1'), ('KU2.F', 'Kuka'), ('GIL.F', 'DMG Mori'), ('LXS.F', 'Lanxess'),
                   ('VAR1.F', 'Varta'),
                   ('MNV6.F', 'Mainova'), ('ECV.F', 'Encavis'), ('SAX.F', 'Ströer'), ('B4B.F', 'Metro AG'),
                   ('FNTN.F', 'Freenet'),
                   ('CVAC', 'Curevac'), ('DMP.F', 'Dermapharm'), ('AIXA.F', 'Aixtron'), ('TEG.F', 'TAG Immobilien'),
                   ('TMV.DE', 'TeamViewer'), ('COP.DE', 'CompuGroup Medical'), ('WAF.F', 'Siltronic'),
                   ('SZU.F', 'Südzucker'),
                   ('KRN.F', 'Krones'), ('HAG.F', 'Hensoldt'), ('JUN3.F', 'Jungheinrich'),
                   ('PSM.F', 'ProSiebenSat.1 Media'),
                   ('SSU', 'SIGNA Sports United'), ('YSN.F', 'secunet'), ('SOW.F', 'Software AG'),
                   ('MVV1.F', 'MVV Energie'),
                   ('BYW.F', 'BayWa'), ('GXI.F', 'Gerresheimer'), ('KWS.F', 'KWS'), ('AG1.F', 'AUTO1'),
                   ('SZG.F', 'Salzgitter'),
                   ('ARL.F', 'Aareal Bank'), ('HBH.F', 'Hornbach Holding'), ('NDX1.F', 'Nordex'), ('DUE.F', 'Dürr'),
                   ('WUW.F', 'Wüstenrot & Württembergische'), ('GWK3.HM', 'GAG Immobilien'), ('HYQ.F', 'Hypoport'),
                   ('PFV.F', 'Pfeiffer Vacuum'), ('BIO.F', 'Biotest'), ('S92.F', 'SMA Solar Technology'),
                   ('HBM.F', 'Hornbach Baumarkt'), ('FTK.DE', 'flatexDEGIRO AG'), ('JEN.F', 'Jenoptik'),
                   ('COK.F', 'Cancom'),
                   ('WAC.F', 'Wacker Neuson'), ('SBS.F', 'STRATEC'), ('HHFA.F', 'Hamburger Hafen'), ('GLJ.F', 'Grenke'),
                   ('P1Z.VI', 'Patrizia Immobilien'), ('GBF.F', 'Bilfinger'), ('AOF.F', 'Atoss'),
                   ('CE2.F', 'CropEnergies'),
                   ('RHK.DE', 'Rhön-Klinikum'), ('DEQ.F', 'Deutsche EuroShop'), ('GTY.F', 'Gateway Real Estate'),
                   ('EUZ', 'Eckert & Ziegler'), ('MUM.F', 'Mensch und Maschine'), ('DRW8.F', 'Drägerwerk'),
                   ('NBG6.F', 'Nürnberger Versicherung'), ('VIH1.F', 'VIB Vermögen'), ('TIMA.F', 'Zeal Network'),
                   ('MYTE', 'MYT Netherlands Parent (Mytheresa)'), ('NOEJ.F', 'Norma Group'), ('LILM', 'Lilium'),
                   ('NWO.F', 'New Work'), ('INH.F', 'Indus Holding'), ('CWC.F', 'CEWE'), ('ATAI', 'Atai Life Sciences'),
                   ('MOR', 'Morphosys'), ('TRVG', 'trivago'), ('ADL.DE', 'Adler Real Estate'), ('JMIA', 'Jumia'),
                   ('SIM0.F', 'Simona'), ('AFMD', 'Affimed'), ('BVB.F', 'Borussia Dortmund'), ('IMTX', 'Immatics'),
                   ('PAG.F', 'PREOS Real Estate'), ('SEV', 'Sono'), ('MYNA', 'Mynaric'), ('MRX.F', 'Mister Spex'),
                   ('IUR.F', 'KAP AG'), ('C0M.F', 'Compleo Charging Solutions'), ('MYNZ', 'Mainz Biomed'),
                   ('IFRX', 'InflaRx')]


def run():
    AVExtractor(COMPANY_SYMBOLS).extract()


if __name__ == "__main__":
    run()

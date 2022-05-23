import logging

import pandas as pd
from pandas import DataFrame
import requests
from av_extractor import AVExtractor

API_KEY = '2KAXFVFXLKF0TWUN'

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

def extract_data():
    df = pd.read_csv('../frankfurt-stock-exchange-companies.csv')

    company_symbols = []
    for _, row in df.iterrows():
        company_symbols.append((row['Symbol'], row['Name'].strip(), row['Name'].strip()))


COMPANY_SYMBOLS = [('SAP', 'SAP', 'SAP'), ('VOW3.DE', 'Volkswagen', 'Volkswagen'), ('SIE.DE', 'Siemens', 'Siemens'),
                   ('DTE.DE', 'Deutsche Telekom', 'Deutsche Telekom'), ('ALV.DE', 'Allianz', 'Allianz'),
                   ('HLAG.DE', 'Hapag-Lloyd', 'Hapag-Lloyd'), ('MRK.DE', 'Merck KGaA', 'Merck KGaA'),
                   ('MBG.DE', 'Mercedes-Benz', 'Mercedes-Benz'),
                   ('SHL.DE', 'Siemens Healthineers', 'Siemens Healthineers'), ('BAYZF', 'Bayer', 'Bayer'),
                   ('BMW.DE', 'BMW', 'BMW'), ('DPW.DE', 'Deutsche Post', 'Deutsche Post'), ('BAS.DE', 'BASF', 'BASF'),
                   ('IFX.DE', 'Infineon', 'Infineon'), ('ADS.DE', 'Adidas', 'Adidas'), ('BNTX', 'BioNTech', 'BioNTech'),
                   ('MUV2.DE', 'Munich RE (Münchener Rück)', 'Munich RE (Münchener Rück)'),
                   ('VNA.DE', 'Vonovia', 'Vonovia'), ('DB1.DE', 'Deutsche Börse', 'Deutsche Börse'),
                   ('RWE.DE', 'RWE', 'RWE'), ('EBK.DE', 'EnBW Energie', 'EnBW Energie'), ('HEN3', 'Henkel', 'Henkel'),
                   ('EOAN.DE', 'E.ON', 'E.ON'), ('DTG.F', 'Daimler Truck', 'Daimler Truck'),
                   ('SRT.DE', 'Sartorius', 'Sartorius'), ('PAH3.DE', 'Porsche SE', 'Porsche SE'),
                   ('FRE.DE', 'Fresenius', 'Fresenius'), ('BEI.DE', 'Beiersdorf', 'Beiersdorf'),
                   ('DB', 'Deutsche Bank', 'Deutsche Bank'), ('HNR1.DE', 'Hannover Rück', 'Hannover Rück'),
                   ('FMS', 'Fresenius Medical Care', 'Fresenius Medical Care'), ('SY1.DE', 'Symrise', 'Symrise'),
                   ('CON.DE', 'Continental', 'Continental'), ('EVK.DE', 'Evonik Industries', 'Evonik Industries'),
                   ('ENR.F', 'Siemens Energy', 'Siemens Energy'), ('KBX.DE', 'Knorr-Bremse', 'Knorr-Bremse'),
                   ('BNR.DE', 'Brenntag', 'Brenntag'), ('AFXA.F', 'Carl Zeiss Meditec', 'Carl Zeiss Meditec'),
                   ('DWNI.DE', 'Deutsche Wohnen', 'Deutsche Wohnen'),
                   ('HEI.DE', 'HeidelbergCement', 'HeidelbergCement'), ('TLX', 'Talanx', 'Talanx'),
                   ('PUM.DE', 'PUMA', 'PUMA'), ('UN01.DE', 'Uniper', 'Uniper'),
                   ('MTX.DE', 'MTU Aero Engines', 'MTU Aero Engines'), ('ZAL.DE', 'Zalando', 'Zalando'),
                   ('8TRA.DE', 'Traton', 'Traton'), ('CBK.F', 'Commerzbank', 'Commerzbank'),
                   ('WCH.F', 'Wacker Chemie', 'Wacker Chemie'), ('RHM.F', 'Rheinmetall', 'Rheinmetall'),
                   ('LHA.DE', 'Lufthansa', 'Lufthansa'), ('1COV.F', 'Covestro', 'Covestro'),
                   ('DHER.F', 'Delivery Hero', 'Delivery Hero'), ('NEM.F', 'Nemetschek', 'Nemetschek'),
                   ('HFG.DE', 'HelloFresh', 'HelloFresh'), ('LEG.DE', 'LEG Immobilien', 'LEG Immobilien'),
                   ('HLE.F', 'HELLA', 'HELLA'), ('KGX.DE', 'KION Group', 'KION Group'),
                   ('DWS.F', 'DWS Group', 'DWS Group'), ('G1A.F', 'GEA Group', 'GEA Group'),
                   ('EVD.F', 'CTS Eventim', 'CTS Eventim'), ('RAA.F', 'Rational AG', 'Rational AG'),
                   ('UTDI.F', 'United Internet', 'United Internet'), ('SDF.F', 'K+S', 'K+S'),
                   ('BC8.F', 'Bechtle', 'Bechtle'), ('TKA.F', 'Thyssenkrupp', 'Thyssenkrupp'),
                   ('SIX2.F', 'Sixt', 'Sixt'), ('WWG.F', 'Gelsenwasser', 'Gelsenwasser'), ('TUI1.F', 'TUI', 'TUI'),
                   ('FRA.DE', 'Fraport', 'Fraport'), ('LEC.F', 'Lechwerke', 'Lechwerke'),
                   ('G24.F', 'Scout24', 'Scout24'), ('EVO', 'Evotec', 'Evotec'), ('HOT.F', 'Hochtief', 'Hochtief'),
                   ('FIE.F', 'Fielmann', 'Fielmann'), ('NDA.F', 'Aurubis', 'Aurubis'),
                   ('SHA.F', 'Schaeffler', 'Schaeffler'), ('FPE.F', 'Fuchs Petrolub', 'Fuchs Petrolub'),
                   ('BOSS.DE', 'HUGO BOSS', 'HUGO BOSS'), ('VBK.F', 'Verbio', 'Verbio'), ('1U1.DE', '1&1', '1&1'),
                   ('KU2.F', 'Kuka', 'Kuka'), ('GIL.F', 'DMG Mori', 'DMG Mori'), ('LXS.F', 'Lanxess', 'Lanxess'),
                   ('VAR1.F', 'Varta', 'Varta'), ('MNV6.F', 'Mainova', 'Mainova'), ('ECV.F', 'Encavis', 'Encavis'),
                   ('SAX.F', 'Ströer', 'Ströer'), ('B4B.F', 'Metro AG', 'Metro AG'), ('FNTN.F', 'Freenet', 'Freenet'),
                   ('CVAC', 'Curevac', 'Curevac'), ('DMP.F', 'Dermapharm', 'Dermapharm'),
                   ('AIXA.F', 'Aixtron', 'Aixtron'), ('TEG.F', 'TAG Immobilien', 'TAG Immobilien'),
                   ('TMV.DE', 'TeamViewer', 'TeamViewer'), ('COP.DE', 'CompuGroup Medical', 'CompuGroup Medical'),
                   ('WAF.F', 'Siltronic', 'Siltronic'), ('SZU.F', 'Südzucker', 'Südzucker'),
                   ('KRN.F', 'Krones', 'Krones'), ('HAG.F', 'Hensoldt', 'Hensoldt'),
                   ('JUN3.F', 'Jungheinrich', 'Jungheinrich'),
                   ('PSM.F', 'ProSiebenSat.1 Media', 'ProSiebenSat.1 Media'),
                   ('SSU', 'SIGNA Sports United', 'SIGNA Sports United'), ('YSN.F', 'secunet', 'secunet'),
                   ('SOW.F', 'Software AG', 'Software AG'), ('MVV1.F', 'MVV Energie', 'MVV Energie'),
                   ('BYW.F', 'BayWa', 'BayWa'), ('GXI.F', 'Gerresheimer', 'Gerresheimer'), ('KWS.F', 'KWS', 'KWS'),
                   ('AG1.F', 'AUTO1', 'AUTO1'), ('SZG.F', 'Salzgitter', 'Salzgitter'),
                   ('ARL.F', 'Aareal Bank', 'Aareal Bank'), ('HBH.F', 'Hornbach Holding', 'Hornbach Holding'),
                   ('NDX1.F', 'Nordex', 'Nordex'), ('DUE.F', 'Dürr', 'Dürr'),
                   ('WUW.F', 'Wüstenrot & Württembergische', 'Wüstenrot & Württembergische'),
                   ('GWK3.HM', 'GAG Immobilien', 'GAG Immobilien'), ('HYQ.F', 'Hypoport', 'Hypoport'),
                   ('PFV.F', 'Pfeiffer Vacuum', 'Pfeiffer Vacuum'), ('BIO.F', 'Biotest', 'Biotest'),
                   ('S92.F', 'SMA Solar Technology', 'SMA Solar Technology'),
                   ('HBM.F', 'Hornbach Baumarkt', 'Hornbach Baumarkt'),
                   ('FTK.DE', 'flatexDEGIRO AG', 'flatexDEGIRO AG'), ('JEN.F', 'Jenoptik', 'Jenoptik'),
                   ('COK.F', 'Cancom', 'Cancom'), ('WAC.F', 'Wacker Neuson', 'Wacker Neuson'),
                   ('SBS.F', 'STRATEC', 'STRATEC'), ('HHFA.F', 'Hamburger Hafen', 'Hamburger Hafen'),
                   ('GLJ.F', 'Grenke', 'Grenke'), ('P1Z.VI', 'Patrizia Immobilien', 'Patrizia Immobilien'),
                   ('GBF.F', 'Bilfinger', 'Bilfinger'), ('AOF.F', 'Atoss', 'Atoss'),
                   ('CE2.F', 'CropEnergies', 'CropEnergies'), ('RHK.DE', 'Rhön-Klinikum', 'Rhön-Klinikum'),
                   ('DEQ.F', 'Deutsche EuroShop', 'Deutsche EuroShop'),
                   ('GTY.F', 'Gateway Real Estate', 'Gateway Real Estate'),
                   ('EUZ', 'Eckert & Ziegler', 'Eckert & Ziegler'),
                   ('MUM.F', 'Mensch und Maschine', 'Mensch und Maschine'), ('DRW8.F', 'Drägerwerk', 'Drägerwerk'),
                   ('NBG6.F', 'Nürnberger Versicherung', 'Nürnberger Versicherung'),
                   ('VIH1.F', 'VIB Vermögen', 'VIB Vermögen'), ('TIMA.F', 'Zeal Network', 'Zeal Network'),
                   ('MYTE', 'MYT Netherlands Parent (Mytheresa)', 'MYT Netherlands Parent (Mytheresa)'),
                   ('NOEJ.F', 'Norma Group', 'Norma Group'), ('LILM', 'Lilium', 'Lilium'),
                   ('NWO.F', 'New Work', 'New Work'), ('INH.F', 'Indus Holding', 'Indus Holding'),
                   ('CWC.F', 'CEWE', 'CEWE'), ('ATAI', 'Atai Life Sciences', 'Atai Life Sciences'),
                   ('MOR', 'Morphosys', 'Morphosys'), ('TRVG', 'trivago', 'trivago'),
                   ('ADL.DE', 'Adler Real Estate', 'Adler Real Estate'), ('JMIA', 'Jumia', 'Jumia'),
                   ('SIM0.F', 'Simona', 'Simona'), ('AFMD', 'Affimed', 'Affimed'),
                   ('BVB.F', 'Borussia Dortmund', 'Borussia Dortmund'), ('IMTX', 'Immatics', 'Immatics'),
                   ('PAG.F', 'PREOS Real Estate', 'PREOS Real Estate'), ('SEV', 'Sono', 'Sono'),
                   ('MYNA', 'Mynaric', 'Mynaric'), ('MRX.F', 'Mister Spex', 'Mister Spex'),
                   ('IUR.F', 'KAP AG', 'KAP AG'), ('C0M.F', 'Compleo Charging Solutions', 'Compleo Charging Solutions'),
                   ('MYNZ', 'Mainz Biomed', 'Mainz Biomed'), ('IFRX', 'InflaRx', 'InflaRx')]


def run():
    AVExtractor(COMPANY_SYMBOLS).extract()


if __name__ == "__main__":
    run()

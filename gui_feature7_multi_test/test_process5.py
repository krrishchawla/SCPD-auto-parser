import unittest
import csv
from io import StringIO
from process5 import get_filtered_rows

class TestGetFilteredRows(unittest.TestCase):

    def setUp(self):
        self.csv_content = """Stu Class Enrl Status Desc,Current Term Ind,Term Code,Course Offering Subject-Num Desc,Unified Course Offering Subject-Num Desc,Class Instr List Name,EMPLID,Preferred Email Address,Last First Name,Tuition Group Desc,Tuition Group Code,Stu Current Acad Plan Code,SUNet ID,Stu Current All Acad Plan Code,Study Program Desc,Study Agreement Code
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,05778471,ashoeb@stanford.edu,"Shoeb, Ali H",SCPD NDO,SCPD_NDO,GR-NDO,ashoeb,GR-NDO,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06020199,sid94@stanford.edu,"Kataria, Siddharth Deepak",SCPD NDO,SCPD_NDO,GR-NDO,sid94,GR-NDO,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06139305,hongm@stanford.edu,"Hong, Michael Peter",Engineering Graduate,ENG_GRAD,ME-MS,hongm,ME-MS; MGTSC-MS; MGTSC-PHD,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06139305,hongm@stanford.edu,"Hong, Michael Peter",Engineering Graduate,ENG_GRAD,MGTSC-MS,hongm,ME-MS; MGTSC-MS; MGTSC-PHD,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06139305,hongm@stanford.edu,"Hong, Michael Peter",Engineering Graduate,ENG_GRAD,MGTSC-PHD,hongm,ME-MS; MGTSC-MS; MGTSC-PHD,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06172976,qingmu@stanford.edu,"Deng, Qingmu",SCPD NDO,SCPD_NDO,GR-NDO,qingmu,GR-NDO,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06205103,sabliu@stanford.edu,"Liu, Sabrina",Engineering Graduate,ENG_GRAD,EE-PHD,sabliu,EE-PHD,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06226921,mbwang@stanford.edu,"Wang, Margaret Bai",Engineering Graduate,ENG_GRAD,AA-PHD,mbwang,AA-PHD,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06269684,martac2@stanford.edu,"Cortinovis, Marta",Engineering Graduate,ENG_GRAD,AA-MS,martac2,AA-MS; AA-PHD,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06269684,martac2@stanford.edu,"Cortinovis, Marta",Engineering Graduate,ENG_GRAD,AA-PHD,martac2,AA-MS; AA-PHD,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06312145,khting@stanford.edu,"Ting, Karina Hsueh-Ting",Engineering Grad - Unit Based,ENG_UB,ME-MS,khting,ME-MS,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06324999,cchuanqi@stanford.edu,"Chen, Chuanqi",SCPD NDO,SCPD_NDO,GR-NDO,cchuanqi,GR-NDO,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06330018,aw1605@stanford.edu,"Wang, Andrew Haomin",Engineering Graduate,ENG_GRAD,ME-MS,aw1605,ME-MS,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06336714,mason747@stanford.edu,"Llewellyn, Mason T",Engineering Graduate,ENG_GRAD,CS-BS,mason747,ME-MS; CS-BS,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06336714,mason747@stanford.edu,"Llewellyn, Mason T",Engineering Graduate,ENG_GRAD,ME-MS,mason747,ME-MS; CS-BS,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06337562,asdutt2@stanford.edu,"Dutt, Aditya Sunil",Engineering Graduate,ENG_GRAD,ME-MS,asdutt2,ME-MS,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06338754,swang11@stanford.edu,"Wang, Stanley J",Engineering Graduate,ENG_GRAD,ME-PHD,swang11,ME-PHD,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06346881,kcoimbra@stanford.edu,"Coimbra, Kaila",Engineering Graduate,ENG_GRAD,AA-PHD,kcoimbra,AA-PHD,-,-
Enrolled,N,1246,AA 203,AA 203,Marco Pavone;Matthew Foutter;Daniel Morton,06365348,zhefu@stanford.edu,"Fu, Zhe",Exchange In,XCHANG_IN,AA-NM,zhefu,AA-NM,-,XXBERKELEY
"""

    # Also tests repeats in this CSV
    def test_no_filters(self):
        input_csv = StringIO(self.csv_content)
        reader = csv.DictReader(input_csv)
        filtered_rows = get_filtered_rows("AA 203", reader, [])
        self.assertEqual(len(filtered_rows), 15)
    
    def test_bosp_filter(self):
        input_csv = StringIO(self.csv_content)
        reader = csv.DictReader(input_csv)
        filtered_rows = get_filtered_rows("AA 203", reader, ['BOSP'])
        self.assertEqual(len(filtered_rows), 1)

    def test_bosp_and_scpd_filter(self):
        input_csv = StringIO(self.csv_content)
        reader = csv.DictReader(input_csv)
        filtered_rows = get_filtered_rows("AA 203", reader, ['BOSP', 'SCPD NDO'])
        self.assertEqual(len(filtered_rows), 5)
    
    def test_scpd_filter(self):
        input_csv = StringIO(self.csv_content)
        reader = csv.DictReader(input_csv)
        filtered_rows = get_filtered_rows("AA 203", reader, ['SCPD NDO'])
        self.assertEqual(len(filtered_rows), 4)


if __name__ == "__main__":
    unittest.main()

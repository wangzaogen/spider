from lib.item.spu_instructions import *

class SpuItem(object):
    def __init__(self, name, pinyin, specs, dosage, packing, approval_num,
                 manufacturer, main_diseases):
        self.name = name
        self.pinyin = pinyin
        ##规格
        self.specs = specs
        ##剂型
        self.dosage = dosage
        ##包装单位
        self.packing = packing
        ##批准文号
        self.approval_num = approval_num
        ##生产厂家
        self.manufacturer = manufacturer
        ##主治疾病
        self.main_diseases = main_diseases

    def text(self):
        return self.name + "," + \
               self.pinyin + "," + \
               self.specs + "," + \
               self.dosage + "," + \
               self.packing + "," + \
               self.approval_num + "," + \
               self.manufacturer + "," + \
               self.main_diseases

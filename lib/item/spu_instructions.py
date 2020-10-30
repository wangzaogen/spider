
class SpuInstructions(object):
    def __init__(self, spu_name, product_name, specs, components, indications,
                 usage_and_dosage, a_reactions, taboo, attention, storage,
                 validity,manufacturer,approval_num,address):
        self.spu_name = spu_name
        self.product_name = product_name
        ##规格
        self.specs = specs
        ##成分
        self.components = components
        ##功能主治
        self.indications = indications
        ##用法用量
        self.usage_and_dosage = usage_and_dosage
        ##不良反应
        self.a_reactions = a_reactions
        ##禁忌
        self.taboo = taboo
        self.attention = attention
        self.storage = storage
        self.validity = validity
        self.manufacturer = manufacturer
        self.approval_num = approval_num
        self.address = address

    def text(self):
        return self.spu_name + "," + \
               self.product_name + "," + \
               self.specs + "," + \
               self.components + "," + \
               self.indications + "," + \
               self.usage_and_dosage + "," + \
               self.a_reactions + "," + \
               self.taboo + "," + \
               self.attention + "," + \
               self.storage + "," + \
               self.validity + "," + \
               self.manufacturer + "," + \
               self.approval_num + "," + \
               self.address

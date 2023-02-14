class Dev(object):
    def __init__(self, cfg):
        self.addr = None
        self.info = None
        addr_l = []
        # 遍历所有visa资源
        for item in cfg["rc"]:
            # 自动(关键字)筛选
            if cfg["instrument"] is None:
                # 遍历关键字
                for key in cfg["key"]:
                    # 匹配生产商
                    if cfg["rc"][item].upper().find(
                            key["manufacturer"].upper()) == 0:
                        if key["model"] is None:
                            addr_l.append(item)
                        else:
                            # 遍历型号
                            for model in key["model"]:
                                # 匹配到机型
                                if cfg["rc"][item].upper().find(
                                        model.upper()) > 0:
                                    addr_l.append(item)
            # 根据型号筛选
            else:
                # 匹配到机型
                if type(cfg["instrument"]) is str:
                    if cfg["rc"][item].upper().find(
                            cfg["instrument"].upper()) >= 0:
                        addr_l.append(item)
                else:
                    for inst in cfg["instrument"]:
                        if cfg["rc"][item].upper().find(inst.upper()) >= 0:
                            addr_l.append(item)
        # 机型列表排序
        addr_l.sort()
        if len(addr_l) > 0:
            try:
                self.addr = addr_l[int(cfg["sel"])]
            except Exception:
                self.addr = addr_l[0]
        # 选中机型信息
        self.info = cfg["rc"][self.addr]


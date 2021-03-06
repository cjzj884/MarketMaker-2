import pybitflyer
import json
import logging
import time
import datetime

#注文処理をまとめている
class BFOrder:
    def __init__(self):
        #config.jsonの読み込み
        f = open('config/config.json', 'r', encoding="utf-8")
        config = json.load(f)
        self.product_code = config["product_code"]
        self.key = config["key"]
        self.secret = config["secret"]
        self.api = pybitflyer.API(self.key, self.secret)

    def limit(self, side, price, size, minute_to_expire=None):
        logging.info("Order: Limit. Side : {}".format(side))
        response = {"status":"internalError in bforder.py"}
        try:
            response = self.api.sendchildorder(product_code=self.product_code, child_order_type="LIMIT", side=side, price=price, size=size, minute_to_expire = minute_to_expire)
        except:
            pass
        logging.debug(response)
        retry = 0
        while "status" in response:
            try:
                response = self.api.sendchildorder(product_code=self.product_code, child_order_type="LIMIT", side=side, price=price, size=size, minute_to_expire = minute_to_expire)
            except:
                pass
            retry += 1
            if retry > 20:
                logging.error(response)
            else:
                logging.debug(response)
            time.sleep(0.5)
        return response

    def market(self, side, size, minute_to_expire= None):
        logging.info("Order: Market. Side : {}".format(side))
        response = {"status": "internalError in bforder.py"}
        try:
            response = self.api.sendchildorder(product_code=self.product_code, child_order_type="MARKET", side=side, size=size, minute_to_expire = minute_to_expire)
        except:
            pass
        logging.info(response)
        retry = 0
        while "status" in response:
            try:
                response = self.api.sendchildorder(product_code=self.product_code, child_order_type="MARKET", side=side, size=size, minute_to_expire = minute_to_expire)
            except:
                pass
            retry += 1
            if retry > 20:
                logging.error(response)
            else:
                logging.debug(response)
            time.sleep(0.5)
        return response

    def ticker(self):
        response = {"status": "internalError in bforder.py"}
        try:
            response = self.api.ticker(product_code=self.product_code)
        except:
            pass
        logging.debug(response)
        retry = 0
        while "status" in response:
            try:
                response = self.api.ticker(product_code=self.product_code)
            except:
                pass
            retry += 1
            if retry > 20:
                logging.error(response)
            else:
                logging.debug(response)
            time.sleep(0.5)
        return response

    def getexecutions(self, order_id):
        response = {"status": "internalError in bforder.py"}
        #child orderのとき 
        try:
            response = self.api.getexecutions(product_code=self.product_code, child_order_acceptance_id=order_id)
        except:
            pass
        #parent orderのとき 
        try:
            response = self.api.getexecutions(product_code=self.product_code, parent_order_acceptance_id=order_id)
        except:
            pass
        logging.debug(response)
        retry = 0
        while ("status" in response or not response):
            #child orderのとき 
            try:
                response = self.api.getexecutions(product_code=self.product_code, child_order_acceptance_id=order_id)
            except:
                pass
            #parent orderのとき 
            try:
                response = self.api.getexecutions(product_code=self.product_code, parent_order_acceptance_id=order_id)
            except:
                pass
            retry += 1
            if retry > 500:
                logging.error(response)
            else:
                logging.debug(response)
            time.sleep(0.5)
        return response

    def getparentexecutions(self, order_id):
        response = {"status": "internalError in bforder.py"}
        try:
            response = self.api.getexecutions(product_code=self.product_code, parent_order_acceptance_id=order_id)
        except:
            pass
        logging.debug(response)
        retry = 0
        while ("status" in response or not response):
            try:
                response = self.api.getexecutions(product_code=self.product_code, parent_order_acceptance_id=order_id)
            except:
                pass
            retry += 1
            if retry > 500:
                logging.error(response)
            else:
                logging.debug(response)
            time.sleep(0.5)
        return response

    def getboardstate(self):
        response = {"status": "internalError in bforder.py"}
        try:
            response = self.api.getboardstate(product_code=self.product_code)
        except:
            pass
        logging.debug(response)
        retry = 0
        while "status" in response:
            try:
                response = self.api.getboardstate(product_code=self.product_code)
            except:
                pass
            retry += 1
            if retry > 20:
                logging.error(response)
            else:
                logging.debug(response)
            time.sleep(0.5)
        return response

    def stop(self, side, size, trigger_price, minute_to_expire=None):
        logging.info("Order: Stop. Side : {}".format(side))
        response = {"status": "internalError in bforder.py"}
        try:
            response = self.api.sendparentorder(order_method="SIMPLE", parameters=[{"product_code": self.product_code, "condition_type": "STOP", "side": side, "size": size,"trigger_price": trigger_price, "minute_to_expire": minute_to_expire}])
        except:
            pass
        logging.debug(response)
        retry = 0
        while "status" in response:
            try:
                response = self.api.sendparentorder(order_method="SIMPLE", parameters=[{"product_code": self.product_code, "condition_type": "STOP", "side": side, "size": size,"trigger_price": trigger_price, "minute_to_expire": minute_to_expire}])
            except:
                pass
            retry += 1
            if retry > 20:
                logging.error(response)
            else:
                logging.debug(response)
            time.sleep(0.5)
        return response

    def stop_limit(self, side, size, trigger_price, price, minute_to_expire=None):
        logging.info("Side : {}".format(side))
        response = {"status": "internalError in bforder.py"}
        try:
            response = self.api.sendparentorder(order_method="SIMPLE", parameters=[{"product_code": self.product_code, "condition_type": "STOP_LIMIT", "side": side, "size": size,"trigger_price": trigger_price, "price": price, "minute_to_expire": minute_to_expire}])
        except:
            pass
        logging.debug(response)
        while "status" in response:
            try:
                response = self.api.sendparentorder(order_method="SIMPLE", parameters=[{"product_code": self.product_code, "condition_type": "STOP_LIMIT", "side": side, "size": size,"trigger_price": trigger_price, "price": price, "minute_to_expire": minute_to_expire}])
            except:
                pass
            logging.debug(response)
        return response

    def OCO(self, side, size, trigger_price, price, minute_to_expire=None):
        logging.info("Side : {}".format(side))
        response = {"status": "internalError in bforder.py"}
        0
        order2 = { 
                "product_code": "FX_BTC_JPY",
                "condition_type": "LIMIT",
                "side": side,
                "price": price,
                "size": size
                };
        order3 = { 
                "product_code": "FX_BTC_JPY",
                "condition_type": "STOP",
                "side": side,
                "trigger_price": trigger_price,
                "size": size
                };
        try:
            response = self.api.sendparentorder(order_method="OCO", parameters=[order2,order3])
        except:
            pass
        logging.debug(response)
        while "status" in response:
            try:
                #orderの定義
                order2 = { 
                        "product_code": "FX_BTC_JPY",
                        "condition_type": "LIMIT",
                        "side": side,
                        "price": price,
                        "size": size
                        };
                order3 = { 
                        "product_code": "FX_BTC_JPY",
                        "condition_type": "STOP",
                        "side": side,
                        "trigger_price": trigger_price,
                        "size": size
                        };
                response = self.api.sendparentorder(order_method="OCO", parameters=[order2,order3])
            except:
                pass
            logging.debug(response)
        return response

    def IFDOCO(self, side, size, trigger_price, parentprice, price, minute_to_expire = None):
        logging.info("Side : {}".format(side))
        response = {"status": "internalError in bforder.py"}
        
        if side == "BUY":
            reverseside = "SELL";
        else:
            reverseside = "BUY";
            
        order1 = { 
                "product_code": "FX_BTC_JPY",
                "condition_type": "LIMIT",
                "side": side,
                "price": parentprice,
                "size": size
                };
        order2 = { 
                "product_code": "FX_BTC_JPY",
                "condition_type": "LIMIT",
                "side": reverseside,
                "price": price,
                "size": size
                };
        order3 = { 
                "product_code": "FX_BTC_JPY",
                "condition_type": "STOP",
                "side": reverseside,
                "trigger_price": trigger_price,
                "size": size
                };
        try:
            response = self.api.sendparentorder(order_method="IFDOCO", minute_to_expire = minute_to_expire, parameters=[order1,order2,order3])
        except:
            pass
        logging.debug(response)
        while "status" in response:
            try:
                if side == "BUY":
                    reverseside = "SELL";
                else:
                    reverseside = "BUY";

                #orderの定義
                order1 = { 
                        "product_code": "FX_BTC_JPY",
                        "condition_type": "LIMIT",
                        "side": side,
                        "price": parentprice,
                        "size": size
                        };
                order2 = { 
                        "product_code": "FX_BTC_JPY",
                        "condition_type": "LIMIT",
                        "side": reverseside,
                        "price": price,
                        "size": size
                        };
                order3 = { 
                        "product_code": "FX_BTC_JPY",
                        "condition_type": "STOP",
                        "side": reverseside,
                        "trigger_price": trigger_price,
                        "size": size
                        };
                response = self.api.sendparentorder(order_method="IFDOCO", minute_to_expire = minute_to_expire, parameters=[order1,order2,order3])
            except:
                pass
            logging.debug(response)
        return response

    def trailing(self, side, size, offset, minute_to_expire=None):
        logging.info("Side : {}".format(side))
        response = {"status": "internalError in bforder.py"}
        try:
            response = self.api.sendparentorder(order_method="SIMPLE", parameters=[{"product_code": self.product_code, "condition_type": "TRAIL", "side": side, "size": size, "offset": offset, "minute_to_expire": minute_to_expire}])
        except:
            pass
        logging.debug(response)
        while "status" in response:
            try:
                response = self.api.sendparentorder(order_method="SIMPLE", parameters=[{"product_code": self.product_code, "condition_type": "TRAIL", "side": side, "size": size, "offset": offset, "minute_to_expire": minute_to_expire}])
            except:
                pass
            logging.debug(response)
        return response

    def getcollateral(self):
        response = {"status": "internalError in bforder.py"}
        try:
            response = self.api.getcollateral()
        except:
            pass
        logging.debug(response)
        while "status" in response:
            try:
                response = self.api.getcollateral()
            except:
                pass
            logging.info(response)
            time.sleep(0.5)
        return response

    def getmypos(self):
        side = ""
        size = 0
        response = {"status": "internalError in bforder.py"}
        index =0
        while(index < 10):
            try:
                poss = self.api.getpositions(product_code = self.product_code)

                #もしポジションがあれば合計値を取得
                if len(poss) != 0:
                    for pos in poss:
                        side = pos["side"]
                        size += pos["size"]
                break;
            except:
                pass
            index += 1
        return side,size

    def getmyparentorder(self):
        side = ""
        ordersize = 0
        childordersize = 0
        response = {"status": "internalError in bforder.py"}
        try:
            orders = self.api.getparentorders(product_code = "FX_BTC_JPY")
            #もしポジションがあれば合計値を取得
            if len(orders) != 0:
                for order in orders:
                    side = order["side"]
                    id = order["parent_order_id"]
                    ordersize += order["outstanding_size"]
                    childordersize += self.api.getchildorders(product_code = "FX_BTC_JPY", parent_order_id = id)
                    if order == 10:
                        break;  #10回以上前を見ても仕方がないのでやめる
        except:
            pass
        return side,ordersize, childordersize

    #すべての注文をキャンセル
    def cancelAllOrder(self):
        index =0
        while(index < 50):
            try:
                self.api.cancelallchildorders(product_code = "FX_BTC_JPY")
                break;
            except:
                pass
            index += 1

    #すべての注文をキャンセル
    def cancelAllOrderFutures(self):
        index =0
        while(index < 50):
            try:
                self.api.cancelallchildorders(product_code = "BTCJPY28SEP2018")
                break;
            except:
                pass
            index += 1